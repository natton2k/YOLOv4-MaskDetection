from datetime import datetime
import time,board,busio
import numpy as np
import adafruit_mlx90640
import matplotlib.pyplot as plt
from scipy import ndimage

cal_temp_col = 5
cal_temp_row = 5
cal_temp_width = 24
cal_temp_height = 32

i2c = busio.I2C(board.SCL, board.SDA, frequency=800000) # setup I2C
mlx = adafruit_mlx90640.MLX90640(i2c) # begin MLX90640 with I2C comm
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_16_HZ # set refresh rate
mlx_shape = (24,32) # mlx90640 shape

mlx_interp_val = 10 # interpolate # on each dimension
mlx_interp_shape = (mlx_shape[0]*mlx_interp_val,
                    mlx_shape[1]*mlx_interp_val) # new shape

fig = plt.figure(figsize=(5,7)) # start figure
ax = fig.add_subplot(111) # add subplot
fig.subplots_adjust(0.05,0.05,0.95,0.95) # get rid of unnecessary padding
fig = plt.figure(figsize=(8, 6))  # start figure
fig.canvas.set_window_title('Test')
fig.canvas.toolbar_visible = True
ax = fig.add_subplot(1, 2, 1)  # add subplot
#ax2 = fig.add_subplot(1, 2, 2)
fig.subplots_adjust(0.05, 0.05, 0.95, 0.95)  # get rid of unnecessary padding

therm1 = ax.imshow(np.zeros(mlx_interp_shape),interpolation='none',
                   cmap=plt.cm.bwr,vmin=25,vmax=45) # preemptive image
cbar = fig.colorbar(therm1) # setup colorbar
cbar.set_label('Temperature [$^{\circ}$C]',fontsize=14) # colorbar label

fig.canvas.draw() # draw figure to copy background
ax_background = fig.canvas.copy_from_bbox(ax.bbox) # copy background
fig.show() # show the figure before blitting

frame = np.zeros(mlx_shape[0] * mlx_shape[1]) # 768 pts
def plot_update(x,y,w,h):
    fig.canvas.restore_region(ax_background) # restore background
    mlx.getFrame(frame) # read mlx90640
    data_array = np.fliplr(np.reshape(frame,mlx_shape)) # reshape, flip data
    data_array = ndimage.zoom(data_array,mlx_interp_val) # interpolate
        # Vẽ ảnh nhiệt lên plot
    vmin = round(np.min(data_array), 2)
    vmax = round(np.max(data_array), 2)
    therm1.set_array(data_array)
    therm1.set_clim(vmin=vmin, vmax=vmax)
    ax.draw_artist(therm1)  # draw new thermal image
        # Tính nhiệt face
    #print(str(data_array[y:y+h,x:w+x]))
    vface_temp = round(np.max(data_array[y:y+h,x:w+x]), 2)
    if vface_temp < 38:
        print('Normal temperature: ' + str(vface_temp))
    else:
        print('High temperature: ' + str(vface_temp))
    fig.canvas.blit(ax.bbox)
    fig.canvas.flush_events()
    cbar.on_mappable_changed(therm1) # update colorbar range

    ax.draw_artist(therm1) # draw new thermal image
    fig.canvas.blit(ax.bbox) # draw background
    fig.canvas.flush_events() # show the new image
    return

t_array = []
while True:
  #  t1 = time.monotonic() # for determining frame rate
    try:
        plot_update(cal_temp_width, cal_temp_height, cal_temp_col, cal_temp_height) # update plot
    except:
        continue
    # approximating frame rate
   # t_array.append(time.monotonic()-t1)
    #if len(t_array)>10:
     #   t_array = t_array[1:] # recent times for frame rate approx
    #print('Frame Rate: {0:2.1f}fps'.format(len(t_array)/np.sum(t_array)))