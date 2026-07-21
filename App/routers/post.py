from fastapi import FastAPI, Response, status,HTTPException,Depends,APIRouter
from ..import models,schemas
from sqlalchemy.orm import Session
from ..dataBase import get_db
from .. import outh2


router=APIRouter(
    prefix="/posts",
    tags=['posts']
)

@router.get("/", status_code=status.HTTP_200_OK,response_model=list[schemas.Post])
# ,response_model=list[schemas.Post] without using this we can also get all posts
def data(db:Session= Depends(get_db),current_user:int =Depends(outh2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts=cursor.fetchall()
    posts=db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post: schemas.PostCreate,db:Session= Depends(get_db),
                current_user:int =Depends(outh2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit() using SQL
    # using ORM
    print(current_user.email)
    new_post =models.Post(user_id=current_user.id,**post.model_dump())
    # (title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
    

@router.get("/{id}",response_model=schemas.Post)
def get_posts(id: int,db:Session= Depends(get_db),
              current_user:int =Depends(outh2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()
    post=db.query(models.Post).filter(models.Post.id==id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"post with id: {id} was not found") 
     
    return  post


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db:Session= Depends(get_db),
                current_user: int=Depends(outh2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # delete_post=cursor.fetchone()
    # conn.commit()
    delete_post_query=db.query(models.Post).filter(models.Post.id==id)

    delete_post=delete_post_query.first()
    

    if delete_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"post with id: {id} does not exist")
    
    if delete_post.user_id !=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested Action.")
    
    delete_post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate,db:Session= Depends(get_db),
                current_user:int =Depends(outh2.get_current_user)):
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
    
    if db_post.user_id !=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested Action.")
    
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()


    # post.model_dump()=>{'title':'hay this is updated post','content':'This is the updated content'}
    # post_model_dump = post.model_dump()
    # post_model_dump['id'] = id
    # my_posts[index] = post_model_dump
    return  post_query.first()

