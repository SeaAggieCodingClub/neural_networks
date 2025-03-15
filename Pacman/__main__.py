import os

import pygame
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from PacManGame import PacManGame
from Position import Position
import numpy as np
import random
import datetime
import time
from collections import deque
import tensorflow as tf
from tensorflow.keras.layers import Input, Dense # type: ignore
from tensorflow.keras.models import Sequential, load_model # type: ignore
from tensorflow.keras.optimizers import Adam # type: ignore

action_keys = {
    0: 'w',
    1: 'a',
    2: 's',
    3: 'd'
}

checkpoint_path = "Pacman/models/model4.keras"
'''
model1: 2 layers, 100 neurons
    very poopy testing
model2: 3 layers, 100 neurons
    movement
model3: 2 layers, 30 neurons
    better movement, position tracking and character state
model4: 2 layers, 50 neurons

'''

run_from_config = None

def build_model(env):
    global run_from_config
    
    if run_from_config:
        model = load_model(checkpoint_path)
    else:
        model = Sequential([
            Input(shape=(len(env.flatten_state()),)),
            Dense(50, activation="relu"),
            Dense(50, activation="relu"),
            Dense(4, activation="linear")  # Output: Predicts best action
        ])
        model.compile(loss="mse", optimizer=Adam(learning_rate=0.01))
    return model

def train_ai(episodes=1000, do_wait=False, do_render=False):
    global action_keys
    env = PacManGame(fps=20, do_wait=do_wait, do_render=do_render)
    model = build_model(env)
    target_model = build_model(env)  # Stable target network
    target_model.set_weights(model.get_weights()) # Initialize
    
    # memory = deque(maxlen=2000)
    gamma = 0.95  # Higher discount factor for future rewards, closer to 1 means remembering more
    epsilon = 1.0  # Initial exploration
    epsilon_min = 0.01
    epsilon_decay = (epsilon / 2) ** (1 / episodes) if episodes != 0 else 0.995 # Decay rate
    batch_size = 32
    
    for episode in range(episodes):        
        # Run through the game
        memory = deque(maxlen=2000)
        memory = play_game(model, env, memory, epsilon)\
        
        '''
        prev_action = None
        # prev_pos = None
        print("Rewards:", end='')
        while not done:
            # Exploration vs. exploitation
            if np.random.rand() < epsilon:
                action = env.action_space.sample()
            else:
                q_values = model.predict(np.array([state]), verbose=0) # Output of the model
                choices = env.pacman.get_choices(env.grid) # Valid actions
                valid_q_values = np.multiply(q_values[0], choices) # Set invalid actions to zero
                for q in valid_q_values:
                    if q == 0:
                        np.delete(valid_q_values, q) # Remove zeros
                
                action = np.argmax(valid_q_values) # Highest rated action based on valid actions
                print(choices, q_values, action, prev_action)
            
            new_state, reward, done = env.step(action_keys[action], prev_action)
            memory.append((state, new_state, action, reward, done)) # Store experience
            
            state = new_state
            total_reward += reward
            step_count += 1
            if step_count > 100:
                done = True
                break
            
            for _ in range(10): # Run to smooth action
                if done:
                    break
                done = env.step() # Move the same way
            prev_action = action_keys[action]
            # prev_pos = Position(state[0], state[1])
        print()
        '''
        
        # Train the model
        loss = 0
        if len(memory) > batch_size:
            batch = random.sample(memory, batch_size)
            states, new_states, actions, rewards, dones = zip(*batch)
            
            states = np.stack(states) # Turn into np array
            new_states = np.stack(new_states)
            
            # Get target Q-values
            q_values = model.predict(states, verbose=0)
            next_q_values = target_model.predict(new_states, verbose=0)
            for i in range(batch_size):
                target = rewards[i]
                if not dones[i]:
                    target += gamma * np.max(next_q_values[i])
                q_values[i][actions[i]] = target  # Update Q-values
            
            history = model.fit(states, q_values, epochs=10, verbose=0, batch_size=batch_size)
            loss = history.history['loss'][0]
        
        # Update target model periodically
        if episode % 10 == 0:
            target_model.set_weights(model.get_weights())
        
        # Decay exploration rate
        if epsilon > epsilon_min:
            epsilon *= epsilon_decay
        
        # **Log Metrics in TensorBoard**
        # with summary_writer.as_default():
        #     tf.summary.scalar("Total Reward", total_reward, step=episode)
        #     tf.summary.scalar("Loss", loss, step=episode)
        #     tf.summary.scalar("Epsilon", epsilon, step=episode)
        #| R:{total_reward:12.4f}
        print(f"Ep:{(episode+1):3d} | L:{loss:10.4f} | E:{epsilon:6.4f}, Score:{env.pacman.score:5d}")
    
    env.close()
    return model

def play_game(model, env, memory, epsilon):
    done = False
    step_count = 0
    prev_action = None
    state = env.reset()
    total_reward = 0
    
    print("Action:", end=' ')
    while not done:
        ''' Add # to switch modes
        action = None
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            action = 'w'
        if keys[pygame.K_a]:
            action = 'a'
        if keys[pygame.K_s]:
            action = 's'
        if keys[pygame.K_d]:
            action = 'd'
        
        if action is None:
            env.step()
        else:
            # print(action, prev_action)
            env.step(action, prev_action)
            prev_action = action
        '''
        
        # Exploration vs. exploitation
        if np.random.rand() < epsilon: # Set epsilon to 0 for no exploration
            action = env.action_space.sample()
        else:
            q_values = model.predict(np.array([state]), verbose=0)[0] # Output of the model
            choices = env.pacman.get_choices(env.grid) # Valid actions
            # valid_q_values = np.multiply(q_values, choices) # Set invalid actions to zero
            # valid_q_values = valid_q_values[valid_q_values != 0] # Remove zeros
            
            valid_q_values = np.where(choices == 1, q_values, -np.inf)
            # valid_q_values = np.abs(np.multiply(q_values, choices))
            
            action = np.argmax(valid_q_values) # Highest rated action based on valid actions
            # print(choices, valid_q_values, action, prev_action)
        
        new_state, reward, done = env.step(action_keys[action], prev_action)
        memory.append((state, new_state, action, reward, done)) # Store experience
        
        prev_action = action_keys[action]
        state = new_state
        total_reward += reward
        step_count += 1
        if epsilon and step_count > 100:
            done = True
            break
        
        for _ in range(10): # Run to smooth action
            if done:
                break
            done = env.step() # Move the same way
        '''#'''
    
    return memory

run_from_config = 1
trained_model = train_ai(episodes=300, do_render=0)
trained_model.save(checkpoint_path)
env = PacManGame(fps=30, do_wait=True)

# play_game(trained_model, env, deque(), 0)
