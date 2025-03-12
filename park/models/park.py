from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from park.database import Base

class Park(Base):
    __tablename__ = "parks"

    id = Column(Integer, primary_key=True, index=True)
    osm_id = Column(Integer, unique=True)
    name = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)
    
    address = relationship("Address", uselist=False, back_populates="park")
    facilities = relationship("Facility", secondary="park_facility", back_populates="parks")

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    park_id = Column(Integer, ForeignKey("parks.id"))
    street = Column(String(255))
    subdistrict = Column(String(100))
    district = Column(String(100))
    postcode = Column(String(10))
    
    park = relationship("Park", back_populates="address")

class Facility(Base):
    __tablename__ = "facilities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True)
    
    parks = relationship("Park", secondary="park_facility", back_populates="facilities")

class ParkFacility(Base):
    __tablename__ = "park_facility"

    park_id = Column(Integer, ForeignKey("parks.id"), primary_key=True)
    facility_id = Column(Integer, ForeignKey("facilities.id"), primary_key=True)