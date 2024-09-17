// Define LED pins for the North traffic light set
const int redNorth = 21;   
const int yellowNorth = 19;  
const int greenNorth = 18;   

// Define LED pins for the South traffic light set
const int redSouth = 17;  
const int yellowSouth = 16;  
const int greenSouth = 15;   

// Define LED pins for the East traffic light set
const int redEast = 14;  
const int yellowEast = 12; 
const int greenEast = 13;  

// Define LED pins for the West traffic light set
const int redWest = 33;   
const int yellowWest = 32;  
const int greenWest = 25;  

void setup() {
  // Initialize the LED pins as outputs for North traffic light
  pinMode(redNorth, OUTPUT);
  pinMode(yellowNorth, OUTPUT);
  pinMode(greenNorth, OUTPUT);

  // Initialize the LED pins as outputs for South traffic light
  pinMode(redSouth, OUTPUT);
  pinMode(yellowSouth, OUTPUT);
  pinMode(greenSouth, OUTPUT);

  // Initialize the LED pins as outputs for East traffic light
  pinMode(redEast, OUTPUT);
  pinMode(yellowEast, OUTPUT);
  pinMode(greenEast, OUTPUT);

  // Initialize the LED pins as outputs for West traffic light
  pinMode(redWest, OUTPUT);
  pinMode(yellowWest, OUTPUT);
  pinMode(greenWest, OUTPUT);
  
  // Start with all red lights on
  digitalWrite(redNorth, HIGH);
  digitalWrite(redSouth, HIGH);
  digitalWrite(redEast, HIGH);
  digitalWrite(redWest, HIGH);
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
  // Delay for 1 second before the green light turns on
  delay(1000);  // 1-second delay
  digitalWrite(redPin, LOW);    // Turn off red
  digitalWrite(greenPin, HIGH); // Turn on green
  delay(5000);                  // Green light for 5 seconds
  
  // Blink the green light
  blinkGreenLight(greenPin, 5, 500);  // Blink green light 5 times with a 0.5 second interval
  digitalWrite(greenPin, LOW);        // Ensure green is off after blinking
}

void yellowPhase(int yellowPin, int redPin) {
  // Yellow phase
  digitalWrite(yellowPin, HIGH); // Turn on yellow
  delay(2000);                    // Yellow light for 2 seconds
  digitalWrite(yellowPin, LOW);  // Turn off yellow
  digitalWrite(redPin, HIGH);    // Turn red back on
}

void northTrafficLight() {
  greenPhase(redNorth, greenNorth); 
  yellowPhase(yellowNorth, redNorth); 
}

void southTrafficLight() {
  greenPhase(redSouth, greenSouth);  
  yellowPhase(yellowSouth, redSouth);
}

void eastTrafficLight() {
  greenPhase(redEast, greenEast);  
  yellowPhase(yellowEast, redEast); 
}

void westTrafficLight() {
  greenPhase(redWest, greenWest); 
  yellowPhase(yellowWest, redWest);
}

void loop() {
  // Start with all red lights on for 5 seconds
  delay(500);
  
  // Traffic light sequence: North -> South -> East -> West
  northTrafficLight();  
  southTrafficLight();  
  eastTrafficLight();  
  westTrafficLight();  
}
