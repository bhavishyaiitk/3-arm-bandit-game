import gym
from gym import spaces
import numpy as np
import pygame
import sys
import csv
import random
import time

count = 0
diff = 0

class BanditEnv(gym.Env):
    def __init__(self):
        super(BanditEnv, self).__init__()
        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Box(low=0, high=1, shape=(3,), dtype=np.float32)
        self.total_reward = 0
        self.num_rounds = 0
        self.random_number = "Start!"
        self.number_sequence = []

    def step(self, action):
        if action < 0 or action >= self.action_space.n:
            raise ValueError("Invalid action")

        if action == 0:
            reward = np.random.randint(15, 35)  # High reward for Q
        elif action == 1:
            reward = np.random.randint(33, 49)  # Medium reward for W
        elif action == 2:
            reward = np.random.randint(27, 38)  # Low reward for E

        self.total_reward += reward
        done = True if self.num_rounds >= 30 else False
        self.num_rounds += 1
        return self._get_obs(), reward, done, {}

    def reset(self):
        self.total_reward = 0
        self.num_rounds = 0
        self.number_sequence = []
        return self._get_obs()

    def _get_obs(self):
        return np.zeros(3)  # You can modify this to return additional information if needed

# Initialize the environment
env = BanditEnv()
env.reset()

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("3-Armed Bandit Game")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Create buttons
font = pygame.font.SysFont(None, 30)
button_q = pygame.Rect(100, 100, 100, 50)
button_w = pygame.Rect(200, 100, 100, 50)
button_e = pygame.Rect(300, 100, 100, 50)

last_click_time = None
def convert(list):
    s = [str(i) for i in list]
    res = int("".join(s))
    return res

# Open CSV file for writing
with open('player_data.csv', mode='a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Choice', 'Reward', 'Reaction Time (ms)'])
    # Main loop
    running = True
    while running:
        screen.fill(WHITE)

        # Display random number
        text_number = font.render(("PLAY!!!"), True, BLACK)
        screen.blit(text_number, (200, 50))

        # Draw buttons
        pygame.draw.rect(screen, GREEN, button_q)
        pygame.draw.rect(screen, RED, button_w)
        pygame.draw.rect(screen, BLUE, button_e)

        # Display button labels
        text_q = font.render('Q', True, BLACK)
        text_w = font.render('W', True, BLACK)
        text_e = font.render('E', True, BLACK)
        screen.blit(text_q, (150, 115))
        screen.blit(text_w, (250, 115))
        screen.blit(text_e, (350, 115))

        # Display total reward on the screen
        text_total_reward = font.render("Total Reward: " + str(env.total_reward), True, BLACK)
        screen.blit(text_total_reward, (50, 200))

        # Display reward obtained in this turn on the screen
        if last_click_time is not None:
            text_reward_obtained = font.render("Reward obtained: " + str(reward), True, BLACK)
            screen.blit(text_reward_obtained, (50, 80))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if last_click_time is None:
                    last_click_time = pygame.time.get_ticks()

                x, y = pygame.mouse.get_pos()
                if button_q.collidepoint(x, y):
                    action = 0
                elif button_w.collidepoint(x, y):
                    action = 1
                elif button_e.collidepoint(x, y):
                    action = 2
                else:
                    action = None

                if action is not None:
                    reaction_time = pygame.time.get_ticks() - last_click_time

                    observation, reward, done, _ = env.step(action)
                    choice_str = 'q' if action == 0 else ('w' if action == 1 else 'e')  # Convert action to choice string
                    print("Reward obtained:", reward)
                    writer.writerow([choice_str, reward, reaction_time - diff])  # Write reward and reaction time to CSV
                    diff = reaction_time

                    # Display reward obtained in this turn on the screen
                    # text_reward_obtained = font.render("Reward obtained: " + str(reward), True, BLACK)
                    # screen.blit(text_reward_obtained, (50, 80))

        pygame.display.flip()

        # Check if 30 rounds are completed
        if env.num_rounds >= 30:
            # Display total reward gained on the screen
            print("GAME OVER!!!")
            # total_reward_text = font.render("Total Reward: " + str(env.total_reward), True, BLACK)
            # screen.blit(total_reward_text, (150, 200))
            pygame.display.flip()

            # Wait for a moment before exiting
            pygame.time.wait(5000)
            running = False

# Exit pygame and save CSV file
pygame.quit()
sys.exit()
