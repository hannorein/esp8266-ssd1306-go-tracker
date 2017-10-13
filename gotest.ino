#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
#include <ESP8266HTTPClient.h>

// Uses the esp8266-oled-ssd130 library
#include <Wire.h>  
#include "SSD1306.h" 
#define go_width 64
#define go_height 32
static char go_bits[] = {
  0xFF, 0xCC, 0xFF, 0xFF, 0xC0, 0xFF, 0xFF, 0xFF, 0x3F, 0x0C, 0xFE, 0x1F,
  0x00, 0xFF, 0xFF, 0xFF, 0x1F, 0x0C, 0xFE, 0x1F, 0x00, 0xFE, 0xFF, 0xFF,
  0x0F, 0x0C, 0xFC, 0x0F, 0x00, 0xFC, 0xFF, 0xFF, 0x07, 0x0C, 0xF8, 0x07,
  0x00, 0xF8, 0xFF, 0xFF, 0x03, 0x0C, 0xF0, 0x03, 0x00, 0xF0, 0xFF, 0xFF,
  0x01, 0x0C, 0xE0, 0x01, 0x00, 0xE0, 0xFF, 0xFF, 0x01, 0x0C, 0xE0, 0x01,
  0x00, 0xE0, 0xFF, 0xFF, 0x00, 0x0C, 0xC0, 0x00, 0x00, 0xC0, 0xFF, 0xFF,
  0x00, 0x0C, 0xC0, 0x01, 0x00, 0xC0, 0xFF, 0xFF, 0x00, 0xFC, 0xFF, 0xFF,
  0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0xFC, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
  0x00, 0x0C, 0xC0, 0x01, 0x00, 0xC0, 0xFF, 0xFF, 0x00, 0x0C, 0xC0, 0x00,
  0x00, 0xC0, 0xFF, 0xFF, 0x01, 0x0C, 0xC0, 0x01, 0x00, 0xE0, 0xFF, 0xFF,
  0x01, 0x0C, 0xC0, 0x01, 0x00, 0xE0, 0xFF, 0xFF, 0x01, 0x0C, 0xC0, 0x03,
  0x00, 0xE0, 0xFF, 0xFF, 0x07, 0x0C, 0xC0, 0x07, 0x00, 0xF8, 0xFF, 0xFF,
  0x0F, 0x0C, 0xC0, 0x0F, 0x00, 0xF8, 0xFF, 0xFF, 0x1F, 0x0C, 0xC0, 0x1F,
  0x00, 0xFE, 0xFF, 0xFF, 0x3F, 0x0C, 0xC0, 0x1F, 0x00, 0xFF, 0xFF, 0xFF,
  0xFF, 0x0C, 0xC0, 0xFF, 0x80, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
  0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
  0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
  0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
  0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
  0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
  0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
  0xFF, 0xFF, 0xFF, 0xFF, };

// Pin connections
// D3 -> SDA
// D5 -> SCL

// Initialize the OLED display using Wire library
SSD1306  display(0x3c, D3, D5);

ESP8266WiFiMulti WiFiMulti;

void setup() {
  WiFiMulti.addAP("yourssid", "yourpassword");
  
  display.init();
  display.flipScreenVertically();
  display.setFont(ArialMT_Plain_16);
  display.setTextAlignment(TEXT_ALIGN_LEFT);

}

int status = 0;

void loop() {
  if (status==0){
    display.clear();
    display.drawString(0, 0, "Connecting to Wifi...");
    display.display();
  }
  
  if((WiFiMulti.run() == WL_CONNECTED) && status==0) {
    status = 1;
    HTTPClient http;
    display.clear();
    display.drawString(0, 0, "Getting data...");
    display.display();
    http.begin("http://hanno-rein.de/go/rougehill.xbm");
    int httpCode = http.GET();
    if(httpCode > 0) {
      status = 4;
      String payload = http.getString();
      delay(100);
      display.clear();
      display.drawXbm(0, 0, 128, 32, payload.c_str());
      display.drawXbm(0, 0, go_width, go_height, go_bits);
      display.display();
      delay(100);
    }else{
      status = 3;
      display.clear();
      display.drawString(0, 0, "HTTP error.");
      display.display();
    }
    http.end();  
  }
  if (status>=4){
    // Display a progress bar
    status += 1;
    display.drawLine(0, 31, status*2, 31);
    display.display();
  }
  if (status==64){
    // Update about once per minute.
    status = 0;
  }
  delay(1000);
}
