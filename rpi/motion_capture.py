from gpiozero import MotionSensor
# from picamera import PiCamera
from time import sleep
from signal import pause

print("Taking 3 seconds to warm up motion sensor...")
sleep(3)
print("Motion sensor should be warmed up!")

pir = MotionSensor(4)
while True:
  pir.wait_for_motion()
  print("Motion detected!")
  pir.wait_for_no_motion()
  print("No motion detected")

camera = PiCamera()
# camera.start_preview()

def take_photo():
  global image
  i = i + 1
  camera.capture('image_%s.jpg' % i)
  print("photo taken")
  sleep(10)

def stop_camera():
  camera.stop_preview()
  exit()

# pir.when_motion = take_photo

pause()