from fastapi import Query, HTTPException, Depends, FastAPI
from requests import Session
from database import base,engine,get_db
from models import Gym_Branch,Membership_plans
from schemas import (
    BranchOut,
    BranchCreate,
    MembershipPlanOut,
    MembershipPlanCreate,
    MembershipPlanUpdate,
    BranchWithPlans
)
import uvicorn

app = FastAPI()

base.metadata.create_all(bind = engine)

@app.post("/branches",response_model=BranchOut,status_code=201)
def Branches(
    data:BranchCreate,
    db: Session = Depends(get_db)
): 
    parent = db.query(Gym_Branch).filter(Gym_Branch.name == data.name).first()
    if parent is None:
        new_branch = Gym_Branch(**data.model_dump())
    db.add(new_branch)
    db.commit()
    db.refresh(new_branch)
    return new_branch

    
#create a membership under specific branch

@app.post("/branches/{parent_id}/membership_plans",response_model=MembershipPlanOut,status_code=201)
def CreatePlan(
    parent_id : int,
    data : MembershipPlanCreate,
    db: Session = Depends(get_db)
):
    parent = db.query(Gym_Branch).filter(Gym_Branch.id == parent_id).first()

    if parent is None:
        raise HTTPException(status_code=404,detail="Branch Not Found")
    new_membership = Membership_plans(branch_id=parent_id,**data.model_dump())
    db.add(new_membership)
    db.commit()
    db.refresh(new_membership)
    return new_membership

@app.get("/branches/{parent_id}",response_model=BranchWithPlans,status_code=200)
def GetbranchwithPlan(
    parent_id : int,
    duration_months : int |None = None,
    sort : str| None = None,
    db : Session = Depends(get_db)
):
    parent = db.query(Gym_Branch).filter(Gym_Branch.id == parent_id).first()

    if parent is None:
            raise HTTPException(status_code= 404,description="Gym Not Found")

    
    query = db.query(Membership_plans).filter(Membership_plans.branch_id == parent_id)

    if duration_months is not None:
         query = query.filter(Membership_plans.duration_months == duration_months)

    if sort is not None:
        if sort == "name":
            query = query.order_by(Membership_plans.name,Membership_plans.id)
        elif sort == "monthly_fee":
            query = query.order_by(Membership_plans.monthly_fee,Membership_plans.id)
        else :
            raise HTTPException(status_code=400,description ="Provide valid sort")

    result = query.all()

    return{
            "id ": parent.id,
            "name": parent.name,
            "city":parent.city,
            "membership_plans":result
        }


@app.put("/branches/{parent_id}/membership_plans/{child_id}",response_model=MembershipPlanOut,status_code=201)
def UpdatePlan(
    parent_id : int ,
    child_id : int ,
    data : MembershipPlanUpdate,
    db: Session = Depends(get_db)
):
    parent = db.query(Membership_plans).filter(Membership_plans.branch_id == parent_id)
    child = db.query(Membership_plans).filter(Membership_plans.branch_id == child_id)

    if parent is None:
            raise HTTPException(status_code= 404,description="Gym Not Found")
    if child is None:
                raise HTTPException(status_code= 404,description="Mmebership Not Found")

    new_plan = Gym_Branch(branch_id=child_id,**data.model_dump())
    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)
    return new_plan


if __name__ == "__main__": 
    uvicorn.run(
        "main:app",
        host = "0.0.0.0",
        port = 8000
    )