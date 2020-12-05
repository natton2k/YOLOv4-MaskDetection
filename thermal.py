from datetime import datetime
import sqlite3
import time
import board
import busio
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

i2c = busio.I2C(board.SCL, board.SDA,
                frequency=MLX90640_BUS_FREQUENCY)  # setup I2C
mlx = adafruit_mlx90640.MLX90640(i2c)  # begin MLX90640 with I2C comm
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_16_HZ  # set refresh rate
mlx_shape = (MLX90640_WIDTH, MLX90640_HEIGHT)  # mlx90640 shape

mlx_interp_val = MLX90640_INTERPOLATE_VALUE  # interpolate # on each dimension
mlx_interp_shape = (mlx_shape[0] * mlx_interp_val,
                    mlx_shape[1] * mlx_interp_val)  # new shape

# We got number 768 pts because of 24 * 32
frame = np.zeros(mlx_shape[0] * mlx_shape[1])  # 768 pts

# Getting connection from database
conn = sqlite3.connect(DATABASE_LOCATION)
if conn is None:
    print("Connecting to database failed. Please check the code")
    exit(0)


class Rect(object):

    def __init__(self) -> None:
        super().__init__()
        self.__x = 0.0
        self.__y = 0.0
        self.__w = 0.0
        self.__h = 0.0

    def setX(x: float, self) -> None:
        self.__x = x

    def setY(y: float, self) -> None:
        self.__y = y

    def setW(w: float, self) -> None:
        self.__w = w

    def setH(h: float, self) -> None:
        self.__h = h

    def getX(self) -> float:
        return self.__x

    def getY(self) -> float:
        return self.__y

    def getW(self) -> float:
        return self.__w

    def getH(self) -> float:
        return self.__h

    def __str__(self) -> str:
        return "Rect: {" + "x: " + str(self.__x) + ", y: " + str(self.__y) + ", w: " + str(self.__w) + ", h: " + str(self.__h) + " }"


def calculate_temp(x, y, w, h, frame, args: tuple):
    # Tinh max toan bo
    # Tinh average toan bo
    # Dua vo toa do cua hinh chu nhat gom (x,y,w,h)
    # Tinh max trong hinh chu nhat do va tinh average trong hinh chu nhat

    data_array = np.fliplr(np.reshape(frame, mlx_shape))  # reshape, flip data
    data_array = ndimage.zoom(data_array, mlx_interp_val)  # interpolate
    temp = 0.0
    if args is None:
        raise Exception("Please pass the required argument (tuple).")
    else:
        data_array_input = None
        if len(args) == 3:
            if args[0] == "rect" and isinstance(args[2], Rect) is True:
                data_array_input = data_array[args[2].getY():args[2].getH(), args[2].getX():args[2].getW()]
        elif len(args) == 2:
            if args[0] == "all":
                data_array_input = data_array[y:y+h, x:w+x]
        else:
            raise Exception("Only accept a tuple with 2 or 3 parameters. Try again.")
        if data_array_input is not None:
            if args[1] == "max":
                temp = round(np.max(data_array_input), ROUNDING_NUMBER)
            elif args[1] == "average":
                temp = round(np.average(data_array_input), ROUNDING_NUMBER)
            elif args[1] == "median":
                temp = round(np.median(data_array_input), ROUNDING_NUMBER)
            elif args[1] == "min":
                temp = round(np.min(data_array_input), ROUNDING_NUMBER)
            else:
                raise Exception("The second param in the tuple is not correct. Must be 'max' or 'average' or 'median' or 'min'")
        else:
            raise Exception("The passing argument(s) is/are not correct. Please correct the arguments and try again.")
    return temp

#

# Neu param truyen vao la: ("all", "average")
# -> Thi dung 24x32 co san tinh average temp
# ? Neu param truyen vao la: ("rect", "average", "*class Rect*")
# -> Tinh avg temp cua box do
#

def catch_temp():
    mlx.getFrame(frame)  # read mlx90640
    try:
        temp = calculate_temp(WIDTH_SIZE_CALCULATING, HEIGHT_SIZE_CALCULATING,
                              NUM_OF_COLUMNS_CALCULATING, NUM_OF_ROWS_CALCULATING, frame, ('all','average'))  # update plot
        unix_time = int(time.mktime(datetime.now().timetuple()))
        values = (temp, unix_time)
        if temp < 38:
            print(values)
            # print('Normal temperature: ' + str(temp))
        else:
            print(values)
            # print('High temperature: ' + str(temp))
    except Exception as e:
        print(e)

if __name__ == "__main__":
# Main program
    while True:
        catch_temp()

