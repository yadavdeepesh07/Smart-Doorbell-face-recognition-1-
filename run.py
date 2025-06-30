import cv2
import os
from app.aws_rekognition import (
    search_face,
    frame_to_bytes,
    create_collection
)
from app.notification import send_email_notification
from app.visitor_log import log_visitor
from app.sms_alert import send_sms_alert
from app.config import get_env

def main():
    create_collection()
    cap = cv2.VideoCapture(0)
    print("📷 Smart Doorbell Camera Running — Press 'q' to quit.")

    notified_faces = set()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Camera not accessible.")
            break

        cv2.imshow("Smart Doorbell - Live Feed", frame)

        if int(cap.get(cv2.CAP_PROP_POS_FRAMES)) % 30 == 0:
            image_bytes = frame_to_bytes(frame)
            result = search_face(image_bytes)

            # ⚠️ Skip if no face detected
            if result.get("reason") == "no_face_detected":
                print("⚠️ No face detected in frame. Skipping.")
                continue

            if result["matched"]:
                name = result["person"]
                confidence = result["confidence"]

                if name not in notified_faces:
                    log_visitor(name, confidence, frame)
                    send_email_notification(
                        subject="🚪 Smart Doorbell Alert",
                        body=f"{name} is at the door! (Confidence: {confidence:.2f}%)",
                        to_email=get_env("EMAIL_ADDRESS")
                    )
                    send_sms_alert(name, confidence)
                    notified_faces.add(name)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("👋 Smart Doorbell session ended.")

if __name__ == "__main__":
    main()
