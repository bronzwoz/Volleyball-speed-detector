""" 
Loads the entire video into memory and defines the functions used to move throughout the video
"""

import cv2

class VideoPlayer:

    def __init__(self, filename):

        #Empty list that stores all the frames
        self.frames = []

        #opens the video
        video = cv2.VideoCapture(filename)

        #Stops program if video cant be opened
        if not video.isOpened():
            raise FileNotFoundError(f"Could not open {filename}")
        
        #Read useful information
        self.fps = video.get(cv2.CAP_PROP_FPS)
        self.width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

        print("Loading video into memory...")

        while True:

            #Reads the next frame
            ret, frame = video.read()

            #if no more frames exit the loop
            if not ret:
                break

            #Add the frame to our list
            self.frames.append(frame)

        video.release()

        #total number of frames loaded
        self.total_frames = len(self.frames)

        #Length of video
        self.duration = self.total_frames / self.fps

        #Current frame being viewed
        self.current_frame = 0

        print(f"Loaded {self.total_frames} frames.")

    @property
    def current_time(self):
        #Returns the current time in video in seconds
        return self.current_frame / self.fps

    def get_frame(self):
        #Returns the frame being currently displayed
        return self.frames[self.current_frame]
    
    def next_frame(self):
        #Move forwards by one frame, not past max time
        if self.current_frame < self.total_frames - 1:
            self.current_frame += 1

    def previous_frame(self): 
        #Move back one frame but not past min time
        if self.current_frame > 0:
            self.current_frame -= 1

    def restart(self):
        #Restart from frame zero
        self.current_frame = 0

    def jump_to_frame(self, frame_number):
        #Clamps the max and min number of frame skips to amount of frames in video and 0
        self.current_frame = max(0, min(frame_number, self.total_frames - 1))

    def jump_forward(self, amount):
        #Skip forward an amount of frames
        self.jump_to_frame(self.current_frame + amount)

    def jump_backward(self, amount):
        #Skip back an amount of frames
        self.jump_to_frame(self.current_frame - amount)