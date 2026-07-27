"""
Adds a timeline at the bottom of the video that shows current time and progress. It can be manipulated with the mouse.
"""
import cv2

class Timeline:

    def __init__(self, player):

        #saves the Video player as an object
        self.player = player

    # ----------------------------------
    # Appearance
    # ----------------------------------

        #Distance from the edge of the window
        self.margin = 35

        #Thickness of the timeline
        self.height = 14

        #Radius of the handle
        self.handle_radius = 12

    # ----------------------------------
    # Position
    # ----------------------------------

        #sets timeline position
        self.start_x = 0
        self.end_x = 0
        self.y = 0
        self.width = 0

    # ----------------------------------
    # Interactions
    # ----------------------------------

        #is the user dragging the slider
        self.dragging = False

        #if the mouse hovering on timeline
        self.hovering = False


    # ----------------------------------
    # Clock
    # ----------------------------------

    def format_time(self, seconds):

        minutes = int(seconds // 60)
        seconds = int(seconds % 60)

        return f"{minutes}:{seconds:02d}"

    # ----------------------------------
    # Navigaion
    # ----------------------------------

    def jump_to_mouse(self, mouse_x):
    #convert a mouse position into a frame number

        #mouse position relative to start of slider
        relative_x = mouse_x - self.start_x

        #prevent mouse from going outside the slider
        relative_x = max(0, min(relative_x, self.width))

        #convert progress to a percentage
        progress = relative_x / self.width

        #convert percentage into a frame number
        frame_number = int(progress * (self.player.total_frames - 1))

        #Tell video player to jump to mouse position
        self.player.jump_to_frame(frame_number)

    # ----------------------------------
    # Mouse Events
    # ----------------------------------

    def handle_mouse(self, event, x, y):
        #Left mouse button was pressed
        if event == cv2.EVENT_LBUTTONDOWN:

            #was the click inside the timeline
            if (self.start_x <= x <= self.end_x and self.y <= y <= self.y + self.height):

                self.dragging = True
                self.jump_to_mouse(x)

        #Mouse moved
        elif event == cv2.EVENT_MOUSEMOVE:

            #check if mouse is hovering
            self.hovering = (self.start_x <= x <= self.end_x and self.y - 20 <= y <= self.y + self.height + 20)

            #move the slider to mouse position if mouse is dragged on timeline
            if self.dragging:
                self.jump_to_mouse(x)

        #Mouse button up
        elif event == cv2.EVENT_LBUTTONUP:
            self.dragging = False

    # ----------------------------------
    # Drawing
    # ----------------------------------

    def draw(self, frame):

        current_time = self.format_time(self.player.current_time)

        total_time = self.format_time(self.player.duration)

        #calculates timelines position
        self.y = frame.shape[0] - 35

        self.start_x = self.margin
        
        self.end_x = frame.shape[1] - self.margin 

        self.width = self.end_x - self.start_x

        #safe guard against dividing by zero
        if self.width <= 0:
            return
        
        #colors for timeline and if mouse is hovering
        if self.hovering:

            background_color = (110, 110, 110)
            radius = 15

        else: 
            background_color = (70, 70, 70)
            radius = self.handle_radius

        #draw the timeline background
        cv2.rectangle(frame, (self.start_x, self.y), (self.end_x, self.y + self.height), background_color, -1)

    # ----------------------------------
    # Progress
    # ----------------------------------

        #calculate how far into the video the frame is
        if self.player.total_frames <= 1:
            progress = 0
        else :
            progress = self.player.current_frame / (self.player.total_frames - 1)

        #convert the progress into pixels
        marker_x = int(self.start_x + progress * self.width)

        #draw progress
        cv2.rectangle(frame, (self.start_x, self.y), (marker_x, self.y + self.height), (0, 255, 0), -1)

        #draw current frame marker handle
        cv2.circle(frame, (marker_x, self.y + self.height // 2), radius, (255, 255, 255), -1)

        #places the current time in the video at end start of timeline
        cv2.putText(frame, current_time,(self.start_x, self.y - 12), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        #places total time of video at end of timeline
        cv2.putText(frame, total_time, (self.end_x - 60, self.y -12), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.8, (255, 255, 255), 2)