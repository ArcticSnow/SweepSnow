# README.md

## Description
Package to operate the Scanse Sweep scanner, and a Maxbotix sonic ranger with python from a raspberrypi.

Written by S. Filhol, August 2017

## Usage

```bash
# perform 20 scans with Sweep
python sweep_collect.py -nbscans 20

# perform 30 measurement from the maxbotix
python maxbotix_collect.py -nbm 30

```

## Idea, TODOs

- TODO: problem with the database initialization function
- Add module to convert data from cylindrical to cartesian coordinate, add colum to table
- currently, the path to database is hardcoded, see how to pass it as an argument
- redesign code to avoid using the Pandas library
- ...

## Installation

This installation guide is not bug proof. USE AT YOUR OWN RISK!!!!!!!

Be careful with Path, and packages versions.

### 1. Install libsweep

  Documentation here: <https://github.com/scanse/sweep-sdk/blob/master/libsweep/README.md> 

```shell
git clone https://github.com/scanse/sweep-sdk.git
cd sweep-sdk
cd libsweep
sudo aptitude install cmake
cmake .
cmake --build .
sudo cmake --build . --target install
sudo ldconfig
```

### 2. Install MiniConda

```shell
wget http://repo.continuum.io/miniconda/Miniconda-3.5.5-Linux-armv6l.sh
md5sum Miniconda-3.5.5-Linux-armv6l.sh
/bin/bash Miniconda-3.5.5-Linux-armv6l.sh

sudo apt-get install python-pandas

# install lsusb if not available
sudo apt-get install usbutils
```

### 3. Install Sweepy

```shell
cd ..
cd ..
cd sweeppy

# if conda is installed, and return error: `GLIBCXX_3.4.21' not found
conda install libgcc
sudo python setup.py install --user

# sweeppy is installed on the system python /usr/bin/python
```

 IF:     *WARNING: the setup.py does not install the path to the entire system.*  

 Create a simulink to the sweeppy folder where the python is run: 

```shell
ln -s <path to sweeppy folder>


# Also make sure to give permission to the USB port with
sudo chmod 666 /dev/ttyUSB0

```

### 4. Python script example

<https://pythonpath.wordpress.com/2017/05/06/scanse-io-sweep-lidar-installation-on-gopigo2/> 

```python
from sweeppy import Sweep
    
with Sweep('/dev/ttyUSB0') as sweep:
	print(sweep.get_motor_speed())
	print(sweep.get_sample_rate())
	sweep.start_scanning()
    
	for scan in sweep.get_scans():
		print('{}\n'.format(scan))
```

### 5. Install Database

use sqlite3:

```shell
sqlite3 scanse.db


# within the sqlite shell:
sqlite> create table if not exists sweep_raw (id integer, angle integer, distance integer, signal_strength integer, timestamp integer, sample_rate integer, motor_speed integer)

```

### 6. Settings to include at Start up

```sh
#!/bin/sh -e
#
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.

# Print the IP address
_IP=$(hostname -I) || true
if [ "$_IP" ]; then
  printf "My IP address is %s\n" "$_IP"
fi

echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-1/new_device
sudo hwclock -s
date

exit 0

```

## Extra ressources for Raspberry Pi

 		==== RTC clock  ====

 <https://thepihut.com/blogs/raspberry-pi-tutorials/17209332-adding-a-real-time-clock-to-your-raspberry-pi>  

​		==== Mopi ====

 <https://pi.gate.ac.uk/pages/mopi.html> 

​		=== Scanse ===

 see [Instruction to install Sweeppy](file:///home/arcticsnow/github/Notes/WorkTODO/Electronic/Scanse_lidar_SWEEP/Instruction_to_install_Sweeppy.txt) 

 		==== Maxbotix ====

 <https://www.maxbotix.com/Raspberry-Pi-with-Ultrasonic-Sensors-144> 

​		=== Pi Power setting ===

 <https://www.jeffgeerling.com/blogs/jeff-geerling/raspberry-pi-zero-conserve-energy>
 <http://www.earth.org.uk/note-on-Raspberry-Pi-setup.html> 

