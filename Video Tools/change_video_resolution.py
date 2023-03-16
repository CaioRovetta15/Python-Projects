#!#!/usr/bin/env python3
import cv2

# Open the video file
input_video = cv2.VideoCapture('untitled.mp4')

# Get the input video resolution
frame_width = int(input_video.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(input_video.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define the output video resolution
new_frame_width = 752
new_frame_height = 480

# Create an output video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output_video = cv2.VideoWriter('video2.mp4', fourcc, 10, (new_frame_width, new_frame_height))

# Loop through the frames of the input video
while True:
    ret, frame = input_video.read()
    
    if not ret:
        break
    
    # Resize the frame to the new resolution
    resized_frame = cv2.resize(frame, (new_frame_width, new_frame_height))
    
    # Write the resized frame to the output video
    output_video.write(resized_frame)
    
    # Show the resized frame (optional)
    # cv2.imshow('Resized frame', resized_frame)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

# Release the input and output video
input_video.release()
output_video.release()

# Close all windows
cv2.destroyAllWindows()
