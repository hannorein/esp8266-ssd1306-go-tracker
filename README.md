OLED GoTracker Display
======================

This project displays the status of departing GO Transit trains on a mini OLED display.

You need an ESP8266 module (WEMOS D1 mini) and on OLED display with an SSD1306 driver. Both of these can be ordered from China for a combined $6 (including shipping). 

The python code runs on a linux machine and renders an image with train status information from the GO Tracker website. I use a cron job to update it once per minute. The ESP8266 pulls that image over Wifi (also once per minute) and display it.
