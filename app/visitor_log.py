import json, os, cv2
from datetime import datetime
import shutil
import csv

LOG_FILE = "logs/visitor_log.json"
CSV_FILE = "logs/visitor_log.csv"
RAW_DIR = "logs/snapshots"
STATIC_DIR = "static/snapshots"

os.makedirs("logs", exist_ok=True)
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)

def log_visitor(name, confidence, frame):
    if not name or name.strip().lower() in ["none", ""]:
        name = "Unknown"

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{name}_{timestamp}.jpg"

    raw_path = os.path.join(RAW_DIR, filename)
    static_path = os.path.join(STATIC_DIR, filename)
    public_path = f"static/snapshots/{filename}"

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
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []
        data.append(entry)
        f.seek(0)
        json.dump(data, f, indent=2)

    write_header = not os.path.exists(CSV_FILE)
    with open(CSV_FILE, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if write_header:
            writer.writerow(["Name", "Confidence", "Timestamp", "Snapshot_Path"])
        writer.writerow([name, round(confidence, 2), entry["timestamp"], public_path])

    print(f"Visitor logged: {entry}")
