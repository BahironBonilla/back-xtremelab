from fastapi import FastAPI, HTTPException
import boto3
import psycopg2

# Configura la conexión a S3
s3 = boto3.client(
    's3',
    aws_access_key_id='https://749429957265.signin.aws.amazon.com/console',
    aws_secret_access_key='14-de-Octubre',
    region_name='us-east-2'
)

# Configura la conexión a RDS
db_connection = psycopg2.connect(
    host='basededatoslabsebastian.clmeb76jyzoh.us-east-2.rds.amazonaws.com',
    database='basededatoslabsebastian',
    user='postgresql',
    password='12345'
)

app = FastAPI()

# Definir una tabla para almacenar la información sobre los objetos de S3 en RDS
with db_connection.cursor() as cur:
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS s3_objects (
            id SERIAL PRIMARY KEY,
            object_key VARCHAR,
            object_description VARCHAR
        )
        """
    )
    db_connection.commit()

@app.post("/upload/{object_key}/{object_description}")
def upload_to_s3(object_key: str, object_description: str):
    # Subir el objeto a S3
    try:
        s3.upload_fileobj(
            open(object_key, 'rb'),
            'bukcketlabsebastian',
            object_key
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Registrar la información del objeto en la base de datos
    with db_connection.cursor() as cur:
        cur.execute(
            "INSERT INTO s3_objects (object_key, object_description) VALUES (%s, %s)",
            (object_key, object_description)
        )
        db_connection.commit()

    return {"message": "Objeto subido correctamente"}

@app.get("/download/{object_key}")
def download_from_s3(object_key: str):
    # Descargar el objeto desde S3
    try:
        s3.download_file('arn:aws:s3:::bukcketlabsebastian ', object_key, object_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Obtener la descripción del objeto desde la base de datos
    with db_connection.cursor() as cur:
        cur.execute(
            "SELECT object_description FROM s3_objects WHERE object_key = %s",
            (object_key,)
        )
        description = cur.fetchone()

    if description:
        return {"object_description": description[0]}

    raise HTTPException(status_code=404, detail="Objeto no encontrado")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
