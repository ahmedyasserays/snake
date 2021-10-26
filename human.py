import pygame, random, json
from pygame.time import Clock

class Snake:
    def __init__(self, window):
        self.size = 10
        self.score = 0
        self.direction = 'stop'
        self.x = 200
        self.y = 200
        self.window = window
        self.rects = [pygame.Rect(self.x - i*10, self.y, 10, 10) for i in range(self.size)]


        
    def draw(self):
        for rect in self.rects:
            pygame.draw.rect(self.window,(0, 255, 0), rect)


    def move(self):
        if self.direction == 'right' and self.x < 410:
            rect = self.rects.pop()
            rect.x = self.x + 10
            rect.y = self.y
            self.x += 10
            self.rects = [rect] + self.rects
        elif self.direction == 'left' and self.x > 10:
            rect = self.rects.pop()
            rect.x = self.x - 10
            rect.y = self.y
            self.x -= 10
            self.rects = [rect] + self.rects
        elif self.direction == 'up' and self.y >20:
            rect = self.rects.pop()
            rect.y = self.y - 10
            rect.x = self.x
            self.y -= 10
            self.rects = [rect] + self.rects
        elif self.direction == 'down' and self.y < 410:
            rect = self.rects.pop()
            rect.y = self.y + 10
            rect.x = self.x
            self.y += 10
            self.rects = [rect] + self.rects


    def check_lose(self):
        hit_wall = not 20 <= self.x <= 400 or not 40 <= self.y <= 400
        hit_tail = False
        for block in self.rects[1:]:
            if block.x == self.x and block.y == self.y:
                hit_tail = True
        if hit_tail or hit_wall:
            self.__init__(self.window)
            return True
        return False
    
    def eat(self):
        self.size += 1
        self.score += 1
        rect = pygame.Rect(0, 0, 10, 10)
        tail = self.rects[-1]
        before = self.rects[-2]
        rect.x = before.x - tail.x
        rect.y = before.y - tail.y
        self.rects.append(rect)






def draw_window(window, snake:Snake):
    global high_score
    window.fill((0, 0, 0))
    snake.draw()
    # borders
    pygame.draw.rect(window, WHITE, pygame.Rect(10, 30, 10, 390)) # left
    pygame.draw.rect(window, WHITE, pygame.Rect(410, 30, 10, 390)) # right
    pygame.draw.rect(window, WHITE, pygame.Rect(20, 30, 400, 10)) # top
    pygame.draw.rect(window, WHITE, pygame.Rect(20, 410, 400, 10)) # bottom

    
    font = pygame.font.SysFont(None, 48)
    scoretext=font.render(f"Score: {snake.score}", False, WHITE)
    rect = scoretext.get_rect()
    rect.x = 450
    rect.y = 60
    window.blit(scoretext, rect)

    high_score_text = font.render(f"High Score: {data['high_score']}", False, WHITE)
    rect = high_score_text.get_rect()
    rect.x = 450
    rect.y = 20
    window.blit(high_score_text, rect)


def create_food(window, snake):
    found = False
    while not found:
        xnums = [i for i in range(20, 400, 10)]
        ynums = [i for i in range(40, 400, 10)]
        x = random.choice(xnums)
        y= random.choice(ynums)
        
        for block in snake.rects:
            if block.x == x and block.y == y:
                pass
            else:
                found = True
    food = pygame.Rect(x, y, 10, 10)
    return food

def main():
    WIDTH, HEIGHT = 700, 450
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    snake = Snake(window)
    food = create_food(window, snake)
    clock = Clock()
    pygame.font.init()
    run = True
    last = None

    while run:
        clock.tick(15)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and snake.direction != 'down':
            snake.direction = 'up'
        elif keys[pygame.K_DOWN] and snake.direction != 'up':
            snake.direction = 'down'
        elif keys[pygame.K_RIGHT] and snake.direction != 'left':
            snake.direction = 'right'
        elif keys[pygame.K_LEFT] and snake.direction not in ['right', 'stop']:
            snake.direction = 'left'


        if snake.x == food.x and snake.y == food.y:

            snake.eat()
            food = create_food(window, snake)

        # sheating
        # if snake.x < food.x:
        #     snake.direction = 'right'
        #     print('right')
        # elif snake.x > food.x and snake.direction not in ['right', 'stop']:
        #     snake.direction = 'left'
        #     print('left')
        # else:
        #     if snake.y < food.y:
        #         snake.direction = 'down'
        #         print('down')
        #     elif snake.y > food.y and snake.direction != 'down':
        #         snake.direction = 'up'
        #         print('up')
        #     else:
        #         print('hhhhhh')
        if snake.check_lose():
            pass
        else:
            snake.move()

        draw_window(window, snake)

        pygame.draw.rect(window, (255, 0, 0), food)
        pygame.display.update()

        
    with open('data.json', 'w') as f:
        f.write(json.dumps(data))
    pygame.quit()

if __name__ == '__main__':
    WHITE = (255, 255, 255)
    with open('human_data.json') as f:
        data = json.loads(f.read())

    main()
