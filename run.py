import cv2
import time
from app.aws_rekognition import search_face, frame_to_bytes, create_collection
from app.notification import send_email_notification
from app.visitor_log import log_visitor
from app.config import get_env, get_config

def main():
    create_collection()
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("❌ Could not open webcam.")
        return

    print("📷 Smart Doorbell Running — Press 'q' to quit.")
    notified_faces = set()
    last_check_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Frame capture failed.")
            break

        # Live feed toggle
        if get_config("ENABLE_LIVE_FEED", True):
            cv2.imshow("Smart Doorbell - Live Feed", frame)

        # Check every 1 sec
        if time.time() - last_check_time > 1:
            last_check_time = time.time()

            if not get_config("ENABLE_RECOGNITION", True):
                print("🔒 Face recognition disabled by user.")
                continue

            image_bytes = frame_to_bytes(frame)
            result = search_face(image_bytes)
            print("🔍 Rekognition result:", result)

            if result.get("reason") == "no_face_detected":
                print("⚠️ No face detected.")
                continue

            if result["matched"]:
                name = result["person"]
                confidence = result["confidence"]

                if name not in notified_faces:
                    log_visitor(name, confidence, frame)

                    if get_env("ENABLE_EMAIL", "True") == "True":
                        send_email_notification(
                            subject="🚪 Visitor Alert",
                            body=f"{name} is at the door! (Confidence: {confidence:.2f}%)",
                            to_email=get_env("EMAIL_ADDRESS")
                        )

                    notified_faces.add(name)
            else:
                name = "Unknown"
                confidence = result.get("confidence", 0)
                log_visitor(name, confidence, frame)

                if get_env("ENABLE_EMAIL", "True") == "True":
                    send_email_notification(
                        subject="🚨 Unknown Visitor Alert",
                        body="An unrecognized person is at your door. Check the dashboard.",
                        to_email=get_env("EMAIL_ADDRESS")
                    )

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("👋 Smart Doorbell session ended.")

if __name__ == "__main__":
    main()
