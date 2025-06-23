from Fibonacci import fibonacci_frames_full_lifecycle
from Factorial import factorial_frames_full_lifecycle
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pymongo import MongoClient
from fastapi import Depends
import uuid
from fastapi.responses import Response
import os
import zipfile
import io
from fastapi import Form
from fastapi import HTTPException,Request
from pymongo import MongoClient


app = FastAPI()
# import shutil
# print(shutil.which("dot"))

# MongoDB setup
from dotenv import load_dotenv
load_dotenv()
client = MongoClient(host=os.getenv("MONGO_DB_URL"))
db = client["authdb"]
tokens_collection = db["tokens"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React dev server
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

def varify_token(request: Request):
    auth = request.headers.get("Authorization")
    # print(auth)
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    
    token = auth.split(" ")[1]
    token_record = tokens_collection.find_one({"token": token})
    # print(token_record)
    # print(token)
    if not token_record:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # print(token_record['username'])
    return token_record["username"]



@app.post('/fibonacci')
def fibonacci(n: int,username:str = Depends(varify_token)):
    # print(n,username)
    # 1. Generate frames (into ./frames)
    id = str(uuid.uuid4())
    # print(id)
    fibonacci_frames_full_lifecycle(n,id)

    # 2. Zip the frames in memory
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        for filename in sorted(os.listdir(id)):
            if filename.endswith(".png"):
                path = os.path.join(id, filename)
                zipf.write(path, arcname=filename)

    # 3. Clean up (delete frames folder)
    for file in os.listdir(id):
        os.remove(os.path.join(id, file))
    os.rmdir(id)

    buffer.seek(0)

    return Response(
        content=buffer.getvalue(),
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=frames.zip"}
    )


@app.post("/factorial")
def factorial(n: int,username:str = Depends(varify_token)):
    id = str(uuid.uuid4());
    factorial_frames_full_lifecycle(n,id)

    buffer = io.BytesIO()  # ✅ Instantiate the buffer

    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        for filename in sorted(os.listdir(id)):
            if filename.endswith(".png"):
                path = os.path.join(id, filename)
                zipf.write(path, arcname=filename)

    # Clean up (delete files but keep folder)
    for file in os.listdir(id):
        os.remove(os.path.join(id, file))
    # Optionally delete the folder:
    os.rmdir(id)

    buffer.seek(0)  # ✅ reset pointer to beginning of zip

    return Response(
        content=buffer.getvalue(),
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=frames.zip"},
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8080)
# from pymongo import MongoClient

# client = MongoClient(host="mongodb+srv://ayushgarg5002:o8zHILwIQ9HnhcWx@cluster0.7gau7mw.mongodb.net/")
# print(client.list_database_names())
