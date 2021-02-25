# Setup
import apa102, time, threading, sys, json
try:
    import queue as Queue
except ImportError:
    import Queue as Queue

from config import wakeword,mqtt_username,mqtt_password,mqtt_server,mqtt_port,rhasspy_siteid
from gpiozero import LED
from alexa_led_pattern import AlexaLedPattern
from threading import Thread


# Respeaker GPIO Data
class Pixels:
    PIXELS_N = 12

    def __init__(self, pattern=AlexaLedPattern):
        self.pattern = pattern(show=self.show)

        self.dev = apa102.APA102(num_led=self.PIXELS_N)
        
        self.power = LED(5)
        self.power.on()

        self.queue = Queue.Queue()
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()

        self.last_direction = None

    def wakeup(self, direction=0):
        self.last_direction = direction
        def f():
            self.pattern.wakeup(direction)

        self.put(f)

    def listen(self):
        if self.last_direction:
            def f():
                self.pattern.wakeup(self.last_direction)
            self.put(f)
        else:
            self.put(self.pattern.listen)

    def think(self):
        self.put(self.pattern.think)

    def speak(self):
        self.put(self.pattern.speak)
    
    def error(self):
        self.put(self.pattern.error)

    def bootup(self):
        self.put(self.pattern.bootup)

    def off(self):
        self.put(self.pattern.off)

    def put(self, func):
        self.pattern.stop = True
        self.queue.put(func)

    def _run(self):
        while True:
            func = self.queue.get()
            self.pattern.stop = False
            func()

    def show(self, data):
        for i in range(self.PIXELS_N):
            self.dev.set_pixel(i, int(data[4*i + 1]), int(data[4*i + 2]), int(data[4*i + 3]))

        self.dev.show()


pixels = Pixels()


# Loop Code:
if __name__ == '__main__':
    print '### Respeaker LED Ring Controller Script ###'
    try:
        while True:
            import paho.mqtt.client as mqtt


            def on_connect(client,userdata,flags,rc):
                print("Connected to MQTT Server (Code:"+str(rc)+")")
                
                #Subscribe to manual MQTT Controls
                client.subscribe("ledring/wake")
                client.subscribe("ledring/think")
                client.subscribe("ledring/speak")
                client.subscribe("ledring/off")
                client.subscribe("ledring/error")

                #Subscribe to automatic MQTT Controls
                client.subscribe("hermes/asr/startListening")
                client.subscribe("hermes/audioServer/"+rhasspy_siteid+"/audioFrame")
                client.subscribe("rhasspy/asr/"+rhasspy_siteid+"/"+rhasspy_siteid+"/audioCaptured")

                #Subscribe to your wakeword
                client.subscribe("hermes/hotword/"+wakeword+"/detected")
                
            def on_message(client,userdata,msg):
                #print(msg.topic+" "+str(msg.payload)) #Debug
                #sys.stdout.flush()
                
                # Manual Led Ring Activation
                if msg.topic == "ledring/wake":
                    pixels.wakeup()
                if msg.topic == "ledring/think":
                    pixels.think()
                if msg.topic == 'ledring/speak':
                    pixels.speak()
                if msg.topic == 'ledring/error':
                    pixels.error()
                if msg.topic == 'ledring/off':
                    pixels.off()
                    
                # Rhasspy Automatic Led Ring Activation
                if msg.topic == "hermes/asr/startListening":
                    pixels.wakeup()
                if msg.topic == "hermes/hotword/"+wakeword+"/detected":
                    if json.loads(msg.payload)["siteId"] == rhasspy_siteid:
                        pixels.wakeup()
                if msg.topic == "rhasspy/asr/"+rhasspy_siteid+"/"+rhasspy_siteid+"/audioCaptured":
                    pixels.think()
                #Run once if rhasspy emits any message on this topic, then unsub
                if msg.topic == "hermes/audioServer/"+rhasspy_siteid+"/audioFrame":
                   if (client.unsubscribe("hermes/audioServer/"+rhasspy_siteid+"/audioFrame")):
                        pixels.bootup()

            def on_subscribe(client,userdata,result,mid):
                   print("Subscribed to MQTT - "+result)


            client = mqtt.Client()
            client.username_pw_set(mqtt_username,mqtt_password)
            client.on_connect = on_connect
            client.on_message = on_message
            client.connect(mqtt_server,mqtt_port,60)
            client.on_subscribe = on_subscribe

            client.loop_forever()            
            
            
            

    except KeyboardInterrupt:
        print '\nProgram halted.'
        sys.exit(0)
    pixels.off()
