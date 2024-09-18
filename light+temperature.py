import time
from datetime import datetime
from grove.adc import ADC
from grove.gpio import GPIO
from seeed_dht import DHT
from pyrebase import pyrebase
from grove.grove_air_quality_sensor_v1_3 import GroveAirQualitySensor

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
user = auth.sign_in_with_email_and_password("oscarlai0308@gmail.com", "123456")
db = firebase.database()

def main():
    # Define thresholds (adjust as needed)
    LIGHT_THRESHOLD = 300  # Light intensity threshold for turning on the LEDs
    WATER_THRESHOLD = 500  # Water detection threshold for turning on the LEDs

    # Initialize sensors and LEDs
    light_sensor = GroveLightSensor(2)  # Light sensor connected to A0
    water_sensor = GroveWaterSensor(4)  # Water sensor connected to A2
    led1 = GPIO(5, GPIO.OUT)  # First LED connected to D5 (GPIO 5)
    led2 = GPIO(6, GPIO.OUT)  # Second LED connected to D6 (GPIO 6)

    # Initialize DHT sensor
    DHT_pin = 5
    dht_sensor = DHT("11", DHT_pin)

    # Initialize Air Quality sensor
    AQS_pin = 0
    air_sensor = GroveAirQualitySensor(AQS_pin)

    # Update interval
    update_interval = 5  # in seconds
    last_update_time = time.time()

    print('Monitoring sensors, controlling LED lights, and uploading data...')

    while True:
        try:
            current_time = time.time()
            
            # Read light and water sensor values
            light_value = light_sensor.light
            water_value = water_sensor.water

            print(f'Light value: {light_value}, Water value: {water_value}')

            # Control LEDs based on sensor readings
            if light_value >= LIGHT_THRESHOLD and water_value > WATER_THRESHOLD:
                print('High light intensity and water detected. Turning ON one LED.')
                led1.write(1)  # Turn on LED 1
                led2.write(0)  # Turn off LED 2
            elif light_value < LIGHT_THRESHOLD:
                print('Low light intensity. Turning ON both LEDs.')
                led1.write(1)  # Turn on LED 1
                led2.write(1)  # Turn on LED 2
            elif light_value >= LIGHT_THRESHOLD and water_value <= WATER_THRESHOLD:
                print('High light intensity and no water detected. Turning OFF both LEDs.')
                led1.write(0)  # Turn off LED 1
                led2.write(0)  # Turn off LED 2

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
            
            # Sleep before the next iteration
            time.sleep(5)
            
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
