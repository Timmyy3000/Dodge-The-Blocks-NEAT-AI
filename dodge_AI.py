import pygame
import random
import math
import os
import neat
import numpy as np

pygame.init()
pygame.font.init()

WIDTH = 800
HEIGHT = 900
FONT = pygame.font.SysFont('comicsans', 50)
clock = pygame.time.Clock()

# Color catalogue
blue = (0, 50, 200)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# light shade of the button
color_light = (170, 170, 170)

# dark shade of the button
color_dark = (100, 100, 100)

block_speed = 5
score = 0
score_h = 0

GAME_STATE = 0
window = pygame.display.set_mode((WIDTH, HEIGHT))
window_img = pygame.transform.scale(pygame.image.load(os.path.join('img', 'bg.png')),
                                    (WIDTH, HEIGHT))
ttl_img = pygame.transform.scale(pygame.image.load(os.path.join('img', 'ttl.png')),
                                    (600, 200))

# Player Attributes
player_width = 80
player_height = 40
player_x = WIDTH / 2 - (player_width / 2)
player_y = HEIGHT - 100
player_speed = 20

# Block Attributes
block_count = 4
block_width = 120
block_height = 80
block_x = 50
block_y = -100
padding = 30

gen = 0

# Global variables
state = True
block_speed = 8
spawn_freq = math.floor(500 / block_speed)
ai_run = True


