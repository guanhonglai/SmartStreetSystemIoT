// Define LED pins for the North traffic light set
const int redNorth = 21;   // Red LED for the North traffic light
const int yellowNorth = 19;  // Yellow LED for the North traffic light
const int greenNorth = 18;   // Green LED for the North traffic light

// Define LED pins for the South traffic light set
const int redSouth = 17;   // Red LED for the South traffic light
const int yellowSouth = 16;  // Yellow LED for the South traffic light
const int greenSouth = 15;   // Green LED for the South traffic light

// Define LED pins for the East traffic light set
const int redEast = 14;   // Red LED for the East traffic light
const int yellowEast = 12;  // Yellow LED for the East traffic light
const int greenEast = 13;   // Green LED for the East traffic light

// Define LED pins for the West traffic light set
const int redWest = 33;   // Red LED for the West traffic light
const int yellowWest = 32;  // Yellow LED for the West traffic light
const int greenWest = 25;   // Green LED for the West traffic light

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
  // Blink the green light a specified number of times
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
  greenPhase(redNorth, greenNorth);  // North light green phase
  yellowPhase(yellowNorth, redNorth); // North light yellow phase
}

void southTrafficLight() {
  greenPhase(redSouth, greenSouth);  // South light green phase
  yellowPhase(yellowSouth, redSouth); // South light yellow phase
}

void eastTrafficLight() {
  greenPhase(redEast, greenEast);  // East light green phase
  yellowPhase(yellowEast, redEast); // East light yellow phase
}

void westTrafficLight() {
  greenPhase(redWest, greenWest);  // West light green phase
  yellowPhase(yellowWest, redWest); // West light yellow phase
}

void loop() {
  // Start with all red lights on for 5 seconds
  delay(500);
  
  // Traffic light sequence: North -> South -> East -> West
  northTrafficLight();   // North light sequence
  southTrafficLight();   // South light sequence
  eastTrafficLight();    // East light sequence
  westTrafficLight();    // West light sequence
}
