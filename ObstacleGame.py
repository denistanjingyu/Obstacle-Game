#!/usr/bin/env python
# coding: utf-8

# Import pygame module
import pygame

# Setting up the display for the game
# Screen title
screen_title = 'Obstacle Game'
# Screen size
screen_width = 800
screen_height = 800
# Screen color in RGB
white_color = (255, 255, 255)
black_color = (0, 0, 0)

# Initialize all imported pygame modules            
pygame.init()
# Set the font
pygame.font.init
font = pygame.font.SysFont('comicsans', 75)
# Create a clock that can be used to track an amount of time
clock = pygame.time.Clock()

# Create a class for the game
class Game:
    # Set the FPS
    tick_rate = 60
    
    # Initialise screen variables
    def __init__(self, image_path, title, width, height):
        self.title = title
        self.width = width
        self.height = height
        
        # Create window of specified width and height
        self.game_screen = pygame.display.set_mode((width, height))
        
        # reate window of specified color
        self.game_screen.fill(white_color)
        
        # Set screen title
        pygame.display.set_caption(screen_title)
        
        # Load background
        background_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(background_image, (width, height))
        
    # Method to run the game
    def run_game_loop(self, speed_difficulty):
        # Default game status
        is_game_over = False
        # Default win condition set to False
        win_condition = False
        # Default direction
        direction = 0
        
        # Load player character
        player = PlayerCharacter(r"C:\\Users\user\\Desktop\\Pygame Project Files\\player.png", 375, 700, 50, 50)
        
        # Load enemy characters
        enemy_0 = EnemyCharacter(r"C:\\Users\user\\Desktop\\Pygame Project Files\\enemy.png",20,600,50,50)
        enemy_1 = EnemyCharacter(r"C:\\Users\user\\Desktop\\Pygame Project Files\\enemy.png", self.width - 40, 400, 50, 50)
        enemy_2 = EnemyCharacter(r"C:\\Users\user\\Desktop\\Pygame Project Files\\enemy.png", 20, 200, 50, 50)
        
        # Set difficulty of enemy characters based on speed
        enemy_0.speed *= speed_difficulty
        enemy_1.speed *= speed_difficulty
        enemy_2.speed *= speed_difficulty
        
        # Load treasure
        treasure = GameObject(r"C:\\Users\user\\Desktop\\Pygame Project Files\\treasure.png", 375, 50, 50, 50)
        
        # Main game loop
        while not is_game_over:
            # Make a call to one of four functions in the pygame.event module in order for pygame to internally interact with your OS
            pygame.event.get
            # A loop to get all of the events
            for event in pygame.event.get():
                # Exit game loop upon encountering a quit type event
                if event.type == pygame.QUIT:
                    is_game_over = True
                # Detect when key is pressed
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        direction = 1
                    elif event.key == pygame.K_DOWN:
                        direction = -1
                # Detect when key is released        
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        direction = 0
                print(event) 
                
            # Redraw the screen
            self.game_screen.fill(white_color)  
            self.game_screen.blit(self.image, (0, 0))
            
            # Draw the treasure
            treasure.draw(self.game_screen)
            
            # Update player position
            player.move(direction, screen_height)
            # Draw player at new position
            player.draw(self.game_screen)
            
            # Update enemy position
            enemy_0.move(self.width)
            # Draw enemy at new position
            enemy_0.draw(self.game_screen)
            
            # Introduce one more enemy atlevel 4
            if speed_difficulty > 3:
                enemy_1.move(self.width)
                enemy_1.draw(self.game_screen)
                
            # Introduce one more enemy atlevel 6
            if speed_difficulty > 5:
                enemy_1.move(self.width)
                enemy_1.draw(self.game_screen)
                
            # Detect collision
            if player.detect_collision(enemy_0):
                is_game_over = True
                win_condition = False
                text = font.render('You lose!', True, black_color)
                self.game_screen.blit(text, (300, 350))
                pygame.display.update()
                clock.tick(1)
                break
                
            # Reach the treasure
            elif player.detect_collision(treasure):
                is_game_over = True
                win_condition = True
                text = font.render('You won!', True,black_color)
                self.game_screen.blit(text, (300, 350))
                pygame.display.update()
                clock.tick(1)
                break
                
            # Update game graphics        
            pygame.display.update()
            # Tick the clock to update at given fps    
            clock.tick(self.tick_rate)
            
        # Restart the game if win and exit if lose    
        if win_condition:
            self.run_game_loop(speed_difficulty + 1)
        else:
            return

# Create a class for the game object            
class GameObject:
    # Initialize variables
    def __init__(self, image_path, x, y, width,height):
        # Load player image
        object_image = pygame.image.load(image_path)
        
        # Scale image
        self.image = pygame.transform.scale(object_image, (width, height))
        
        # Determine the coordinates of the object where it first appear on the screen
        self.x_pos = x
        self.y_pos = y
        self.width = width
        self.height= height
    
    # Draw the object on the screen
    def draw(self, background):
        background.blit(self.image, (self.x_pos, self.y_pos))
        
# Create a class for the player character              
class PlayerCharacter(GameObject):
    speed = 10
    
    # Inherit attributes and methods from superclass GameObject
    def __init__(self, image_path, x, y, width,height):
        super().__init__(image_path, x, y, width,height)
    
    # Method to move the player
    def move(self,direction, max_height):
        if direction > 0:
            self.y_pos -= self.speed
        elif direction < 0:
            self.y_pos += self.speed
        if self.y_pos >= max_height - 40:
            self.y_pos = max_height - 40
    
    # Method to detect collision
    def detect_collision(self, enemy):
        if self.y_pos > enemy.y_pos+enemy.height:
            return False
        elif self.y_pos+self.height < enemy.y_pos:
            return False
        if self.x_pos > enemy.x_pos + enemy.width:
            return False
        elif self.x_pos + self.width < enemy.x_pos:
            return False
        return True
            
# Create a class for the enemy character              
class EnemyCharacter(GameObject):
    speed = 10
    
    # Inherit attributes and methods from superclass GameObject
    def __init__(self, image_path, x, y, width,height):
        super().__init__(image_path, x, y, width, height)
    
    # Method to move the enemy back and forth
    def move(self, max_width):
        if self.x_pos <= 20:
            self.speed = abs(self.speed)
        elif self.x_pos >= max_width - 40:
            self.speed = -abs(self.speed)
        self.x_pos += self.speed
    
# Execute the game loop        
new_game = Game(r"C:\\Users\user\\Desktop\\Pygame Project Files\\background.png", screen_title, screen_width, screen_height)
new_game.run_game_loop(1)

# Quit pygame and the program
pygame.quit()
quit()
