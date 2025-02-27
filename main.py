import pygame  
import time    
import random  
import os  

# Initialize Pygame (including the mixer for sound effects and music)
pygame.font.init()
pygame.mixer.pre_init(44100, -16, 2, 512)  # Pre-initialize mixer for better performance
pygame.mixer.init()  # Initialize the mixer

# Set game window dimensions
WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  
pygame.display.set_caption("Pokeball Dodge")  # Set game title

# Load background image and scale it to fit the screen
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "bg.jpeg")), (WIDTH, HEIGHT))

# Load and play background music (loop indefinitely)
pygame.mixer.music.load(os.path.join("assets", "Pokemon FireRedLeafGreen- Pallet Town.mp3"))
pygame.mixer.music.set_volume(0.5)  # Set music volume to 50%
pygame.mixer.music.play(-1)  # Play music infinitely

# Load player (Pikachu) image, resize it, and optimize for performance
pikachu_img = pygame.image.load(os.path.join("assets", "pikachu.png")).convert_alpha()
PLAYER_WIDTH, PLAYER_HEIGHT = 75, 75  # Set player size
pikachu_img = pygame.transform.scale(pikachu_img, (PLAYER_WIDTH, PLAYER_HEIGHT))

# Load obstacle (Pokeball) image, resize it, and optimize for performance
pokeball_img = pygame.image.load(os.path.join("assets", "pokeball.png")).convert_alpha()
STAR_WIDTH, STAR_HEIGHT = 35, 30  # Set obstacle size
pokeball_img = pygame.transform.scale(pokeball_img, (STAR_WIDTH, STAR_HEIGHT))

# Define player and obstacle movement speeds
PLAYER_VEL = 6  # Player movement speed
STAR_VEL = 3  # Falling speed of Pokeballs

# Define fonts for text rendering
FONT = pygame.font.SysFont("Pokemon Solid Normal", 50)  # Large font for main text
BUTTON_FONT = pygame.font.SysFont("Pokemon Solid Normal", 40)  # Slightly smaller font for buttons

def draw(player, elapsed_time, stars):
    
#    Draws all game elements on the screen.
    
    WIN.blit(BG, (0, 0))  # Draw the background image

    # Render and display elapsed time
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "yellow")
    WIN.blit(time_text, (10, 10))

    # Draw the player (Pikachu)
    WIN.blit(pikachu_img, (player.x, player.y))

    # Draw falling obstacles (Pokeballs)
    for star in stars:
        WIN.blit(pokeball_img, (star.x, star.y))
    
    pygame.display.update()  # Refresh the screen

def draw_game_over():
    
   # Displays the 'You Lost!' screen, stops the music, and draws a restart button.
    
    pygame.mixer.music.stop()  # Stop music when the game ends

    WIN.fill((0, 0, 0))  # Fill the screen with black

    # Display "YOU LOST!" message
    lost_text = FONT.render("YOU GOT CAUGHT!", True, (255, 0, 0))
    WIN.blit(lost_text, (WIDTH//2 - lost_text.get_width()//2, HEIGHT//2 - 100))

    # Create "Play Again" button
    button_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2, 200, 60)
    pygame.draw.rect(WIN, (255, 0, 0), button_rect, border_radius=10)  # Red button with rounded corners

    # Display button text
    button_text = BUTTON_FONT.render("Play Again", True, (255, 255, 255))
    WIN.blit(button_text, (WIDTH//2 - button_text.get_width()//2, HEIGHT//2 + 10))

    # Display restart instruction
    restart_text = FONT.render("Press ENTER to Restart", True, (200, 200, 200))
    WIN.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 80))

    pygame.display.update()  # Refresh the screen

    return button_rect  # Return button rectangle for click detection

def main():

#   Main game loop that resets when 'Play Again' is clicked.
    
    while True:  # Restartable game loop
        pygame.mixer.music.play(-1)  # Restart background music when game restarts

        run = True  # Control variable for the game loop
        player = pygame.Rect(180, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)  # Create player rectangle
        clock = pygame.time.Clock()  # Clock for managing frame rate
        start_time = time.time()  # Record game start time
        elapsed_time = 0  # Reset elapsed time

        # Star (Pokeball) spawning properties
        star_add_increment = 3000  # Interval to add new stars (milliseconds)
        star_count = 0  # Counter for tracking star addition
        stars = []  # List to store Pokeball objects
        hit = False  # Track if player has been hit

        while run:
            star_count += clock.tick(70)  # Limit game to 60 FPS and update star counter
            elapsed_time = time.time() - start_time  # Calculate elapsed time

            # Add new stars at intervals
            if star_count > star_add_increment:
                for _ in range(4):  # Add 3 stars at a time
                    star_x = random.randint(0, WIDTH - STAR_WIDTH)  # Random x position
                    star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                    stars.append(star)
                
                # Decrease interval for spawning new stars, making the game harder
                star_add_increment = max(200, star_add_increment - 50)
                star_count = 0
            
            # Event handling (check for quitting the game)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            
          # Handle player movement (Arrow keys & A/D/W/S keys)
            keys = pygame.key.get_pressed()
            if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player.x - PLAYER_VEL >= 0:
                player.x -= PLAYER_VEL  # Move left
            if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player.x + PLAYER_VEL + player.width <= WIDTH:
                player.x += PLAYER_VEL  # Move right
            if (keys[pygame.K_UP] or keys[pygame.K_w]) and player.y - PLAYER_VEL >= 0:
                player.y -= PLAYER_VEL  # Move up
            if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player.y + PLAYER_VEL + player.height <= HEIGHT:
                player.y += PLAYER_VEL  # Move down
        
            
            # Move Pokeballs downward and check for collisions
            for star in stars[:]:  # Iterate over a copy of the list to allow modifications
                star.y += STAR_VEL  # Move Pokeball downward
                
                if star.y > HEIGHT:
                    stars.remove(star)  # Remove Pokeballs that move off-screen
                elif star.y + star.height >= player.y and star.colliderect(player):
                    stars.remove(star)  # Remove Pokeball if it collides with player
                    hit = True  # Player is hit
                    break  # Exit loop after collision
            
            # If player is hit, display "You Lost!" message and show restart options
            if hit:
                button_rect = draw_game_over()
                waiting_for_input = True
                
                while waiting_for_input:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            return
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if button_rect.collidepoint(event.pos):  
                                waiting_for_input = False  # Restart game
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:  
                                waiting_for_input = False  # Restart game
                
                break  # Restart the main loop
            
            draw(player, elapsed_time, stars)  # Update screen with new positions

if __name__ == "__main__":
    main()  # Start the game
