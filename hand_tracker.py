import cv2
import mediapipe as mp
import pyautogui
import math
import time
import spark_state


# ============================================================
# SPARK ADVANCED HAND CONTROLLER
# ============================================================

CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720

# Cursor speed
SENSITIVITY = 2.2

# Cursor smoothing
SMOOTHING = 0.28

# Ignore extremely tiny movements
DEADZONE = 0.35

# Maximum movement allowed per frame
# Prevents tracking glitches from throwing the cursor
# into a screen corner.
MAX_MOVE = 35

# Pinch detection
PINCH_START = 0.42
PINCH_RELEASE = 0.58

# Click cooldown
CLICK_COOLDOWN = 0.6


# ============================================================
# SCREEN
# ============================================================

screen_width, screen_height = pyautogui.size()

pyautogui.PAUSE = 0

# Keep PyAutoGUI's emergency safety feature enabled.
pyautogui.FAILSAFE = True


# ============================================================
# STATE
# ============================================================

running = True

prev_x = None
prev_y = None

smooth_x = 0.0
smooth_y = 0.0

last_click_time = 0

pinching = False

gesture_lock = None
gesture_time = 0


# ============================================================
# DISTANCE
# ============================================================

def distance(a, b):

    return math.sqrt(
        (a.x - b.x) ** 2 +
        (a.y - b.y) ** 2 +
        (a.z - b.z) ** 2
    )


def palm_size(hand):

    size = distance(
        hand[0],
        hand[9]
    )

    return max(size, 0.001)


def pinch_ratio(hand):

    return (
        distance(
            hand[4],
            hand[8]
        )
        /
        palm_size(hand)
    )


# ============================================================
# FINGER DETECTION
# ============================================================

def finger_up(hand, tip, pip):

    return (
        hand[tip].y <
        hand[pip].y
    )


def finger_states(hand):

    return (
        finger_up(hand, 8, 6),
        finger_up(hand, 12, 10),
        finger_up(hand, 16, 14),
        finger_up(hand, 20, 18)
    )


def is_open_palm(hand):

    index, middle, ring, pinky = (
        finger_states(hand)
    )

    return (
        index and
        middle and
        ring and
        pinky
    )


def is_fist(hand):

    index, middle, ring, pinky = (
        finger_states(hand)
    )

    return not (
        index or
        middle or
        ring or
        pinky
    )


def is_peace(hand):

    index, middle, ring, pinky = (
        finger_states(hand)
    )

    return (
        index and
        middle and
        not ring and
        not pinky
    )


def is_thumb_up(hand):

    index, middle, ring, pinky = (
        finger_states(hand)
    )

    thumb_up = (
        hand[4].y <
        hand[3].y
    )

    return (
        thumb_up and
        not index and
        not middle and
        not ring and
        not pinky
    )


# ============================================================
# STABLE GESTURE
# ============================================================

def stable_gesture(name, delay=0.10):

    global gesture_lock
    global gesture_time

    now = time.time()

    if gesture_lock != name:

        gesture_lock = name
        gesture_time = now

        return False

    return (
        now - gesture_time
        >= delay
    )


# ============================================================
# RESET MOVEMENT
# ============================================================

def reset_movement():

    global prev_x
    global prev_y

    global smooth_x
    global smooth_y

    prev_x = None
    prev_y = None

    smooth_x = 0.0
    smooth_y = 0.0


# ============================================================
# SAFE GRAB RELEASE
# ============================================================

def release_grab():

    global pinching

    if pinching:

        try:

            pyautogui.mouseUp()

        except pyautogui.FailSafeException:

            pass

        pinching = False

    reset_movement()


# ============================================================
# SAFE CURSOR MOVEMENT
# ============================================================

def safe_move(dx, dy):

    global smooth_x
    global smooth_y

    # Limit movement per frame.
    dx = max(
        -MAX_MOVE,
        min(MAX_MOVE, int(dx))
    )

    dy = max(
        -MAX_MOVE,
        min(MAX_MOVE, int(dy))
    )

    if dx == 0 and dy == 0:
        return

    try:

        pyautogui.moveRel(
            dx,
            dy
        )

    except pyautogui.FailSafeException:

        # The cursor reached a safety corner.
        # Stop movement for this frame.
        reset_movement()


# ============================================================
# CAMERA
# ============================================================

cap = cv2.VideoCapture(
    0,
    cv2.CAP_DSHOW
)

cap.set(
    cv2.CAP_PROP_FRAME_WIDTH,
    CAMERA_WIDTH
)

cap.set(
    cv2.CAP_PROP_FRAME_HEIGHT,
    CAMERA_HEIGHT
)

# Keep only the newest camera frame.
cap.set(
    cv2.CAP_PROP_BUFFERSIZE,
    1
)


if not cap.isOpened():

    print()
    print("ERROR: Webcam unavailable.")
    print()

    spark_state.hand_status = "ERROR"

    raise SystemExit


# ============================================================
# MEDIAPIPE MODERN API
# ============================================================

