import time 
import jwt 

from .config import config 

def generate_token(email: str) -> str: 
    payload = { 
        "user_id": email,  
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, config.JWT_SECRET, config.JWT_ALG)
    return token 

def decode_jwt(token: str) -> dict: 
    try: 
        decoded_token = jwt.decode(token, config.JWT_SECRET, [config.JWT_ALG])
        if decoded_token["expires"] >= time.time(): 
            return decoded_token 
        return None 
    except: 
        return None 
    