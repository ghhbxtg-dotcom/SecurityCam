import cv2
import requests
import time
from ultralytics import YOLO
from pathlib import Path

PUSHBULLET_TOKEN = "token"

def send_push_image(image_path):

    headers = {"Access-Token": PUSHBULLET_TOKEN}
    file_name = Path(image_path).name

    r = requests.post(
        "https://api.pushbullet.com/v2/upload-request",
        headers=headers,
        json={
            "file_name": file_name,
            "file_type": "image/jpeg"
        }
    ).json()

    upload_url = r["upload_url"]
    file_url = r["file_url"]
    data = r["data"]

    with open(image_path, "rb") as f:
        files = {"file": (file_name, f, "image/jpeg")}
        requests.post(upload_url, data=data, files=files)

    requests.post(
        "https://api.pushbullet.com/v2/pushes",
        headers={**headers, "Content-Type": "application/json"},
        json={
            "type": "file",
            "title": "Person ",
            "body": "Camera detected someone",
            "file_name": file_name,
            "file_type": "image/jpeg",
            "file_url": file_url
        }
    )

cap = cv2.VideoCapture(0)

model = YOLO("yolov8n.pt")

last_alert_time = 0
ALERT_COOLDOWN = 30  

while True:

    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)[0]
    person_found = False

    for box in results.boxes:

        cls = int(box.cls[0])

        if model.names[cls] == "person":

            person_found = True

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)

            cv2.putText(
                frame,
                "PERSON",
                (x1, y1-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0,255,0),
                2
            )

            person_crop = frame[y1:y2, x1:x2]

            image_path = "person.jpg"
            cv2.imwrite(image_path, person_crop)

    if person_found:

        now = time.time()

        if now - last_alert_time > ALERT_COOLDOWN:

            last_alert_time = now

            send_push_image("person.jpg")

            print("Push notification sent")

    cv2.imshow("securitycam", frame)

    if cv2.waitKey(1) == 27:
        break


cap.release()
cv2.destroyAllWindows()