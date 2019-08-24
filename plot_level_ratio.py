import matplotlib.pyplot as plt
import numpy as np


def plot_level_ratio(Level_ratio_history, ego_car_id, opp_car_id, params, step, episode, max_step, fig):

    plt.figure(fig.number)

    if params.sim_case == 0:
        plot_fname = 'level_ratio_history_agg'
    elif params.sim_case == 1:
        plot_fname = 'level_ratio_history_adp'
    else:
        plot_fname = 'level_ratio_history_con'

    num_cars = params.num_cars
    plot_format = params.plot_format

    plt.cla()
    ax = plt.gca()

    x_lim_min = 0
    x_lim_max = max_step * params.t_step_DT
    x_lim_max = 28 * params.t_step_DT   # 14 sec
    x_lim = np.array([x_lim_min, x_lim_max])

    plt.plot(np.arange(0, (step+1)*params.t_step_DT, params.t_step_DT),
             np.squeeze(Level_ratio_history[episode, 0:step+1, ego_car_id * (num_cars - 1) + opp_car_id - 1, 0]))

    ax.set_xlim(x_lim)
    ax.set_ylim([0, 1])
    plt.minorticks_on()


    # Customize the major grid
    plt.grid()
    # Customize the minor grid
    plt.grid(which='minor', linestyle=':', linewidth='0.15', color='black')

    plt.savefig(params.outdir+'/'+plot_fname+str(step)+plot_format, dpi=1200)
    plt.show(block=False)
    plt.pause(0.001)
    plt.clf()