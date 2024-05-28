import torch
import random
import numpy as np
from collections import deque
from main import CarGame
from model import Linear_QNet, QTrainer
from playerCar import PlayerCar
import pygame


MAX_MEMORY = 100000
BATCH_SIZE = 1000
LR = 0.001
IS_PLAYER = False
FINAL_MOVE_LIST = [
    [0, 0, 1, 0],  # forward
    # [1, 0, 0, 0],  # left turn
    # [0, 1, 0, 0],  # right turn
    [0, 0, 0, 1],  # brake
    [1, 0, 1, 0],  # forward + left turn
    [0, 1, 1, 0],  # forward + right turn
    # [1, 0, 0, 1],  # brake + left turn
    # [0, 1, 0, 1]   # brake + right turn
]

class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(10 + 1 + 1, 256, 4)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
        
    def get_state(self, game):
        # temp = game.collision_point_list + game.target
        temp = game.collision_point_list[:]
        temp.append(int(game.player_car.vel))
        temp.append(game.target)
        # print(game.collision_point_list)
        if len(temp) != 12:
            return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        return temp

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        #for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):

        if not IS_PLAYER:
            # random moves: tradeoff exploration / exploitation
            self.epsilon = 200 - self.n_games
            move = 0
            if random.randint(0, 200) < self.epsilon:
                move = random.randint(0, 15)

                
            else:
                state0 = torch.tensor(state, dtype=torch.float)
                prediction = self.model(state0)
                move = torch.argmax(prediction).item()
                

            if move > 3:
                move = 0

            return FINAL_MOVE_LIST[move]
        
        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                return [1, 0, 1, 0]
            if keys[pygame.K_d]:
                return [0, 1, 1, 0]
            if keys[pygame.K_w]:
                return [0, 0, 1, 0]
            if keys[pygame.K_s]:
                return [0, 0, 0, 1]
                    
            return [0, 0, 0, 0]




def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = CarGame()
    
    while True:

        
        # get old state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = game.play_game(final_move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)


        

        # if reward != 0:
        #     print(f"reward: {reward}")

        if done:
            # train long memory, plot result
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record:', record)

            print(f"score: {score}")
            


if __name__ == '__main__':
    train()