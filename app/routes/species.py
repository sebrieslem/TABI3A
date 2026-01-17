from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..db import get_db
from .. import schemas, crud
from ..auth import require_researcher_or_admin

router = APIRouter(prefix="/species", tags=["Species"])


@router.get("/", response_model=List[schemas.SpeciesResponse])
def read_species(db: Session = Depends(get_db)):
    return crud.get_species(db)


@router.post("/", response_model=schemas.SpeciesResponse)
def create_species(
    species: schemas.SpeciesCreate,
    db: Session = Depends(get_db),
    user=Depends(require_researcher_or_admin)
):
    return crud.create_species(db, species)

@router.put("/{species_id}")
def update_species(
    species_id: int,
    data: schemas.SpeciesUpdate,
    db: Session = Depends(get_db),
    user=Depends(require_researcher_or_admin)
):
    species = crud.update_species(db, species_id, data)
    if not species:
        raise HTTPException(status_code=404, detail="Species not found")
    return species
