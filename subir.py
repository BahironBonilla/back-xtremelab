import boto3
from botocore.client import Config



# Define el nombre del bucket
BUCKET_NAME = 'bukcketlabsebastian'

# Crea una instancia del cliente de S3
s3 = boto3.resource('s3')
data = open('e.jpg', 'rb')

s3.Bucket(BUCKET_NAME).put_object(Key='e.jpg', Body=data)


print("Done")

