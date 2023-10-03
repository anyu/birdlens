from gpiozero import Button, MotionSensor
from picamera import PiCamera
from time import sleep
from signal import pause

button = Button(2)
pir = MotionSensor(4)
camera = PiCamera()

camera.start_preview()

def take_photo():
  global image
  i = i + 1
  camera.capture('image_%s.jpg' % i)
  print("photo taken")
  sleep(10)

def stop_camera():
  camera.stop_preview()
  exit()

button.when_pressed = stop_camera

pir.when_motion = take_photo

pause()