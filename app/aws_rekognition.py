import boto3
import cv2
from app.config import get_env

# Default Rekognition collection
COLLECTION_ID = "smart-doorbell-faces"

# AWS Rekognition client
rekognition = boto3.client(
    'rekognition',
    aws_access_key_id=get_env("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=get_env("AWS_SECRET_ACCESS_KEY"),
    region_name=get_env("AWS_REGION")
)

def create_collection(collection_id: str = COLLECTION_ID) -> None:
    try:
        rekognition.create_collection(CollectionId=collection_id)
        print(f"✅ Collection '{collection_id}' created.")
    except rekognition.exceptions.ResourceAlreadyExistsException:
        print(f"ℹ️ Collection '{collection_id}' already exists.")

def index_face(image_bytes: bytes, external_id: str, collection_id: str = COLLECTION_ID) -> dict:
    return rekognition.index_faces(
        CollectionId=collection_id,
        Image={'Bytes': image_bytes},
        ExternalImageId=external_id,
        DetectionAttributes=['DEFAULT']
    )

def search_face(image_bytes: bytes, collection_id: str = COLLECTION_ID) -> dict:
    # ✅ Step 1: Make sure there's at least one face in the image
    face_response = rekognition.detect_faces(
        Image={'Bytes': image_bytes},
        Attributes=['DEFAULT']
    )

    if not face_response['FaceDetails']:
        return {
            "matched": False,
            "confidence": 0,
            "person": None,
            "reason": "no_face_detected"
        }

    # ✅ Step 2: Attempt face matching
    response = rekognition.search_faces_by_image(
        CollectionId=collection_id,
        Image={'Bytes': image_bytes},
        MaxFaces=1,
        FaceMatchThreshold=85
    )

    if response['FaceMatches']:
        match = response['FaceMatches'][0]
        return {
            "matched": True,
            "confidence": match['Similarity'],
            "person": match['Face']['ExternalImageId']
        }

    return {
        "matched": False,
        "confidence": 0,
        "person": None
    }

def list_faces(collection_id: str = COLLECTION_ID) -> list:
    return rekognition.list_faces(CollectionId=collection_id).get('Faces', [])

def delete_face(face_id: str, collection_id: str = COLLECTION_ID) -> None:
    rekognition.delete_faces(CollectionId=collection_id, FaceIds=[face_id])
    print(f"🗑️ Face ID {face_id} removed from collection '{collection_id}'")

def frame_to_bytes(frame) -> bytes:
    _, buffer = cv2.imencode('.jpg', frame)
    return buffer.tobytes()
