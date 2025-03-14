import os
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

checkpoint_path = "Pacman/models/model3.keras"
'''
model1: 2 layers, 100 neurons
    very poopy testing
model2: 3 layers, 100 neurons
    movement
model3: 
    better movement
'''

def build_model(env):
    run_from_config = 0
    
    if run_from_config:
        model = load_model(checkpoint_path)
    else:
        model = Sequential([
            Input(shape=(len(env.flatten_state()),)),
            Dense(30, activation="relu"),
            Dense(30, activation="relu"),
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
    
    memory = deque(maxlen=2000)
    gamma = 0.95  # Higher discount factor for future rewards
    epsilon = 1.0  # Initial exploration
    epsilon_min = 0.01
    epsilon_decay = epsilon_min ** (1 / episodes) if episodes != 0 else 0.995 # Decay rate
    batch_size = 32
    
    for episode in range(episodes):
        state = env.reset()
        done = False
        total_reward = 0
        step_count = 0
        
        # Run through the game
        prev_action = None
        prev_pos = None
        print("Rewards:", end='')
        while not done:
            # Exploration vs. exploitation
            if np.random.rand() < epsilon:
                action = env.action_space.sample()
            else:
                q_values = model.predict(np.array([state]), verbose=0)[0] # Single state, store in np array
                # action = np.argmax(q_values) # The highest rated action
                choices = env.pacman.get_choices(env.grid)
                action = np.argmax(np.multiply(q_values, choices)) # Highest rated action based on valid actions
            
            new_state, reward, done = env.step(action_keys[action], prev_action, prev_pos)
            memory.append((state, new_state, action, reward, done)) # Store experience
            
            state = new_state
            total_reward += reward
            step_count += 1
            if step_count > 30:
                done = True
                break
            
            for _ in range(10): # Run to smooth action
                if done:
                    break
                done = env.step() # Move the same way
            prev_action = action_keys[action]
            prev_pos = Position(state[0], state[1])
        print()
        
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
        
        print(f"Ep:{(episode+1):3d} | R:{total_reward:12.4f} | L:{loss:10.4f} | E:{epsilon:6.4f}, Score:{env.pacman.score:5d}")
    
    env.close()
    return model

def play_game(model, env):
    state = env.reset()
    done = False
    steps = 0
    
    # print("Action:", end=' ')
    while not done:
        q_values = model.predict(np.array([state]), verbose=0)
        choices = env.pacman.get_choices(env.grid)
        action = np.argmax(np.multiply(q_values, choices)) # Highest rated action based on valid actions
        state, _, done = env.step(action_keys[action])
        steps += 1
        # print(action, end='  ')
        for _ in range(10): # Run to smooth action
            if done:
                break
            done = env.step() # Move the same way

trained_model = train_ai(episodes=100, do_render=0)
trained_model.save(checkpoint_path)
env = PacManGame(fps=20, do_wait=False)
play_game(trained_model, env)
