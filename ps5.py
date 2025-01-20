import pygame
import pyautogui

# Initialize pygame
pygame.init()
pygame.joystick.init()

# Map joystick directions to letters
joystick_to_letter = {
    "LEFT": "a",
    "RIGHT": "d",
    "UP": "w",
    "DOWN": "s"
}

def get_joystick_direction(joystick):
    """
    Determine the direction of the joystick based on its axis values.
    Returns 'LEFT', 'RIGHT', 'UP', 'DOWN', or None.
    """
    x_axis = joystick.get_axis(0)  # Left joystick horizontal movement
    y_axis = joystick.get_axis(1)  # Left joystick vertical movement
    
    if x_axis < -0.5:
        return "LEFT"
    elif x_axis > 0.5:
        return "RIGHT"
    elif y_axis < -0.5:
        return "UP"
    elif y_axis > 0.5:
        return "DOWN"
    return None

# Check if a joystick is connected
if pygame.joystick.get_count() == 0:
    print("No joystick connected. Please connect a controller and restart.")
else:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Connected to joystick: {joystick.get_name()}")

    try:
        print("Move the joystick to type letters. Press Ctrl+C to quit.")
        while True:
            pygame.event.pump()
            direction = get_joystick_direction(joystick)
            
            if direction:
                # Simulate typing the corresponding letter
                letter = joystick_to_letter.get(direction)
                if letter:
                    print(f"Typed: {letter}")
                    pyautogui.write(letter)
    except KeyboardInterrupt:
        print("\nExiting program...")
    finally:
        pygame.quit()

