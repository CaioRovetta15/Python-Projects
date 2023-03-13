import cv2

# Set the input and output video paths


# Set the desired frame rate
frame_rate = 5

input_path = '640x640-30fps.mp4'
output_path = '640x640-' + str(frame_rate) + 'fps.mp4'


# Open the input video
cap = cv2.VideoCapture(input_path)

# Get the current frame rate of the input video
current_frame_rate = cap.get(cv2.CAP_PROP_FPS)

# Get the number of frames in the input video
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Calculate the number of frames to skip between each frame
skip_frames = int(current_frame_rate / frame_rate)

# Get the video codec
fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))

# Get the frame size
frame_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

# Create a video writer object for the output video
out = cv2.VideoWriter(output_path, fourcc, frame_rate, frame_size)

# Read and write each desired frame to the output video
for i in range(frame_count):
    ret, frame = cap.read()
    if ret and i % skip_frames == 0:
        out.write(frame)

# Release the input and output videos
cap.release()
out.release()
