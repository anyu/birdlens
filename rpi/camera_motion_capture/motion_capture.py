from gpiozero import MotionSensor
from time import sleep
import datetime
import subprocess

print("Taking 3 seconds to warm up motion sensor...")
sleep(3)
print("Motion sensor should be warmed up!")

pir = MotionSensor(4)
camera_process = None

def take_photo():
  timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
  image_name = f'image_{timestamp}.jpg'
  camera_capture_cmd = f'libcamera-still -o {image_name}'
  camera_process = subprocess.Popen(camera_capture_cmd, shell=True)
  print(f"Photo taken: {image_name}")
  sleep(10)

def stop_camera():
  if camera_process is not None:
    camera_process.terminate()
    camera_process.wait()
    exit()

pir.when_motion = take_photo
pir.when_no_motion = stop_camera

try:
  while True:
    sleep(1)
except KeyboardInterrupt:
  exit()