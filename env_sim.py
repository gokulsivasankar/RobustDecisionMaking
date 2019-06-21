# Date Apr 26, 2019
 
#import math
import get_params
import Init_position
import traff
import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt
import decisiontree_l0
import DecisionTree_L1
import environment_multi
import Environment_Multi_Sim
import plot_sim
import save_plot
import time
import os


params = get_params.get_params()    # call a user-defined function
w_lane = params.w_lane
v_nominal = params.v_nominal
num_cars = params.num_cars
l_car = params.l_car 
w_car = params.w_car
max_episode = params.max_episode
t_step_DT = params.t_step_DT
t_step_DT_2 = params.t_step_DT_2
complete_flag = params.complete_flag
AV_cars = np.array([1])
params.num_AV = len(AV_cars)
num_Human = num_cars - params.num_AV
params.num_Human = num_Human
num_lanes = params.num_lanes
l_road = params.l_road
outdir = params.outdir

# Initial guess for the level ratio (0 1 2)
Level_ratio = np.array([[0.05, 0.95]])
# Level_ratio = np.array([[0.6, 0.4]])
Level_ratio = np.matlib.repmat(Level_ratio, num_cars * (num_cars-1), 1)

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
    
    step = 0
    # Initial frame
    plot_sim.plot_sim(X_old, params, step)
    
    step_size = 40
    
    for step in range(1, step_size): 
        t0 = time.time()
#        plt.figure(1)
#        plt.plot(step, Level_ratio[0,0], 'b.')
#        plt.plot(step, Level_ratio[0,1], 'r.')
#        plt.plot(step, Level_ratio[0,2], 'g.')
#        plt.show()
#        plt.title('Car1')
        
        #plt.figure(2)
        #plt.plot(step, Level_ratio[1,0], 'b.')
        #plt.plot(step, Level_ratio[1,1], 'r.')
        #plt.plot(step, Level_ratio[1,2], 'g.')
        #plt.title('Car2')
        
        print(X_old)
        # L-0
        L0_action_id =  [None]*num_cars    # set the action sizes according to car numbers
        L0_Q_value =  [None]*num_cars      # set the Q value sizes according to car numbers
        for car_id in range(0, num_cars):
            L0_Q_value[car_id], L0_action_id[car_id] = decisiontree_l0.decisiontree_l0(X_old, car_id, action_space, params, Level_ratio)
        
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
            L1_Q_value[car_id], L1_action_id[car_id] = DecisionTree_L1.DecisionTree_L1(X_pseudo_L0_Id[car_id], car_id, action_space,  params, Level_ratio) # Call the decision tree function
        
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
                Action_id[car_id] = L0_action_id[car_id][0]
#                Action_id[car_id] = D1_action_id[car_id]
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
        Level_ratio_history=np.zeros( (max_episode, step_size, np.shape(Level_ratio)[0], np.shape(Level_ratio)[1]) )
        Level_ratio_history[episode, step, :, :] = Level_ratio
                
        # State update
        X_new, R = Environment_Multi_Sim.Environment_Multi_Sim(X_old, Action_id, params.t_step_Sim, params)
        X_old = X_new

        
        color = ['b','r','m','g']
        # Animation plot
        plot_sim.plot_sim(X_old, params, step)
        
        
        
       
        
        
        R_history = np.zeros((max_episode, num_cars, step_size))
        R_history[episode, :, step] = np.transpose(R)
        
        
        
        
        # plt.figure(2)
        # plt.plot(step,R[0],color='b',marker='.',markersize=16)
        # plt.plot(step,R[1],color='r',marker='.',markersize=16)
       
        if sum(complete_flag[episode,:])==num_cars:
            break
        
        t1 = time.time()
        time_per_step = t1 - t0
        
#        print(time_per_step)
        
        
save_plot.save_plot(params,step)        

complete_ratio = sum(complete_flag[:,1]*complete_flag[:,2])/max_episode

#fig = plt.subplots()
#plt.plot(range(1:len(R_history[1,:,end])]*t_step_Sim,R_history(1,:,end),'b-','LineWidth',3)
#plot([1:1:length(R_history(2,:,end))]*t_step_Sim,R_history(2,:,end),'r-','LineWidth',3)
#xlabel('t [s]')
#ylabel('R')

#figure(21) hold on
#plot([1:1:length(reshape(Level_ratio_history(1,1,:,end),[],1))]*t_step_Sim,reshape(Level_ratio_history(1,1,:,end),[],1),'b-','LineWidth',3)
#plot([1:1:length(reshape(Level_ratio_history(1,1,:,end),[],1))]*t_step_Sim,reshape(Level_ratio_history(1,2,:,end),[],1),'r-','LineWidth',3)
#plot([1:1:length(reshape(Level_ratio_history(1,1,:,end),[],1))]*t_step_Sim,reshape(Level_ratio_history(1,3,:,end),[],1),'g-','LineWidth',3)
#title('Car 1''s estimate on car 2')
#xlabel('t [s]')
#ylabel('Ratio')

#figure(22) hold on
#plot([1:1:length(reshape(Level_ratio_history(1,1,:,end),[],1))]*t_step_Sim,reshape(Level_ratio_history(2,1,:,end),[],1),'b-','LineWidth',3)
#plot([1:1:length(reshape(Level_ratio_history(1,1,:,end),[],1))]*t_step_Sim,reshape(Level_ratio_history(2,2,:,end),[],1),'r-','LineWidth',3)
#plot([1:1:length(reshape(Level_ratio_history(1,1,:,end),[],1))]*t_step_Sim,reshape(Level_ratio_history(2,3,:,end),[],1),'g-','LineWidth',3)
#title('Car 2''s estimate on car 1')
#xlabel('t [s]')
#ylabel('Ratio')
