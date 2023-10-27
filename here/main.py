from fastapi import FastAPI
from pydantic import BaseModel
from coder import rsa_decrypt, AEScoder, check_token, get_user_token
from dbserver import DbServer

from fastapi.staticfiles import StaticFiles


app = FastAPI()

class User(BaseModel):
    id: int
    name: str | None
    code: str  # Base64格式


aes = AEScoder()
db = DbServer()

admin_id = 123456
admin_psw = "admin"


@app.post("/api/user/signup")
async def sign_up(user: User):
    try:
        psw = rsa_decrypt(user.code)
    except:
        return {"code": 405, "msg": "错误的加密方式"}

    try:
        if user.id == admin_id:
            return {"code": 400, "msg": "管理员无需注册"}
        db_code = aes.encrypt(psw)
        db.add(user.id, user.name, db_code)
        return {"code": 200, "token": get_user_token(user.id), "admin": False}

    except Exception as e:
        return {"code": 406, "msg": "账号已注册"}


@app.post("/api/user/login")
async def login(user: User):
    global admin_id, admin_psw
    try:
        psw = rsa_decrypt(user.code)
    except:
        return {"code": 405, "msg": "错误的加密方式"}

    try:
        if user.id == int(admin_id) and psw == str(admin_psw):
            return {"code": 200, "token": get_user_token(str(user.id)), "admin": True}

        db_user = db.query_one(user.id)

        if aes.decrypt(db_user["code"]) == psw:
            return {"code": 200, "token": get_user_token(str(user.id)), "admin": False}

        else:
            return {"code": 405, "msg": "密码错误"}

    except:
        return {"code": 404, "msg": "用户不存在"}


@app.get("/api/data/get")
async def get_data(token: str):
    id = check_token(token)
    if not id:
        return None
    lst = db.query_all()
    for item in lst:
        del item["code"]  # 防止泄露密码
    res = [
        {
            **item,
            "total": int(item["score1"])
            + int(item["score2"])
            + int(item["score3"])
            + int(item["score4"]),
        }
        for item in lst
    ]

    res.sort(key=lambda item: item["total"], reverse=True)

    try:
        res[0]["rank"] = 1
        for i in range(1, len(res)):
            if res[i]["total"] == res[i - 1]["total"]:
                res[i]["rank"] = res[i - 1]["rank"]
            else:
                res[i]["rank"] = i + 1

        return res
    except:
        return []


class UserData(BaseModel):
    id: int
    name: str | None
    score1: int
    score2: int
    score3: int
    score4: int


@app.put("/api/data/update")
async def update_data(token: str, data: UserData):
    id = check_token(token)
    if not id or id != admin_id:
        return {"code": 403, "msg": "普通用户无法更改数据"}
    db.update(data.id, data.name, data.score1, data.score2, data.score3, data.score4)
    return {"code": 200}


@app.delete("/api/data/delete")
async def update_data(token: str, id: int):
    user_id = check_token(token)
    if not user_id or user_id != admin_id:
        return {"code": 403, "msg": "普通用户无法更改数据"}
    db.delete(id)
    return {"code": 200}



app.mount("/", StaticFiles(directory="static"), name="static")
