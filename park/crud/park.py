from sqlalchemy.orm import Session
from sqlalchemy.dialects.mysql import insert
from park.models.park import Park, Address, Facility, ParkFacility

class ParkCRUD:
    @staticmethod
    def create_or_update_park(db: Session, park_data: dict):

        stmt = insert(Park).values(
            osm_id=park_data['osm_id'],
            name=park_data['name'],
            latitude=park_data['lat'],
            longitude=park_data['lon']
        )

        stmt = stmt.on_duplicate_key_update(
            name=stmt.inserted.name,
            latitude=stmt.inserted.latitude,
            longitude=stmt.inserted.longitude
        )
        
        db.execute(stmt)
        db.flush() 

        park = db.query(Park).filter(Park.osm_id == park_data['osm_id']).first()

        if park_data.get('address'):
            address_data = park_data['address']
            address_stmt = insert(Address).values(
                park_id=park.id,
                street=address_data.get('street'),
                subdistrict=address_data.get('subdistrict'),
                district=address_data.get('district'),
                postcode=address_data.get('postcode')
            ).on_duplicate_key_update(
                street=address_data.get('street'),
                subdistrict=address_data.get('subdistrict'),
                district=address_data.get('district'),
                postcode=address_data.get('postcode')
            )
            db.execute(address_stmt)

        if park_data.get('facilities'):
            for facility_name in park_data['facilities']:

                facility = db.query(Facility).filter(Facility.name == facility_name).first()
                if not facility:
                    facility = Facility(name=facility_name)
                    db.add(facility)
                    db.flush()

                db.execute(
                    insert(ParkFacility).values(
                        park_id=park.id,
                        facility_id=facility.id
                    ).on_duplicate_key_update(
                        park_id=park.id,
                        facility_id=facility.id
                    )
                )
        
        db.commit()