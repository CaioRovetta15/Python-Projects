
import cv2
import os

# Open the video file
video_path = '640x640-1fps.mp4'
cap = cv2.VideoCapture(video_path)

# Create the frames directory if it doesn't exist
if not os.path.exists('frames3'):
    os.makedirs('frames3')

# Loop through the video frames and save every 10th frame as an image
frame_number = 0
while cap.isOpened():
    # Read a frame from the video
    ret, frame = cap.read()
    frame = cv2.resize(frame, (640, 640))

    # If there are no more frames, break out of the loop
    if not ret:
        break

    # Save every 10th frame as an image
    if frame_number % 1 == 0:
        frame_path = os.path.join('frames3', f'frame_{frame_number:06d}.jpg')
        cv2.imwrite(frame_path, frame)

    # Increment the frame number
    frame_number += 1

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
