from sqlalchemy import Integer,Column,String,ForeignKey
from database import base
from sqlalchemy.orm import relationship

class PracticeArea(base):
    __tablename__ = "practicearea"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String,nullable=False)
    floor_number = Column(Integer, nullable=False)

    consultants=relationship("Consultant",back_populates="practice_areas")

class Consultant(base):
    __tablename__ = "consultants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    designation = Column(String, nullable=False)
    consultation_fee = Column(Integer, nullable=False)
    experience_years = Column(Integer, nullable=False)

    practice_area_id = Column(Integer,ForeignKey("practicearea.id"),nullable=False)

    practice_areas = relationship("PracticeArea",back_populates="consultants")
