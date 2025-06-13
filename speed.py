import pygame
  import random
    import time
      import sys
pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
ROAD_WIDTH = 300
LANE_WIDTH = ROAD_WIDTH // 3
FPS = 60


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car Racing Game")
clock = pygame.time.Clock()


try:
    collision_sound = pygame.mixer.Sound("collision.wav")
    score_sound = pygame.mixer.Sound("score.wav")
except:
    
    class DummySound:
        def play(self): pass
    collision_sound = DummySound()
    score_sound = DummySound()

class Car:
    def __init__(self, x, y, width=50, height=80, color=RED):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = 5
        self.lane = 1  
        
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
          pygame.draw.rect(surface, BLACK, (self.x + 5, self.y + 10, self.width - 10, self.height - 20), 2)
            pygame.draw.rect(surface, YELLOW, (self.x + 10, self.y + 15, 10, 10))
              pygame.draw.rect(surface, YELLOW, (self.x + self.width - 20, self.y + 15, 10, 10))
                pygame.draw.rect(surface, YELLOW, (self.x + 10, self.y + self.height - 25, 10, 10))
                  pygame.draw.rect(surface, YELLOW, (self.x + self.width - 20, self.y + self.height - 25, 10, 10))
        
    def move_left(self):
        if self.lane > 0:
            self.lane -= 1
            
    def move_right(self):
        if self.lane < 2:
            self.lane += 1
            
    def update(self):
        
        target_x = (SCREEN_WIDTH - ROAD_WIDTH) // 2 + self.lane * LANE_WIDTH + (LANE_WIDTH - self.width) // 2
        
        
        if abs(self.x - target_x) > 2:
            self.x += (target_x - self.x) * 0.2
            
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class OpponentCar(Car):
    def __init__(self):
        lane = random.randint(0, 2)
          x = (SCREEN_WIDTH - ROAD_WIDTH) // 2 + lane * LANE_WIDTH + (LANE_WIDTH - 50) // 2
            y = -100
              color = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
                super().__init__(x, y, 50, 80, color)
                  self.speed = random.randint(3, 8)
        
    def update(self):
        self.y += self.speed

class Road:
    def __init__(self):
        self.y = 0
        self.speed = 5
        self.stripes = []
        for i in range(10):
            self.stripes.append(pygame.Rect(SCREEN_WIDTH // 2 - 5, i * 60, 10, 30))
            
    def update(self):
        self.y += self.speed
        if self.y > 60:
            self.y = 0
            
        for stripe in self.stripes:
            stripe.y += self.speed
            if stripe.y > SCREEN_HEIGHT:
                stripe.y = -30
                
    def draw(self, surface):
      
        pygame.draw.rect(surface, GRAY, ((SCREEN_WIDTH - ROAD_WIDTH) // 2, 0, ROAD_WIDTH, SCREEN_HEIGHT))
          pygame.draw.rect(surface, WHITE, ((SCREEN_WIDTH - ROAD_WIDTH) // 2 - 10, 0, 10, SCREEN_HEIGHT))
            pygame.draw.rect(surface, WHITE, ((SCREEN_WIDTH + ROAD_WIDTH) // 2, 0, 10, SCREEN_HEIGHT))
        
     
        for stripe in self.stripes:
            pygame.draw.rect(surface, YELLOW, stripe)

class Game:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.player = Car(SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT - 150)
          self.opponents = []
            self.road = Road()
              self.score = 0
                self.last_score_time = time.time()
                  self.last_opponent_time = time.time()
                    self.game_over = False
                      self.in_menu = True
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                    
                if self.in_menu:
                    if event.key == pygame.K_RETURN:
                        self.in_menu = False
                        if self.game_over:
                            self.reset()
                            self.game_over = False
                elif not self.game_over:
                    if event.key == pygame.K_LEFT:
                        self.player.move_left()
                    elif event.key == pygame.K_RIGHT:
                        self.player.move_right()
                else:
                    if event.key == pygame.K_RETURN:
                        self.reset()
                        
        return True
        
    def update(self):
        if self.in_menu or self.game_over:
            return
            
      
        self.player.update()
        
     
        self.road.update()
       
        current_time = time.time()
        if current_time - self.last_opponent_time > 1.5:
            self.opponents.append(OpponentCar())
            self.last_opponent_time = current_time
            
    
        for opponent in self.opponents[:]:
            opponent.update()
            if opponent.y > SCREEN_HEIGHT:
                self.opponents.remove(opponent)
                
    
        if current_time - self.last_score_time > 0.1:
            self.score += 1
            self.last_score_time = current_time
            if self.score % 10 == 0:
                score_sound.play()
                
      
        player_rect = self.player.get_rect()
        for opponent in self.opponents:
            if player_rect.colliderect(opponent.get_rect()):
                collision_sound.play()
                self.game_over = True
                break
                
    def draw(self):
      
        screen.fill(BLACK)
        
      
        self.road.draw(screen)
        
        if self.in_menu:
            self.draw_menu()
        elif self.game_over:
            self.draw_game_over()
        else:
          
            for opponent in self.opponents:
                opponent.draw(screen)
            self.player.draw(screen)
            
          
            font = pygame.font.SysFont(None, 36)
            score_text = font.render(f"Score: {self.score}", True, WHITE)
            screen.blit(score_text, (10, 10))
            
        pygame.display.flip()
        
    def draw_menu(self):
        font_large = pygame.font.SysFont(None, 72)
        font_small = pygame.font.SysFont(None, 36)
        
        title = font_large.render("CAR RACER", True, WHITE)
        start = font_small.render("Press ENTER to Start", True, WHITE)
        
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 3))
        screen.blit(start, (SCREEN_WIDTH // 2 - start.get_width() // 2, SCREEN_HEIGHT // 2))
        
    def draw_game_over(self):
        font_large = pygame.font.SysFont(None, 72)
        font_small = pygame.font.SysFont(None, 36)
        
        game_over = font_large.render("GAME OVER", True, RED)
         score = font_small.render(f"Score: {self.score}", True, WHITE)
          restart = font_small.render("Press ENTER to Restart", True, WHITE)      
           screen.blit(game_over, (SCREEN_WIDTH // 2 - game_over.get_width() // 2, SCREEN_HEIGHT // 3))
            screen.blit(score, (SCREEN_WIDTH // 2 - score.get_width() // 2, SCREEN_HEIGHT // 2))
             screen.blit(restart, (SCREEN_WIDTH // 2 - restart.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

# Run the game
if __name__ == "__main__":
    game = Game()
    game.run()
