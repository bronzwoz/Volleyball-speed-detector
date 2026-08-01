from turtle import speed

import cv2

class BallTracker:

    def __init__(self, player):

        self.player = player

        #current selected ball position
        self.ball_x = None
        self.ball_y = None

        #Stores ball position for each frame
        self.positions = []
        #Initial speed
        self.speed_kph = 0.0
        #Calibration estimate of how many pixels correspond to one meter in the video
        self.pixels_per_meter = 105.0

    def calculate_speed(self, fps):
        #Calculates the speed of the ball based on the recorded positions and fps
        if len(self.positions) < 2:
            return 
        
        (x1, y1) = self.positions[-2]
        (x2, y2) = self.positions[-1]

        dx = x2 - x1
        dy = y2 - y1

        pixel_distance = (dx ** 2 + dy ** 2) ** 0.5
    
        #Speed in pixels per second
        meters = pixel_distance / self.pixels_per_meter

        dt = 1.0 / self.player.fps

        speed_mps = meters / dt

        self.speed_kph = speed_mps * 3.6

    def detect_ball(self, frame):
        
        #Detect ball in current frame based on last known position
        region = self.get_region(frame)
        if region is None or region.size == 0:
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
        
        best_direction = None
        best_area = 0

        #Check all contours to find the largest bright object within the specified aspect ratio
        for contour in contours:
            
            area = cv2.contourArea(contour)
            
            if area < 40:
                continue

            x, y, w, h = cv2.boundingRect(contour)

            aspect_ratio = w / float(h)

            if aspect_ratio < 0.6 or aspect_ratio > 1.4:
                continue

            if area > best_area:
                best_area = area
                best_direction = contour

        if best_direction is None:
            return None
        
        #find the center of the largest bright object
        M = cv2.moments(best_direction)

        #If the area is zero, return None to avoid division by zero
        if M["m00"] == 0:
            return None
        
        #convert region coordinates to frame coordinates
        x = int(M["m10"] / M["m00"])
        y = int(M["m01"] / M["m00"])

        #convert region coordinates back into frame coordinates
        x += self.ball_x - 50
        y += self.ball_y - 50

        if self.ball_x is not None and self.ball_y is not None:

            dx = x - self.ball_x
            dy = y - self.ball_y

            distance = (dx ** 2 + dy ** 2) ** 0.5

            if distance > 40:
                return None
            
        return (x,y)

    def update_tracking(self, frame):
        #Detect the ball in the current frame and update its position
        detected = self.detect_ball(frame)
        if detected is not None:
            self.ball_x, self.ball_y = detected
            #Save the detected position to the list of positions
            if len(self.positions) == 0 or self.positions[-1] != detected: self.positions.append(detected)
            self.calculate_speed(fps=self.player.fps)

    def handle_mouse(self, event, x, y, flags, param):

        #Left mouse button selects ball positon
        if event == cv2.EVENT_LBUTTONDOWN:

            self.ball_x = x
            self.ball_y = y

            self.positions.append((x, y))

            #print(f"Ball positions recorded at: {x}, {y}")

    def record_position(self):
        if self.ball_x is not None and self.ball_y is not None:

            self.positions.append((self.ball_x, self.ball_y))

    #creates a 100x100 box around the last position of the ball
    def get_region(self, frame):

        if self.ball_x is None or self.ball_y is None:
            return None
        
        size = 50

        x1 = max(0, self.ball_x - size)
        y1 = max(0, self.ball_y - size)

        x2 = min(frame.shape[1], self.ball_x + size)
        y2 = min(frame.shape[0], self.ball_y + size)

        if x2 <= x1 or y2 <= y1:
            return None

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

        #Display speed in km/h
        speed_text = f"Speed: {self.speed_kph:.1f} km/h"
        cv2.putText(frame, speed_text, (20, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)