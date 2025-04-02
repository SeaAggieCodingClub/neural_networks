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
from tensorflow.keras.layers import Input, Dense, Conv2D, Flatten, concatenate # type: ignore
from tensorflow.keras.models import Sequential, load_model, Model # type: ignore
from tensorflow.keras.optimizers import Adam # type: ignore

action_keys = {
    0: 'w',
    1: 'a',
    2: 's',
    3: 'd'
}

checkpoint_path = "neural_networks/Pacman/models/model4.keras"
'''
model1: 2 layers, 100 neurons
    very poopy testing
model2: 3 layers, 100 neurons
    movement
model3: 2 layers, 30 neurons
    better movement, position tracking and character state
model4: 
    cnn: 2 layers, 32 and 64 neurons
    mlp: 2 layers, 64 and 32 neurons
    

'''

run_from_config = None

def build_model(env):
    global run_from_config
    state_dim = len(env.game_state)
    
    if run_from_config:
        model = load_model(checkpoint_path)
    else:
        # CNN for grid state
        cnn_model = Sequential([
            Conv2D(32, (3, 3), activation='relu', input_shape=(28, 31, 1)),
            Conv2D(64, (3, 3), activation='relu'),
            Flatten()
        ])
        
        # MLP for game state
        mlp_model = Sequential([
            Dense(64, activation='relu', input_shape=(state_dim,)),
            Dense(32, activation='relu')
        ])
        
        # Functional API to merge both models
        grid_input = Input(shape=(28, 31, 1))  # Input for CNN
        game_input = Input(shape=(state_dim,))  # Input for MLP
        
        # Apply the Sequential models to their respective inputs
        cnn_output = cnn_model(grid_input)
        mlp_output = mlp_model(game_input)
        
        # Merge both outputs
        merged = concatenate([cnn_output, mlp_output])
        
        # Fully connected decision-making layers
        z = Dense(128, activation='relu')(merged)
        z = Dense(64, activation='relu')(z)
        output = Dense(4, activation='linear')(z)  # Q-values for DQN
        
        # Define and compile the final model
        model = Model(inputs=[grid_input, game_input], outputs=output)
        model.compile(optimizer=Adam(learning_rate=0.01), loss="mse")
        
        # model = Sequential([
        #     Input(shape=(len(env.flatten_state()),)),
        #     Dense(50, activation="relu"),
        #     Dense(50, activation="relu"),
        #     Dense(4, activation="linear")  # Output: Predicts best action
        # ])
        # model.compile(loss="mse", optimizer=Adam(learning_rate=0.01))
    return model

def train_ai(episodes=1000, do_wait=False, do_render=False):
    global action_keys
    env = PacManGame(fps=20, do_wait=do_wait, do_render=do_render)
    model = build_model(env)
    # model.summary()  # Show model architecture
    target_model = build_model(env)  # Stable target network
    target_model.set_weights(model.get_weights()) # Initialize
    
    # memory = deque(maxlen=2000)
    gamma = 0.95  # Higher discount factor for future rewards, closer to 1 means remembering more
    epsilon = 1.0  # Initial exploration
    epsilon_min = 0.01
    epsilon_decay = (epsilon / 2) ** (1 / episodes) if episodes != 0 else 0.995 # Decay rate
    batch_size = 128
    memory = deque(maxlen=2000)
    
    for episode in range(episodes):
        # Run through the game
        memory = play_game(model, env, memory, epsilon)
        
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
            batch = random.sample(memory, batch_size) # [(...),(...),(...),(...)]
            states, new_states, actions, rewards, dones = zip(*batch) # ([....],[....],[....])
            # print(rewards)
            states = [np.array(col) for col in zip(*states)] # Format for predict()
            new_states = [np.array(col) for col in zip(*new_states)]
            
            # Get target Q-values
            q_values = model.predict(states, verbose=0)
            new_q_values = target_model.predict(new_states, verbose=0)
            
            normalized_rewards = (rewards - np.mean(rewards)) / (np.std(rewards) + 1e-5)
            
            updated_q_values = np.copy(q_values)  # Avoid modifying q_values directly
            for i in range(batch_size):
                # target = rewards[i]
                target = normalized_rewards[i]
                if not dones[i]:
                    target += gamma * np.max(new_q_values[i])
                updated_q_values[i][actions[i]] = target  # Update Q-values
                alpha = 0.1 # Learning rate
                updated_q_values[i][actions[i]] = (1 - alpha) * q_values[i][actions[i]] + alpha * target
            
            history = model.fit(states, updated_q_values, epochs=1, verbose=0, batch_size=batch_size)
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
        print(f"Ep:{(episode+1):3d} | L:{loss:10.4f} | E:{epsilon:6.4f} | Score:{env.pacman.score:5d}")
    
    env.close()
    return model

def play_game(model, env, memory, epsilon=0):
    done = False
    step_count = 0
    prev_action = None
    state = env.reset()
    total_reward = 0
    
    while not done:
        # env.step(' ')
        # for _ in range(5): # Run to smooth action
        #     env.step(' ') # Move the same way
        # continue
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
            # print("rand:  ", end='')
        else:#[np.array(state[0]), np.array([state[1]])]
            # print("State:", [np.array([state[0]]), np.array([state[1]])])
            q_values = model.predict([np.array([state[0]]), np.array([state[1]])], verbose=0)[0] # Output of the model
            
            choices = env.pacman.get_choices(env.grid) # Valid actions
            valid_q_values = np.where(choices == 1, q_values, -np.inf)
            
            action = np.argmax(valid_q_values) # Highest rated action based on valid actions
            # print(choices, valid_q_values, action, prev_action)
            # print("model: ", end='')
        # print(('  ' * action) + action_keys[action])
        
        new_state, reward, done = env.step(action_keys[action], prev_action)
        memory.append((state, new_state, action, reward, done)) # Store experience
        
        prev_action = action_keys[action]
        state = new_state
        total_reward += reward
        step_count += 1
        if epsilon and step_count > 200:
            done = True
            break
        
        for _ in range(10): # Run to smooth action
            if done:
                break
            done = env.step() # Move the same way
        '''#'''
    
    return memory

run_from_config = 0
trained_model = train_ai(episodes=200, do_render=0)
trained_model.save(checkpoint_path)
env = PacManGame(fps=60, do_wait=True)
play_game(trained_model, env, deque(maxlen=1))
# env.pacman.pos.tile().get_manhattan_dist(env.grid, (26, 29))