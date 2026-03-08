from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

users = {}

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()

@app.get("/")
def home():
    return {"message": "JWT Auth API running successfully"}

@app.post("/register")
def register(username: str, password: str):

    if username in users:
        return {"error": "User already exists"}

    hashed_password = pwd_context.hash(password[:72])
    users[username] = hashed_password

    return {"message": "User registered successfully"}

@app.post("/login")
def login(username: str, password: str):

    if username not in users:
        return {"error": "User not found"}

    hashed_password = users[username]

    if not pwd_context.verify(password, hashed_password):
        return {"error": "Invalid password"}

    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": token}

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):

    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        return username
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/profile")
def profile(username: str = Depends(verify_token)):

    return {"message": f"Welcome {username}, this is your profile"}