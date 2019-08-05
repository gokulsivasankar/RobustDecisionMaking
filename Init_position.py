# -*- coding: utf-8 -*-
import numpy as np
import traff
from shapely.geometry import Polygon
import math

def Init_position(params,traffic,AV_cars):
    
    num_cars = params.num_cars
    num_lanes = params.num_lanes
    w_lane = params.w_lane
    init_x_range = params.init_x_range
    v_min = params.v_min
    v_max = params.v_max
    l_road = params.l_road
    
    Target_x = 400
    
    l_car = params.l_car
    w_car = params.w_car
    
    l_car_safe = 1.2*l_car     
    w_car_safe = 1.2*w_car
    
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

    # manual init positions
    x_init = 5
    headway = l_car
    for id in range(0, num_cars):
        if id ==0:
           lane = 1
           lane_center = w_lane*(lane-1) + (w_lane/2) # first lane
           x_car = x_init + 4*headway
           y_car = lane_center
           Final_y = lane_center
        elif id == 1: # AV
           lane = 2
           lane_center = w_lane*(lane-1) + (w_lane/2) # second lane
           x_car = 0 +x_init + 0.*l_car
#            x_car = 2*l_car
           y_car = lane_center
           Final_y = w_lane*(lane) + (w_lane/2) # third lane
        elif id == 2:
           lane = 2
           lane_center = w_lane*(lane-1) + (w_lane/2) # second lane
           x_car = x_init + 5*l_car
           y_car = lane_center
           Final_y = lane_center
        elif id == 3:
           lane = 3
           lane_center = w_lane*(lane-1) + (w_lane/2) # third lane
           x_car = x_init
           y_car = lane_center
           Final_y = lane_center
        elif id == 4:
            lane = 3
            lane_center = w_lane * (lane - 1) + (w_lane / 2)  # third lane
            x_car = x_init + 6*l_car
            y_car = lane_center
            Final_y = lane_center
        elif id == 5:
            lane = 1
            lane_center = w_lane * (lane - 1) + (w_lane / 2)  # third lane
            x_car = x_init
            y_car = lane_center
            Final_y = lane_center
        elif id == 6:
            lane = 2
            lane_center = w_lane * (lane - 1) + (w_lane / 2)  # third lane
            x_car = x_init - 2*l_car
            y_car = lane_center
            Final_y = lane_center



            
#         if id ==0:
#             lane = 2
#             lane_center = w_lane*(lane-1) + (w_lane/2) # second lane
#             x_car = x_init + 5*l_car
#             y_car = lane_center
#             Final_y = lane_center
#         elif id == 1: # AV
#             lane = 2
#             lane_center = w_lane*(lane-1) + (w_lane/2) # second lane
#             x_car = 0 +x_init + 0.5*l_car
# #            x_car = 2*l_car
#             y_car = lane_center
#             Final_y = w_lane*(lane) + (w_lane/2) # third lane
#         elif id == 2:
#             lane = 3
#             lane_center = w_lane*(lane-1) + (w_lane/2) # third lane
#             x_car = x_init
#             y_car = lane_center
#             Final_y = lane_center
            
        
        Final_x = Target_x
        orientation_car = 0
        Final_orientation = 0
        v_car = np.random.uniform(v_min, v_max)
        v_car = params.v_nominal



