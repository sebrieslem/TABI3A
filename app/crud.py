from sqlalchemy.orm import Session
from . import models, schemas


def create_park(db: Session, park: schemas.ParkCreate):
    db_park = models.Park(**park.dict())
    db.add(db_park)
    db.commit()
    db.refresh(db_park)
    return db_park


def get_parks(db: Session):
    return db.query(models.Park).all()


def get_park(db: Session, park_id: int):
    return db.query(models.Park).filter(models.Park.id == park_id).first()


def delete_park(db: Session, park_id: int):
    park = get_park(db, park_id)
    if park:
        db.delete(park)
        db.commit()
    return park
def update_user_role(db: Session, user_id: int, role: str):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        user.role = role
        db.commit()
        db.refresh(user)
    return user

def create_species(db: Session, species: schemas.SpeciesCreate):
    parks = db.query(models.Park).filter(
        models.Park.id.in_(species.park_ids)
    ).all()

    db_species = models.Species(
        common_name=species.common_name,
        scientific_name=species.scientific_name,
        category=species.category,
        conservation_status=species.conservation_status,
        endemic=species.endemic,
        parks=parks
    )

    db.add(db_species)
    db.commit()
    db.refresh(db_species)
    return db_species


def get_species(db: Session):
    return db.query(models.Species).all()

def update_park(db: Session, park_id: int, park_data: schemas.ParkUpdate):
    park = db.query(models.Park).filter(models.Park.id == park_id).first()
    if not park:
        return None

    for key, value in park_data.dict(exclude_unset=True).items():
        setattr(park, key, value)

    db.commit()
    db.refresh(park)
    return park

def update_species(db: Session, species_id: int, data: schemas.SpeciesUpdate):
    species = db.query(models.Species).filter(models.Species.id == species_id).first()
    if not species:
        return None

    for key, value in data.dict(exclude_unset=True).items():
        setattr(species, key, value)

    db.commit()
    db.refresh(species)
    return species

def delete_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return None

    db.delete(user)
    db.commit()
    return user

def get_species_by_park(db: Session, park_id: int):
    park = db.query(models.Park).filter(models.Park.id == park_id).first()
    if not park:
        return None
    return park.species