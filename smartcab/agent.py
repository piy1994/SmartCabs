import random
import math
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    """ An agent that learns to drive in the Smartcab world.
        This is the object you will be modifying. """ 

    def __init__(self, env, learning=False, epsilon=1.0, alpha=0.5):
        super(LearningAgent, self).__init__(env)     # Set the agent in the evironment 
        self.planner = RoutePlanner(self.env, self)  # Create a route planner
        self.valid_actions = self.env.valid_actions  # The set of valid actions

        # Set parameters of the learning agent
        self.learning = learning # Whether the agent is expected to learn
        self.Q = dict()          # Create a Q-table which will be a dictionary of tuples
        self.epsilon = epsilon   # Random exploration factor
        self.alpha = alpha       # Learning factor

        ###########
        ## TO DO ##
        ###########
        # Set any additional class parameters as needed
        self.trial_num = 0
        self.a = 0


    def reset(self, destination=None, testing=False):
        """ The reset function is called at the beginning of each trial.
            'testing' is set to True if testing trials are being used
            once training trials have completed. """

        # Select the destination as the new location to route to
        self.planner.route_to(destination)
        
        ########### 
        ## TO DO ##
        ###########
        # Update epsilon using a decay function of your choice
        # Update additional class parameters as needed
        # If 'testing' is True, set epsilon and alpha to 0
        #over here set the decay fuction value.
        if testing:
            self.epsilon = 0
            self.alpha = 0
        else:
            self.decay_function(func_val = 4)

        return None

    def decay_function(self,func_val):
        """ if func_val == 1 then linear else exponential"""
        #self.a = 0.01
        self.a = self.alpha
        self.trial_num+=1
        if func_val == 1:
            self.epsilon -= 0.05
        elif func_val == 2:
            # 1/t**2
            self.epsilon = 1.0/(self.trial_num**2)
        elif func_val == 3:
            # a**t
            self.epsilon = self.a**self.trial_num
        elif func_val == 4:
            self.epsilon = math.exp(-self.a*self.trial_num)
        elif func_val == 5:
            self.epsilon = math.cos(self.a*self.trial_num)
        elif func_val == 6:
            self.epsilon = 1.0/(self.trial_num**2 - self.alpha*self.trial_num)
        elif func_val == 7:
        	self.epsilon = 1.0/(self.trial_num**2 - self.a*self.trial_num)
        elif func_val == 8:
        	self.epsilon = abs(math.cos(self.a*self.trial_num))
        return


    def build_state(self):
        """ The build_state function is called when the agent requests data from the 
            environment. The next waypoint, the intersection inputs, and the deadline 
            are all features available to the agent. """

        # Collect data about the environment
        waypoint = self.planner.next_waypoint() # The next waypoint 
        inputs = self.env.sense(self)           # Visual input - intersection light and traffic
        deadline = self.env.get_deadline(self)  # Remaining deadline

        ########### 
        ## TO DO ##
        ###########
        
        # NOTE : you are not allowed to engineer eatures outside of the inputs available.
        # Because the aim of this project is to teach Reinforcement Learning, we have placed 
        # constraints in order for you to learn how to adjust epsilon and alpha, and thus learn about the balance between exploration and exploitation.
        # With the hand-engineered features, this learning process gets entirely negated.
        
        # Set 'state' as a tuple of relevant data for the agent        
        #state = (inputs['light'],waypoint,inputs['oncoming'],inputs['left'],inputs['right'])
        state = (inputs['light'],waypoint,inputs['oncoming'],inputs['left'])

        return state


    def get_maxQ(self, state):
        """ The get_max_Q function is called when the agent is asked to find the
            maximum Q-value of all actions based on the 'state' the smartcab is in. """

        ########### 
        ## TO DO ##
        ###########
        # Calculate the maximum Q-value of all actions for a given state

        maxQ = max(self.Q[state].values())

        return maxQ 


    def createQ(self, state):
        """ The createQ function is called when a state is generated by the agent. """

        ########### 
        ## TO DO ##
        ###########
        # When learning, check if the 'state' is not in the Q-table
        # If it is not, create a new dictionary for that state
        #   Then, for each action available, set the initial Q-value to 0.0

        if state not in self.Q:
            self.Q[state] = dict(zip(self.valid_actions,[0]*len(self.valid_actions)))
        
        return


    def choose_action(self, state):
        """ The choose_action function is called when the agent is asked to choose
            which action to take, based on the 'state' the smartcab is in. """

        # Set the agent state and default action
        self.state = state
        self.next_waypoint = self.planner.next_waypoint()
        action = None

        ########### 
        ## TO DO ##
        ###########
        # When not learning, choose a random action
        # When learning, choose a random action with 'epsilon' probability
        # Otherwise, choose an action with the highest Q-value for the current state
        # Be sure that when choosing an action with highest Q-value that you randomly select between actions that "tie".
        if self.learning == False:
            action = random.choice(self.valid_actions)
        else:
            if self.epsilon > 0.01 and self.epsilon > random.random():
                action = random.choice(self.valid_actions)
            else:
                possible_actions = []
                max_Q = self.get_maxQ(state)
                for key in self.Q[state].keys():
                    if self.Q[state][key] == max_Q:
                        possible_actions.append(key)
                action = random.choice(possible_actions)

        return action


    def learn(self, state, action, reward):
        """ The learn function is called after the agent completes an action and
            receives a reward. This function does not consider future rewards 
            when conducting learning. """

        ########### 
        ## TO DO ##
        ###########
        # When learning, implement the value iteration update rule
        #   Use only the learning rate 'alpha' (do not use the discount factor 'gamma')
        """self.Q[state][action] = self.Q[state][action]*(1 - self.alpha) + \
        self.alpha*(reward + self.Q[state][action])"""
        if self.learning:
            self.Q[state][action] = self.Q[state][action]*(1 - self.alpha) + \
            self.alpha*(reward)


        return


    def update(self):
        """ The update function is called when a time step is completed in the 
            environment for a given trial. This function will build the agent
            state, choose an action, receive a reward, and learn if enabled. """

        state = self.build_state()          # Get current state
        self.createQ(state)                 # Create 'state' in Q-table
        action = self.choose_action(state)  # Choose an action
        reward = self.env.act(self, action) # Receive a reward
        self.learn(state, action, reward)   # Q-learn

        return
        

