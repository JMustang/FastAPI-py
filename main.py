from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()


@app.get('/')
def root():
    return {'message': 'Hello, world!'}


@app.get("/posts")
def get_post():
    return {"data": "This is your posts"}


@app.post("/createposts")
def create_post(payload: dict = Body(...)):
    print(payload)
    return {"new_post": f"title: {payload['title']} content: {payload['content']}"}