BaseOptions = mp.tasks.BaseOptions

HandLandmarker = (
    mp.tasks.vision.HandLandmarker
)

HandLandmarkerOptions = (
    mp.tasks.vision.HandLandmarkerOptions
)

RunningMode = (
    mp.tasks.vision.RunningMode
)


options = HandLandmarkerOptions(

    base_options=BaseOptions(

        model_asset_path="hand_landmarker.task"

    ),

    running_mode=RunningMode.VIDEO,

    num_hands=1,

    min_hand_detection_confidence=0.65,

    min_hand_presence_confidence=0.65,

    min_tracking_confidence=0.70

)


# ============================================================
# START
# ============================================================

print()
print("==============================================")
print("      SPARK OPTIMIZED HAND CONTROLLER")
print("==============================================")
print()
print("INDEX       = MOVE")
print("PINCH       = GRAB + DRAG")
print("PEACE       = LEFT CLICK")
print("THUMB UP    = DOUBLE CLICK")
print("OPEN PALM   = PAUSE")
print("FIST        = PAUSE")
print()
print("PINCH -> HOLD -> MOVE -> RELEASE")
print()
print("Press Q to stop.")
print()
print("==============================================")


# ============================================================
# MAIN LOOP
# ============================================================

with HandLandmarker.create_from_options(
    options
) as landmarker:

    timestamp = 0

    while running:

        # ====================================================
        # CAMERA
        # ====================================================

        success, frame = cap.read()

        if not success:
            continue


        # Mirror camera
        frame = cv2.flip(
            frame,
            1
        )


        height, width, _ = (
            frame.shape
        )


        # ====================================================
        # RGB
        # ====================================================

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )


        image = mp.Image(

            image_format=(
                mp.ImageFormat.SRGB
            ),

            data=rgb

        )


        # ====================================================
        # DETECT HAND
        # ====================================================

        result = (
            landmarker.detect_for_video(
                image,
                timestamp
            )
        )

        timestamp += 33


        # ====================================================
        # NO HAND
        # ====================================================

        if not result.hand_landmarks:

            # Never leave the mouse button held
            # if the camera temporarily loses the hand.
            release_grab()

            spark_state.hand_status = "READY"

            cv2.putText(
                frame,
                "NO HAND",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 0),
                2
            )

            cv2.imshow(
                "Spark - Hand Controller",
                frame
            )

            if (
                cv2.waitKey(1)
                & 0xFF
                == ord("q")
            ):

                running = False
                break

            continue


        # ====================================================
        # GET HAND
        # ====================================================

        hand = result.hand_landmarks[0]


        # ====================================================
        # GESTURES
        # ====================================================

        palm = is_open_palm(hand)

        fist = is_fist(hand)

        peace = is_peace(hand)

        thumb = is_thumb_up(hand)

        pinch_value = pinch_ratio(hand)

        pinch = (
            pinch_value
            < PINCH_START
        )


        # ====================================================
        # RELEASE PINCH
        # ====================================================

        if pinching:

            if (
                pinch_value
                > PINCH_RELEASE
            ):

                try:

                    pyautogui.mouseUp()

                except pyautogui.FailSafeException:

                    pass

                pinching = False

                reset_movement()


        # ====================================================
        # OPEN PALM / FIST
        # ====================================================

        if palm or fist:

            release_grab()

            spark_state.hand_status = "PAUSED"


            if palm:

                status = (
                    "OPEN PALM // PAUSED"
                )

            else:

                status = (
                    "FIST // PAUSED"
                )


        # ====================================================
        # PINCH = GRAB + DRAG
        # ====================================================

        elif pinch:

            spark_state.hand_status = (
                "GRABBING"
            )


            # ------------------------------------------------
            # START GRAB
            # ------------------------------------------------

            if not pinching:

                try:

                    pyautogui.mouseDown()

                    pinching = True

                    reset_movement()

                except pyautogui.FailSafeException:

                    pinching = False

                status = "GRAB START"


            else:

                status = "GRABBING"


            # ------------------------------------------------
            # PALM CENTER
            # ------------------------------------------------

            current_x = hand[9].x
            current_y = hand[9].y


            if prev_x is None:

                prev_x = current_x
                prev_y = current_y

            else:

                dx = (
                    current_x
                    - prev_x
                )

                dy = (
                    current_y
                    - prev_y
                )


                # Ignore tiny camera noise.
                if abs(dx) < 0.0015:
                    dx = 0

                if abs(dy) < 0.0015:
                    dy = 0


                # ------------------------------------------------
                # SCREEN MOVEMENT
                #
                # Camera is mirrored, so:
                #
                # HAND RIGHT -> CURSOR RIGHT
                # HAND LEFT  -> CURSOR LEFT
                # ------------------------------------------------

                target_x = (
                    dx
                    * screen_width
                    * SENSITIVITY
                )

                target_y = (
                    dy
                    * screen_height
                    * SENSITIVITY
                )


                # ------------------------------------------------
                # SMOOTH
                # ------------------------------------------------

                smooth_x = (
                    smooth_x
                    +
                    (
                        target_x
                        - smooth_x
                    )
                    * SMOOTHING
                )

                smooth_y = (
                    smooth_y
                    +
                    (
                        target_y
                        - smooth_y
                    )
                    * SMOOTHING
                )


                # ------------------------------------------------
                # MOVE
                # ------------------------------------------------

                if (
                    abs(smooth_x)
                    >= DEADZONE
                    or
                    abs(smooth_y)
                    >= DEADZONE
                ):

                    safe_move(
                        smooth_x,
                        smooth_y
                    )


                prev_x = current_x
                prev_y = current_y


        # ====================================================
        # PEACE = LEFT CLICK
        # ====================================================

        elif peace:

            release_grab()

            spark_state.hand_status = "ACTIVE"


            if stable_gesture("PEACE"):

                now = time.time()


                if (
                    now
                    - last_click_time
                    >
                    CLICK_COOLDOWN
                ):

                    try:

                        pyautogui.click()

                    except pyautogui.FailSafeException:

                        pass

                    last_click_time = now


            status = (
                "PEACE // LEFT CLICK"
            )


        # ====================================================
        # THUMB UP = DOUBLE CLICK
        # ====================================================

        elif thumb:

            release_grab()

            spark_state.hand_status = "ACTIVE"


            if stable_gesture("THUMB"):

                now = time.time()


                if (
                    now
                    - last_click_time
                    >
                    CLICK_COOLDOWN
                ):

                    try:

                        pyautogui.doubleClick()

                    except pyautogui.FailSafeException:

                        pass

                    last_click_time = now


            status = (
                "THUMB // DOUBLE CLICK"
            )


        # ====================================================
        # NORMAL INDEX MOVEMENT
        # ====================================================

        else:

            if pinching:

                try:

                    pyautogui.mouseUp()

                except pyautogui.FailSafeException:

                    pass

                pinching = False


            spark_state.hand_status = "ACTIVE"


            index = hand[8]


            current_x = index.x
            current_y = index.y


            if prev_x is None:

                prev_x = current_x
                prev_y = current_y

            else:

                dx = (
                    current_x
                    - prev_x
                )

                dy = (
                    current_y
                    - prev_y
                )


                # Deadzone
                if abs(dx) < 0.0015:
                    dx = 0

                if abs(dy) < 0.0015:
                    dy = 0


                target_x = (
                    dx
                    * screen_width
                    * SENSITIVITY
                )

                target_y = (
                    dy
                    * screen_height
                    * SENSITIVITY
                )


                # Smooth movement
                smooth_x = (
                    smooth_x
                    +
                    (
                        target_x
                        - smooth_x
                    )
                    * SMOOTHING
                )

                smooth_y = (
                    smooth_y
                    +
                    (
                        target_y
                        - smooth_y
                    )
                    * SMOOTHING
                )


                if (
                    abs(smooth_x)
                    >= DEADZONE
                    or
                    abs(smooth_y)
                    >= DEADZONE
                ):

                    safe_move(
                        smooth_x,
                        smooth_y
                    )


                prev_x = current_x
                prev_y = current_y


            status = (
                "INDEX // MOUSE ACTIVE"
            )


        # ====================================================
        # DRAW HAND LANDMARKS
        # ====================================================

        for point in hand:

            px = int(
                point.x
                * width
            )

            py = int(
                point.y
                * height
            )


            cv2.circle(
                frame,
                (px, py),
                3,
                (0, 255, 0),
                -1
            )


        # ====================================================
        # DRAW PINCH
        # ====================================================

        thumb_x = int(
            hand[4].x
            * width
        )

        thumb_y = int(
            hand[4].y
            * height
        )

        index_x = int(
            hand[8].x
            * width
        )

        index_y = int(
            hand[8].y
            * height
        )


        if pinch:

            cv2.line(
                frame,
                (thumb_x, thumb_y),
                (index_x, index_y),
                (0, 255, 255),
                3
            )


            cv2.putText(
                frame,
                "GRAB",
                (
                    index_x + 15,
                    index_y
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (0, 255, 255),
                2
            )


        # ====================================================
        # STATUS
        # ====================================================

        cv2.putText(
            frame,
            status,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.72,
            (0, 255, 0),
            2
        )


        # ====================================================
        # PINCH VALUE
        # ====================================================

        cv2.putText(
            frame,
            f"Pinch: {pinch_value:.2f}",
            (20, 72),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.52,
            (255, 255, 255),
            1
        )


        # ====================================================
        # DISPLAY
        # ====================================================

        cv2.imshow(
            "Spark - Hand Controller",
            frame
        )


        # ====================================================
        # EXIT
        # ====================================================

        if (
            cv2.waitKey(1)
            & 0xFF
            == ord("q")
        ):

            running = False
            break


# ============================================================
# CLEANUP
# ============================================================

release_grab()

spark_state.hand_status = "OFFLINE"

cap.release()

cv2.destroyAllWindows()


print()
print("Spark optimized hand controller stopped.")