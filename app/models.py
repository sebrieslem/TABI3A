from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from .db import Base


park_species = Table(
    "park_species",
    Base.metadata,
    Column("park_id", Integer, ForeignKey("parks.id")),
    Column("species_id", Integer, ForeignKey("species.id"))
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)


class Park(Base):
    __tablename__ = "parks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    rules = Column(String)
    best_seasons = Column(String)

    species = relationship(
        "Species",
        secondary=park_species,
        back_populates="parks"
    )

    trips = relationship("TripRecommendation", back_populates="park")

    park_location = relationship("Location", back_populates="park", uselist=False)

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(String, nullable=False)
    longitude = Column(String, nullable=False)
    governorate = Column(String)

    park_id = Column(Integer, ForeignKey("parks.id"), unique=True)
    park = relationship("Park", back_populates="park_location")


class Species(Base):
    __tablename__ = "species"

    id = Column(Integer, primary_key=True, index=True)
    common_name = Column(String, nullable=False)
    scientific_name = Column(String, nullable=True)
    category = Column(String, nullable=False)  # FAUNA or FLORA
    conservation_status = Column(String, nullable=True)
    endemic = Column(Boolean, default=False)
    parks = relationship("Park", secondary=park_species, back_populates="species")


class TripRecommendation(Base):
    __tablename__ = "trip_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    activity = Column(String, nullable=False)
    season = Column(String, nullable=False)
    reason = Column(Text)

    park_id = Column(Integer, ForeignKey("parks.id"))
    park = relationship("Park", backref="location", uselist=False)