def run():
    """ Driving function for running the simulation. 
        Press ESC to close the simulation, or [SPACE] to pause the simulation. """

    ##############
    # Create the environment
    # Flags:
    #   verbose     - set to True to display additional output from the simulation
    #   num_dummies - discrete number of dummy agents in the environment, default is 100
    #   grid_size   - discrete number of intersections (columns, rows), default is (8, 6)
    env = Environment(verbose = False)
    
    ##############
    # Create the driving agent
    # Flags:
    #   learning   - set to True to force the driving agent to use Q-learning
    #    * epsilon - continuous value for the exploration factor, default is 1
    #    * alpha   - continuous value for the learning rate, default is 0.5
    agent = env.create_agent(LearningAgent,learning=True,alpha = 0.01)
    
    ##############
    # Follow the driving agent
    # Flags:
    #   enforce_deadline - set to True to enforce a deadline metric
    env.set_primary_agent(agent,enforce_deadline=True)

    ##############
    # Create the simulation
    # Flags:
    #   update_delay - continuous time (in seconds) between actions, default is 2.0 seconds
    #   display      - set to False to disable the GUI if PyGame is enabled
    #   log_metrics  - set to True to log trial and simulation results to /logs
    #   optimized    - set to True to change the default log file name
    sim = Simulator(env,update_delay=0.01,log_metrics = True,optimized = True,display = False)
    
    ##############
    # Run the simulator
    # Flags:
    #   tolerance  - epsilon tolerance before beginning testing, default is 0.05 
    #   n_test     - discrete number of testing trials to perform, default is 0
    sim.run(n_test = 100,tolerance = 0.001)


if __name__ == '__main__':
    run()

    """
    some notes: deadline = 5*distance so each trail has its own deadline
    hard_dealine = -100, so if enforce dealine is False it will start from distance*5 to -100
    if it is the it will go till 0

    """