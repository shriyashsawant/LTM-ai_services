from fastapi import FastAPI, Depends, HTTPException
import models
import schemas
from database import engine, get_db
from sqlalchemy.orm import Session


models.base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/practice-area", response_model=schemas.PracticeAreaOut, status_code= 201)
def createpract(
    data: schemas.PracticeAreaCreate,
    db: Session = Depends(get_db)
):
    newPracticearea = models.PracticeArea(name = data.name, floor_number = data.floor_number)
    db.add(newPracticearea)
    db.commit()
    db.refresh(newPracticearea)
    return newPracticearea

@app.post("/practice-area/{parent_id}/consultant", response_model=schemas.ConsultantOut, status_code= 201)
def createcons(
    parent_id: int,
    data: schemas.ConsultantCreate,
    db: Session = Depends(get_db)
):
    parent = db.query(models.PracticeArea).filter(models.PracticeArea.id == parent_id).first()
    if parent is None:
        raise HTTPException(status_code = 404, detail="parent not found")
    newCon = models.Consultant(
        name = data.name, designation = data.designation, experience_years = data.experience_years, consultation_fee = data.consultation_fee
    )
    db.add(newCon)
    db.commit()
    db.refresh(newCon)
    return newCon

@app.get("/practice-area/{parent_id}", response_model=schemas.PracticeAreaWithConsultat, status_code= 200)
def getPrac(
    parent_id: int,
    db: Session = Depends(get_db),
    designation : str | None = None,
    sort: str | None = None
):
    parent = db.query(models.PracticeArea).filter(models.PracticeArea.id == parent_id).first()
    if parent is None:
        raise HTTPException(status_code = 404, detail="parent not found")

    consultant_query = db.query(models.Consultant).filter(models.Consultant.practice_area_id == parent_id)
 
    if designation is not None or designation.strip() != "":
        consultant_query = consultant_query.filter(models.Consultant.designation == designation)

    if sort is not None:
        if sort == "name":
            consultant_query = consultant_query.sort(models.Consultant.name.asc())
        elif sort == "consultation_fee":
            consultant_query = consultant_query.sort(models.Consultant.consultation_fee.asc())
        else:
            raise HTTPException(status_code= 422, detail="invalid sort field")

    consultants = consultant_query.all()

    return {
        "id" : parent.id,
        "name" : parent.name,
        "floor_number" : parent.floor_number,
        "consultants" : consultants
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000
    )
        
    






