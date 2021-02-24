# 4mics_mqtt
MQTT controlled LED-ring for the Respeaker with 4 microphone (circular LED)
Controllable via Node-RED / Home Assistant or any MQTT service.

## PREREQUISITES:
* 4 Microphone Respeaker with LED Ring fully set up (test with github.com/respeaker/4mics_hat)
* sudo apt install python3-pip python-pip
* pip install paho-mqtt spidev python-gpiozero numpy

To start:

```
$ python /path/to/file/ledring.py
```

Currently paired with Rhasspy to respond to MQTT messages from the rhasspy server. Flashes green when Rhasspy is ready.

The file can be configured to subcribe and respond to any MQTT message. Right now it responds to:
```
ledring/wake
ledring/think
ledring/speak
ledring/error
ledring/off
```
This can be run as a system service in linux.

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
ExecStart=python /path/to/file/ledring.py

[Install]
WantedBy=multi-user.target
```
