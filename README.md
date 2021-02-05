# 4mics_mqtt
MQTT controlled LED-ring for the Respeaker with 4 microphone (circular LED)

PREREQUISITES:
- 4 Microphone Respeaker with LED Ring fully set up (test with github.com/respeaker/4mics_hat)
- pip install paho-mqtt

To start:
$ python /path/to/file/ledring.py

The file can be configured to subcribe and respond to any MQTT message. Right now it responds to:
ledring/wake
ledring/think
ledring/speak
ledring/error
ledring/off

This can be run as a system service.
