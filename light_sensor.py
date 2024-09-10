import time
from grove.adc import ADC
from grove.gpio import GPIO


class GroveLightSensor:
    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()

    @property
    def light(self):
        value = self.adc.read(self.channel)
        return value


def main():
    # Define threshold for light level (adjust based on your environment)
    LIGHT_THRESHOLD = 500

    # Initialize the light sensor and LED
    light_sensor = GroveLightSensor(4)  # Assuming light sensor is connected to A0
    led = GPIO(21, GPIO.OUT)  # Assuming the LED is connected to D5 (GPIO 5)

    print('Detecting light and controlling LED street light...')

    while True:
        # Read the current light level
        light_value = light_sensor.light
        print(f'Light value: {light_value}')

        # Turn on the LED street light if it's dark
        if light_value < LIGHT_THRESHOLD:
            print('It is dark, turning ON the LED street light.')
            led.write(1)  # LED ON
        else:
            print('It is bright, turning OFF the LED street light.')
            led.write(0)  # LED OFF

        # Wait before checking again
        time.sleep(1)


if __name__ == '__main__':
    main()
