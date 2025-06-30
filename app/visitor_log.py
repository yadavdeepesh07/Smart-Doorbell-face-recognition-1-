import json, os, cv2
from datetime import datetime
import shutil

LOG_FILE = "logs/visitor_log.json"
RAW_DIR = "logs/snapshots"
STATIC_DIR = "static/snapshots"

# Ensure folders exist
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)

def log_visitor(name, confidence, frame):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{name}_{timestamp}.jpg"

    raw_path = os.path.join(RAW_DIR, filename)
    static_path = os.path.join(STATIC_DIR, filename)
    public_path = f"static/snapshots/{filename}"

    # Save snapshot
    cv2.imwrite(raw_path, frame)
    shutil.copy(raw_path, static_path)

    entry = {
        "name": name,
        "confidence": round(confidence, 2),
        "timestamp": timestamp.replace("_", " "),
        "image_path": public_path
    }

    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as f:
            json.dump([], f)

    with open(LOG_FILE, 'r+') as f:
        data = json.load(f)
        data.append(entry)
        f.seek(0)
        json.dump(data, f, indent=2)

    print(f"Logged visitor: {entry}")
