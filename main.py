#imports OpenCV
import cv2

#imports class
from video_player import VideoPlayer
from timeline import Timeline


player = VideoPlayer("videos/test.mp4")

timeline = Timeline(player)

playing = False

#passes the event position of the mouse back to the timeline
#OpenCV calls back with five arguments
def mouse_callback(event, x, y, flags, param):

    timeline.handle_mouse(event, x, y)

#Avoids repeatoing the window name and ensures callback is attached to correct window
window_name = "volleyball Speed Detector"
cv2.namedWindow(window_name)
cv2.setMouseCallback(window_name, mouse_callback)

# --====================--
#           Main
# --====================--

while True:
    
    #Creates a temp copy of the frame for display
    frame = player.get_frame().copy()

    #Draw the timeline
    timeline.draw(frame)

    #Displays current frame being displayed
    cv2.putText(frame, f"Frame: {player.current_frame + 1}/{player.total_frames}", (20, 40), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (0, 255, 0), 2)

    status = "playing" if playing else "paused"

    #Displays 
    cv2.putText(frame, status, (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    #Title on the window
    cv2.imshow(window_name, frame)

    #Wait up to 30ms for a keypress (uses 'Ex' to read extended key strokes like arrow keys)
    key = cv2.waitKeyEx(30)

    # ESC = Quit
    if key == 27:
        break

    # SPACE = Play / Pause
    elif key == ord(" "):
        playing = not playing

    # Right Arrow = Next frame
    elif key == 63235:
        player.next_frame()

    # Left Arrow = Back one frame
    elif key == 63234:
        player.previous_frame()

    # Up Arrow = forwards ten frame
    elif key == 63232:
        player.jump_forward(10)

    # Down Arrow = backwards ten frame
    elif key == 63233:
        player.jump_backward(10)

    # r = Restart video
    elif key == ord("r"):
        player.restart()

    #Continues playing the video
    elif playing:
        player.next_frame()

cv2.destroyAllWindows()