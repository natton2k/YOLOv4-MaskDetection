from datetime import datetime
import sqlite3
import time,board,busio
import numpy as np
import adafruit_mlx90640
import matplotlib.pyplot as plt
from scipy import ndimage

#################################
# Configuration

# DATABASE
DATABASE_LOCATION = "thermal.db"

# DATABSE QUERY
INSERT_QUERY = "INSERT INTO ThermalData VALUES(?,?)"

# MLX90640
MLX90640_BUS_FREQUENCY = 800000
MLX90640_WIDTH = 24
MLX90640_HEIGHT = 32
MLX90640_INTERPOLATE_VALUE = 10

# PRE-DEFINE CONST VALUE
NUM_OF_COLUMNS_CALCULATING = 50
NUM_OF_ROWS_CALCULATING = 50
WIDTH_SIZE_CALCULATING = 24
HEIGHT_SIZE_CALCULATING = 32
ROUNDING_NUMBER = 5
#################################

i2c = busio.I2C(board.SCL, board.SDA, frequency=MLX90640_BUS_FREQUENCY) # setup I2C
mlx = adafruit_mlx90640.MLX90640(i2c) # begin MLX90640 with I2C comm
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_16_HZ # set refresh rate
mlx_shape = (MLX90640_WIDTH, MLX90640_HEIGHT) # mlx90640 shape

mlx_interp_val = MLX90640_INTERPOLATE_VALUE # interpolate # on each dimension
mlx_interp_shape = (mlx_shape[0] * mlx_interp_val, mlx_shape[1] * mlx_interp_val) # new shape

# We got number 768 pts because of 24 * 32
frame = np.zeros(mlx_shape[0] * mlx_shape[1]) # 768 pts

# Getting connection from database
conn = sqlite3.connect(DATABASE_LOCATION)
if conn is None:
    print("Connecting to database failed. Please check the code")
    exit(0)


def calculate_temp(x,y,w,h, frame):
    # Tinh max toan bo
    # Tinh average toan bo
    # Dua vo toa do cua hinh chu nhat gom (x,y,w,h)
    # Tinh max trong hinh chu nhat do va tinh average trong hinh chu nhat
    data_array = np.fliplr(np.reshape(frame,mlx_shape)) # reshape, flip data
    data_array = ndimage.zoom(data_array,mlx_interp_val) # interpolate
    return round(np.max(data_array[y:y+h, x:w+x]), ROUNDING_NUMBER)

#

#Neu param truyen vao la: ("all", "average")
# -> Thi dung 24x32 co san tinh average temp
# ? Neu param truyen vao la: ("rect", "average", "*class Rect*")
# -> Tinh avg temp cua box do
#

# Main program
while True:
    mlx.getFrame(frame) # read mlx90640
    try:
        temp = calculate_temp(WIDTH_SIZE_CALCULATING, HEIGHT_SIZE_CALCULATING,
                              NUM_OF_COLUMNS_CALCULATING, NUM_OF_ROWS_CALCULATING, frame) # update plot
        unix_time = int(time.mktime(datetime.now().timetuple()))
        values = (temp,unix_time)
        if temp < 38:
            print(values)
            #print('Normal temperature: ' + str(temp))
        else:
            print(values)
            #print('High temperature: ' + str(temp))
    except:
        continue