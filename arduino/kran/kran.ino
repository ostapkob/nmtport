#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#define OLED_RESET 4
#define sensor1 2
#define sensor2 3
#define sensor3 4
#define sensor4 5
Adafruit_SSD1306 display(OLED_RESET);

uint32_t Timer1, Timer2, Timer3, Timer4;
int temp180;
int p90, p180;
String data, res;
int Led = 13;//LED pin

void setup()
{
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  display.clearDisplay();
  pinMode(Led, OUTPUT);
  pinMode(sensor1, INPUT_PULLUP);
  pinMode(sensor2, INPUT_PULLUP);
  pinMode(sensor3, INPUT_PULLUP);
  pinMode(sensor4, INPUT);
  Serial.begin(9600);
}

void loop()
{

  if (digitalRead(sensor1) == LOW && millis() - Timer1 > 1000)
  {
    Timer1 = millis();
    data += "1";
    LED();
  }

  if (digitalRead(sensor2) == LOW && millis() - Timer2 > 1000)
  {
    Timer2 = millis();
    data += "2";
    LED();
  }

  if (digitalRead(sensor3) == LOW && millis() - Timer3 > 1000)
  {
    Timer3 = millis();
    data += "3";
    LED();
  }
  if (digitalRead(sensor4) == 1 && millis() - Timer4 > 1000)
  {
    Timer4 = millis();
    data += "4";
    LED();
  }

  Serial.println(data + "-" + p90 + "-" + p180);
  if (data.length() > 1) {
    if (data == "11" || data == "22" || data == "33" || data == "44")  {
      p90 += 1;
    }
    if (data == "12" || data == "21" || data == "34" || data == "43")  {
      temp180 += 1;
    }
    data = "";
  }
  p180 = temp180 / 2;


  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0, 0);
  display.println(data);
  res = String(p90) + "     " + String(p180);
  display.println("90          180");
  //  display.println(p90);
  //  display.println(p180);
  display.setTextSize(2);
  display.println(res);
  display.display();
  display.clearDisplay();
}




void LED() {
  digitalWrite(Led, HIGH);
  delay(200);
  digitalWrite(Led, LOW);
}
