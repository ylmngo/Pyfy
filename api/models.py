class FileModel: 
    def __init__(self, file_id: int, uploaded_at: str, *, user_id:int, filename: str, metadata: str): 
        self.file_id = file_id
        self.user_id = user_id 
        self.filename = filename 
        self.metadata = metadata 
        self.uploaded_at = uploaded_at

    def __str__(self): 
        return f"{self.filename}"

class UserModel: 
    def __init__(self, id: int, created_at, name: str, email: str, password_hash: bytes, version: int) -> None:
        self.id = id 
        self.name = name 
        self.email = email 
        self.password_hash = password_hash 
        self.version = version 

    