def AI_STATE():
    global gen, state, score, block_speed, spawn_freq, ai_run
    state = True
    score = 0
    block_speed = 10
    spawn_freq = math.floor(500 / block_speed)
    gen = 0

    block_img = pygame.transform.scale(pygame.image.load(os.path.join('img', 'bug.png')),
                                       (block_width, block_height))

    class Player:

        def __init__(self, x, y, ):
            self.x = x
            self.y = y
            self.width = player_width
            self.height = player_height
            self.speed = player_speed
            self.colour = green
            self.img = pygame.transform.scale(pygame.image.load(os.path.join('img', 'code_sprite.png')),
                                              (player_width, player_height))

        def draw(self, win):
            self.hitbox = self.img.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)

            win.blit(self.img, self.hitbox.topleft)

        def move(self, dir):

            # move left1
            if dir == 1:
                if self.x <= 10:
                    self.x = 10
                else:
                    self.x -= self.speed

            # move right
            if dir == 2:
                if self.x >= WIDTH - self.width - 10:
                    self.x = WIDTH - self.width - 10
                else:
                    self.x += self.speed

        def dead(self):

            self.img = pygame.transform.scale(pygame.image.load(os.path.join('img', 'code_sprite_dead.png')),
                                              (player_width, player_height))

        def getInputs(self, blocks):

            input = []

            gap_dist = 0
            left_gap = 0
            right_gap = 0
            gap_y = 0

            input.append(0)
            count = 0

            for block in blocks:
                if count < 4 and block.y < HEIGHT:
                    input.append(block.x)
                    input.append(block.x + block.width)
                    gap_y = block.y + + block.height
                    count += 1

            input.append(WIDTH)
            input.append(self.x)

            for i in range(len(input) - 1):

                dist = 0

                dist = input[i + 1] - input[i]

                if dist > gap_dist:
                    gap_dist = dist
                    left_gap = input[i]
                    right_gap = input[i + 1]

            # pygame.draw.line(window, red, (self.x + self.width, self.y), (left_gap, gap_y), 5)
            # pygame.draw.line(window, red, (self.x + self.width, self.y), (right_gap, gap_y), 5)
            #
            return [left_gap, right_gap, self.x]

    class Block:

        def __init__(self, x, y, width, height):
            self.width = width
            self.height = height
            self.velocity = block_speed
            self.x = None
            self.x = x
            self.y = y
            self.img = block_img
            self.hitbox = self.img.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)

        def draw(self, win):
            self.hitbox = self.img.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
            win.blit(self.img, self.hitbox.topleft)

        def fall(self):
            self.y += self.velocity

        def collisionChecker(self, player):
            return pygame.Rect.colliderect(self.hitbox, player.hitbox)

    def getClosest(player, blocks, window):

        count = 0

        for block in blocks:
            if count < 4 and block.y + block.height < player_y + player.height:

                if (player.x > block.x and player.x < block.x + block.width) or (
                        player.x + player.width > block.x and player.x < block.x):
                    pygame.draw.line(window, white, (player.x, player.y), (block.x, block.y + block.height), 2)
                    pygame.draw.line(window, white, (player.x + player.width, player.y),
                                     (block.x + block.width, block.y + block.height), 2)
                    count += 1

                # To the left
                elif player.x >= block.x + block.width:

                    pygame.draw.line(window, red, (player.x, player.y), (block.x + block.width, block.y + block.height),
                                     2)
                    count += 1

                # To the right
                elif player.x + player.width <= block.x:

                    pygame.draw.line(window, blue, (player.x + player.width, player.y),
                                     (block.x, block.y + block.height), 2)
                    count += 1

    def spawner(blocks):
        row = []

        for i in range(block_count + 1):
            row.append(Block(block_x + i * 150, block_y, block_width, block_height))

        id = random.randint(0, block_count)

        row.pop(id)

        for block in row:
            blocks.append(block)

    def update(agents, blocks, ge, nets):

        c = 0

        for block in blocks:

            for agent in agents:

                if block.collisionChecker(agent):
                    agent.dead()
                    ge[agents.index(agent)].fitness -= 1
                    nets.pop(agents.index(agent))
                    ge.pop(agents.index(agent))
                    agents.pop(agents.index(agent))

            if block and block.y > HEIGHT:

                blocks.remove(block)

                global score, block_speed
                score += 0.25
                block_speed += 0.05

                for genome in ge:
                    genome.fitness += 5

            else:
                block.fall()

    def draw(window, agents, blocks, score, gen):


        # window.blit(window_img, (0, 0))
        window.fill((0, 0, 0))

        for agent in agents:
            agent.draw(window)
            getClosest(agent, blocks, window)

        for block in blocks:
            block.draw(window)

        text = FONT.render('Score : ' + str(score), 1, (255, 255, 255))
        window.blit(text, (WIDTH - text.get_width() - 20, 10))

        generations = FONT.render('Generation : ' + str(gen) + ' / 30 ', 1, (255, 255, 255))
        window.blit(generations, (0, 10))

        # alive
        alive = FONT.render("Alive: " + str(len(agents)), 1, (255, 255, 255))
        window.blit(alive, (10, 50))

        # alive
        tran = FONT.render("Training...", 1, (120, 255, 120))
        window.blit(tran, (WIDTH / 2 - tran.get_width() /2,  HEIGHT - 50 ))

        pygame.display.update()

    def main(genomes, config):

        counter = 0

        global gen, score, block_speed, spawn_freq
        score = 0

        block_speed = 10
        spawn_freq = math.floor(500 / block_speed)

        gen += 1

        blocks = []

        nets = []
        agents = []

        ge = []

        spawner(blocks)

        for genome_id, genome in genomes:
            genome.fitness = 0  # start with fitness level of 0
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            nets.append(net)
            agents.append(Player(player_x, player_y))
            ge.append(genome)

        run_ai = True

        spawn_freq = math.floor(500 / block_speed)

        while run_ai and len(agents) > 0:

            clock.tick(60)

            counter += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    for g in ge:
                        g.fitness = 2000
                    run_ai = False

            draw(window, agents, blocks, score, gen)

            if counter % spawn_freq == 0:
                spawner(blocks)

            update(agents, blocks, ge, nets)

            if block_speed % 100 == 0 and block_speed % 5 == 0:
                spawn_freq = math.floor(500 / block_speed)

            for x, agent in enumerate(agents):
                ge[x].fitness += 0.1

                inputs = agent.getInputs(blocks)

                output = nets[agents.index(agent)].activate((
                    inputs[0],
                    inputs[1],
                    inputs[2],

                ))

                if output[0] >= 0.5:
                    agent.move(1)  # move left
                else:
                    agent.move(2)  # move right

    def run(conifg_path):
        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                    neat.DefaultStagnation, config_path)

        pop = neat.Population(config)
        pop.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        pop.add_reporter(stats)

        winner = pop.run(main, 30)

        print('------- AI ------ \n', winner)

    if __name__ == '__main__':
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, 'NeatConfig.txt')
        run(config_path)


