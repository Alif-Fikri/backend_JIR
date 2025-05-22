# from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
# from sqlalchemy.orm import relationship
# from datetime import datetime
# from auth.database import Base

# class Report(Base):
#     __tablename__ = "reports"

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     image_path = Column(String, nullable=False)
#     description = Column(Text, nullable=False)
#     status = Column(String, default="Menunggu")
#     created_at = Column(DateTime, default=datetime.utcnow)

#     user = relationship("User", back_populates="reports")