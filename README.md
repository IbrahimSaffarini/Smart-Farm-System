# Smart Farm System

<p align="justify">
This project is an advanced agricultural solution designed to optimize farming practices through the integration of embedded systems and IoT technologies. This project employs a variety of sensors to continuously monitor environmental conditions such as temperature, humidity, soil moisture, and light intensity. By collecting and analyzing this data, the system can automate responses to maintain optimal conditions for crop growth, thereby improving overall farm efficiency and productivity.
</p>

## Key Features & Technologies

### 1- Sensors and Inputs:

  - RFID Sensor: For identifying and tracking animals and humans within the farm.

  - DHT11 Sensor: Measures temperature and humidity.

  - Ultrasonic Sensor: Measures distance for various applications.

  - Soil Moisture Sensor: Monitors soil moisture levels.

  - Light Intensity Sensor: Measures light levels to optimize growth conditions.

  - Water Flow Sensor: Monitors the flow of water in irrigation systems.

### 2- Outputs and Actuators:

  - LEDs: Indicate system status and alerts.

  - Buzzer: Provides audible alerts and notifications.

  - LCD Display: Shows real-time data and system status.

### 3- Data Processing and Communication:

  - Raspberry Pi: Central processing unit for managing sensor data and executing control logic.

  - ThingSpeak Integration: Uploads sensor data to the cloud for remote monitoring and analysis.

  - Flask Web Application: Provides a web interface for viewing sensor data and managing the system.

  - MIT App Inventor: Used to create a mobile application for monitoring and controlling the system remotely.

### 4- Control and Automation:

  - Keypad: Allows users to input commands and settings.

  - Camera Module: Captures images and videos for monitoring purposes.

  - PWM Output: Controls actuators such as motors or valves.

### 5- Security and Access Control:

  - RFID Tags: Used for identifying authorized personnel and tracking animals.

  - Motion Sensor: Detects unauthorized access or movement within the farm.

### 6- Visualization and Monitoring:

  - ThingSpeak Widgets: Display real-time data and historical trends using various visualization tools.

  - LCD Display: Provides local monitoring of key variables such as temperature, humidity, and soil moisture.
## System Design & Implementation

### Hardware Block Diagram

<div align="center">
  <img src="https://drive.google.com/uc?export=view&id=1M8ubKjEnpI7tDips0lCqvoa9RPLSE3-B" alt="Hardware Block Diagram" />
</div>

### Hardware Setup

<div align="center">
  <img src="https://drive.google.com/uc?export=view&id=1U5cSVfmxXTq7DOwMfwEjGtn-WipEpuqR" alt="Hardware Setup" />
</div>

### ThingSpeak Visualizations & Widgets

<div align="center">
  <img src="https://drive.google.com/uc?export=view&id=1fPNv-1jztodfN9tjEjj-OmnnzUwHIyNs" alt="ThingSpeak Visualizations" />
</div>

<div align="center">
  <img src="https://drive.google.com/uc?export=view&id=14p8RhbYDyf6Z_Bj39w2E-FlGiE3ylM-3" alt="ThingSpeak Widgets" />
</div>

### MIT App Inventor

<div align="center">
  <img src="https://drive.google.com/uc?export=view&id=1KoB92lhKFk4mV6z0HXxzPWO0w1EG2cTB" alt="MIT App Inventor" width="250"/>
</div>

## Installation & Setting Up the Project

### Prerequisites

#### 1- Ensure you have a Raspberry Pi set up and connected to the internet.

#### 2- Ensure Python is installed on your Raspberry Pi.

#### 3- Create a ThingSpeak account if you do not have one.

#### 4- Create a new project (channel) in your ThingSpeak account.

#### 5- Configure the channel with the following five fields:

  - Temperature

  - Humidity

  - Light Intensity

  - Soil Moisture

  - Water Flow

#### 5- Obtain the Write API Key and the Channel ID for your ThingSpeak channel.

#### 6- Set up the visualizations and widgets for the fields in the public view.

### Running The Project

#### 1- Download the Repository.

#### 2- Install Required Libraries.

<p align="justify"><i>
Note: Some modules used in the project (e.g., LCD1602, DHT11, keypadfunc, RFIDTest, PCF8591) are custom or specific to certain hardware configurations and may not be available online. Ensure you have the appropriate modules or find equivalent replacements for your setup.
</i></p>

#### 3- Integrate ThingSpeak in the .py file.

  - Replace **ThingSpeak API Key** with your ThingSpeak Write API Key.

  - Replace **Use your ThingSpeak Channel ID** with your Channel ID.

#### 4- Run and Monitor the System.

## Contact for Support

For any queries or support related to this project, feel free to contact me at ibrahimsaffarini2001@gmail.com.
