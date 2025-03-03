import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from PacManGame import PacManGame
import numpy as np
import random
import datetime
import time
from collections import deque
import tensorflow as tf
from tensorflow.keras.layers import Input, Dense # type: ignore
from tensorflow.keras.models import Sequential, load_model # type: ignore
from tensorflow.keras.optimizers import Adam # type: ignore

checkpoint_path = "Pacman/models/model1.keras"

action_keys = {
    0: 'w',
    1: 'a',
    2: 's',
    3: 'd'
}

def build_model():
    run_from_config = 1
    
    if run_from_config:
        model = load_model(checkpoint_path)
    else:
        model = Sequential([
            Input(shape=(15,)),
            Dense(100, activation="relu"),
            Dense(100, activation="relu"),
            Dense(100, activation="relu"),
            Dense(4, activation="linear")  # Output: Predicts best action
        ])
        model.compile(loss="mse", optimizer=Adam(learning_rate=0.01))
    return model

def train_ai(episodes=1000, do_wait=False, do_render=False):
    global action_keys
    env = PacManGame(fps=20, do_wait=do_wait, do_render=do_render)
    model = build_model()
    target_model = build_model()  # Stable target network
    target_model.set_weights(model.get_weights()) # Initialize
    
    gamma = 0.95  # Higher discount factor for future rewards
    epsilon = 1.0  # Initial exploration
    epsilon_min = 0.01
    epsilon_decay = 0.9 # Decay rate
    batch_size = 32
    
    for episode in range(episodes):
        memory = deque(maxlen=2000)
        state = env.reset()
        done = False
        total_reward = 0
        step_count = 0
        
        # Run through the game
        while not done:
            # Exploration vs. exploitation
            if np.random.rand() < epsilon:
                action = env.action_space.sample()
            else:
                q_values = model.predict(np.array([state]), verbose=0)[0] # Single state, store in np array
                action = np.argmax(q_values) # The highest rated action
            
            new_state, reward, done = env.step(action_keys[action])
            memory.append((state, new_state, action, reward, done)) # Store experience
            
            state = new_state
            total_reward += reward
            step_count += 1
            
            for _ in range(12): # Run to smooth action
                if done:
                    break
                new_state, reward, done = env.step() # Move the same way
        
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
        
        print(f"Ep. {(episode+1):3d}: R = {total_reward:12.4f}, L = {loss:10.4f}, E = {epsilon:6.4f}, Steps = {step_count:3d}")
    
    env.close()
    return model

def play_game(model, env):
    state = env.reset()
    done = False
    steps = 0
    
    while not done:
        action = np.argmax(model.predict(np.array([state]), verbose=0)) # Though state is an array, it only holds data for a single gamestate, store in array of multiple states with size 1
        state, _, done= env.step(action)
        steps += 1

trained_model = train_ai(episodes=100, do_render=False)
trained_model.save(checkpoint_path)
# env = PacManGame(fps=60, do_wait=True, do_render=True)
# play_game(trained_model, env)
# while True:
#     action_space = ['w', 'a', 's', 'd']
#     action = action_space[random.randint(0, 3)]
#     for _ in range(10): # Apply action to x steps to smooth movement
#         time.sleep(0.1)
#         env.step()
# env.close()
