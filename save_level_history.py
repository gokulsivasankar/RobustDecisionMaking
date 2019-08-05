import cv2
import os


def save_level_history(params, step):
    if params.sim_case == 0:
        out_fname = params.outdir + '/' + 'level_history_agg.mp4'
        plot_fname = params.outdir + '/' + 'level_ratio_history_agg'
    elif params.sim_case == 1:
        out_fname = params.outdir + '/' + 'level_history_adp.mp4'
        plot_fname = params.outdir + '/' + 'level_ratio_history_adp'
    else:
        out_fname = params.outdir + '/' + 'level_history_con.mp4'
        plot_fname = params.outdir + '/' + 'level_ratio_history_con'


    plot_format = params.plot_format
    img_array = []

    if os.path.exists(out_fname):
        os.remove(out_fname)

    for i in range(0, step):
        filename = plot_fname + str(i) + plot_format
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)

    out = cv2.VideoWriter(out_fname, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), params.fps, size)

    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()