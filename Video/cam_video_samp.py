import cv2
import pygame
import time
import threading


def play_audio(audio_path):
    """Play audio in a separate thread."""
    pygame.mixer.init()
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()


def play_video(video_path):
    """Play video using OpenCV."""
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Cannot open video file.")
        return

    # Get video frame rate
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    delay = int(1000 / fps)  # Delay between frames in milliseconds

    # Start audio playback in a separate thread
    threading.Thread(target=play_audio, args=(video_path,)).start()

    # Display the video
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Video Player', frame)

        # Close the video on pressing the 'q' key
        if cv2.waitKey(delay) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    pygame.mixer.music.stop()


# Path to your video file
video_file = r"C:\Users\fizzasadath\Documents\FINAL YEAR PROJECT\youtube_videos\1.mp4"
play_video(video_file)
