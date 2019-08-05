import cv2
import os


def save_plot(params,step):   
    out_fname = params.outdir+'/'+params.outfile
    plot_fname = params.outdir+'/'+params.plot_fname
    plot_format = params.plot_format
    img_array = []

    
    if os.path.exists(out_fname):
        os.remove(out_fname)
    
    for i in range(0,step):
        filename = plot_fname+str(i)+plot_format
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)
 
 
    out = cv2.VideoWriter(out_fname,cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), params.fps, size)
 
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()