#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

// LED pins
const int amberLED = 2;
const int blueLED  = 3;
const int greenLED = 4;

// Create MPU object
Adafruit_MPU6050 mpu;

void setup() {
  // Initialize LEDs
  pinMode(amberLED, OUTPUT);
  pinMode(blueLED, OUTPUT);
  pinMode(greenLED, OUTPUT);

  // Initialize Serial
  Serial.begin(9600);
  while (!Serial) delay(10);

  Serial.println("Initializing MPU6050...");

  if (!mpu.begin()) {
    Serial.println("Could not find a valid MPU6050 sensor, check wiring!");
    while (1) delay(10);
  }

  // Configure the accelerometer range
  mpu.setAccelerometerRange(MPU6050_RANGE_2_G);
  mpu.setGyroRange(MPU6050_RANGE_2000_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

  Serial.println("MPU6050 initialized successfully!");
  Serial.println("**********************************************");
}

void loop() {
  // Get new sensor events
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  // Pitch and roll approximation
  float pitch = a.acceleration.x;
  float roll  = a.acceleration.y;

  // Output to Serial
  Serial.print("Pitch = "); Serial.print(pitch);
  Serial.print("  Roll = "); Serial.println(roll);
  Serial.println("**********************************************");

  // Pitch detection
  if (pitch < 0.0) {
    Serial.println("Pitch front detected!");
    digitalWrite(amberLED, HIGH);
  } else if (pitch > 0.9) {
    Serial.println("Pitch back detected!");
    digitalWrite(amberLED, LOW);
  }

  // Roll detection
  if (roll > 0.6) {
    Serial.println("Roll Right Detected!");
    digitalWrite(blueLED, HIGH);
  } else if (roll < 0.0) {
    Serial.println("Roll Left Detected!");
    digitalWrite(blueLED, LOW);
  }

  // Stability
  if ((pitch > 0.0 && pitch < 0.9) && (roll > 0 && roll < 0.6)) {
    Serial.println("No Pitch and No Roll");
    digitalWrite(greenLED, HIGH);
  } else {
    digitalWrite(greenLED, LOW);
  }

  delay(1500); // adjust delay as needed
}
