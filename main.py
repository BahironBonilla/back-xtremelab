import os
from flask import Flask, request, jsonify
import boto3
from botocore.exceptions import NoCredentialsError
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app = Flask(__name__)

# Configura las credenciales de AWS
AWS_ACCESS_KEY_ID = 'AKIA247MBUKIV45MHGGS'
AWS_SECRET_ACCESS_KEY = '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'
S3_BUCKET_NAME = 'bukcketlabsebastian'

s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

# Ruta para subir un archivo a S3
@app.route('/upload', methods=['POST'])
def upload_file():
    
    if request.method == 'POST':
        file = request.files['file']
        if file:
            try:
                data = open(file, 'rb')
                s3.Bucket(S3_BUCKET_NAME).put_object(Key=file, Body=data)
                #s3.upload_fileobj(file, S3_BUCKET_NAME, file.filename)
                return jsonify({"message": "Archivo subido exitosamente"})
            except NoCredentialsError:
                return jsonify({"error": "Credenciales de AWS no válidas"})
        else:
            return jsonify({"error": "No se proporcionó ningún archivo en la solicitud"})

# Ruta para listar todos los archivos en S3
@app.route('/list', methods=['GET'])
def list_files():
    try:
        objects = s3.list_objects_v2(Bucket=S3_BUCKET_NAME)
        file_list = [obj['Key'] for obj in objects.get('Contents', [])]
        return jsonify({"files": file_list})
    except NoCredentialsError:
        return jsonify({"error": "Credenciales de AWS no válidas"})

# Ruta para eliminar un archivo de S3
@app.route('/delete/<file_name>', methods=['DELETE'])
def delete_file(file_name):
    try:
        s3.delete_object(Bucket=S3_BUCKET_NAME, Key=file_name)
        return jsonify({"message": f"Archivo '{file_name}' eliminado exitosamente"})
    except NoCredentialsError:
        return jsonify({"error": "Credenciales de AWS no válidas"})

if __name__ == '__main__':
    app.run(debug=True)
