from fastapi import FastAPI
import uvicorn
from user import *
app=FastAPI()
app.include_router(user_app)

if __name__=="__main__":
   uvicorn.run("main:app",host="127.0.0.1",port=8000,reload=True)
