from gym import Env
from gym.spaces import Discrete, Box
import numpy as np
import random
import numpy as np



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


def density(no_L1,no_L2,no_L3,no_L4,total_lanekm):
    
    rand1=random.randint(3,5) #genrate random no
    density_L1 = (no_L1+rand1)/total_lanekm
    no_L1 += rand1
    
    rand2=random.randint(4,6) #genrate random no
    density_L2 = (no_L2+rand2)/total_lanekm
    no_L2 += rand2

    rand3=random.randint(2,5) #genrate random no
    density_L3 = (no_L3+rand3)/total_lanekm
    no_L3 += rand3

    rand4=random.randint(2,5) #genrate random no
    density_L4 = (no_L4+rand4)/total_lanekm
    no_L1 += rand1 

    return  density_L1, density_L2, density_L3, density_L4, no_L1, no_L2, no_L3, no_L4, density_L1 + density_L2 +density_L3 +density_L4


 # t=30 sec
def junctionflow(action,no_L1,no_L2,no_L3,no_L4,total_lanekm):
    #for A1 t= 15, 30, 45
    if action==0:
        no_L1-=random.randint(2,5)
        dir = rand_dir(no_L1)
        density(no_L1,no_L2,no_L3,no_L4,total_lanekm);
        
    elif action==1:
        no_L1-=random.randint(4,6)
        dir = rand_dir(no_L1)
        density(no_L1,no_L2,no_L3,no_L4,total_lanekm);
    
    elif action==2:
        no_L1-=random.randint(7,8)
        dir = rand_dir(no_L1)
        density(no_L1,no_L2,no_L3,no_L4,total_lanekm);
    #forA2 t= 15,30,45
    elif action==3:
        no_L2-=random.randint(1,4)
        dir = rand_dir(no_L2)
        density(no_L1,no_L2,no_L3,no_L4,total_lanekm);
        
        
    elif action==4:
        no_L2-=random.randint(3,7)
        dir = rand_dir(no_L2)
        density(no_L1,no_L2,no_L3,no_L4,total_lanekm);
        
        
    elif action==5:
        no_L2-=random.randint(5,8)
        dir = rand_dir(no_L2)
        density(no_L1,no_L2,no_L3,no_L4,total_lanekm);
        
    #for A3 t=15,30,45
    elif action==6:
        no_L3-=random.randint(2,7)
        dir = rand_dir(no_L3)
        density(no_L1,no_L2,no_L3,no_L4,total_lanekm);
        
        
    elif action==7:
        no_L3-=random.randint(4,7)
        dir = rand_dir(no_L3)
        density(no_L1,no_L2,no_L3,no_L4,total_lanekm);
        
        
    elif action==8:
        no_L3-=random.randint(5,7)
        dir = rand_dir(no_L3)
        density(no_L1,no_L2,no_L3,no_L4,total_lanekm);
    
    #for A4 t=15,30,45    
    elif action==9:
        no_L4-=random.randint(3,7)
        dir = rand_dir(no_L4)
        density(no_L1,no_L2,no_L3,no_L4,total_lanekm);
        
        
    elif action==10:
        no_L4-=random.randint(7,8)
        dir = rand_dir(no_L4)
        density(no_L1,no_L2,no_L3,no_L4,total_lanekm);
    
            
    elif action==11:
        no_L4-=random.randint(5,10)
        dir = rand_dir(no_L4)
        density(no_L1,no_L2,no_L3,no_L4,total_lanekm);
    
    
    new_state =  density(no_L1,no_L1,no_L1,no_L1,0.1)[8]
    
    # new_sate, striaght, right, left
    return new_state,dir[0],dir[1],dir[2]

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
    


def rand_dir(no_ofV):
    #straight
    percent_chance=[15,35,39,25]
    random_num = random.choice(percent_chance)
    x = (random_num/100)*no_ofV
    no_ofV-=x
    
    #right 
    percent_chance=[45,67,23,18]
    random_num = random.choice(percent_chance)
    y = (random_num/100)*no_ofV
    no_ofV-=y
    
    #left
    z=no_ofV
    
    return x,y,z
    

def flow(state):
    kj=1000
    vf=22.22
    flow = vf*(1-(state/kj))*state

    return flow


def flow_data(k):
    flow_state.append(flow(state))
