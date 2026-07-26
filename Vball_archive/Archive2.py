#imports OpenCV
import cv2

#imports class
from video_player import VideoPlayer

player = VideoPlayer("videos/test.mp4")

playing = False

while True:
    
    #Creates a temp copy of the frame for display
    frame = player.get_frame().copy()

    #Displays current frame being displayed
    cv2.putText(frame, f"Frame: {player.current_frame + 1}/{player.total_frames}", (20, 40), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (0, 255, 0), 2)

    status = "playing" if playing else "paused"

    #Displays 
    cv2.putText(frame, status, (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    #Title on the window
    cv2.imshow("Volleyball Speed Detector", frame)

    #Wait up to 30ms for a keypress (uses 'Ex' to read extended key strokes like arrow keys)
    key = cv2.waitKeyEx(30)

    if key != -1:
        print(key)

    # q = Quit
    if key == ord("q"):
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