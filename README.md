<br />
<p align="center">
  <h3 align="center">Yolov4 for mask detection</h3>

  <p align="center">
    Yolov4 mask detection using Darknet and OpenCV
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)



<!-- ABOUT THE PROJECT -->
## About The Project

Mask detection


<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.

*python 3.x:

https://www.python.org/downloads/

*numpy
```sh
pip install numpy
```
*openCV 

For Window: https://pypi.org/project/opencv-python/
```sh
pip install opencv-python
```
For Raspberry 4, for the love of god please follow this link: https://qengineering.eu/install-opencv-4.4-on-raspberry-pi-4.html

### Installation

Clone the repo
```sh
git clone https://github.com/TienTruong98/Hackathon
```

---------
### Setting up the libraries for the Melexis MLX90640

```
Check if the MLX90640 sensor is working correctly (see if the number 33 appear):
  sudo i2cdetect -y 1
```


1. Install the visualization library in Python 3

```sh
sudo pip3 install matplotlib scipy numpy
```


2. Install the I2C tools:
```sh
sudo apt-get install -y python-smbus
sudo apt-get install -y i2c-tools
```


3. Install the Adafruit MLX90640 library:
```sh
sudo pip3 install RPI.GPIO adafruit-blinka
sudo pip3 install adafruit-circuitpython-mlx90640
```

### Run the thermal camera script:

```sh
python3 thermal.py
```

<!-- USAGE EXAMPLES -->
## Usage

To begin using this, you need to have 3 config files in the yolo-custom directory.

* .names file
* .cfg file
* .weights file

We already have 6 files for 2 categories: face detection and mask detection. 
But feel free to customize your config.

After that, you need to make sure that you have the correct file path at line 5, 6, 7 in detect.py

Ex:
```sh
labels_path = "yolo-custom\\face.names"
weights_path = "yolo-custom\yolov4-tiny-custom-face-detection.weights"
config_path = "yolo-custom\yolov4-tiny-custom-face-detection.cfg"
```
After that, you just need to run the run.py file in the command line to begin detect things.
```sh
python run.py
```

<!-- CONTACT -->
## Contact

Truong Tran Tien - tienttse1998@gmail.com
Ngo Nguyen Bang - bangmapleproject@gmail.com



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* https://www.pyimagesearch.com/2018/11/12/yolo-object-detection-with-opencv/
