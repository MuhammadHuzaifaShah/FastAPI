from typing import Optional
from fastapi import FastAPI, Response, status,HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import session
from . import models,schemas
from .dataBase import engine,get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:

    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
                                password='Huz123Shah', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
             {"title": "favourite foods", "content": "I like pizza", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p
        
def find_idx(id):
    for i,p in enumerate(my_posts):

        if p['id']==id:
            return i


@app.get("/")  
def root():
    return {"message": "Welcome to my API!!!!"}

@app.get("/posts", status_code=status.HTTP_200_OK)
def data(db:session= Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts=cursor.fetchall()
    posts=db.query(models.Post).all()
    return {"data " : posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate,db:session= Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit() using SQL
    # using ORM
    new_post =models.Post(**post.dict())
    # (title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data" : new_post}
    

@app.get("/post/{id}")
def get_posts(id: int,db:session= Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()
    post=db.query(models.Post).filter(models.Post.id==id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"post with id: {id} was not found")  
    return {"post_detail" : post}


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db:session= Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # delete_post=cursor.fetchone()
    # conn.commit()
    delete_postpost=db.query(models.Post).filter(models.Post.id==id)
    

    if delete_postpost.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"post with id: {id} does not exist")
    
    delete_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: schemas.PostCreate,db:session= Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, str(id)))
    # update_post=cursor.fetchone()
    # conn.commit()
    # index=find_idx(id)
    post_query=db.query(models.Post).filter(models.Post.id==id)
    db_post=post_query.first()

    if db_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"post with id: {id} does not exist")
    
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()


    # post.dict()=>{'title':'hay this is updated post','content':'This is the updated content'}
    # post_dict = post.model_dump()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    return {'Data' : post_query.first()}