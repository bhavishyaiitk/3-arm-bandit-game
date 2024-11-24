import gym
from gym import spaces
import numpy as np
import pygame
import sys
import csv
import random

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
            reward = np.random.randint(33, 49)  # High reward for Q
        elif action == 1:
            reward = np.random.randint(15, 35)  # Medium reward for W
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

def convert(list):
	s = [str(i) for i in list]
	res = int("".join(s))
	return(res)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("3-Armed Bandit Game")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Create buttons
font = pygame.font.SysFont(None, 30)
button_q = pygame.Rect(100, 100, 100, 50)
button_w = pygame.Rect(200, 100, 100, 50)
button_e = pygame.Rect(300, 100, 100, 50)

# Set up timer variables
start_time = None
count = 0
large_font = pygame.font.SysFont(None, 40)
# Open CSV file in append mode
with open('player_data.csv', mode='a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Choice', 'Reward', 'Reaction Time (ms)'])
    # Main loop
    running = True
    while running:
        screen.fill(WHITE)

        # Display random number
        text_number = large_font.render(str(env.random_number), True, BLACK)
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

        # Calculate elapsed time since the start time
        elapsed_time = pygame.time.get_ticks() - start_time if start_time is not None else 0

        # Display timer on the screen
        text_timer = font.render("Timer: " + str(int(elapsed_time / 1000)), True, BLACK)
        screen.blit(text_timer, (50, 50))

        # Display total reward on the screen
        text_total_reward = font.render("Total Reward: " + str(env.total_reward), True, BLACK)
        screen.blit(text_total_reward, (50, 200))

        # Display reward obtained in this turn on the screen
        if start_time is not None:
            text_reward_obtained = font.render("Reward obtained: " + str(reward), True, BLACK)
            screen.blit(text_reward_obtained, (50, 80))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if button_q.collidepoint(x, y):
                    action = 0
                    count += 1
                    if env.random_number == 'Start!':
                        count -= 1
                        env.num_rounds -= 1
                elif button_w.collidepoint(x, y):
                    action = 1
                    count += 1
                    if env.random_number == 'Start!':
                        count -= 1
                        env.num_rounds -= 1
                elif button_e.collidepoint(x, y):
                    action = 2
                    count += 1
                    if env.random_number == 'Start!':
                        count -= 1
                        env.num_rounds -= 1
                else:
                    action = None

                if action is not None:
                    # Calculate reaction time
                    reaction_time = pygame.time.get_ticks() - start_time if start_time is not None else 0
                    observation, reward, done, _ = env.step(action)
                    choice_str = 'q' if action == 0 else ('w' if action == 1 else 'e')  # Convert action to choice string
                    if reaction_time > 1200:
                        env.total_reward -= 50  # Subtract 50 points from total reward
                        print("Time pressure exceeded! Total Reward reduced by 50 points.")
                    print("Reward obtained:", reward)
                    text_reward_obtained = font.render("Reward obtained: " + str(reward), True, BLACK)
                    start_time = pygame.time.get_ticks()
                    
                    # Write data to CSV file
                    writer.writerow([choice_str, reward, reaction_time])

                if count == 0 or count == 5:
                    # Reset timer and generate a new random number
                    count = 0  # Reset count
                    env.random_number = random.randint(1, 9)
                    env.number_sequence.append(env.random_number)

            # Check for timeout or rounds completion
            if env.num_rounds >= 30:
                # Stop displaying buttons
                button_q = pygame.Rect(0, 0, 0, 0)
                button_w = pygame.Rect(0, 0, 0, 0)
                button_e = pygame.Rect(0, 0, 0, 0)

                # Ask for number string
                text_input = font.render("Enter the number string:", True, BLACK)
                screen.blit(text_input, (100, 100))
                input_box = pygame.Rect(150, 150, 140, 32)
                color_inactive = pygame.Color('lightskyblue3')
                color_active = pygame.Color('dodgerblue2')
                color = color_inactive
                active = False
                text = ''
                done = False

                while not done:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if input_box.collidepoint(event.pos):
                                active = not active
                            else:
                                active = False
                            color = color_active if active else color_inactive
                        if event.type == pygame.KEYDOWN:
                            if active:
                                if event.key == pygame.K_RETURN:
                                    input_sequence = list(map(int, text))
                                    entered_number = convert(input_sequence)
                                    toCompare = env.number_sequence[:-1]
                                    correct_answer = convert(toCompare)
                                    if entered_number == correct_answer:
                                        print("Correct! Doubling reward.")
                                        env.total_reward *= 2
                                        print("Your Total Reward is :", env.total_reward)

                                    else:
                                        print("Incorrect. Reward remains the same.")
                                        print("Your Total Reward is :", env.total_reward)
                                        print(f'Number you entered: {entered_number}')
                                        print(f"Number expected in environment {correct_answer}")
                                    done = True
                                    text = ''  # Clear text variable after each trial
                                elif event.key == pygame.K_BACKSPACE:
                                    text = text[:-1]
                                else:
                                    text += event.unicode

                    screen.fill(WHITE)
                    txt_surface = font.render(text, True, color)
                    width = max(200, txt_surface.get_width()+10)
                    input_box.w = width
                    screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
                    pygame.draw.rect(screen, color, input_box, 2)
                    pygame.display.flip()
                        
        pygame.display.flip()

# Exit pygame
pygame.quit()
sys.exit()

