import pygame, random, json, neat, os, pickle, math
from pygame.time import Clock

class Snake:
    def __init__(self):
        self.size = 10
        self.score = 0
        self.direction = 'right'
        self.x = 200
        self.y = 200
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
            self.__init__()
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



def draw_window(window, snake:Snake, gen_num):
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

    patch_text = font.render(f"genome: {gen_num}", False, WHITE)
    rect = patch_text.get_rect()
    rect.x = 450 
    rect.y = 100
    window.blit(patch_text, rect)

def create_food(snake):
    found = False
    while not found:
        xnums = [i for i in range(20, 400, 10)]
        ynums = [i for i in range(40, 400, 10)]
        x = random.choice(xnums)
        y= random.choice(ynums)
        found = True
        for block in snake.rects:
            if block.x == x and block.y == y:
                found = False
                break
    food = pygame.Rect(x, y, 10, 10)
    return food

def get_inputs(snake:Snake, food):
    inputs = []

    # wall distances
    top_wall = 40
    top_dist = abs(snake.y - top_wall)
    inputs.append(top_dist)
    right_wall = 400
    right_dist = abs(snake.x - right_wall)
    inputs.append(right_dist)
    bottom_wall = 400
    bottom_dist = abs(snake.y - bottom_wall)
    inputs.append(bottom_dist)
    left_wall = 20
    left_dist = abs(snake.x - left_wall)
    inputs.append(left_dist)

    # wall to angle distances
    top_right_handler = min(right_dist, top_dist)
    top_right_dist = math.sqrt(top_right_handler**2 + top_right_handler**2)
    inputs.append(top_right_dist)

    bottom_right_handler = min(right_dist, bottom_dist)
    bottom_right_dist = math.sqrt(bottom_right_handler**2 + bottom_right_handler**2)
    inputs.append(bottom_right_dist)

    bottom_left_handler = min(left_dist, bottom_dist)
    bottom_left_dist = math.sqrt(bottom_left_handler**2 + bottom_left_handler**2)
    inputs.append(bottom_left_dist)

    top_left_handler = min(left_dist, top_dist)
    top_left_dist = math.sqrt(top_left_handler**2 + top_left_handler**2)
    inputs.append(top_left_dist)

    # nearest tail

    # straigt dirs
    nearest_up = top_dist
    nearest_right = right_dist
    nearest_down = bottom_dist
    nearest_left = left_dist

    # sloped dirs
    nearest_up_right = top_right_dist
    nearest_down_right = bottom_right_dist
    nearest_down_left = bottom_left_dist
    nearest_up_left = top_left_dist

    for block in snake.rects[1:]:
        # straigt dirs
        if block.x == snake.x: # same y direction distance
            if snake.y > block.y: # block above head
                temp = snake.y - block.y - 10
                if temp < nearest_up:
                    nearest_up = temp
            else: # block below head
                temp = block.y - snake.y - 10
                if temp < nearest_down:
                    nearest_down = temp
        elif block.y == snake.y:  # same x direction distance
            if snake.x > block.x: # block is left 
                temp = snake.x - block.x - 10
                if temp < nearest_left:
                    nearest_left = temp
            else: # block is right
                temp = block.x - snake.x - 10
                if temp < nearest_right:
                    nearest_right = temp
        # slooped dirs
        
        elif abs(snake.x - block.x) == abs(snake.y - block.y): # block on same line
            temp = math.sqrt((snake.x - block.x)**2 + (snake.y - block.y)**2 )
            if snake.x < block.x: # block in the right dir
                if snake.y > block.y: # block in top dir
                    if temp < nearest_up_right:
                        nearest_up_right = temp
                else: # block in bottom dir
                    if temp < nearest_down_right:
                        nearest_down_right = temp
            else: # block in the left dir
                if snake.y < block.y:  # block in bottom dir
                    if temp < nearest_down_left:
                        nearest_down_left = temp
                else:
                    if temp < nearest_up_left:
                        nearest_up_left = temp

    inputs.append(nearest_up)
    inputs.append(nearest_right)
    inputs.append(nearest_down)
    inputs.append(nearest_left)

    inputs.append(nearest_up_right)
    inputs.append(nearest_down_right)
    inputs.append(nearest_down_left)
    inputs.append(nearest_up_left)

    # fruit direction and distance

    if food.y < snake.y:
        inputs.append(1)
    else:
        inputs.append(0)

    if food.x > snake.x:
        inputs.append(1)
    else:
        inputs.append(0)

    if food.y > snake.y:
        inputs.append(1)
    else:
        inputs.append(0)

    if food.x < snake.x:
        inputs.append(1)
    else:
        inputs.append(0)

    distance = math.sqrt(abs(snake.x - food.x)**2 + abs(snake.y - food.y)**2 )
    inputs.append(distance)

    # snake direction
    for dir in ['up', 'right', 'down', 'left']:
        if snake.direction == dir:
            inputs.append(1)
        else:
            inputs.append(0)

    # snake size
    inputs.append(snake.size)

    return inputs 


