import math
import numpy as np
from shapely.geometry import Polygon


def reward(X_reward, car_id, action_id, params, dist_id, Level_ratio):
    

    episode = params.episode
    complete_flag = params.complete_flag

    l_car = params.l_car
    w_car = params.w_car
    w_lane = params.w_lane
    num_lanes = params.num_lanes
    l_road = params.l_road
    num_cars = params.num_cars
    v_ref = params.v_nominal

    l_car_safe = params.l_car_safe_fac * l_car
    w_car_safe = params.w_car_safe_fac * w_car
    
    
    if X_reward[4,car_id] == 1:
        dist_comb = params.dist_comb
        w_ext = dist_comb[dist_id]
        if params.sim_case == 0:
            W_curr = w_ext * np.array([0, 0])
            scale_dist = 0

        elif params.sim_case == 1:
            W_curr = w_ext * np.array([l_car / params.W_l_car_fac, w_car / params.W_w_car_fac])
            scale_dist = 1

        else:
            W_curr = w_ext * np.array([l_car / params.W_l_car_fac, w_car / params.W_w_car_fac])
            scale_dist = 0
        
     
        count = 0
        for id in range(0, num_cars):
            if id!=car_id:
                for i in range(0,2):
                    if scale_dist:
                        X_reward[i,id] = X_reward[i,id] + W_curr[i] * Level_ratio[(car_id)*(num_cars-1) + count][0]
                    else:
                        X_reward[i, id] = X_reward[i, id] + W_curr[i]
                count += 1

    

    # Off road penalty
    Off_road = 0
    Off_road_Penalty = -1e6


    Ego_rectangle = Polygon(
        [[X_reward[0,car_id]-l_car_safe/2*math.cos(X_reward[2,car_id])+w_car_safe/2*math.sin(X_reward[2,car_id]),
          X_reward[1,car_id]-l_car_safe/2*math.sin(X_reward[2,car_id])-w_car_safe/2*math.cos(X_reward[2,car_id])],
        [X_reward[0,car_id]-l_car_safe/2*math.cos(X_reward[2,car_id])-w_car_safe/2*math.sin(X_reward[2,car_id]),
         X_reward[1,car_id]-l_car_safe/2*math.sin(X_reward[2,car_id])+w_car_safe/2*math.cos(X_reward[2,car_id])],
        [X_reward[0,car_id]+l_car_safe/2*math.cos(X_reward[2,car_id])-w_car_safe/2*math.sin(X_reward[2,car_id]),
         X_reward[1,car_id]+l_car_safe/2*math.sin(X_reward[2,car_id])+w_car_safe/2*math.cos(X_reward[2,car_id])],
        [X_reward[0,car_id]+l_car_safe/2*math.cos(X_reward[2,car_id])+w_car_safe/2*math.sin(X_reward[2,car_id]),
         X_reward[1,car_id]+l_car_safe/2*math.sin(X_reward[2,car_id])-w_car_safe/2*math.cos(X_reward[2,car_id])]])

    Upper_RoadBound_rectangle = Polygon(
        [[0, w_lane*num_lanes],
         [0, w_lane*num_lanes*2],
         [l_road, w_lane*num_lanes*2],
         [l_road, w_lane*num_lanes]])
                
    Lower_RoadBound_rectangle = Polygon(
        [[0, 0],
         [0, -w_lane*num_lanes*2],
         [l_road, -w_lane*num_lanes*2],
         [l_road, 0]])
    
    if (Ego_rectangle.intersects(Upper_RoadBound_rectangle) or 
        Ego_rectangle.intersects(Lower_RoadBound_rectangle)):
            Off_road = Off_road + Off_road_Penalty

    # Collision penalty
    Colli = 0
    Colli_Penalty = -1e6

    for id in range(0, len(X_reward[0,:])):
        if id!=car_id:
            Other_rectangle = Polygon(
                [[X_reward[0,id]-l_car_safe/2*math.cos(X_reward[2,id])+w_car_safe/2*math.sin(X_reward[2,id]),
                  X_reward[1,id]-l_car_safe/2*math.sin(X_reward[2,id])-w_car_safe/2*math.cos(X_reward[2,id])],
                [X_reward[0,id]-l_car_safe/2*math.cos(X_reward[2,id])-w_car_safe/2*math.sin(X_reward[2,id]),
                 X_reward[1,id]-l_car_safe/2*math.sin(X_reward[2,id])+w_car_safe/2*math.cos(X_reward[2,id])],
                [X_reward[0,id]+l_car_safe/2*math.cos(X_reward[2,id])-w_car_safe/2*math.sin(X_reward[2,id]),
                 X_reward[1,id]+l_car_safe/2*math.sin(X_reward[2,id])+w_car_safe/2*math.cos(X_reward[2,id])],
                [X_reward[0,id]+l_car_safe/2*math.cos(X_reward[2,id])+w_car_safe/2*math.sin(X_reward[2,id]),
                 X_reward[1,id]+l_car_safe/2*math.sin(X_reward[2,id])-w_car_safe/2*math.cos(X_reward[2,id])]])

            if Ego_rectangle.intersects(Other_rectangle):
                Colli = Colli + Colli_Penalty

    # Safe zone violation penalty
    Safe = 0
    Safe_Penalty = -1e4      # 500

    if params.sim_case == 0:
        l_car_safe_front = 1 * l_car
        l_car_safe_back = 1 * l_car
        w_car_safe = 1 * w_car
    else:
        l_car_safe_front = 1*l_car
        l_car_safe_back = 1*l_car
        w_car_safe = 1*w_car




    Ego_rectangle = Polygon(
        [[X_reward[0,car_id]-l_car_safe_back/2*math.cos(X_reward[2,car_id])+w_car_safe/2*math.sin(X_reward[2,car_id]),
          X_reward[1,car_id]-l_car_safe_back/2*math.sin(X_reward[2,car_id])-w_car_safe/2*math.cos(X_reward[2,car_id])],
        [X_reward[0,car_id]-l_car_safe_back/2*math.cos(X_reward[2,car_id])-w_car_safe/2*math.sin(X_reward[2,car_id]),
         X_reward[1,car_id]-l_car_safe_back/2*math.sin(X_reward[2,car_id])+w_car_safe/2*math.cos(X_reward[2,car_id])],
        [X_reward[0,car_id]+l_car_safe_front/2*math.cos(X_reward[2,car_id])-w_car_safe/2*math.sin(X_reward[2,car_id]),
         X_reward[1,car_id]+l_car_safe_front/2*math.sin(X_reward[2,car_id])+w_car_safe/2*math.cos(X_reward[2,car_id])],
        [X_reward[0,car_id]+l_car_safe_front/2*math.cos(X_reward[2,car_id])+w_car_safe/2*math.sin(X_reward[2,car_id]),
         X_reward[1,car_id]+l_car_safe_front/2*math.sin(X_reward[2,car_id])-w_car_safe/2*math.cos(X_reward[2,car_id])]])
    
    for id in range(0,len(X_reward[1,:])):
        if id!=car_id:
            Other_rectangle = Polygon(
                [[X_reward[0,id]-l_car_safe_back/2*math.cos(X_reward[2,id])+w_car_safe/2*math.sin(X_reward[2,id]),
                  X_reward[1,id]-l_car_safe_back/2*math.sin(X_reward[2,id])-w_car_safe/2*math.cos(X_reward[2,id])],
                [X_reward[0,id]-l_car_safe_back/2*math.cos(X_reward[2,id])-w_car_safe/2*math.sin(X_reward[2,id]),
                 X_reward[1,id]-l_car_safe_back/2*math.sin(X_reward[2,id])+w_car_safe/2*math.cos(X_reward[2,id])],
                [X_reward[0,id]+l_car_safe_front/2*math.cos(X_reward[2,id])-w_car_safe/2*math.sin(X_reward[2,id]),
                 X_reward[1,id]+l_car_safe_front/2*math.sin(X_reward[2,id])+w_car_safe/2*math.cos(X_reward[2,id])],
                [X_reward[0,id]+l_car_safe_front/2*math.cos(X_reward[2,id])+w_car_safe/2*math.sin(X_reward[2,id]),
                 X_reward[1,id]+l_car_safe_front/2*math.sin(X_reward[2,id])-w_car_safe/2*math.cos(X_reward[2,id])]])

            if Ego_rectangle.intersects(Other_rectangle):
                Safe = Safe + Safe_Penalty
                
                
                

    
    
    # Lane overlap violation penalty
    eps = w_car/8
    Lane_1 = Polygon([[0, w_lane-eps],[0, w_lane+eps],[l_road, w_lane+eps],[l_road, w_lane-eps]])
    Lane_2 = Polygon([[0, 2*w_lane-eps],[0, 2*w_lane+eps],[l_road, 2*w_lane+eps],[l_road, 2*w_lane-eps]])
    
    Ego_rectangle = Polygon(
        [[X_reward[0,car_id]-l_car/2*math.cos(X_reward[2,car_id])+w_car/2*math.sin(X_reward[2,car_id]),
          X_reward[1,car_id]-l_car/2*math.sin(X_reward[2,car_id])-w_car/2*math.cos(X_reward[2,car_id])],
        [X_reward[0,car_id]-l_car/2*math.cos(X_reward[2,car_id])-w_car/2*math.sin(X_reward[2,car_id]),
         X_reward[1,car_id]-l_car/2*math.sin(X_reward[2,car_id])+w_car/2*math.cos(X_reward[2,car_id])],
        [X_reward[0,car_id]+l_car/2*math.cos(X_reward[2,car_id])-w_car/2*math.sin(X_reward[2,car_id]),
         X_reward[1,car_id]+l_car/2*math.sin(X_reward[2,car_id])+w_car/2*math.cos(X_reward[2,car_id])],
        [X_reward[0,car_id]+l_car/2*math.cos(X_reward[2,car_id])+w_car/2*math.sin(X_reward[2,car_id]),
         X_reward[1,car_id]+l_car/2*math.sin(X_reward[2,car_id])-w_car/2*math.cos(X_reward[2,car_id])]])
    
    
    Lane_overlap = 0
    Lane_overlap_penalty = -1e4
    if abs(X_reward[2, car_id]- X_reward[7,car_id] ) <= 1e-2:
        if Ego_rectangle.intersects(Lane_1) or Ego_rectangle.intersects(Lane_2):
            Lane_overlap = Lane_overlap + Lane_overlap_penalty    
            
            

    
    # Lane off-center penalty
    Lane = 0
    LC_penalty = -1e-5/(w_lane/2)
    
    for i in range(0, num_lanes):
        if X_reward[1,car_id] <= (i+1)*w_lane and X_reward[1,car_id] > (i)*w_lane:
            lane = i+1
            break  
        elif X_reward[1,car_id] > num_lanes*w_lane:
            lane = num_lanes
        elif X_reward[1,car_id] < 0:
            lane = 1
    lane_center = (lane-1)*w_lane + (w_lane/2)     
    Lane = Lane + LC_penalty*abs(lane_center-(X_reward[1,car_id]))
    
    
    
   
    
    # Completion reward
    Complete = 0
    Complete_Penalty = -1

    if X_reward[0,car_id]<X_reward[5,car_id]:
        # if X_reward[4,car_id] == 0: # if not AV
            # x pos error
            Complete = Complete + 1e-5 * Complete_Penalty/X_reward[5,car_id]*abs(X_reward[5,car_id]-X_reward[0,car_id])
            # orientation error
            Complete = Complete + 1e-3 * Complete_Penalty*abs(math.sin(X_reward[2,car_id] - X_reward[7,car_id] ))

        # elif abs(X_reward[6,car_id]-(X_reward[1,car_id])) <= 1e-0:  # if not AV and y error is within threshold
        #
        #     Complete = Complete + 1e-5 * Complete_Penalty/X_reward[5,car_id]*abs(X_reward[5,car_id]-X_reward[0,car_id])
        #     Complete = Complete + 1e-3 * Complete_Penalty*abs(math.sin(X_reward[2,car_id] - X_reward[7,car_id] ))
            
            Complete = Complete + 1e4 * Complete_Penalty/X_reward[6,car_id]*abs(X_reward[6,car_id]-(X_reward[1,car_id]))
        
        
    else:
        complete_flag[episode,car_id] = 1
        
 
    # Speed reward
    if lane == num_lanes:
        Speed = -1e2*abs(X_reward[3, car_id] - v_ref*1.05)
    else:
        Speed = -1e2 * abs(X_reward[3, car_id] - v_ref)


    

    # Effort penalty
    Effort = 0
    #Effort_penalty = -1e1
    if(action_id==1 or action_id==2):
        Effort = 0
    else:
        Effort = 0
        
        

    # Encourage braking if opponent vehicle is parallel
    Brake = 0
    Brake_reward = 1e4
    if X_reward[4,car_id] == 1:
        des_lane = math.ceil(X_reward[6,car_id]/w_lane)
        for id in range(0,len(X_reward[1,:])):
            if id!=car_id:
                opp_lane = math.ceil(X_reward[1,id]/w_lane)
                if opp_lane == des_lane:
                    if (X_reward[0,id]-5*l_car <= X_reward[0,car_id] <= X_reward[0,id]+0.25*l_car):
                        Brake = Brake + Brake_reward * (1/X_reward[3, car_id])




    # Local Reward
    R_l = (Off_road + Colli  + Safe   + Complete + Speed + Effort*0  + Lane *0  + Lane_overlap *0 + Brake*0)
    if X_reward[4,car_id] == 1 and not(abs(X_reward[6,car_id]-(X_reward[1,car_id])) <= w_lane/2):
        R_l = (Off_road + Colli + Safe  + Complete + Speed * 1e-2+ Effort *0+ Lane *0 + Lane_overlap*0 + Brake*0)

    params.complete_flag = complete_flag







    ### Social Reward 
    
    if X_reward[4, car_id]==1:
    
        # Speed
        v_target = params.v_target
        v_sum = 0

        for i in range(0, num_cars):
            if X_reward[4, i] == 1:
                v_sum = v_sum + X_reward[3, i]    

        v_avg = v_sum / params.num_AV
    
        Vavg_penalty = -1e-1
        R_Vavg = Vavg_penalty*abs(v_avg-v_target)
    
    
    
        #Headway
        num_AV_lane_1 = 0 
        num_AV_lane_2 = 0 
        num_AV_lane_3 = 0
    
        AV_x_lane_1 = np.empty(shape=[1, 0])
        AV_x_lane_2 = np.empty(shape=[1, 0])
        AV_x_lane_3 = np.empty(shape=[1, 0])
    
        for i in range(0, num_cars):
            if X_reward[4, i] == 1:
                if (X_reward[1, i] >= 0) and (X_reward[1, i] <= w_lane):
                    num_AV_lane_1 = num_AV_lane_1 + 1
                    #if X_reward[2,i]==0:
                    AV_x_lane_1 = np.append(AV_x_lane_1, X_reward[0, i])
                elif (X_reward[1, i] >= w_lane) and (X_reward[1, i] <= 2*w_lane):
                    num_AV_lane_2 = num_AV_lane_2 + 1
                    #if X_reward[2,i]==0:
                    AV_x_lane_2 = np.append(AV_x_lane_2, X_reward[0, i])              
                elif (X_reward[1, i] >= 2*w_lane) and (X_reward[1, i] <= 3*w_lane):
                    num_AV_lane_3 = num_AV_lane_3 + 1
                    #if X_reward[2,i]==0:
                    AV_x_lane_3 = np.append(AV_x_lane_3, X_reward[0, i])
          
    
    
        h_opt = l_car_safe
        R_s = 0
        Prop_headway_penalty = -1e-4
        Head_way_Penalty = -1e2
        Head_way_Penalty_tilt = -1e4*0
    
        if num_AV_lane_1 ==0:
            head_1 = 0
            R_s = R_s + 0
        elif num_AV_lane_1 ==1:
            head_1 = 0
            R_s = R_s + Head_way_Penalty
        else:
            head_1 = 0
            head_sum_opt_1 = (num_AV_lane_1 - 1)*h_opt # desired value
            if len(AV_x_lane_1)>=2:
                for j in range(0, num_AV_lane_1-1):
                    head_temp = AV_x_lane_1[j+1] - AV_x_lane_1[j] - l_car
                    head_1 = abs(head_temp) + head_1
