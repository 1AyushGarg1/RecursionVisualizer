from fastapi import Request
from fastapi import HTTPException

def verify_token(request: Request):
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    
    token = auth.split(" ")[1]
    token_record = tokens_collection.find_one({"token": token})
    
    if not token_record:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return token_record["username"] 