import pygame

pygame.init()

# Create a window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Button Test")
clock = pygame.time.Clock()

# Define a simple button as a rect
button_rect = pygame.Rect(300, 250, 200, 100)

running = True
while running:
    # Get all events
    events = pygame.event.get()
    
    for event in events:
        # Handle quitting
        if event.type == pygame.QUIT:
            running = False
        
        # Handle button press detection
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(pygame.mouse.get_pos()):
                print("Button clicked!")

    # Draw button (red color)
    screen.fill((255, 255, 255))  # Clear screen
    pygame.draw.rect(screen, (255, 0, 0), button_rect)  # Draw the button
    
    pygame.display.flip()
    clock.tick(60)  # Limit to 60 FPS

pygame.quit()
