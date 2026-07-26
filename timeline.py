import cv2

class Timeline:

    def __init__(self, player):

        #saves the Video player as an object
        self.player = player

        #Distance from the edge of the window
        self.margin = 30

        #Thickness of the timeline
        self.height = 8

        #sets timeline position
        self.start_x = 0
        self.end_x = 0
        self.y = 0
        self.width = 0

        #is the user dragging the slider
        self.dragging = False

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

    def handle_mouse(self, event, x, y):
        #Left mouse button was pressed
        if event == cv2.EVENT_LBUTTONDOWN:

            #was the click inside the timeline
            if (self.start_x <= x <= self.end_x and self.y <= y <= self.y + self.height):

                self.dragging = True
                self.jump_to_mouse(x)

        #Mouse moved
        elif event == cv2.EVENT_MOUSEMOVE:

            if self.dragging:
                self.jump_to_mouse(x)

        #Mouse button up
        elif event == cv2.EVENT_LBUTTONUP:
            self.dragging = False

    def draw(self, frame):
        
        #calculates timelines position
        self.y = frame.shape[0] - 25

        self.start_x = self.margin
        
        self.end_x = frame.shape[1] - self.margin 

        self.width = self.end_x - self.start_x

        #draw the back ground
        cv2.rectangle( frame, (self.start_x, self.y), (self.end_x, self.y + self.height), (70, 70, 70), -1)

        #safe guard against dividing by zero
        if self.width <= 0:
            return

        #calculate how far into the video the frame is
        progress = self.player.current_frame / (self.player.total_frames - 1)

        #convert the progress into pixels
        marker_x = int(self.start_x + progress * self.width)

        #draw progress
        cv2.rectangle(frame, (self.start_x, self.y), (marker_x, self.y + self.height), (0, 255, 0), -1)

        #draw current frame marker
        cv2.circle(frame, (marker_x, self.y + self.height // 2), 7, (255, 255, 255), -1)