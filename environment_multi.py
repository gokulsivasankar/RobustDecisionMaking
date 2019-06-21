# -*- coding: utf-8 -*-
import numpy as np
import motion_update

def environment_multi(X_old, action_id, t_step, params):
    
    X_new = X_old.copy()
    
    # the selected car moves based on the action
    # 1:maintian  2:turn left  3:turn right  4:accelerate  5:decelerate  6:hard brake
    
    X_sub = np.zeros((len(action_id[0]), X_new.shape[0], X_new.shape[1]))
    for step in range(0, len(action_id[0])):
        size_action_cell = len(action_id)
        for car_id in range(0, size_action_cell):
            X_new = motion_update.motion_update(X_new, car_id, action_id[car_id][step], t_step, params)
        
        X_sub[step,:,:]=X_new.copy()     
       
    
    return X_sub