import cv2
import os
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
from .uploader import upload_to_s3
from .emailer import send_email
from ultralytics import YOLO
import yt_dlp

load_dotenv()

executor = ThreadPoolExecutor(max_workers=4)
yolo_model = YOLO("yolov8n.pt")
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


def get_youtube_stream_url(youtube_url: str) -> str:
    try:
        ydl_opts = {"format": "best", "noplaylist": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            stream_url = info.get("url")
            print(f"✅ YouTube stream resolved: {stream_url[:60]}...")
            return stream_url
    except Exception as e:
        print(f"❌ Failed to resolve YouTube URL: {e}")
        return youtube_url


def detect_objects(video_path, max_duration=3, mode="object"):
    if "youtube.com" in video_path or "youtu.be" in video_path:
        print("🔗 Resolving YouTube video stream...")
        video_path = get_youtube_stream_url(video_path)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"❌ Could not open video stream: {video_path}")
        return []

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    run_dir = os.path.join("images", f"run_{timestamp}")
    os.makedirs(run_dir, exist_ok=True)

    print(f"Processing feed: {video_path}")
    print(f"Saving temporary frames in: {run_dir}")

    events = []
    detected_images = []
    frame_count = 0
    start_time = time.time()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if mode == "object":
            results = yolo_model(frame)
            detections = []

            for box in results[0].boxes:
                cls_id = int(box.cls[0])
                label = results[0].names[cls_id]
                conf = float(box.conf[0])
                if conf > 0.5:
                    detections.append(label)
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            if detections:
                frame_file = os.path.join(run_dir, f"frame_{frame_count}.jpg")
                cv2.imwrite(frame_file, frame)
                executor.submit(upload_to_s3, frame_file, f"detected_frames/{os.path.basename(frame_file)}")
                events.append(f"Detected {', '.join(set(detections))} at frame {frame_count}")
                detected_images.append(frame_file)
                frame_count += 1

        else:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(30, 30))
            if len(faces) > 0:
                frame_file = os.path.join(run_dir, f"frame_{frame_count}.jpg")
                cv2.imwrite(frame_file, frame)
                executor.submit(upload_to_s3, frame_file, f"detected_frames/{os.path.basename(frame_file)}")
                events.append(f"Human detected at frame {frame_count}")
                detected_images.append(frame_file)
                frame_count += 1

        if time.time() - start_time > max_duration:
            print(f"Reached max duration ({max_duration}s). Stopping detection.")
            break

    cap.release()

    if detected_images:
        send_email(detected_images)

    print(f"Detection finished: {len(events)} events found.")
    print(f"Frames stored at: {run_dir}")
    print("You can safely delete that folder after reviewing/uploading.")

    return events
