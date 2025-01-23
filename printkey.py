import pygame

# Initialize Pygame
pygame.init()
pygame.joystick.init()

# Check for joystick connection
if pygame.joystick.get_count() == 0:
    print("No joystick connected. Please connect a controller and restart.")
else:
    # Initialize the first joystick
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Connected to joystick: {joystick.get_name()}")

    try:
        print("Press any button on the controller. Press Ctrl+C to quit.")
        while True:
            # Process Pygame events
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:
                    print(f"Button {event.button} pressed.")
                elif event.type == pygame.JOYBUTTONUP:
                    print(f"Button {event.button} released.")
                elif event.type == pygame.JOYAXISMOTION:
                    print(f"Axis {event.axis} moved to {event.value:.2f}")
                elif event.type == pygame.JOYHATMOTION:
                    print(f"Hat {event.hat} moved to {event.value}")
    except KeyboardInterrupt:
        print("\nExiting program...")
    finally:
        pygame.quit()
