# Date Apr 26, 2019
 
#import math
import get_params
import Init_position
import traff
import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt
import decisiontree_l01
import DecisionTree_L11
import environment_multi
import Environment_Multi_Sim
import plot_sim
import save_plot
import save_level_history
import plot_level_ratio
import time
import os



# Parameters
params = get_params.get_params()
w_lane = params.w_lane
v_nominal = params.v_nominal
num_cars = params.num_cars
l_car = params.l_car 
w_car = params.w_car
max_episode = params.max_episode
t_step_DT = params.t_step_DT
complete_flag = params.complete_flag
AV_cars = np.array([1])
params.num_AV = len(AV_cars)
num_Human = num_cars - params.num_AV
params.num_Human = num_Human
num_lanes = params.num_lanes
l_road = params.l_road
outdir = params.outdir

# pick a simulation case
# 0 - Aggressive
# 1 - Adaptive
# 2 - Conservative
params.sim_case = 1

# parameters based on the simulation case
if params.sim_case == 0:
    params.outfile = 'aggressive.mp4'
    params.plot_fname = 'plot_agg'
elif params.sim_case == 1:
    params.outfile = 'adaptive.mp4'
    params.plot_fname = 'plot_adp'
else:
    params.outfile = 'conservative.mp4'
    params.plot_fname = 'plot_con'


# number of simulation steps
max_step = 30


# Initial guess for the level ratio (0 1)
Level_ratio = np.array([[0.2, 0.8]])
Level_ratio = np.array([[0.99, 0.01]])
Level_ratio = np.matlib.repmat(Level_ratio, num_cars * (num_cars-1), 1)

# Define the sizes of the variables
Level_ratio_history=np.zeros((max_episode, max_step, np.shape(Level_ratio)[0], np.shape(Level_ratio)[1]))
R_history = np.zeros((max_episode, num_cars, max_step))

# action space 
# 0: maintain 1: turn left 2: turn right 3:accelerate 4: decelerate 5: hard brake 6:increased acceleration
# 7: small left turn 8: small right turn
action_space = np.array([[0, 1, 2, 3, 4, 5, 6, 7, 8]])


# Create output folder
if not(os.path.exists(outdir)):
        os.mkdir(outdir)


