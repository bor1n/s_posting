from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from core.exceptions import DatabaseConnectionFailException
from db.base import database
from endpoint import users, auth, posts
import uvicorn

app = FastAPI(title="S Posting")
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(posts.router, prefix="/posts", tags=["posts"])


@app.exception_handler(DatabaseConnectionFailException)
async def database_exception_handler(request: Request, exc: DatabaseConnectionFailException):
    return JSONResponse(
        status_code=500,
        content={"message": f"Database connection fail: {exc.msg}"},
    )


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.connect()

if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)
