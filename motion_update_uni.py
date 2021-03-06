import math
import numpy as np

def motion_update(X_old, car_id, action_id, t_step, params):

    # 0:maintian  1:turn left  2:turn right  3:accelerate  4:decelerate  5:hard brake 6: lane change (left) 7: lane change (right)
    
    X_new = X_old.copy()
#    fac = 2
    
    steer_angle = math.pi/8
    steer_angle_lane = math.pi/4
    max_dec = 5
    nom_acc = 2.5
    nom_dec = 2.5
    
#    if X_new[4,car_id] == 1:
#        steer_angle = fac*steer_angle
#        steer_angle_lane = fac*steer_angle_lane
#        #max_dec = 1/fac*max_dec
#        nom_acc = fac*nom_acc
#        #nom_dec = 1/fac*nom_dec
    
    if action_id == 0:
        X_new[3,car_id] = X_new[3,car_id]
        X_new[2,car_id] = X_new[2,car_id]
        X_new[0,car_id] = (X_new[0,car_id]+X_new[3,car_id]*math.cos(X_new[2,car_id])*t_step)
        X_new[1,car_id] = (X_new[1,car_id]+X_new[3,car_id]*math.sin(X_new[2,car_id])*t_step)

    elif action_id == 1:
        X_new[3,car_id] = X_new[3,car_id]
        X_new[2,car_id] = X_new[2,car_id]+steer_angle*t_step
        X_new[0,car_id] = (X_new[0,car_id]+X_new[3,car_id]*math.cos(X_new[2,car_id])*t_step)
        X_new[1,car_id] = (X_new[1,car_id]+X_new[3,car_id]*math.sin(X_new[2,car_id])*t_step)
            
    elif action_id == 2:
        X_new[3,car_id] = X_new[3,car_id]
        X_new[2,car_id] = X_new[2,car_id]-steer_angle*t_step
        X_new[0,car_id] = (X_new[0,car_id]+X_new[3,car_id]*math.cos(X_new[2,car_id])*t_step)
        X_new[1,car_id] = (X_new[1,car_id]+X_new[3,car_id]*math.sin(X_new[2,car_id])*t_step)

    elif action_id == 3:
        X_new[3,car_id] = X_new[3,car_id]+nom_acc*t_step
        if X_new[3,car_id]>params.v_max:
            X_new[3,car_id]=params.v_max
        X_new[2,car_id] = X_new[2, car_id]
        X_new[0,car_id] = (X_new[0, car_id]+X_new[3,car_id]*math.cos(X_new[2, car_id])*t_step)
        X_new[1,car_id] = (X_new[1, car_id]+X_new[3,car_id]*math.sin(X_new[2, car_id])*t_step)
    
    elif action_id == 4:
        X_new[3,car_id] = X_new[3, car_id]-nom_dec*t_step
        if X_new[3,car_id]<params.v_min:
            X_new[3,car_id]=params.v_min
        X_new[2, car_id] = X_new[2, car_id]
        X_new[0, car_id] = X_new[0, car_id]+X_new[3, car_id]*math.cos(X_new[2, car_id])*t_step
        X_new[1, car_id] = X_new[1, car_id]+X_new[3, car_id]*math.sin(X_new[2, car_id])*t_step
    
    elif action_id == 5:
        X_new[3, car_id] = X_new[3, car_id]-max_dec*t_step
        if X_new[3,car_id]<params.v_min:
            X_new[3,car_id] = params.v_min
        X_new[2,car_id] = X_new[2,car_id]
        X_new[0,car_id] = X_new[0,car_id]+X_new[3,car_id]*math.cos(X_new[2,car_id])*t_step
        X_new[1,car_id] = X_new[1,car_id]+X_new[3,car_id]*math.sin(X_new[2,car_id])*t_step
        
#    elif action_id == 6:
##        if X_new[4, car_id] != 1:
##            nom_acc = fac*nom_acc
#        X_new[3,car_id] = X_new[3,car_id]+nom_acc*t_step
#        if X_new[3,car_id]>params.v_max:
#            X_new[3,car_id]=params.v_max
#        X_new[2,car_id] = X_new[2,car_id]+steer_angle_lane*t_step
#        X_new[0,car_id] = X_new[0,car_id] + X_new[3,car_id]*math.cos(X_new[2,car_id])*t_step
#        X_new[1,car_id] = (X_new[1,car_id]+X_new[3,car_id]*math.sin(X_new[2,car_id])*t_step)
#    
#    elif action_id == 7:
##        if X_new[4,car_id] != 1:
##            nom_acc = fac*nom_acc
#        X_new[3,car_id] = X_new[3,car_id]+nom_acc*t_step
#        if X_new[3,car_id]>params.v_max:
#            X_new[3,car_id]=params.v_max
#        X_new[2,car_id] = X_new[2,car_id]-steer_angle_lane*t_step
#        X_new[0,car_id] = (X_new[0,car_id]+X_new[3,car_id]*math.cos(X_new[2,car_id])*t_step)
#        X_new[1,car_id] = (X_new[1,car_id]+X_new[3,car_id]*math.sin(X_new[2,car_id])*t_step)

    return X_new