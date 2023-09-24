from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.security import OAuth2AuthorizationCodeBearer
from pydantic import BaseModel
from jose import JWTError, jwt
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")

ALGORITHM = "HS256"

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    email: str
    roles: str

users_db = {}

oauth2_google = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://accounts.google.com/o/oauth2/auth",
    tokenUrl="https://oauth2.googleapis.com/token",
    clientId=GOOGLE_CLIENT_ID,
    clientSecret=GOOGLE_CLIENT_SECRET,
    scopes=["email"]
)

oauth2_github = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://github.com/login/oauth/authorize",
    tokenUrl="https://github.com/login/oauth/access_token",
    clientId=GITHUB_CLIENT_ID,
    clientSecret=GITHUB_CLIENT_SECRET,
    scopes=["user:email"]
)

def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/token", response_model=Token)
async def login_for_access_token(email: str = Query(...), password: str = Query(...)):
    user = users_db.get(email)
    if not user or user.get("password") != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": email, "roles": user.get("roles")})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/register", response_model=User)
async def register(email: str, password: str, roles: str):
    if email in users_db:
        raise HTTPException(status_code=400, detail="Email already exists")

    users_db[email] = {"email": email, "password": password, "roles": roles}
    return {"email": email, "roles": roles}

@app.get("/login/google")
async def login_google(code: str):
    data = {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": "http://localhost:8000/login/google"
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post("https://oauth2.googleapis.com/token", data=data)
        google_token_info = resp.json()

    google_access_token = google_token_info.get("access_token")
    headers = {"Authorization": f"Bearer {google_access_token}"}

    async with httpx.AsyncClient() as client:
        resp = await client.get("https://www.googleapis.com/oauth2/v3/userinfo", headers=headers)
        user_info = resp.json()

    email = user_info.get("email")

    if email not in users_db:
        users_db[email] = {"email": email, "roles": "user"}

    access_token = create_access_token({"sub": email, "roles": users_db[email]["roles"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/login/github")
async def login_github(code: str):
    data = {
        "client_id": GITHUB_CLIENT_ID,
        "client_secret": GITHUB_CLIENT_SECRET,
        "code": code
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post("https://github.com/login/oauth/access_token", data=data)
        github_token_info = resp.text.split("&")

    github_access_token = github_token_info[0].split("=")[1]
    headers = {"Authorization": f"Bearer {github_access_token}"}

    async with httpx.AsyncClient() as client:
        resp = await client.get("https://api.github.com/user/emails", headers=headers)
        user_info = resp.json()

    email = user_info[0].get("email")

    if email not in users_db:
        users_db[email] = {"email": email, "roles": "user"}

    access_token = create_access_token({"sub": email, "roles": users_db[email]["roles"]})
    return {"access_token": access_token, "token_type": "bearer"}
