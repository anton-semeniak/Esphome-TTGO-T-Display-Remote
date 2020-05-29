# Exampe of ESPHome configuration how to use TTGO T-Display with IR Remote Control to control lights in Home Assistant.

## Components: 
* [TTGO T-Display](https://github.com/Xinyuan-LilyGO/TTGO-T-Display)
* IR sensor like TL1838
* Remote Control

## Remote Control
This configuration for Apple Remote (aluminum), but it can be replaces by any other model, just change IR codes in the config file

## IR Sensor connections
* 1- GPIO27
* 2- GND
* 3- +5V

![Image of schematic](https://github.com/anton-semeniak/Esphome-TTGO-T-Display-Remote/blob/master/documents/images/IR_schematic.PNG)

# Home Assistant entities:
* Badrom Main Light Commands - sensor for commands from ESPHome
* Screen Backlight - switch for backlight 
* left_button - left onboard button on TTGO T-Display, turn off screen 
* right_button - right onboard button on TTGO T-Display, turn on screen

![Image of entities](https://github.com/anton-semeniak/Esphome-TTGO-T-Display-Remote/blob/master/documents/images/HAEntities.PNG)

# Usage
* Change secrets.yaml file for WiFi, OTA and API credentials. 
* Apply ESPhome configuration
* Register new device in Home Assistant.
* Change and include automations to the Home Assistant.


Display custom component based on [musk95](https://github.com/musk95/esphome)
