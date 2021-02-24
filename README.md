# 4mics_mqtt
MQTT controlled LED-ring for the Respeaker with 4 microphone (circular LED)
Controllable via Node-RED / Home Assistant or any MQTT service.

### Installation/Prerequisites:
1. Make sure your 4mics_hat Respeaker is fully set up according to [this page](https://github.com/respeaker/4mics_hat)
1. Run the following commands:
```
sudo apt install python3-pip python-pip git-all
sudo pip install paho-mqtt spidev python-gpiozero numpy
cd /home/pi/
sudo git clone https://github.com/skisbit/4mics_mqtt/
sudo nano /home/pi/4mics_mqtt/config.py
```
1. Change variables in this file according to your Rhasspy and MQTT configuration
1. Run the script:
```
python /home/pi/4mics_mqtt/ledring.py
```

### MQTT Controls
Currently paired with Rhasspy to respond to MQTT messages from the rhasspy server. Flashes green when Rhasspy is ready.
The file can be configured to subcribe and respond to any MQTT message. Right now it responds to:
```
ledring/wake
ledring/think
ledring/speak
ledring/error
ledring/off
```

### Run as a system service
```
sudo nano "/etc/systemd/system/ledring.service"
```

```
[Unit]
Description=Led-Ring MQTT
After=network.target

[Service]
Type=simple
Restart=always
ExecStart=python /home/pi/4mics_mqtt/ledring.py

[Install]
WantedBy=multi-user.target
```
