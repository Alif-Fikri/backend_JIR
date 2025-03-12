from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from park.models.park import Address
from .. import schemas, crud
from ..dependencies import get_db
from park.schemas import ParkResponse, park  
from .. import models
from sqlalchemy.orm import joinedload

router = APIRouter(prefix="/parks", tags=["parks"])

@router.get("/", response_model=List[schemas.ParkResponse])
def get_parks(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    try:
        parks = db.query(models.Park)\
            .options(
                joinedload(models.Park.address),
                joinedload(models.Park.facilities)
            )\
            .offset(skip)\
            .limit(limit)\
            .all()
            
        return [
            schemas.ParkResponse(
                id=park.id,
                osm_id=park.osm_id,
                name=park.name,
                latitude=park.latitude,
                longitude=park.longitude,
                address=schemas.Address(
                    street=park.address.street,
                    subdistrict=park.address.subdistrict,
                    district=park.address.district,
                    postcode=park.address.postcode
                ) if park.address else None,
                facilities=[f.name for f in park.facilities]
            )
            for park in parks
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))