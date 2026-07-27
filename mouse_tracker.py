import cv2

class MouseTracker:

    def __init__(self):

        #current mouse position
        self.x = 0
        self.y = 0

        #Is the mouse in the window
        self.active = False

    def handle_mouse(self, event, x, y, flags, param):

        if event == cv2.EVENT_MOUSEMOVE:

            self.x = x
            self.y = y
            self.active = True

    def draw(self, frame):

        if not self.active:
            return
            
        #draw virtical line
        cv2.line(frame, (self.x, 0), (self.x, frame.shape[0]), (255, 0, 0), 1)
        #draw horizontal line
        cv2.line(frame, (0, self.y), ( frame.shape[1], self.y), (255, 0, 0), 1) 

        #displays coordinates
        text = f"X: {self.x} Y: {self.y}"
        cv2.putText(frame, text, (20, 120), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.8, (255, 255, 255), 2)          
            

            

