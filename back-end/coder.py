from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher

from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
import base64

import time
import jwt

# 用于网站传输加密
# 公钥、私钥，公钥前端用
# pub_key = "-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCTeeUgm3kuYTWbb3G25LnCTSuI\n4Kc6is+339ZoABc376sPWS5jr72yHs/tePxVCi4aKVmdRhBatXP5DoiZ9d4AETRE\nxAZWa5JMO9NxFE6Uu2Vtaj6xKyh1nMwEb+XgBI3d5f8MBSg//TrJYDwDa26G+P9g\neJzUCjr+h0ti6u83BQIDAQAB\n-----END PUBLIC KEY-----"
priv_key = RSA.import_key("-----BEGIN RSA PRIVATE KEY-----\nMIICWwIBAAKBgQCTeeUgm3kuYTWbb3G25LnCTSuI4Kc6is+339ZoABc376sPWS5j\nr72yHs/tePxVCi4aKVmdRhBatXP5DoiZ9d4AETRExAZWa5JMO9NxFE6Uu2Vtaj6x\nKyh1nMwEb+XgBI3d5f8MBSg//TrJYDwDa26G+P9geJzUCjr+h0ti6u83BQIDAQAB\nAoGACJWQEX+TRHCanPdV9GooaOeyiMdg3I6/bAnOsmOM9m/QMnbDtUBBx7g07LL9\n5xpOWC3/fiDZq1oEC+N9bo7J8vrqSOd/jWjK6YNkuOdthBdpEUmwsiK3p4F1NtTU\nf/NL8D+fb+RjQatqGChgQMvvm3wN/rroQwYuDcXswkKWLmECQQC68LzgP9C0HxIC\nkXRjVp+BE0/58W/RCba+ZvIbdCLkcz50iFBKlXP6QmC8HjrSxKPBelxGFAPepday\nDXK3gcRlAkEAyfT1pH7fwJa5Se9fv9JTazK+2XpQLAOnDf4+Kkc9mbYGZkLXUml0\nX7q3Bm951R4XHS5cZosqorpArl4WXLPuIQJAWYvx3bWT4oQzm1lTmDYpR6oZmE+n\n0UlG6WPku3PhNu9hTm7xjxiSKqHbNqGAae/ZxVc4ljUGOYPVGQtKFU8q5QJAK99Q\nIa0CNJdJpzseJNCvGIGMnjgJBJbCirKplIunYSX+2+Y3WorYIhewvPAomliQEuHI\nZupil7k4ZejAmODpoQJAEFcD8LuJav0JjPeOhnzDw9tEe2Y1yAMeSUH8RyG4NwuR\nXCIHkETmWcdKVxKd4nz6oAnfuKzdlzK7sGkQEYD2Sg==\n-----END RSA PRIVATE KEY-----")
jwt_key = "jwt@8am.run"


# # rsa加密
# def encrypt(s: str) -> (str, str):
#     global pub_key
#     # 明文编码格式
#     content = s.encode("utf-8")
#     # 公钥加密
#     crypto = rsa.encrypt(content, pub_key)
#     return (crypto, priv_key)


# rsa解密
def rsa_decrypt(code: str) -> str:
    global priv_key
    data = base64.b64decode(code)
    cipher = PKCS1_cipher.new(priv_key)
    content = cipher.decrypt(data, None)
    # content = rsa.decrypt(data, priv_key)
    return content.decode("utf-8")


class AEScoder:
    def __init__(self):
        self.__encrypt_key = "iEpSxImA0vpMUAabsjJWug=="
        self.__key = base64.b64decode(self.__encrypt_key)

    # AES加密
    def encrypt(self, psw: str) -> str:
        data = psw.encode()
        cipher = AES.new(self.__key, AES.MODE_ECB)
        encrData = cipher.encrypt(pad(data, 16, "pkcs7"))
        encrData = base64.b64encode(encrData)
        return encrData

    # AES解密
    def decrypt(self, code: str) -> str:
        code = base64.b64decode(code)
        cipher = AES.new(self.__key, AES.MODE_ECB)
        decrData = unpad(cipher.decrypt(code), 16, "pkcs7")
        return decrData.decode("utf-8")


def get_user_token(id: int):
    global jwt_key
    token_dict = {
        "iat": time.time(),  # 时间戳
        # 因考虑token过期时间太过复杂，这里略去
        "id": id,
    }
    headers = {
        "alg": "HS256",  # 声明所使用的算法
    }
    jwt_token = jwt.encode(
        token_dict,  # payload, 有效载体
        jwt_key,  # 进行加密签名的密钥
        algorithm="HS256",  # 指明签名算法方式, 默认也是HS256
        headers=headers,  # json web token 数据结构包含两部分, payload(有效载体), headers(标头)
    )

    return jwt_token


def check_token(jwt_token: str) -> str | None:
    global jwt_key
    try:
        id = int(jwt.decode(jwt_token, jwt_key, algorithms="HS256")["id"])
        return id
    except:
        return None
