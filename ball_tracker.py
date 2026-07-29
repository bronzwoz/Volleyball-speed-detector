import cv2

class BallTracker:

    def __init__(self):

        #current selected ball position
        self.ball_x = None
        self.ball_y = None

        #Stores ball position for each frame
        self.positions = []

    def detect_ball(self, frame):

        region = self.get_region(frame)
        if region is None:
            return None
        
        #convert to gray scale
        gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)

        #Blur for less noise
        gray = cv2.GaussianBlur(gray, (5, 5), 0)

        #find bright object
        _, threshold = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

        contours,_ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) == 0:
            return None
        
        #find largest bright object
        largest = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest)
        if area < 5:
            return None

        #get center of object
        M = cv2.moments(largest)

        if M["m00"] == 0:
            return None
        
        x = int(M["m10"] / M["m00"])
        y = int(M["m01"] / M["m00"])

        #convert region coordinates back into frame coordinates
        x += self.ball_x - 50
        y += self.ball_y - 50

        return (x,y)

    def handled_mouse(self, event, x, y, flags, param):

        #Left mouse button selects ball positon
        if event == cv2.EVENT_LBUTTONDOWN:

            self.ball_x = x
            self.ball_y = y

            self.positions.append((x, y))

            print(f"Ball positions recorded at: {x}, {y}")

    def record_positon(self):
        if self.ball_x is not None and self.ball_y is not None:

            self.positions.append((self.ball_x, self.ball_y))

    #creates a 100x100 box around the last position of the ball
    def get_region(self, frame):

        if self.ball_x is None:
            return None
        
        size = 50

        x1 = max(0, self.ball_x - size)
        y1 = max(0, self.ball_y - size)

        x2 = min(frame.shape[1], self.ball_x + size)
        y2 = min(frame.shape[0], self.ball_y + size)

        return frame[y1:y2, x1:x2]

    def draw(self, frame):
        region = self.get_region(frame)
        if region is not None:
            cv2.imshow("search Area", region)

        detected = self.detect_ball(frame)
        
        if detected:
            cv2.circle(frame, detected, 8, (255, 0, 255), 2)

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