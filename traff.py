import numpy as np

def initial():
    class Bunch:
        def __init__(self, **kwds):
            self.__dict__.update(kwds)
    traffic = Bunch( 
        x = np.empty(shape=[1, 0]),     
        y = np.empty(shape=[1, 0]), 
        orientation = np.empty(shape=[1, 0]),
        v_car = np.empty(shape=[1, 0]), 
        AV_flag = np.empty(shape=[1, 0]),
        Final_x = np.empty(shape=[1, 0]),
        Final_y = np.empty(shape=[1, 0]),
        Final_orientation = np.empty(shape=[1, 0]),
        )
    return traffic

def update(traffic, x_car, y_car, orientation_car, v_car, AV_flag, Final_x, Final_y, Final_orientation):
    traffic.x = np.append(traffic.x, [[x_car]], axis=1 )
    traffic.y = np.append(traffic.y, [[y_car]], axis=1)
    traffic.orientation = np.append(traffic.orientation, [[orientation_car]], axis=1)
    traffic.v_car = np.append(traffic.v_car, [[v_car]], axis=1)
    traffic.AV_flag = np.append(traffic.AV_flag, [[AV_flag]], axis=1)
    traffic.Final_x = np.append(traffic.Final_x, [[Final_x]], axis=1)
    traffic.Final_y = np.append(traffic.Final_y, [[Final_y]], axis=1)
    traffic.Final_orientation = np.append(traffic.Final_orientation, [[Final_orientation]], axis=1)
    return traffic
