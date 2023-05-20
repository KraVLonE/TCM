from gym import Env
from gym.spaces import Discrete, Box
import numpy as np
import random
import numpy as np
from functions import Junction
import json

env = Junction()  # creating the enviornment

action_size = env.action_space.n
print("Action size ", action_size)

state_size = env.observation_space.n
print("State size ", state_size)

qtable = np.zeros((state_size, action_size))
print(qtable)

total_episodes = 80000       # Total episodes
total_test_episodes = 100     # Total test episodes
max_steps = 100           # Max steps per episode

learning_rate = 0.4           # Learning rate
gamma = 0.618                 # Discounting rate

# Exploration parameters
epsilon = 1.0                 # Exploration rate
max_epsilon = 1.0             # Exploration probability at start
min_epsilon = 0.01            # Minimum exploration probability 
decay_rate = 0.01             # Exponential decay rate for exploration 


data_bef=[]
data_aft=[]
time_step=[]
flow_state=[]

def flow(state):
    kj=1000
    vf=22.22
    flow = vf*(1-(state/kj))*state

    return flow


def flow_data(k):
    flow_state.append(flow(state))


def append_data_bef(before_state):
    data_bef.append(before_state)

def append_data_aft(after_state):
    data_aft.append(after_state)

def append_time_slot(t):
    time_step.append(t)

def batch_time(current_action):
    if current_action==0 or current_action==3 or current_action==6 or current_action==9:
        t=15

    elif current_action==1 or current_action==4 or current_action==7 or current_action==10:
        t=30

    elif current_action==2 or current_action==5 or current_action==8 or current_action==11:
        t=45

    else:
        t=0

    return t


# 2 For life or until learning is stopped
for episode in range(total_episodes):
    # Reset the environment
    state = env.reset()
    step = 0
    done = False
    
    for step in range(max_steps):
        # 3. Choose an action a in the current world state (s)
        ## First we randomize a number
        exp_exp_tradeoff = random.uniform(0,1)
        
        ## If this number > greater than epsilon --> exploitation (taking the biggest Q value for this state)
        if exp_exp_tradeoff > epsilon:
            action = np.argmax(qtable[int(state),:])
        
        # Else doing a random choice --> exploration
        else:
            action = env.action_space.sample()
        
        # Take the action (a) and observe the outcome state(s') and reward (r)
        new_state, reward, done, info = env.step(action)

        # Update Q(s,a):= Q(s,a) + lr [R(s,a) + gamma * max Q(s',a') - Q(s,a)]
        qtable[int(state), action] = qtable[int(state), action] + learning_rate * (reward + gamma * 
                                    np.max(qtable[int(new_state), :]) - qtable[int(state), action])
                
        # Our new state is state
        state = new_state
        
        # If done : finish episode
        if done == True: 
            break
    
    # Reduce epsilon (because we need less and less exploration)
    epsilon = min_epsilon + (max_epsilon - min_epsilon)*np.exp(-decay_rate*episode) 


rewards = []



class Junction(Env):
    def __init__(self):
        # Actions we can take,A1 ,A2, A3, A4 with t1,t2,t3 = 15,30,45
        self.action_space = Discrete(12)
        self.observation_space = Discrete(1000)
        
        self.no_L1=random.randint(10,16)
        self.no_L2=random.randint(14,25)
        self.no_L3=random.randint(11,18)
        self.no_L4=random.randint(13,16)
        
        self.state = density(self.no_L1,self.no_L2,self.no_L3,self.no_L4,0.1)[8]
        self.kstate = 0

        
    def step(self, action):
        # Apply action
        
        self.kstate=self.state
        
        self.state = junctionflow(action,self.no_L1,self.no_L2,self.no_L3,self.no_L4,0.1)[0]

        #cycle completion
        
        self.timer -= 1 
        
        if self.kstate-self.state>0.1:
            reward=1
        else:
            reward=-1

    
        if self.timer <= 0: 
            done = True
        else:
            done = False
        

        info = {}
        
        # Return step information
        return self.state, reward, done, info

    def render(self):
        # Implement viz
        pass
    
    def reset(self):
        self.state = density(random.randint(12,15),random.randint(14,17),random.randint(16,19),random.randint(21,23),0.1)[8]
        self.timer = 4 

        return self.state


env.reset()

for episode in range(total_test_episodes):
    state = env.reset()
    step = 0
    done = False
    total_rewards = 0
    #print("****************************************************")
    #print("EPISODE ", episode)

    for step in range(max_steps):
        # UNCOMMENT IT IF YOU WANT TO SEE OUR AGENT PLAYING
        # env.render()
        # Take the action (index) that have the maximum expected future reward given that state
        action = np.argmax(qtable[int(state),:])
        append_time_slot(batch_time(action))
        
        new_state, reward, done, info = env.step(action)
        
      
        append_data_aft(new_state)
        flow_data(flow(new_state))
        
        total_rewards += reward
        
        if done:
            rewards.append(total_rewards)
            print ("Score", total_rewards)
            break
        state = int(new_state)
env.close()
print ("Score over time: " +  str(sum(rewards)/total_test_episodes))
print(rewards)
print("--------------------------------------------------------------------------------------------------------------------")
print(time_step)
print("--------------------------------------------------------------------------------------------------------------------")
print(data_aft)  # density after
print("--------------------------------------------------------------------------------------------------------------------")
print(flow_state)


#dict = {
 ##  "den_aft" : data_aft
#}
#data = json.dumps(dict)
##with open("sample1.json", "w") as outfile:
  #  outfile.write(data)

