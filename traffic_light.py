import time
from grove.gpio import GPIO

# Set up the pins for Red, Yellow, and Green LEDs
red_pin = 19   # Connected to D5
yellow_pin = 26  # Connected to D6
green_pin = 5   # Connected to D2

# Initialize the GPIO pins as output
red_led = GPIO(red_pin, GPIO.OUT)
yellow_led = GPIO(yellow_pin, GPIO.OUT)
green_led = GPIO(green_pin, GPIO.OUT)

def blink_green_light(blink_count, blink_interval):
    """Blink the green light a specified number of times."""
    for _ in range(blink_count):
        green_led.write(1)  # Turn green light on
        time.sleep(blink_interval)  # Wait for the blink interval
        green_led.write(0)  # Turn green light off
        time.sleep(blink_interval)  # Wait for the blink interval

def traffic_light_sequence():
    while True:
        # Red light on, Yellow and Green off
        red_led.write(1)
        yellow_led.write(0)
        green_led.write(0)
        print("Red Light ON")
        time.sleep(5)  # Wait for 5 seconds

        # Green light on, Red and Yellow off
        red_led.write(0)
        yellow_led.write(0)
        green_led.write(1)
        time.sleep(5)
        blink_green_light(blink_count=5, blink_interval=0.5)  # Blink green light 5 times with 0.5 second interval
        print("Green Light ON")


        # Yellow light on, Red and Green off
        red_led.write(0)
        yellow_led.write(1)
        green_led.write(0)
        print("Yellow Light ON")
        time.sleep(2)  # Wait for 2 seconds

if __name__ == '__main__':
    try:
        traffic_light_sequence()
    except KeyboardInterrupt:
        # Clean up GPIO settings before exiting
        red_led.write(0)
        yellow_led.write(0)
        green_led.write(0)
        print("Traffic light simulation stopped")
