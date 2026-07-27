import cv2

class BallTracker:

    def __init__(self):

        #current selected ball position
        self.ball_x = None
        self.ball_y = None

        #Stores ball position for each frame
        self.positions = []

    def handled_mouse(self, event, x, y, flags, param):

        #Left mouse button selects ball positon
        if event == cv2.EVENT_LBUTTONDOWN:

            self.ball_x = x
            self.ball_y = y

            self.positions.append((x, y))

            print(f"Ball positions recorded at: {x}, {y}")

    def draw(self, frame):
        
        #Draw previous ball positions
        for position in self.positions:
            cv2.circle(frame, position, 4, (0, 255, 255), -1)

        #Nothing is drawn until ball is selected
        if self.ball_x is None:
            return
        
        #Draw current ball marker
        cv2.circle(frame, (self.ball_x, self.ball_y), 10, (0, 0, 255), 2)

        #Draw center point
        cv2.circle(frame, (self.ball_x, self.ball_y), 3, (0, 0, 255), -1)

        #Display coordinates
        text = f"Ball: ({self.ball_x}, {self.ball_y})"
        cv2.putText(frame, text, (20, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)