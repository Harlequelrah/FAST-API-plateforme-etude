from fastapi import APIRouter
user_app=APIRouter(
    prefix='/user',
    tags=['user']
)
@user_app.get('/')
async def hello():
    return{
        "message":"welcome user"
    }
