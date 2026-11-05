from sqlalchemy import CheckConstraint, CheckConstraint, Integer,Column,String,ForeignKey
from database import base
from sqlalchemy.orm import relationship


class Branches(base):
    __tablename__ = "branches"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String,nullable=False)
    city = Column(String,nullable=False)

    book_copy = relationship("Book_Copies",back_populates="branch")

class Book_Copies(base):
    __tablenme__ = "book_copies"
    id = Column(Integer,primary_key=True,index=True)
    title = Column(Integer,nullable=False)
    genre = Column(String,nullable=False)
    replacement_cost = Column(String,nullable=False)
    available_cost = Column(Integer,nullable=False)
    branch_id= Column(Integer,ForeignKey("branches.id"),nullable=False)
    branch = relationship("Branches",back_populates="book_copy")





