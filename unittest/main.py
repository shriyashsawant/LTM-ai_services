from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class UserRequest(BaseModel):
    name: str
    age: int


@app.post("/users")
def create_user(user: UserRequest):

    return {
        "name": user.name,
        "age": user.age
    }