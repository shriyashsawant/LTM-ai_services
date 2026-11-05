from pydantic import BaseModel,Field,ConfigDict,StrictInt

class BranchCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    name : str = Field(min_length = 1,nullable=False)
    city : str = Field(min_length = 1,nullable=False)

class BranchOut(BaseModel):
    id : int
    name : str
    city : str

    model_config = ConfigDict(from_attribute=True)

class MembershipPlanCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    name : str  = Field(min_length = 1,nullable=False)
    duration_months : StrictInt =Field(...,ge = 1)
    monthly_fee : StrictInt = Field(...,ge = 300)
    guest_passes : StrictInt = Field(...,ge = 0)


class MembershipPlanUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    name : str| None  = Field(min_length = 1,nullable=False)
    duration_months : StrictInt| None =Field(...,ge = 1)
    monthly_fee : StrictInt | None = Field(...,ge = 300)
    guest_passes : StrictInt | None = Field(...,ge = 0)


class MembershipPlanOut(BaseModel):
    name : str 
    duration_months : int 
    monthly_fee : int 
    guest_passes : int 
    model_config= ConfigDict(from_attributes=True)


class BranchWithPlans(BranchOut):
    membership_plans : list[MembershipPlanOut]=Field(default_factory=[])
