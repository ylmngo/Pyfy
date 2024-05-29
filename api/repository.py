from typing import List, Optional

from databases import Database

from .models import FileModel, UserModel
from .queries import SELECT_ALL_FILES, SELECT_FILE, INSERT_FILE, INSERT_USER, SELECT_USER_BY_EMAIL

class BaseRepository: 
    def __init__(self, db: Database) -> None: 
        self.db = db 

class FileRepository(BaseRepository): 
    async def get_files(self, user_id: int) -> List[FileModel]: 
        rows = await self.db.fetch_all(SELECT_ALL_FILES, values={"user_id": user_id})
        if not rows: 
            return None
        files = [] 
        for row in rows: 
            file = FileModel(**row)
            files.append(file)
        return files 
    
    async def get_file(self, filename: str, user_id: int) -> Optional[FileModel]: 
        row = await self.db.fetch_one(SELECT_FILE, values={"filename": filename, "user_id": user_id})
        if not row: 
            return None 
        return FileModel(**row)
    
    async def post_file(self, user_id: int, filename: str, metadata: str): 
        file_id, uploaded_at = await self.db.fetch_one(INSERT_FILE, values={"user_id": user_id,"filename": filename,"metadata": metadata})
        return file_id, uploaded_at
    
class UserRepository(BaseRepository): 
    async def post_user(self, name: str, password_hash: bytes, email: str): 
        id, created_at = await self.db.fetch_one(INSERT_USER, values={"name": name, "password_hash": password_hash, "email": email})
        return id, created_at 
    
    async def get_user_by_email(self, email: str): 
        user = await self.db.fetch_one(SELECT_USER_BY_EMAIL, values={"email": email})
        return UserModel(**user)