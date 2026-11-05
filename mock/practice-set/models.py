from sqlalchemy import CheckConstraint, CheckConstraint, Integer,Column,String,ForeignKey
from database import base
from sqlalchemy.orm import relationship

class Gym_Branch(base):
    __tablename__ = ("gym_branches")
    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    name = Column(String,nullable=False)
    city = Column(String,nullable=False)

    __table_args__ = (
        CheckConstraint("length(trim(name))>0"),
        CheckConstraint("length(trim(city))>0"),
    )

    member = relationship(
        "Membership_plans",
        back_populates="gym"
    )

class Membership_plans(base):
    __tablename__  = ("membership_plans")
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String,nullable=False)
    duration_months = Column(Integer,nullable=False)
    monthly_fee = Column(Integer,nullable=False)
    guest_passes = Column(Integer,nullable=False)
    branch_id =  Column(Integer,ForeignKey("gym_branches.id"),nullable=False)

    __table_args__ = (
        CheckConstraint ("length(trim(name))>0"),
        CheckConstraint ( "duration_months>=1"),
        CheckConstraint ("monthly_fee>=300"),
        CheckConstraint ( "guest_passes >= 0"),
    )

    gym = relationship(
            "Gym_Branch",
            back_populates="member"
        )