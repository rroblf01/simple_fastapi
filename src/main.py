from starlette.status import HTTP_204_NO_CONTENT
import uvicorn
from fastapi import FastAPI, Response
from ddbb.db import conn
from ddbb.models.user import users
from schemas.user import User
from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key)
app = FastAPI()

@app.get("/user/{id}")
async def get_user(id: str):
    result = conn.execute(users.select().where(users.c.id == id)).first()
    if(result):
        return result
    return {"message": "User not found"}

@app.delete("/user/{id}")
async def delete_user(id: str):
    conn.execute(users.delete().where(users.c.id == id))
    return Response(status_code=HTTP_204_NO_CONTENT)

@app.put("/user")
async def update_user(user: User):

    user_updated = {"name": user.name, "email": user.email}
    user_updated["password"] = f.encrypt(user.password.encode("utf-8"))

    conn.execute(users.update().values(user_updated).where(users.c.id == user.id))
    return {"message": "User updated"}

@app.get("/users")
async def get_users():
    return conn.execute(users.select()).fetchall()

@app.post("/user")
async def create_user(user: User):
    new_user = {"name": user.name, "email": user.email}
    new_user["password"] = f.encrypt(user.password.encode("utf-8"))

    result = conn.execute(users.insert().values(new_user))
    return conn.execute(users.select().where(users.c.id == result.lastrowid)).first()

if __name__ == '__main__':
    uvicorn.run(app=app, port=8000, host='0.0.0.0')