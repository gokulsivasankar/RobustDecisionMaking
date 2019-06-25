import math
import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt
from scipy import ndimage


def plot_sim(X_old, params, step):   
   
    w_lane = params.w_lane
    l_car = params.l_car 
    w_car = params.w_car
    num_lanes = params.num_lanes
    l_road = params.l_road
    plot_format = params.plot_format
    car_rect_lw = 1.5
    x_lim_min = min(X_old[0, :]) - 3 * l_car
    x_lim_max = max(X_old[0, :]) + 3 * l_car
    x_lim = np.array([x_lim_min, x_lim_max])


    color = ['b','r','m','g']
    plt.cla()
    ax = plt.gca()

    img_blue = plt.imread('blue_car.jpg')
    img_red = plt.imread('red_car.jpg')


        
    # Road bound
    Upper_RoadBound_rectangle = np.array(
        [[-3*l_car, w_lane*num_lanes],
         [-3*l_car, w_lane*num_lanes*1.5],
         [l_road, w_lane*num_lanes*1.5],
         [l_road, w_lane*num_lanes]])
                
    Lower_RoadBound_rectangle = np.array(
        [[-3*l_car, 0],
         [-3*l_car, -w_lane*num_lanes/2],
         [l_road, -w_lane*num_lanes/2],
         [l_road, 0]])
    
    plt.fill(np.squeeze(Upper_RoadBound_rectangle[:,0]),np.squeeze(Upper_RoadBound_rectangle[:,1]),color='forestgreen', LineWidth = 2)
    plt.fill(np.squeeze(Lower_RoadBound_rectangle[:,0]),np.squeeze(Lower_RoadBound_rectangle[:,1]),color='forestgreen', LineWidth = 2)
    fig = plt.gcf()
    
    # Road bound lines
    Lanes = np.array([
        [-3*l_car, 0],
        [l_road, 0],
        [-3*l_car, w_lane*num_lanes],
        [l_road, w_lane*num_lanes]])
    
    plt.plot(np.squeeze(Lanes[0:2,0]),np.squeeze(Lanes[0:2,1]),color=(0,0,0),LineWidth = 3, linestyle='-')
    plt.plot(np.squeeze(Lanes[2:4,0]),np.squeeze(Lanes[2:4,1]),color=(0,0,0),LineWidth = 3, linestyle='-')
    
    # Lanes
    Lanes = np.array([
        [-3*l_car, w_lane],
        [l_road, w_lane],
        [-3*l_car, w_lane*2],
        [l_road, w_lane*2]])

    if step % 2 == 0:
        plt.plot(x_lim, np.squeeze(Lanes[0:2,1]),color=(0,0,0),LineWidth = 3, linestyle='--')
        plt.plot(x_lim, np.squeeze(Lanes[2:4,1]),color=(0,0,0),LineWidth = 3, linestyle='--')

    else:
        plt.plot(x_lim+np.array([-l_car*2,l_car*2]), np.squeeze(Lanes[0:2, 1]), color=(0, 0, 0), LineWidth=3, linestyle='--')
        plt.plot(x_lim+np.array([-l_car*2,l_car*2]), np.squeeze(Lanes[2:4, 1]), color=(0, 0, 0), LineWidth=3, linestyle='--')


    
       
    for id in range(0,len(X_old[0,:])):
        rect = np.array(
            [[X_old[0, id] - l_car / 2 * math.cos(X_old[2, id]) - w_car / 2 * math.sin(X_old[2, id]),
              X_old[1, id] - l_car / 2 * math.sin(X_old[2, id]) + w_car / 2 * math.cos(X_old[2, id])],
             [X_old[0, id] - l_car / 2 * math.cos(X_old[2, id]) + w_car / 2 * math.sin(X_old[2, id]),
              X_old[1, id] - l_car / 2 * math.sin(X_old[2, id]) - w_car / 2 * math.cos(X_old[2, id])],
             [X_old[0, id] + l_car / 2 * math.cos(X_old[2, id]) - w_car / 2 * math.sin(X_old[2, id]),
              X_old[1, id] + l_car / 2 * math.sin(X_old[2, id]) + w_car / 2 * math.cos(X_old[2, id])],
             [X_old[0, id] + l_car / 2 * math.cos(X_old[2, id]) + w_car / 2 * math.sin(X_old[2, id]),
              X_old[1, id] + l_car / 2 * math.sin(X_old[2, id]) - w_car / 2 * math.cos(X_old[2, id])],
             [X_old[0, id] + (l_car / 2 - 1) * math.cos(X_old[2, id]) - w_car / 2 * math.sin(X_old[2, id]),
              X_old[1, id] + (l_car / 2 - 1) * math.sin(X_old[2, id]) + w_car / 2 * math.cos(X_old[2, id])],
             [X_old[0, id] + (l_car / 2 - 1) * math.cos(X_old[2, id]) + w_car / 2 * math.sin(X_old[2, id]),
              X_old[1, id] + (l_car / 2 - 1) * math.sin(X_old[2, id]) - w_car / 2 * math.cos(X_old[2, id])]])

        l_car_safe = 1 * l_car
        w_car_safe = 1 * w_car

        coll_rect = np.array(
            [[X_old[0, id] - l_car_safe / 2 * math.cos(X_old[2, id]) + w_car_safe / 2 * math.sin(X_old[2, id]),
              X_old[1, id] - l_car_safe / 2 * math.sin(X_old[2, id]) - w_car_safe / 2 * math.cos(X_old[2, id])],
             [X_old[0, id] - l_car_safe / 2 * math.cos(X_old[2, id]) - w_car_safe / 2 * math.sin(X_old[2, id]),
              X_old[1, id] - l_car_safe / 2 * math.sin(X_old[2, id]) + w_car_safe / 2 * math.cos(X_old[2, id])],
             [X_old[0, id] + l_car_safe / 2 * math.cos(X_old[2, id]) - w_car_safe / 2 * math.sin(X_old[2, id]),
              X_old[1, id] + l_car_safe / 2 * math.sin(X_old[2, id]) + w_car_safe / 2 * math.cos(X_old[2, id])],
             [X_old[0, id] + l_car_safe / 2 * math.cos(X_old[2, id]) + w_car_safe / 2 * math.sin(X_old[2, id]),
              X_old[1, id] + l_car_safe / 2 * math.sin(X_old[2, id]) - w_car_safe / 2 * math.cos(X_old[2, id])]])

        l_car_safe_front = 1.1 * l_car
        l_car_safe_back = 1.1 * l_car
        w_car_safe = 1.1 * w_car


        safe_rect = np.array(
                [[X_old[0,id]-l_car_safe_back/2*math.cos(X_old[2,id])+w_car_safe/2*math.sin(X_old[2,id]),
                  X_old[1,id]-l_car_safe_back/2*math.sin(X_old[2,id])-w_car_safe/2*math.cos(X_old[2,id])],
                [X_old[0,id]-l_car_safe_back/2*math.cos(X_old[2,id])-w_car_safe/2*math.sin(X_old[2,id]),
                 X_old[1,id]-l_car_safe_back/2*math.sin(X_old[2,id])+w_car_safe/2*math.cos(X_old[2,id])],
                [X_old[0,id]+l_car_safe_front/2*math.cos(X_old[2,id])-w_car_safe/2*math.sin(X_old[2,id]),
                 X_old[1,id]+l_car_safe_front/2*math.sin(X_old[2,id])+w_car_safe/2*math.cos(X_old[2,id])],
                [X_old[0,id]+l_car_safe_front/2*math.cos(X_old[2,id])+w_car_safe/2*math.sin(X_old[2,id]),
                 X_old[1,id]+l_car_safe_front/2*math.sin(X_old[2,id])-w_car_safe/2*math.cos(X_old[2,id])]])

        # Create an inset axes to plot the car images
        newax = ax.inset_axes([X_old[0,id], X_old[1,id]-3, 6, 6], transform=ax.transData)

        if X_old[4,id]==1:
            color_id = 0
            img_rot = ndimage.rotate(img_blue, (X_old[2,id]) * 180 / math.pi, reshape=False, cval=255)

        else:
            color_id = 1
            img_rot = ndimage.rotate(img_red, (X_old[2, id]) * 180 / math.pi, reshape=False, cval=255)

        newax.imshow(img_rot)
        newax.axis('off')

        # # Vehicle rectangle
        # plt.plot(np.squeeze(rect[0:2, 0]), np.squeeze(rect[0:2, 1]), color=color[color_id], LineWidth=car_rect_lw,
        #          linestyle='-')
        # plt.plot([rect[0, 0], rect[2, 0]], [rect[0, 1], rect[2, 1]], color=color[color_id], LineWidth=car_rect_lw,
        #          linestyle='-')
        # plt.plot([rect[2, 0], rect[3, 0]], [rect[2, 1], rect[3, 1]], color=color[color_id], LineWidth=car_rect_lw,
        #          linestyle='-')
        # plt.plot([rect[1, 0], rect[3, 0]], [rect[1, 1], rect[3, 1]], color=color[color_id], LineWidth=car_rect_lw,
        #          linestyle='-')
        # plt.plot([rect[4, 0], rect[5, 0]], [rect[4, 1], rect[5, 1]], color=color[color_id], LineWidth=car_rect_lw,
        #          linestyle='-')

        # # Coll rectangle
        #
        # plt.plot([coll_rect[0, 0], coll_rect[1, 0]], [coll_rect[0, 1], coll_rect[1, 1]], color=color[color_id], LineWidth=car_rect_lw+1,
        #          linestyle='-')
        # plt.plot([coll_rect[1, 0], coll_rect[2, 0]], [coll_rect[1, 1], coll_rect[2, 1]], color=color[color_id], LineWidth=car_rect_lw+1,
        #          linestyle='-')
        # plt.plot([coll_rect[2, 0], coll_rect[3, 0]], [coll_rect[2, 1], coll_rect[3, 1]], color=color[color_id], LineWidth=car_rect_lw+1,
        #          linestyle='-')
        # plt.plot([coll_rect[0, 0], coll_rect[3, 0]], [coll_rect[0, 1], coll_rect[3, 1]], color=color[color_id], LineWidth=car_rect_lw+1,
        #          linestyle='-')
        #
        #
        # # Safe rectangle
        #
        # plt.plot([safe_rect[0, 0], safe_rect[1, 0]], [safe_rect[0, 1], safe_rect[1, 1]], color=color[color_id], LineWidth=car_rect_lw+1,
        #          linestyle='-')
        # plt.plot([safe_rect[1, 0], safe_rect[2, 0]], [safe_rect[1, 1], safe_rect[2, 1]], color=color[color_id], LineWidth=car_rect_lw+1,
        #          linestyle='-')
        # plt.plot([safe_rect[2, 0], safe_rect[3, 0]], [safe_rect[2, 1], safe_rect[3, 1]], color=color[color_id], LineWidth=car_rect_lw+1,
        #          linestyle='-')
        # plt.plot([safe_rect[0, 0], safe_rect[3, 0]], [safe_rect[0, 1], safe_rect[3, 1]], color=color[color_id], LineWidth=car_rect_lw+1,
        #          linestyle='-')



    
    
    #fig = plt.figure()    

    ax.set_xlim(x_lim)
    ax.set_ylim([min(Lower_RoadBound_rectangle[:,1]), max(Upper_RoadBound_rectangle[:,1])])
    
    # Display Car_id
    for id in range(0, len(X_old[0,:])):
        ax.annotate(str(id+1), xy=(X_old[0, id], X_old[1, id]-0.5))
    
    # Used to return the plot as an image array
       # ax.set_ylim([-6*w_lane, 6*w_lane])
        
        #ax.annotate('v='+str(X_old[3,0])+'m/s', xy=(5, -10))    
        #ax.annotate('v='+str(X_old[3,1])+'m/s', xy=(5, 10))


        
    plt.yticks([])
    plt.xlabel('x (m)')
    plt.savefig(params.outdir+'/'+params.plot_fname+str(step)+plot_format, dpi=1200)
    plt.show(block=False)
    plt.pause(0.001)
    plt.clf()
