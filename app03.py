from typing import Annotated, List,Union

from fastapi import FastAPI, APIRouter,Header, File,UploadFile,Request
from pydantic import BaseModel

app03 = APIRouter()


class userin(BaseModel):
    username: str
    password: str
    email: str
    full_name: Union[str,None]=None

class userout(BaseModel):
    username: str
    email: str
    full_name: Union[str,None]=None

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: List[str] = []

items={"foo":Item(name="Foo",price=50.2), 
       "bar":Item(name="Bar",price=62,tags=["bar","item"])
       
       }

@app03.post("/user",response_model=userout,tags=["这是一个注册的接口"])
def creat_user(user:userin):

    return user

@app03.get("/items/{item_id}",response_model=Item,response_model_exclude_unset=True)
def read_item(item_id:str): 
    return items[item_id]

@app03.get("/items/{item_id2}",response_model=Item,response_model_include={"name","price"})
def read_item(item_id2:str): 
    return items[item_id2]