def main(genomes, config):
    WIDTH, HEIGHT = 700, 450
    # window = pygame.display.set_mode((WIDTH, HEIGHT))



    for i, gen in genomes:
        gen.fitness = 0
        net:neat.nn.FeedForwardNetwork = neat.nn.FeedForwardNetwork.create(gen, config)
        snake = Snake()
        food = create_food(snake)
        run = True
        times = 0
        score = 0
        latest_dist = math.sqrt((snake.x - food.x)**2 + (snake.y - food.y)**2)
        while run:
            times += 1
            
            
            inputs = get_inputs(snake, food)
            outputs = net.activate(inputs)

            if outputs[0] and snake.direction != 'down':
                snake.direction = 'up'
            if outputs[1] and snake.direction != 'left':
                snake.direction = 'right'
            if outputs[2] and snake.direction != 'up':
                snake.direction = 'down'
            if outputs[3] and snake.direction not in ['right', 'stop']:
                snake.direction = 'left'
            
            # keys = pygame.key.get_pressed()
            # if keys[pygame.K_UP] and snake.direction != 'down':
            #     snake.direction = 'up'
            # if keys[pygame.K_RIGHT] and snake.direction != 'left':
            #     snake.direction = 'right'
            # if keys[pygame.K_DOWN] and snake.direction != 'up':
            #     snake.direction = 'down'
            # if keys[pygame.K_LEFT] and snake.direction not in ['right', 'stop']:
            #     snake.direction = 'left'
            

            
            if snake.x == food.x and snake.y == food.y:
                times = 0
                gen.fitness += 100
                latest_dist = 9999
                snake.eat()
                food = create_food(snake)

            # gen.fitness += 0.01
            dist = inputs[20]
            if dist < latest_dist:
                gen.fitness += 2
            # else:
            #     gen.fitness -= 1
            latest_dist = dist

            if times > 5000 or snake.check_lose():
                if times > 5000:
                    gen.fitness = 0
                run = False
            else:
                score = snake.score
                if snake.score > data['high_score']:
                    data['high_score'] = snake.score
                
                snake.move()

        print(score)
        
        with open('data2.json', 'w') as f:
            f.write(json.dumps(data))
    pygame.quit()

if __name__ == '__main__':
    GENS = 3

    WHITE = (255, 255, 255)
    with open('data2.json') as f:
        data = json.loads(f.read())
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    config = neat.Config(
        neat.DefaultGenome, 
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    # pop = neat.Population(config)
    pop = neat.Checkpointer.restore_checkpoint('live-eat-mut-1197')
    pop.config.genome_config.bias_mutate_power = 5
    pop.config.genome_config.bias_mutate_rate = 7
    pop.config.genome_config.bias_replace_rate = 0.8
    pop.config.genome_config.enabeled_mutate_rate = 0.1
    pop.config.genome_config.node_add_prob = 0.5
    pop.config.genome_config.node_delete_prob = 0.5

    pop.add_reporter(neat.StdOutReporter(True))
    pop.add_reporter(neat.StatisticsReporter())
    pop.add_reporter(neat.Checkpointer(100, filename_prefix='reset-move1-live-'))
    winner = pop.run(main, GENS)
    print(winner)

    with open('live-eat-edited-conf.pkl', 'wb') as f:
        pickle.dump(winner, f)