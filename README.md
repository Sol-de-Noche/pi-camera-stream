# Make you own Raspberry Pi Camera Stream

Create your own live stream from a Raspberry Pi using any camera attached to it. Build your own applications from here.

## How it works

The Pi streams the output of the camera module over the web. Devices connected to the same network would be able to access the camera stream via

```
<raspberry_pi_ip:8023>
```

## Screenshots

| ![Setup](readme/pi-stream-client.jpg) | ![Live Pi Camera Stream](readme/pi-stream-screen-capture.jpg) |
| ------------------------------------- | ------------------------------------------------------------- |
| Pi Setup                              | Pi - Live Stream                                              |

## Preconditions

- Raspberry Pi 4, 2GB is recommended for optimal performance. However you can use a Pi 3 or older, you may see a increase in latency.
- Python 3 recommended.

## Library dependencies

Install the following dependencies to create camera stream.

```
sudo apt-get update
sudo apt-get upgrade

sudo apt-get install libatlas-base-dev
sudo apt-get install libjasper-dev
sudo apt-get install libqtgui4
sudo apt-get install libqt4-test
sudo apt-get install libhdf5-dev
sudo apt-get install ffmpeg
```

## Step 1 – Cloning Raspberry Pi Camera Stream

In your Raspberry PI, Open up terminal and clone the Camera Stream repo:

```
cd /home/pi
git clone https://github.com/Sol-de-Noche/pi-camera-stream.git
```

## Step 2 - Setup dependencies

To install the python dependencies, please first setup [Poetry](https://python-poetry.org/) and then

```
poetry install
```

To install JavaScript dependencies use [Yarn](https://yarnpkg.com/)

```
yarn
```

## Step 2 – Configure it

Copy `.env.example` to `.env` and change the configuration options as it fits better for your case.

## Step 3 – Launch Web Stream

Note: Creating an Autostart of the main.py script is recommended to keep the stream running on bootup.

```bash
./build.sh
./run.sh
```

## Step 4 – Autostart your Pi Stream

Optional: A good idea is to make the the camera stream auto start at bootup of your pi. You will now not need to re-run the script every time you want to create the stream. You can do this by going editing the /etc/profile to:

```
sudo nano /etc/profile
```

Go the end of the and add the following (from above):

```
sudo python3 /home/pi/pi-camera-stream/run.sh
```

This would cause the following terminal command to auto-start each time the Raspberry Pi boots up. This in effect creates a headless setup - which would be accessed via SSH.
Note: make sure SSH is enabled.

## Step 5 - Setup Video Generation

Add the following line to your crontab configuration:

```bash
0 * * * * /home/pi/pi-camera-stream/gen_videos.sh
```

## Extra configurations

- Create a image of your current installation

```
sudo dd bs=4M if=/dev/<Device NAme> of=/home/username/MyImage.img
```

- To enable automatic connection to your local network place a file called `wpa_supplicant.conf` in the root partition with the following content (change the configuration for your local settings)

```
country=<Insert 2 letter ISO 3166-1 country code here>
update_config=1

network={
 ssid="<Name of your wireless LAN>"
 psk="<Password for your wireless LAN>"
}
```

- To enable `ssh` to your RaspberryPi create a empty file called `ssh` in the root partition
