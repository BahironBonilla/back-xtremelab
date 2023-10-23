

import boto3


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware



AWS_ACCESS_KEY_ID = 'AKIA247MBUKIV45MHGGS'
AWS_SECRET_ACCESS_KEY = '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'
AWS_REGION = 'us-east-2'  # Reemplaza con tu región
S3_BUCKET_NAME = 'bukcketlabsebastian'

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import os


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/")
async def upload_file(file: UploadFile):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION
    )

    try:
        with file.file as f:
            s3_client.upload_fileobj(f, S3_BUCKET_NAME, file.filename)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

    return JSONResponse(content={"message": "Archivo cargado exitosamente"})

@app.get("/list/")
async def list_files():
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION
    )

    try:
        response = s3_client.list_objects(Bucket=S3_BUCKET_NAME)
        files = [obj['Key'] for obj in response.get('Contents', [])]
        return JSONResponse(content={"files": files})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

