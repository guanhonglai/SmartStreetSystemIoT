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


class GroveWaterSensor:
    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()

    @property
    def water(self):
        value = self.adc.read(self.channel)
        return value


def main():
    # Define thresholds (adjust as needed)
    LIGHT_THRESHOLD = 300  # Light intensity threshold for turning on the LEDs
    WATER_THRESHOLD = 500  # Water detection threshold for turning on the LEDs

    # Initialize sensors and LEDs
    light_sensor = GroveLightSensor(2)  # Light sensor connected to A0
    water_sensor = GroveWaterSensor(4)  # Water sensor connected to A2
    led1 = GPIO(5, GPIO.OUT)  # First LED connected to D5 (GPIO 5)
    led2 = GPIO(6, GPIO.OUT)  # Second LED connected to D6 (GPIO 6)

    print('Monitoring sensors and controlling LED lights...')

    while True:
        # Read light and water sensor values
        light_value = light_sensor.light
        water_value = water_sensor.water

        print(f'Light value: {light_value}, Water value: {water_value}')

        # Scenario 1: High light intensity and water detected -> One LED ON
        if light_value >= LIGHT_THRESHOLD and water_value > WATER_THRESHOLD:
            print('High light intensity and water detected. Turning ON one LED.')
            led1.write(1)  # Turn on LED 1
            led2.write(0)  # Turn off LED 2

        # Scenario 2: Low light intensity -> Two LEDs ON
        elif light_value < LIGHT_THRESHOLD:
            print('Low light intensity. Turning ON both LEDs.')
            led1.write(1)  # Turn on LED 1
            led2.write(1)  # Turn on LED 2

        # Scenario 3: High light intensity and no water -> Both LEDs OFF
        elif light_value >= LIGHT_THRESHOLD and water_value <= WATER_THRESHOLD:
            print('High light intensity and no water detected. Turning OFF both LEDs.')
            led1.write(0)  # Turn off LED 1
            led2.write(0)  # Turn off LED 2

        # Wait before checking the sensors again
        time.sleep(1)


if __name__ == '__main__':
    main()
