from typing import Type, Callable
import time 

from databases import Database
from fastapi import Request, Depends, HTTPException, status 
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .repository import BaseRepository, UserRepository
from .config import config 
from .models import UserModel
from .utils import decode_jwt

class JWTBearer(HTTPBearer): 
    def __init__(self, auto_error: bool = True): 
        super(JWTBearer, self).__init__(auto_error=auto_error)
    
    async def __call__(self, request: Request) -> dict | None:
        cred: HTTPAuthorizationCredentials = await super().__call__(request)
        if cred: 
            if not cred.scheme == "Bearer": 
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authentication scheme")
            
            decoded_token = decode_jwt(cred.credentials)
            if not decoded_token: 
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
            return decoded_token
        else: 
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Invalid authorization code")

def get_database(request: Request): 
    return request.app.state._db

def get_repository(Repo_type: Type[BaseRepository]) -> Callable: 
    def get_repo(db: Database = Depends(get_database)) -> Type[BaseRepository]: 
        return Repo_type(db=db)
    return get_repo

async def user_from_token(token: dict = Depends(JWTBearer()), user_repo: UserRepository = Depends(get_repository(UserRepository))) -> UserModel: 
    email = token["user_id"] 
    user = await user_repo.get_user_by_email(email=email)
    if not user: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user 


