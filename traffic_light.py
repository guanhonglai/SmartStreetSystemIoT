// Define LED pins for NSWE traffics
const int redNorth = 21;   
const int yellowNorth = 19;  
const int greenNorth = 18;   

const int redSouth = 17;  
const int yellowSouth = 16;  
const int greenSouth = 15;   

const int redEast = 14;  
const int yellowEast = 12; 
const int greenEast = 13;  

const int redWest = 33;   
const int yellowWest = 32;  
const int greenWest = 25;  

void setup() {
  Serial.begin(115200);  // Start serial communication for debugging
  
  // Initialize the LED pins as outputs for NSWE taffics
  pinMode(redNorth, OUTPUT);
  pinMode(yellowNorth, OUTPUT);
  pinMode(greenNorth, OUTPUT);

  pinMode(redSouth, OUTPUT);
  pinMode(yellowSouth, OUTPUT);
  pinMode(greenSouth, OUTPUT);

  pinMode(redEast, OUTPUT);
  pinMode(yellowEast, OUTPUT);
  pinMode(greenEast, OUTPUT);

  pinMode(redWest, OUTPUT);
  pinMode(yellowWest, OUTPUT);
  pinMode(greenWest, OUTPUT);
  
  // Start with all red lights on
  digitalWrite(redNorth, HIGH);
  digitalWrite(redSouth, HIGH);
  digitalWrite(redEast, HIGH);
  digitalWrite(redWest, HIGH);
  
  Serial.println("All lights are RED.");
}

void blinkGreenLight(int greenPin, int blinkCount, int blinkInterval) {
  // Blink the green light
  for (int i = 0; i < blinkCount; i++) {
    digitalWrite(greenPin, HIGH);  // Turn green light on
    delay(blinkInterval);          // Wait for the blink interval
    digitalWrite(greenPin, LOW);   // Turn green light off
    delay(blinkInterval);          // Wait for the blink interval
  }
}

void greenPhase(int redPin, int greenPin) {
  delay(1000);  // 1-second delay before green light turns on
  digitalWrite(redPin, LOW);    // Turn off red
  digitalWrite(greenPin, HIGH); // Turn on green
  Serial.println("Green light ON.");
  delay(5000);                  // Green light for 5 seconds
  
  // Blink the green light
  blinkGreenLight(greenPin, 5, 500);  // Blink green light 5 times with a 0.5 second interval
  digitalWrite(greenPin, LOW);        // Ensure green is off after blinking
}

void yellowPhase(int yellowPin, int redPin) {
  digitalWrite(yellowPin, HIGH); // Turn on yellow
  Serial.println("Yellow light ON.");
  delay(2000);                    // Yellow light for 2 seconds
  digitalWrite(yellowPin, LOW);  // Turn off yellow
  digitalWrite(redPin, HIGH);    // Turn red back on
}

void northTrafficLight() {
  Serial.println("North light sequence starting.");
  greenPhase(redNorth, greenNorth); 
  yellowPhase(yellowNorth, redNorth); 
  Serial.println("North light sequence finished.");
}

void southTrafficLight() {
  Serial.println("South light sequence starting.");
  greenPhase(redSouth, greenSouth);  
  yellowPhase(yellowSouth, redSouth);
  Serial.println("South light sequence finished.");
}

void eastTrafficLight() {
  Serial.println("East light sequence starting.");
  greenPhase(redEast, greenEast);  
  yellowPhase(yellowEast, redEast); 
  Serial.println("East light sequence finished.");
}

void westTrafficLight() {
  Serial.println("West light sequence starting.");
  greenPhase(redWest, greenWest); 
  yellowPhase(yellowWest, redWest);
  Serial.println("West light sequence finished.");
}

void loop() {
  Serial.println("Starting traffic light sequence.");
  
  // Start with all red lights on for 5 seconds
  delay(1000);
  
  // Traffic light sequence: North -> South -> East -> West
  northTrafficLight();  
  southTrafficLight();  
  eastTrafficLight();  
  westTrafficLight();  
}
