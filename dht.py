import time
from datetime import datetime
from seeed_dht import DHT
from pyrebase import pyrebase

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

# Initialize DHT sensor
DHT_pin = 5
sensor = DHT("11", DHT_pin)

# Update interval
update_interval = 60  # in seconds
last_update_time = time.time()

print("Detecting temperature and humidity...")

while True:
    try:
        current_time = time.time()
        
        if current_time - last_update_time >= update_interval:
            # Read temperature and humidity
            humi, temp = sensor.read()
            
            if humi is not None and temp is not None:
                # Format temperature and humidity
                t = "{0:.1f}".format(temp)
                h = "{0:.1f}".format(humi)
                
                # Print to console
                print(f"Temperature: {t}°C, Humidity: {h}%")
                
                # Prepare data with timestamp
                dt = datetime.today().strftime('%Y%m%d')
                timeH = datetime.today().strftime('%H')
                timeM = datetime.today().strftime('%M%S')
                
                # Combine data into a single dictionary
                data = {
                    'temperature': t,
                    'humidity': h,
                    'timestamp': datetime.now().isoformat()  # ISO format timestamp
                }
                
                # Update Firebase with the combined data
                db.child("Current").update(data)
                db.child('History').child(dt).child(timeH).child(timeM).set(data)
                
                # Update last update time
                last_update_time = current_time
            else:
                print("Sensor reading failed.")
        
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
