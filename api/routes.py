import os 
import mimetypes
import bcrypt

from fastapi import APIRouter, Response, Depends 
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from starlette.requests import Request

from .dependencies import get_repository, user_from_token
from .repository import FileRepository, UserRepository
from .models import UserModel
from .limiter import limiter
from .utils import generate_token

router = APIRouter() 

@router.get("/files")
@limiter.limit("5/min")
async def get_files(request: Request, file_repo: FileRepository = Depends(get_repository(FileRepository)), user: UserModel = Depends(user_from_token)): 
    files = await file_repo.get_files(user.id)
    json_response = jsonable_encoder(files)
    return JSONResponse(content=json_response)


@router.get("/file/{filename}")
@limiter.limit("5/min")
async def get_file(request: Request, filename: str, file_repo: FileRepository = Depends(get_repository(FileRepository)), user: UserModel = Depends(user_from_token)): 
    redis = request.app.state._redis 
    path = os.getcwd() + f"\\uploads\\{filename}"
    mt = mimetypes.guess_type(path)
    
    if redis: 
        v = redis.get(f"{user.id}_{filename}")
    if v: 
        return Response(content=v, media_type=mt[0])

    file = await file_repo.get_file(filename=filename, user_id=user.id)
    if not file: 
        return "No such file exists"    
    
    with open(path, 'rb') as f: 
        buf = f.read()

    redis.set(f"{user.id}_{filename}", buf)

    return Response(content=buf, media_type=mt[0])    

@router.post("/upload")
@limiter.limit("5/min")
async def upload_file(request: Request, file_repo: FileRepository = Depends(get_repository(FileRepository)), user: UserModel = Depends(user_from_token)):  
    form_data = await request.form() 
    form_file = form_data["afile"]

    file_id, uploaded_at = await file_repo.post_file(user.id, form_file.filename, "Something about the file")

    buf = form_file.file.read()
    path = os.getcwd() + f"\\uploads\\{form_file.filename}"
    with open(path, 'wb') as f: 
        f.write(buf)

    await form_data.close() 
    return {"response": "Success!", "file_id": file_id, "uploaded_at": uploaded_at}


# User Authentication Routes 

@router.post("/register")
async def register(req: Request, user_repo: UserRepository = Depends(get_repository(UserRepository))): 
    data = await req.json()    
    
    username, password, email = data["username"], data["password"], data["email"]
    if username == "" or password == "" or email == "": 
        return "Invalid User Credentials"
    
    password_hash = bcrypt.hashpw(bytes(password, encoding='utf-8'), bcrypt.gensalt())
    
    user_id, created_at = await user_repo.post_user(username, password_hash, email)

    return {"register": "Success", "user_id": user_id, "created_at": created_at}

@router.post("/login") 
async def login(req: Request, user_repo: UserRepository = Depends(get_repository(UserRepository))): 
    data = await req.json() 

    username, password, email = data["username"], data["password"], data["email"]

    if username == "" or password == "" or email == "": 
        return "Invalid User Credentials"
    
    user = await user_repo.get_user_by_email(email=email)
    if not user: 
        return "Email does not exist"
    if not bcrypt.checkpw(bytes(password, encoding='utf-8'), user.password_hash):
        return "Password does not match" 
    
    token = generate_token(email=user.email)

    return {"response": "Succesfully logged in", "access_token": token}
    