for episode in range(0, params.max_episode):    # simulation will be runned 1 time
    params.episode = episode
    #plt.pyplot.close               # corresponds to close all of matlab, but need to check
    # Traffic initialization
    traffic = traff.initial()       # call a user-defined function, x,y, v, target traffic
    traffic = Init_position.Init_position(params, traffic, AV_cars)
    
    initial_state = np.block ([[traffic.x], [traffic.y], [traffic.orientation], 
                               [traffic.v_car], [traffic.AV_flag], 
                               [traffic.Final_x], [traffic.Final_y],[traffic.Final_orientation]])
    # Traffic state
    X_old = initial_state
    

    # Figure size
    fig_sim = plt.figure(1, figsize=(6, 3))
    fig_lh = plt.figure(2)


    for step in range(0, max_step):
        t0 = time.time()

        # State vector
        print(X_old)

        # Animation plots
        plot_sim.plot_sim(X_old, params, step, Level_ratio, fig_sim)

        # Plot level history
        Level_ratio_history[episode, step, :, :] = Level_ratio


        # L-0
        L0_action_id =  [None]*num_cars    # set the action sizes according to car numbers
        L0_Q_value =  [None]*num_cars      # set the Q value sizes according to car numbers
        for car_id in range(0, num_cars):
            L0_Q_value[car_id], L0_action_id[car_id] = decisiontree_l01.decisiontree_l0(X_old, car_id, action_space, params, Level_ratio)
        
        X_pseudo_L0 = environment_multi.environment_multi(X_old, L0_action_id, t_step_DT, params)
        
        X_pseudo_L0_Id = [None]*num_cars
        for car_id in range(0, num_cars):
            X_pseudo_L0_Id[car_id] = X_pseudo_L0.copy()
            for pre_step in range(0, len(L0_action_id[0])):
                X_pseudo_L0_Id[car_id][pre_step, :, car_id] = X_old[:, car_id]

        # L-1
        L1_action_id = [None]*num_cars
        L1_Q_value = [None]*num_cars
        for car_id in range(0, num_cars):
            L1_Q_value[car_id], L1_action_id[car_id] = DecisionTree_L11.DecisionTree_L1(X_pseudo_L0_Id[car_id], car_id, action_space,  params, Level_ratio) # Call the decision tree function
        
        X_pseudo_L1 = environment_multi.environment_multi(X_old, L1_action_id, t_step_DT, params)
        
        X_pseudo_L1_Id = [None]*num_cars
        for car_id in range(0, num_cars):
            X_pseudo_L1_Id[car_id] = X_pseudo_L1.copy()
            for pre_step in range(0, len(L1_action_id[0])):
                X_pseudo_L1_Id[car_id][pre_step, :, car_id] = X_old[:, car_id]
                
        # D-1
        D1_action_id =[None]*num_cars
        D1_Q_value = [None]*num_cars
        D1_Q_value_opt = [None]*(num_cars-1)
        D1_action_id_opt = [None]*(num_cars-1)
        for car_id in range(0, num_cars):
           for add in range(0, num_cars-1):
                D1_Q_value[add] = np.dot(Level_ratio[car_id*(num_cars-1)+add, 0], L0_Q_value[car_id]) + np.dot(Level_ratio[car_id*(num_cars-1)+add, 1],L1_Q_value[car_id])
                D1_Q_value_opt[add] = np.max(D1_Q_value[add])
                D1_action_id_opt[add] = np.argmax(D1_Q_value[add])
           D1_action_id[car_id] = D1_action_id_opt[np.argmax(D1_Q_value_opt)]
                

        # Controller selection for each cars
        # AV: Auto controller, HV: Level-K contoller
        Action_id = [None]*num_cars
        for car_id in range(0,num_cars):
            if X_old[4][car_id]==1:
                Action_id[car_id] = D1_action_id[car_id]
                # Action_id[car_id] = L1_action_id[car_id][0]
            else:
                Action_id[car_id] = L1_action_id[car_id][0]
                # Action_id[car_id] = L0_action_id[car_id][0]
                # Action_id[car_id] = D1_action_id[car_id]
        print(Action_id)

        # Level estimation update
        for car_id in range(0, num_cars):
            count = 0 
            for inter_car in range(0, num_cars):
                if inter_car != car_id:
                   if (L0_action_id[inter_car][0]==L1_action_id[inter_car][0]):
                       count = count +1
                   else:                                                          
                        if Action_id[inter_car] == L0_action_id[inter_car][0]:
                           Level_ratio[car_id*(num_cars-1)+count, 0] = Level_ratio[car_id*(num_cars-1) + count, 0] + 0.5
                        if Action_id[inter_car] == L1_action_id[inter_car][0]:
                           Level_ratio[car_id*(num_cars-1)+count, 1] = Level_ratio[car_id*(num_cars-1) + count, 1] + 0.5

                        Level_ratio[car_id*(num_cars-1)+count,:] = Level_ratio[car_id*(num_cars-1)+count,:]/ sum(Level_ratio[car_id*(num_cars-1)+count,:])   # normalizing
                        count = count+1
        
        print(Level_ratio)

                
        # State update
        X_new, R = Environment_Multi_Sim.Environment_Multi_Sim(X_old, Action_id, params.t_step_Sim, params)
        X_old = X_new


        # Reward plot
        color = ['b','r','m','g']
        R_history[episode, :, step] = np.transpose(R)
        
        # plt.figure(2)
        # plt.plot(step,R[0],color='b',marker='.',markersize=16)
        # plt.plot(step,R[1],color='r',marker='.',markersize=16)


        # Plot the level_history
        ego_car_id = 1  # AV
        opp_car_id = 3  # Car 4
        plot_level_ratio.plot_level_ratio(Level_ratio_history, ego_car_id, opp_car_id, params, step, episode, max_step, fig_lh)

        # Timer
        t1 = time.time()
        time_per_step = t1 - t0
        # print(time_per_step)


        # Completion check
        if sum(complete_flag[episode, :]) == num_cars:
            break
        
save_plot.save_plot(params,step)
save_level_history.save_level_history(params,step)

# Completion ratio for monte carlo simulation
complete_ratio = sum(complete_flag[:,1]*complete_flag[:,2])/max_episode

