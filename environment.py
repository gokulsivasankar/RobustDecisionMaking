import motion_update
import reward

def environment(X_old, car_id, action_id, t_step, params, dist_id, Level_ratio):
    

    # the selected car moves based on the action
    # 1:maintian  2:turn left  3:turn right  4:accelerate  5:decelerate  6:hard # brake
    
    X_new = motion_update.motion_update(X_old, car_id, action_id, t_step,  params) 

    # compute reward
    R, params = reward.reward(X_new, car_id, action_id, params, dist_id, Level_ratio)   

    return X_new, R