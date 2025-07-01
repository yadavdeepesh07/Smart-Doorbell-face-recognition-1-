import cv2
from app.aws_rekognition import frame_to_bytes, search_face

# Capture a single frame from webcam
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
ret, frame = cap.read()
cap.release()

if not ret:
    print("❌ Could not read frame from webcam.")
    exit()

# Save debug frame for visual inspection
cv2.imwrite("test_frame.jpg", frame)
print("✅ Saved frame as test_frame.jpg")

# Convert frame to bytes
img_bytes = frame_to_bytes(frame)
print("🧪 Image byte size:", len(img_bytes))

# Send to Rekognition
result = search_face(img_bytes)
print("🔍 Rekognition result:", result)
