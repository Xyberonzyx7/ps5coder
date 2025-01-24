import pygame
import pyautogui
import time
import math

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
BUTTON_LB = 9  # Left button (Control)
BUTTON_RB = 10  # Right button (Right key)
BUTTON_UP = 11  # Up key
BUTTON_DOWN = 12  # Down key
BUTTON_LEFT = 13  # Left key
BUTTON_RIGHT = 14  # Right key
BUTTON_TOUCHPAD = 15
BUTTON_MIC = 16

AXIS_LSH = 0  # Left joystick horizontal
AXIS_LSV = 1  # Left joystick vertical
AXIS_RSH = 2  # Right joystick horizontal
AXIS_RSV = 3  # Right joystick vertical
AXIS_LT = 4   # Left trigger (Shift)
AXIS_RT = 5   # Right trigger

# Mode definitions
MODE_MOUSE = 0
MODE_INSERT = 1
current_mode = MODE_MOUSE

# Sensitivity settings
MOUSE_SENSITIVITY = 90
SCROLL_SENSITIVITY = 400
JOYSTICK_DEADZONE = 0.2

# Define character sections
sections = {
    1: 'abcdefg',
    2: 'hijklmn',
    3: 'opqrstu',
    4: 'vwxyz01',
    5: '2345678',
    6: '9,./;\'[',
    7: ']\-=`  ',
}

# Shift mappings for QWERTY layout
shifted_sections = {
    1: 'ABCDEFG',
    2: 'HIJKLMN',
    3: 'OPQRSTU',
    4: 'VWXYZ)!',
    5: '@#$%^&*',
    6: '(<>?:"{',
    7: '}|_+~  ',
}

# Define the joystick angle ranges for each section (in radians)
section_angles = {
    1: (-math.pi, -5 * math.pi / 7),      
    2: (-5 * math.pi / 7, -3 * math.pi / 7),  
    3: (-3 * math.pi / 7, -math.pi / 7),  
    4: (-math.pi / 7, math.pi / 7),  
    5: (math.pi / 7, 3 * math.pi / 7),  
    6: (3 * math.pi / 7, 5 * math.pi / 7),  
    7: (5 * math.pi / 7, math.pi),
}

# Helper function to get the angle of the joystick
def get_joystick_angle(x, y):
    if abs(x) <= JOYSTICK_DEADZONE and abs(y) <= JOYSTICK_DEADZONE:
        return None
    angle = math.atan2(y, x)  # Compute the angle in radians
    return angle

# Helper function to map joystick input to a character section
def get_section(x, y):
    angle = get_joystick_angle(x, y)
    if angle is None:
        return None
    for section, (start, end) in section_angles.items():
        if start <= angle < end:
            return section
    return None

# Helper function to map joystick input to a character within the section
def get_character(lsection, rsection, shift_pressed):
    if not lsection or not rsection:
        return None
    characters = shifted_sections[lsection] if shift_pressed else sections[lsection]
    character = characters[rsection - 1]  # use 'index' to find a character in a collection
    if not character:
        return None
    return character

def handle_mouse_mode():
    """Handle mouse movement, clicking, and scrolling."""
    # Left joystick controls mouse movement
    x = joystick.get_axis(AXIS_LSH)
    y = joystick.get_axis(AXIS_LSV)
    control_pressed = joystick.get_button(BUTTON_LB)
    if abs(x) > JOYSTICK_DEADZONE or abs(y) > JOYSTICK_DEADZONE:
        pyautogui.moveRel(x * MOUSE_SENSITIVITY, y * MOUSE_SENSITIVITY)

    # Handle special buttons
    if joystick.get_button(BUTTON_UP):
        pyautogui.press('up')
    if joystick.get_button(BUTTON_DOWN):
        pyautogui.press('down')
    if joystick.get_button(BUTTON_LEFT):
        pyautogui.press('left')
    if joystick.get_button(BUTTON_RIGHT):
        pyautogui.press('right')
    if joystick.get_button(BUTTON_TRIANGLE):
        if control_pressed:
            pyautogui.hotkey('ctrl', 'backspace')  # Delete a word if control is pressed
        else:
            pyautogui.press('backspace')
    if joystick.get_button(BUTTON_CIRCLE):
        pyautogui.press('enter')
    if joystick.get_button(BUTTON_CROSS):
        pyautogui.click()
    if joystick.get_button(BUTTON_SQUARE):
        pyautogui.press('tab')

    # Right joystick controls scrolling
    scroll_y = joystick.get_axis(AXIS_RSV)
    if abs(scroll_y) > JOYSTICK_DEADZONE:
        pyautogui.scroll(int(-scroll_y * SCROLL_SENSITIVITY))

def handle_insert_mode():
    """Handle character insertion."""
    lx = joystick.get_axis(AXIS_LSH)  # Get the x-axis value
    ly = joystick.get_axis(AXIS_LSV)  # Get the y-axis value
    rx = joystick.get_axis(AXIS_RSH)  # Get the x-axis value
    ry = joystick.get_axis(AXIS_RSV)  # Get the y-axis value
    lx = round(lx, 1)
    ly = round(ly, 1)
    rx = round(rx, 1)
    ry = round(ry, 1)

    shift_pressed = joystick.get_axis(AXIS_LT) > 0.5
    control_pressed = joystick.get_button(BUTTON_LB)
    share_press = joystick.get_button(BUTTON_SHARE)  # Detect if Share button is pressed (Alt)
    esc_press = joystick.get_button(BUTTON_OPTIONS)
    lsection = get_section(lx, ly)
    rsection = get_section(rx, ry)
    character = get_character(lsection, rsection, shift_pressed)
    if character:
        pyautogui.write(character)
    
    # Handle special buttons
    if joystick.get_button(BUTTON_UP):
        pyautogui.press('up')
    if joystick.get_button(BUTTON_DOWN):
        pyautogui.press('down')
    if joystick.get_button(BUTTON_LEFT):
        pyautogui.press('left')
    if joystick.get_button(BUTTON_RIGHT):
        pyautogui.press('right')
    if joystick.get_button(BUTTON_TRIANGLE):
        if control_pressed:
            pyautogui.hotkey('ctrl', 'backspace')  # Delete a word if control is pressed
        else:
            pyautogui.press('backspace')
    if joystick.get_button(BUTTON_CIRCLE):
        pyautogui.press('enter')
    if joystick.get_button(BUTTON_CROSS):
        pyautogui.press('space')
    if joystick.get_button(BUTTON_SQUARE):
        pyautogui.press('tab')
    if share_press:
        pyautogui.hotkey('ctrl', 's')  # Save a file
    if esc_press:
        pyautogui.press('esc')
    time.sleep(0.1)  # Debounce delay

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
