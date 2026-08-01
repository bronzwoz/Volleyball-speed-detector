import cv2

class MouseTracker:

    def __init__(self):

        #current mouse position
        self.x = 0
        self.y = 0

        #Is the mouse in the window
        self.active = False
        self.points = []

    def handle_mouse(self, event, x, y, flags, param):

        if event == cv2.EVENT_MOUSEMOVE:

            self.x = x
            self.y = y
            self.active = True

        if event == cv2.EVENT_LBUTTONDOWN:
            self.points.append((x, y))
            print(self.points)

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

        for point in self.points:
            cv2.circle(frame, point, 5, (0, 255, 255), -1)

        if len(self.points) == 2:
            cv2.line(frame, self.points[0], self.points[1], (0, 255, 255), 2)
            

            

