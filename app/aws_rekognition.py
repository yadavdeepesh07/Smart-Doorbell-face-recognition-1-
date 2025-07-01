import boto3
import cv2
import os
import io
from app.config import get_env

collection_id = get_env("REKOGNITION_COLLECTION_ID", "smart-doorbell-faces")

rekognition = boto3.client(
    "rekognition",
    region_name=get_env("AWS_REGION", "us-east-1"),
    aws_access_key_id=get_env("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=get_env("AWS_SECRET_ACCESS_KEY")
)

def create_collection():
    try:
        rekognition.describe_collection(CollectionId=collection_id)
        print(f"Collection '{collection_id}' already exists.")
    except rekognition.exceptions.ResourceNotFoundException:
        rekognition.create_collection(CollectionId=collection_id)
        print(f"Created collection: {collection_id}")

def frame_to_bytes(frame):
    _, buffer = cv2.imencode(".jpg", frame)
    return io.BytesIO(buffer).read()

def search_face(image_bytes):
    try:
        response = rekognition.search_faces_by_image(
            CollectionId=collection_id,
            Image={'Bytes': image_bytes},
            FaceMatchThreshold=85,
            MaxFaces=1
        )
        matches = response.get('FaceMatches', [])
        if matches:
            match = matches[0]
            return {
                "matched": True,
                "person": match['Face']['ExternalImageId'],
                "confidence": match['Similarity']
            }
        else:
            return {
                "matched": False,
                "confidence": 0
            }
    except rekognition.exceptions.InvalidParameterException:
        return {
            "matched": False,
            "reason": "no_face_detected"
        }
    except Exception as e:
        print("Rekognition error:", e)
        return {"matched": False, "reason": "error"}

def index_face(image_bytes, external_id):
    try:
        response = rekognition.index_faces(
            CollectionId=collection_id,
            Image={'Bytes': image_bytes},
            ExternalImageId=external_id.replace(" ", "_"),
            DetectionAttributes=['DEFAULT']
        )
        return len(response['FaceRecords']) > 0
    except Exception as e:
        print("Index face error:", e)
        return False

def list_faces():
    try:
        response = rekognition.list_faces(CollectionId=collection_id)
        return response.get("Faces", [])
    except Exception as e:
        print("List faces error:", e)
        return []

def delete_face(face_id):
    try:
        rekognition.delete_faces(CollectionId=collection_id, FaceIds=[face_id])
        return True
    except Exception as e:
        print("Delete face error:", e)
        return False
