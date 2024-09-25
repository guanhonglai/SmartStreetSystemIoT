import time
from datetime import datetime
from grove.adc import ADC
from grove.gpio import GPIO
from seeed_dht import DHT
from pyrebase import pyrebase
from grove.grove_led import GroveLed
from grove.grove_air_quality_sensor_v1_3 import GroveAirQualitySensor
from grove.display.grove_lcd import setText


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


# Firebase configuration
config = {
    "apiKey": "AIzaSyBM9PnDavtOXz435UDSz74CcQSKgSzmZpY",
    "authDomain": "iot-smart-city-e86cd.firebaseapp.com",
    "databaseURL": "https://iot-smart-city-e86cd-default-rtdb.firebaseio.com",
    "storageBucket": "iot-smart-city-e86cd.appspot.com"
}

# Initialize Firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
user = auth.sign_in_with_email_and_password("abc123@gmail.com", "abc123")
db = firebase.database()

def main():
    # Define thresholds (adjust as needed)
    LIGHT_THRESHOLD = 300  # Light intensity threshold for turning on the LEDs
    WATER_THRESHOLD = 500  # Water detection threshold for turning on the LEDs

    # Initialize sensors and LEDs
    light_sensor = GroveLightSensor(2)  # Light sensor connected to A2
    water_sensor = GroveWaterSensor(4)  # Water sensor connected to A4
    led1 = GPIO(20, GPIO.OUT)
    led2 = GPIO(21, GPIO.OUT)
    led3 = GPIO(26, GPIO.OUT)
    led4 = GPIO(19, GPIO.OUT)
    relay_pin = 22
    relay = GroveLed(relay_pin)

    # Initialize DHT sensor
    DHT_pin = 5
    dht_sensor = DHT("11", DHT_pin)

    # Initialize Air Quality sensor
    AQS_pin = 0
    air_sensor = GroveAirQualitySensor(AQS_pin)

    # Initialize the switch (input pin)
    switch = GPIO(16, GPIO.IN)  # Switch connected to D8 (GPIO 8)

    # Initial state
    manual_mode = False  # Start in automatic mode
    last_switch_state = switch.read()  # Read the initial state of the switch

    # Update interval
    update_interval = 5  # in seconds
    last_update_time = time.time()

    # Debounce delay
    debounce_delay = 0.2  # in seconds

    print('Monitoring sensors, controlling LED lights, and uploading data...')

    while True:
        try:
            current_time = time.time()
            rock = db.child('camera').child('rock').get().val()
            tree = db.child('camera').child('tree').get().val()

            # Check Firebase for manual mode status (1 for on, 0 for off)
            manual_mode = db.child("ManualMode").get().val()
            
            # Read light and water sensor values
            light_value = light_sensor.light
            water_value = water_sensor.water

            if manual_mode:
                print("Manual mode activated. All lights off.")
                relay.write(0)  # Turn off street light
                led1.write(0)  # Turn off LED 1
                led2.write(0)  # Turn off LED 2
                led3.write(0)
                led4.write(0)
            else:
                print("Automatic mode activated.")


                print(f'Light value: {light_value}, Water value: {water_value}')

                # Control LEDs based on sensor readings
                if light_value >= LIGHT_THRESHOLD and water_value > WATER_THRESHOLD:
                    print('It\'s daytime and raining. Turning ON street light for safety.')
                    led1.write(1)  # Turn on LED 1
                    led2.write(0)
                    led3.write(1)
                    led4.write(0)
                    relay.write(0)  # Turn off street light
                elif light_value < LIGHT_THRESHOLD:
                    print('It\'s night time. Turning ON the street lights.')
                    led1.write(1)  # Turn on LED 1
                    led2.write(1)
                    led3.write(1)
                    led4.write(1)
                    relay.write(1)  # Turn on street light
                elif light_value >= LIGHT_THRESHOLD and water_value <= WATER_THRESHOLD:
                    print('It\'s a clear, bright day. All lights are OFF to save energy.')
                    led1.write(0)  # Turn off LED 1
                    led2.write(0)  # Turn off LED 2
                    led3.write(0)
                    led4.write(0)
                    relay.write(0)  # Turn off street light

            if current_time - last_update_time >= update_interval:
                # Read temperature and humidity
                humi, temp = dht_sensor.read()
                
                # Read air quality
                air_quality = air_sensor.value
                
                if humi is not None and temp is not None:
                    # Format temperature and humidity
                    t = "{0:.1f}".format(temp)
                    h = "{0:.1f}".format(humi)
                    
                    # Print to console
                    print(f"Temperature: {t}°C, Humidity: {h}%, Air Quality: {air_quality}")
                    
                    # Prepare data with timestamp
                    dt = datetime.today().strftime('%Y%m%d')
                    timeH = datetime.today().strftime('%H')
                    timeM = datetime.today().strftime('%M%S')
                    
                    # Combine data into a single dictionary
                    data = {
                        'temperature': t,
                        'humidity': h,
                        'air_quality': air_quality,
                        'light': light_value,
                        'rain': water_value,
                        'timestamp': datetime.now().isoformat()  # ISO format timestamp
                    }
                    
                    # Update Firebase with the combined data
                    db.child("Current").update(data)
                    db.child('History').child(dt).child(timeH).child(timeM).set(data)
                    
                    # Update last update time
                    last_update_time = current_time
                else:
                    print("DHT sensor reading failed.")
                    
            weather = db.child("Current").child("weather").get().val()
            
            # Slightly longer sleep time to slow down loop speed without too much delay
            if rock or tree:
                setText("Obstacles Detected, DANGER!!!")
            elif air_quality > 100:
                setText("Poor Air Quality (" + str(air_quality) +  " AQI)")
            else:
                setText("Temp:" + str(temp) + " Weather:" + weather)
            time.sleep(update_interval)
            
            
        except KeyboardInterrupt:
            print("Program Exited")
            break
        except TypeError:
            print("Type Error occurred")
            time.sleep(10)  # Wait before retrying
        except IOError:
            print("IO Error occurred")
            time.sleep(10)  # Wait before retrying
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            time.sleep(10)  # Wait before retrying

if __name__ == '__main__':
    main()
