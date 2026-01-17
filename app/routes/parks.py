from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Session
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Body

from ..db import get_db
from .. import schemas, crud, models
from ..auth import require_admin

router = APIRouter(prefix="/parks", tags=["Parks"])


@router.get("/", response_model=List[schemas.ParkResponse])
def read_parks(db: Session = Depends(get_db)):
    return crud.get_parks(db)

@router.get("/{park_id}/species", response_model=List[schemas.SpeciesResponse])
def get_species_for_park(
    park_id: int,
    db: Session = Depends(get_db)
):
    species = crud.get_species_by_park(db, park_id)
    if species is None:
        raise HTTPException(status_code=404, detail="Park not found")
    return species


@router.get("/{park_id}", response_model=schemas.ParkResponse)
def read_park(park_id: int, db: Session = Depends(get_db)):
    park = crud.get_park(db, park_id)
    if not park:
        raise HTTPException(status_code=404, detail="Park not found")
    return park


@router.post("/", response_model=schemas.ParkResponse)
def create_park(
    park: schemas.ParkCreate,
    db: Session = Depends(get_db),
    user=Depends(require_admin)
):
    return crud.create_park(db, park)


@router.delete("/{park_id}")
def delete_park(
    park_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_admin)
):
    park = crud.delete_park(db, park_id)
    if not park:
        raise HTTPException(status_code=404, detail="Park not found")
    return {"message": "Park deleted"}

@router.post("/{park_id}/location")
def add_park_location(
    park_id: int,
    latitude: str = Body(...),
    longitude: str = Body(...),
    governorate: str | None = Body(None),
    db: Session = Depends(get_db),
    user=Depends(require_admin)
):
    park = db.query(models.Park).options(joinedload(models.Park.park_location)).filter(models.Park.id == park_id).first()
    if not park:
        raise HTTPException(status_code=404, detail="Park not found")

    # 🔑 Check if location already exists
    if park.park_location:
        park.park_location.latitude = latitude
        park.park_location.longitude = longitude
        park.park_location.governorate = governorate
    else:
        location = models.Location(
            latitude=latitude,
            longitude=longitude,
            governorate=governorate,
            park=park
        )
        db.add(location)

    db.commit()

    return {
        "park": park.name,
        "latitude": latitude,
        "longitude": longitude,
        "governorate": governorate
    }

@router.put("/{park_id}")
def update_park(
    park_id: int,
    park_data: schemas.ParkUpdate,
    db: Session = Depends(get_db),
    user=Depends(require_admin)
):
    park = crud.update_park(db, park_id, park_data)
    if not park:
        raise HTTPException(status_code=404, detail="Park not found")
    return park
