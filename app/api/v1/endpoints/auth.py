from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlmodel import Session, select
from app.db.session import get_session
from app.models import User
from app.core.security import verify_password, create_access_token, decode_access_token

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str
    rememberMe: bool = False

@router.post("/login")
def login(data: LoginRequest, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == data.email)).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    access_token = create_access_token({"sub": str(user.user_id), "username": user.username})
    user_dict = user.dict()
    user_dict.pop("password_hash", None)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_dict
    }

def get_current_user(token: str = Depends(lambda: None), session: Session = Depends(get_session)):
    # Để giữ nguyên cho các endpoint khác, vẫn dùng OAuth2 nếu cần
    from fastapi.security import OAuth2PasswordBearer
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
    if token is None:
        token = Depends(oauth2_scheme)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    user = session.get(User, int(user_id))
    if user is None:
        raise credentials_exception
    return user 