def HUMAN_STATE():
    global state, score_h, block_speed, spawn_freq
    state = True
    score_h = 0
    block_speed = 10
    spawn_freq = math.floor(500 / block_speed)

    block_img = pygame.transform.scale(pygame.image.load(os.path.join('img', 'bug.png')),
                                              (block_width, block_height))

    class Player:

        def __init__(self, x, y, width, height, speed):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.speed = speed
            self.colour = green
            self.img = pygame.transform.scale(pygame.image.load(os.path.join('img', 'code_sprite.png')),
                                              (player_width, player_height))
            self.hitbox = None

        def draw(self, win):
            self.hitbox = self.img.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)

            win.blit(self.img, self.hitbox.topleft)

        def move(self):
            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_LEFT]:
                if self.x <= 0:
                    self.x = 0
                else:
                    self.x -= self.speed

            if pressed[pygame.K_RIGHT]:
                if self.x >= WIDTH - self.width:
                    self.x = WIDTH - self.width
                else:
                    self.x += self.speed

        def dead(self):

            self.img = pygame.transform.scale(pygame.image.load(os.path.join('img', 'code_sprite_dead.png')),
                                              (player_width, player_height))

    class Block:

        def __init__(self, x, y, width, height):
            self.width = width
            self.height = height
            self.velocity = block_speed
            self.x = None
            self.x = x
            self.y = y
            self.img = block_img
            self.hitbox = self.img.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)

        def draw(self, win):
            self.hitbox = self.img.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
            win.blit(self.img, self.hitbox.topleft)

        def fall(self):
            self.y += self.velocity

        def collisionChecker(self, player):
            return pygame.Rect.colliderect(self.hitbox, player.hitbox)

    def spawner(blocks):
        row = []

        for i in range(block_count + 1):
            row.append(Block(block_x + i * (block_width + padding), block_y, block_width, block_height))

        id = random.randint(0, block_count)

        row.pop(id)

        for block in row:
            blocks.append(block)

    def update(player, blocks):
        player.move()

        for block in blocks:

            if block.collisionChecker(player):
                player.dead()
                global state
                state = False

            if block.y > HEIGHT:
                blocks.remove(block)

                global score_h, block_speed
                score_h += 0.25
                block_speed += 0.05

            else:
                block.fall()

    def draw(window, player, blocks):
        window.fill((0, 0, 0))

        player.draw(window)

        for block in blocks:
            block.draw(window)

        text = FONT.render('Score : ' + str(score_h), 1, (255, 255, 255))
        window.blit(text, (WIDTH - text.get_width() - 20, 10))

    # def printInput(player, blocks):
    #     input = []
    #     count = 0
    #
    #     for block in blocks:
    #         if count < 4 and block.y + block.height < player_y + player.height:
    #             input.append(block.x)
    #             input.append(block.x + block.width)
    #             count += 1
    #
    #     input.append(player.x)

    def main():
        counter = 0

        # Object Instantiation
        player = Player(player_x, player_y, player_width, player_height, player_speed)
        blocks = []

        run = True

        while run:

            draw(window, player, blocks)


            if state:

                if counter % spawn_freq == 0:
                    spawner(blocks)

                update(player, blocks)

            else:
                i = 0
                delay = 61
                draw(window, player, blocks)
                while i < delay:

                    if i == 60:
                        run = False
                    i += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            pygame.display.update()

            clock.tick(60)
            counter += 1

    main()


def main():
    counter = 0


    # Object Instantiation

    # defining a font
    smallfont = pygame.font.SysFont('Corbel', 35)

    # rendering a text written in
    # this font
    human_text = smallfont.render('Human Mode', True, white)
    ai_text = smallfont.render('AI Mode', True, white)

    button_height = 50
    button_width = 200

    human_button_x = WIDTH / 2 - button_width / 2
    human_button_y = HEIGHT / 2

    ai_button_x = WIDTH / 2 - button_width / 2
    ai_button_y = HEIGHT / 2 + 70

    run = True

    while run:

        mouse = pygame.mouse.get_pos()

        window.blit(window_img, (0, 0))

        window.blit(ttl_img, (100, 20))

        score_text = FONT.render('Puny Human : ' + str(score_h), 1, (255, 255, 255))
        window.blit(score_text, (WIDTH / 2 - score_text.get_width() / 2, 250))

        score_text = FONT.render('Boss AI : ' + str(score), 1, (255, 255, 255))
        window.blit(score_text, (WIDTH / 2 - score_text.get_width() / 2, 300))

        if human_button_x <= mouse[0] <= human_button_x + button_width and human_button_y <= mouse[
            1] <= human_button_y + button_height:
            pygame.draw.rect(window, color_light, [human_button_x, human_button_y, button_width, button_height])
        else:
            pygame.draw.rect(window, color_dark, [human_button_x, human_button_y, button_width, button_height])

        window.blit(human_text, (WIDTH / 2 - human_text.get_width() / 2, human_button_y + 10))

        if ai_button_x <= mouse[0] <= ai_button_x + button_width and ai_button_y <= mouse[
            1] <= ai_button_y + button_height:
            pygame.draw.rect(window, color_light, [ai_button_x, ai_button_y, button_width, button_height])
        else:
            pygame.draw.rect(window, color_dark, [ai_button_x, ai_button_y, button_width, button_height])

        window.blit(ai_text, (WIDTH / 2 - ai_text.get_width() / 2, ai_button_y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # checks if a mouse is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:

                if human_button_x <= mouse[0] <= human_button_x + button_width and human_button_y <= mouse[1] <= human_button_y + button_height:
                    HUMAN_STATE()

                if ai_button_x <= mouse[0] <= ai_button_x + button_width and ai_button_y <= mouse[
                    1] <= ai_button_y + button_height:

                    AI_STATE()

        pygame.display.update()

        clock.tick(60)
        counter += 1


main()