#                if head_1 >= head_sum_opt_1:
                    R_s = R_s + abs(head_sum_opt_1 - head_1)*Prop_headway_penalty
#                else:
#                   R_s = R_s + -1e6    
            else:
                R_s = R_s + Head_way_Penalty_tilt


        if num_AV_lane_2 ==0:
            head_2 = 0
            R_s = R_s + 0
        elif num_AV_lane_2 ==1:
            head_2 = 0
            R_s = R_s + Head_way_Penalty
        else:
            head_2 = 0
            head_sum_opt_2 = (num_AV_lane_2-1)*h_opt
            if len(AV_x_lane_2)>=2:
                for j in range(0, num_AV_lane_2-1):
                    head_temp = AV_x_lane_2[j+1] - AV_x_lane_2[j]-l_car
                    head_2 = abs(head_temp) + head_2
#               if head_2 >= head_sum_opt_2:
                    R_s = R_s + abs(head_sum_opt_2 - head_2) * Prop_headway_penalty
#               else:
#                   R_s = R_s + -1e6
            else:
                R_s = R_s + Head_way_Penalty_tilt
    
        if num_AV_lane_3 == 0:
            head_3 = 0
            R_s = R_s + 0
        elif num_AV_lane_3 == 1:
            head_3 = 0
            R_s = R_s + Head_way_Penalty
        else:
            head_3 = 0
            head_sum_opt_3 = (num_AV_lane_3-1)*h_opt
            if len(AV_x_lane_3)>=2:
                for j in range(0, num_AV_lane_3-1):
                    head_temp = AV_x_lane_3[j+1]-AV_x_lane_3[j]-l_car
                    head_3 = abs(head_temp) + head_3   
#               if head_3 >= head_sum_opt_3:
                    R_s = R_s + abs(head_sum_opt_3 - head_3)*Prop_headway_penalty
#               else:
#                   R_s = R_s + -1e6
            else:
                R_s = R_s + Head_way_Penalty_tilt
     
        
        R_s = R_s + R_Vavg
    
    
    else:
        R_s = 0
    
    R = R_l +  R_s*0
    return R, params