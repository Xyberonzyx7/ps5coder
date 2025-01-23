import pygame
import pyautogui
import time

# Initialize Pygame
pygame.init()
pygame.joystick.init()

# Check for joystick connection
if pygame.joystick.get_count() == 0:
    print("No joystick connected. Please connect a controller and restart.")
    exit()
else:
    # Initialize the first joystick
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Connected to joystick: {joystick.get_name()}")

# Button and axis mappings
BUTTON_CROSS = 0
BUTTON_CIRCLE = 1
BUTTON_SQUARE = 2
BUTTON_TRIANGLE = 3
BUTTON_SHARE = 4
BUTTON_PS = 5
BUTTON_OPTIONS = 6
BUTTON_LS = 7  # Left joystick click
BUTTON_RS = 8  # Right joystick click
BUTTON_LB = 9  # Left button
BUTTON_RB = 10  # Right button
BUTTON_UP = 11
BUTTON_DOWN = 12
BUTTON_LEFT = 13
BUTTON_RIGHT = 14
BUTTON_TOUCHPAD = 15
BUTTON_MIC = 16

AXIS_LSH = 0  # Left joystick horizontal
AXIS_LSV = 1  # Left joystick vertical
AXIS_RSH = 2  # Right joystick horizontal
AXIS_RSV = 3  # Right joystick vertical
AXIS_LT = 4   # Left trigger
AXIS_RT = 5   # Right trigger

# Mode definitions
MODE_MOUSE = 0
MODE_INSERT = 1
current_mode = MODE_MOUSE

# Sensitivity settings
MOUSE_SENSITIVITY = 10
SCROLL_SENSITIVITY = 500
JOYSTICK_DEADZONE = 0.2

# Character mappings for Insert Mode
# Define mappings for joystick directions and button combinations
char_map = {
    (0, -1): 'w',  # Up
    (0, 1): 's',   # Down
    (-1, 0): 'a',  # Left
    (1, 0): 'd',   # Right
    (0, -1, BUTTON_LB): 'W',  # Shift + Up
    (0, 1, BUTTON_LB): 'S',   # Shift + Down
    (-1, 0, BUTTON_LB): 'A',  # Shift + Left
    (1, 0, BUTTON_LB): 'D',   # Shift + Right
    (0, -1, BUTTON_RB): '1',  # RB + Up
    (0, 1, BUTTON_RB): '2',   # RB + Down
    (-1, 0, BUTTON_RB): '3',  # RB + Left
    (1, 0, BUTTON_RB): '4',   # RB + Right
    # Add more mappings as needed
}

def get_joystick_direction():
    """Get the direction of the left joystick."""
    x = joystick.get_axis(AXIS_LSH)
    y = joystick.get_axis(AXIS_LSV)
    direction = (0, 0)
    if abs(x) > JOYSTICK_DEADZONE:
        direction = (1 if x > 0 else -1, direction[1])
    if abs(y) > JOYSTICK_DEADZONE:
        direction = (direction[0], 1 if y > 0 else -1)
    return direction

def handle_mouse_mode():
    """Handle mouse movement, clicking, and scrolling."""
    # Left joystick controls mouse movement
    x = joystick.get_axis(AXIS_LSH)
    y = joystick.get_axis(AXIS_LSV)
    if abs(x) > JOYSTICK_DEADZONE or abs(y) > JOYSTICK_DEADZONE:
        pyautogui.moveRel(x * MOUSE_SENSITIVITY, y * MOUSE_SENSITIVITY)

    # Cross button simulates mouse click
    if joystick.get_button(BUTTON_CROSS):
        pyautogui.click()
        # time.sleep(0.2)  # Debounce delay

    # Right joystick controls scrolling
    scroll_y = joystick.get_axis(AXIS_RSV)
    if abs(scroll_y) > JOYSTICK_DEADZONE:
        pyautogui.scroll(int(-scroll_y * SCROLL_SENSITIVITY))

    time.sleep(0.01)  # Debounce delay

def handle_insert_mode():
    """Handle character insertion."""
    direction = get_joystick_direction()
    if direction != (0, 0):
        for modifier, button in [('shift', BUTTON_LB), ('ctrl', BUTTON_RB)]:
            if joystick.get_button(button):
                key = char_map.get((*direction, button))
                if key:
                    pyautogui.write(key)
                    time.sleep(0.2)  # Debounce delay
                    return
        key = char_map.get(direction)
        if key:
            pyautogui.write(key)
            time.sleep(0.2)  # Debounce delay

def main():
    global current_mode
    print("Press the PS button to switch modes. Press Ctrl+C to quit.")
    try:
        while True:
            pygame.event.pump()
            if joystick.get_button(BUTTON_PS):
                current_mode = MODE_INSERT if current_mode == MODE_MOUSE else MODE_MOUSE
                mode_name = "Insert Mode" if current_mode == MODE_INSERT else "Mouse Mode"
                print(f"Switched to {mode_name}")
                time.sleep(0.5)  # Debounce delay
            if current_mode == MODE_MOUSE:
                handle_mouse_mode()
            elif current_mode == MODE_INSERT:
                handle_insert_mode()
            time.sleep(0.01)  # Polling delay
    except KeyboardInterrupt:
        print("\nExiting program...")
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
