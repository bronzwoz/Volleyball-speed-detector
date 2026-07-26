""" 
video_player.py

loads the videos into memory instead of reading the video from the disk everytime
"""

import cv2

class VideoPlayer:

    def __init__(self, filename):

        #Stores all frames here
        self.frames = []

        #opens the video
        video = cv2.VideoCapture(filename)

        if not video.isOpened():
            raise FileNotFoundError(f"Cound not open {filename}")
        
        # Read useful information
        self.fps = video.get(cv2.CAP_PROP_FPS)
        self.width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

        print("Loading video into memory...")

        while True:

            ret, frame = video.read()

            if not ret:
                break

            #Add the frame to our list
            self.frames.append(frame)

        video.release()

        #number of frames loaded
        self.total_frames = len(self.frames)

        print(f"Loaded {self.total_frames} frames.")

        #Current frame being viewed
        self.current_frame = 0

    def get_frame(self):

        return self.frames[self.current_frame]
    
    def next_frame(self):

        if self.current_frame < self.total_frames - 1:
            self.current_frame += 1

    def previous_frame(self): 

        if self.current_frame > 0:
            self.current_frame -= 1

    def restart(self):
        self.current_frame = 0

    #Clamps the max and min number of frame skips to amount of frames in video and 0
    def jump_to_frame(self, frame_number):
        self.current_frame = max(0, min(frame_number, self.total_frames - 1))

    def jump_forward(self, amount):
        self.jump_to_frame(self.current_frame + amount)

    def jump_backward(self, amount):
        self.jump_to_frame(self.current_frame - amount)