# # Random init positions
#     for id in range(0, num_cars):
#        AV_flag = 0
#        pos_flag = 0
#        while pos_flag == 0:
#            rand_lane = np.random.randint(1,num_lanes)
#            lane_center = (rand_lane-1)*w_lane + (w_lane/2)
#            Final_y = lane_center
#
#            rand_lane = np.random.randint(1,num_lanes)
#            lane_center = (rand_lane-1)*w_lane + (w_lane/2)
#            x_car = np.random.uniform(0, init_x_range)        # vehicles' initial x position
#            y_car = lane_center #np.random.uniform(lane_center-w_lane/4, lane_center+w_lane/4) # vehicles' initial y position
#            Final_x = params.l_road
#
#            orientation_car = 0 #math.radians(np.random.uniform(-10,10))              # Vehicles' initial heading angle (in the paper, yaw angle)
#            Final_orientation = 0              # Vehicles' final heading angle (in the paper, yaw angle)
#            v_car = np.random.uniform(v_min,v_max)     # vehicles' initial speed
#            if id > 0:
#                curr_rectangle = Polygon(
#                        [[x_car-l_car_safe/2*math.cos(orientation_car)+w_car_safe/2*math.sin(orientation_car), y_car-l_car_safe/2*math.sin(orientation_car)-w_car_safe/2*math.cos(orientation_car)],
#                          [x_car-l_car_safe/2*math.cos(orientation_car)-w_car_safe/2*math.sin(orientation_car), y_car-l_car_safe/2*math.sin(orientation_car)+w_car_safe/2*math.cos(orientation_car)],
#                          [x_car+l_car_safe/2*math.cos(orientation_car)-w_car_safe/2*math.sin(orientation_car), y_car+l_car_safe/2*math.sin(orientation_car)+w_car_safe/2*math.cos(orientation_car)],
#                          [x_car+l_car_safe/2*math.cos(orientation_car)+w_car_safe/2*math.sin(orientation_car), y_car+l_car_safe/2*math.sin(orientation_car)-w_car_safe/2*math.cos(orientation_car)]])
#
#                for id_prev in range(0, id):
#                    prev_rectangle = Polygon(
#                            [[initial_state[0,id_prev]-l_car_safe/2*math.cos(initial_state[2,id_prev])+w_car_safe/2*math.sin(initial_state[2,id_prev]),initial_state[1,id_prev]-l_car_safe/2*math.sin(initial_state[2,id_prev])-w_car_safe/2*math.cos(initial_state[2,id_prev])],
#                          [initial_state[0,id_prev]-l_car_safe/2*math.cos(initial_state[2,id_prev])-w_car_safe/2*math.sin(initial_state[2,id_prev]), initial_state[1,id_prev]-l_car_safe/2*math.sin(initial_state[2,id_prev])+w_car_safe/2*math.cos(initial_state[2,id_prev])],
#                          [initial_state[0,id_prev]+l_car_safe/2*math.cos(initial_state[2,id_prev])-w_car_safe/2*math.sin(initial_state[2,id_prev]), initial_state[1,id_prev]+l_car_safe/2*math.sin(initial_state[2,id_prev])+w_car_safe/2*math.cos(initial_state[2,id_prev])],
#                          [initial_state[0,id_prev]+l_car_safe/2*math.cos(initial_state[2,id_prev])+w_car_safe/2*math.sin(initial_state[2,id_prev]), initial_state[1,id_prev]+l_car_safe/2*math.sin(orientation_car)-w_car_safe/2*math.cos(orientation_car)]])
#
#                    if curr_rectangle.intersects(prev_rectangle) or curr_rectangle.intersects(Upper_RoadBound_rectangle) or curr_rectangle.intersects(Lower_RoadBound_rectangle) :
#                        break
#                    else:
#                        if id_prev == id-1:
#                            pos_flag = 1
#            else:
#                curr_rectangle = Polygon(
#                         [[x_car-l_car_safe/2*math.cos(orientation_car)+w_car_safe/2*math.sin(orientation_car),y_car-l_car_safe/2*math.sin(orientation_car)-w_car_safe/2*math.cos(orientation_car)],
#                          [x_car-l_car_safe/2*math.cos(orientation_car)-w_car_safe/2*math.sin(orientation_car), y_car-l_car_safe/2*math.sin(orientation_car)+w_car_safe/2*math.cos(orientation_car)],
#                          [x_car+l_car_safe/2*math.cos(orientation_car)-w_car_safe/2*math.sin(orientation_car), y_car+l_car_safe/2*math.sin(orientation_car)+w_car_safe/2*math.cos(orientation_car)],
#                          [x_car+l_car_safe/2*math.cos(orientation_car)+w_car_safe/2*math.sin(orientation_car), y_car+l_car_safe/2*math.sin(orientation_car)-w_car_safe/2*math.cos(orientation_car)]])
#
#                if curr_rectangle.intersects(Upper_RoadBound_rectangle) or curr_rectangle.intersects(Lower_RoadBound_rectangle) :
#                        break
#                else:
#                    pos_flag = 1



        for i in range(0, len(AV_cars)):
           if id == AV_cars[i]:
               AV_flag = 1
               break
           else:
               AV_flag = 0

        traffic = traff.update(traffic, x_car, y_car, orientation_car, v_car, AV_flag, Final_x, Final_y,
                              Final_orientation)
        initial_state = np.block([[traffic.x], [traffic.y], [traffic.orientation],
                                 [traffic.v_car], [traffic.AV_flag], [traffic.Final_x], [traffic.Final_y],
                                 [traffic.Final_orientation]])

        
        
        
    return traffic
        