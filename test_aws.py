import boto3
from dotenv import load_dotenv
import os

load_dotenv()

print("KEY:", os.getenv("AWS_ACCESS_KEY_ID"))


# 🔐 Use fresh, working credentials directly here
rekognition = boto3.client(
    'rekognition',
    aws_access_key_id='place_your_access_key_here',
    aws_secret_access_key='place_your_secret_key_here',
    region_name='place_your_region_here'  
)

collection_id = 'smart-doorbell-visitors'

try:
    response = rekognition.create_collection(CollectionId=collection_id)
    print(f"✅ Created collection '{collection_id}' - Status:", response['StatusCode'])
except rekognition.exceptions.ResourceAlreadyExistsException:
    print(f"ℹ️ Collection '{collection_id}' already exists.")
except Exception as e:
    print("❌ Error:", e)
