#imports OpenCV
import cv2

# --------------------------
# Opens the video
# --------------------------

video = cv2.VideoCapture("videos/test.mp4")

#check if video actually opened
if not video.isOpened():
    print("Could not open video")
    exit()

# --------------------------
# Read the video information
# --------------------------

#width of each frame
frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))

#Height of each frame
frame_height =int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

#FPS
fps = video.get(cv2.CAP_PROP_FPS)

#total frames in video
total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

#Length of video
video_length = total_frames / fps

#Print the video information
print("----------------------------")
print("Video Information")
print("----------------------------")
print(f"Resolution : {frame_width} x {frame_height}")
print(f"FPS        : {fps:.2f}")
print(f"Frames     : {total_frames}")
print(f"Length     : {video_length:.2f} seconds")
print("----------------------------")

frame_number = 0

#--------------------------
#Playback settings
#--------------------------

#True = video plays normally
#False = Video is paused
playing = True

#loop until the video finishes or the 'Q' is pressed
while True:

    #only reads a new frame if video is playing    
    if playing:

        #ret = frame was read - frame = the frame
        ret, frame = video.read()

        if not ret:
            break

        frame_number += 1

        #Display current frame number
        cv2.putText( frame, f"Frame: {frame_number}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        #Display the FPS
        cv2.putText(frame, f"FPS: {fps:1f}", (20,80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        #display if video is paused
        status = "Playing"

        if not playing:
            status = "Paused"

        #title, image 
        cv2.imshow("Volleyball Speed Detector", frame)

        #wait for keyboard press
        key = cv2.waitKey(30) & 0xFF

        # Q = Quit
        if key == ord("q"):
            break

        # SPACE = Play / Pause
        elif key == ord(" "):
            #changes playing to false
            playing = not playing
        
        #Forwards 1 frame
        elif key == ord("n"):
            if not playing:

                ret, frame = video.read()

                if ret:
                    frame_number += 1
        
        #Back 1 frame
        elif key == ord("b"):

            if not playing:

                #Go back 2 frames. offsets the 1 frame after read()
                frame_number = max(0, frame_number - 2)

                #moves the videos position
                video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

                #Read the frame it stoped on
                ret, frame = video.read()
                if ret:
                    frame_number += 1

        #Restarts the video
        elif key == ord("r"):
            frame_number = 0

            video.set(cv2.CAP_PROP_POS_FRAMES, 0)

#Close the video file
video.release()

#close all OpenCV windows
cv2.destroyAllWindows()


