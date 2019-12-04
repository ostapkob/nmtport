#include <SoftwareSerial.h>
#define lever 3
#define led  4

SoftwareSerial SimSerial(7, 8); // Rx of GSM —> pin 8 (Tx) of Arduino | //Tx of GSM –> pin 7 (Rx) of Arduino

unsigned long timer, timerShow;
String data[6], dataGPS, POST;
String latitude, longitude;
String const mechanism_id = "32770";
int count, sum;
float  result;

//helper variable
boolean flag = true;
unsigned long n = 100.0;
String val;

void setup() {
  //turn on Sim
  digitalWrite(9, HIGH);
  delay(1000);
  digitalWrite(9, LOW);
  delay(2000); // give time to register Sim online

  Serial.begin(9600);
  SimSerial.begin(9600);
  turnGPS();
  updateSerial();
  registrationSim();
  updateSerial();
  pinMode (lever, INPUT_PULLUP);
  pinMode(led, OUTPUT);
}


void loop() {

  if (millis() - timer > 100 ) {
    timer = millis();
    count ++;
    if (digitalRead(lever) != 1) {
      sum++;
      digitalWrite(led, 1);
    }
    else {
      digitalWrite(led, 0);
    }
  }

  if (millis() - timerShow > 60000 ) {
    timerShow = millis();
    dataGPS = sendData("AT + CGPSINF=2", 1000);
    Serial.println(dataGPS);
    splitBuffer(dataGPS, ',');
    //latitude = data[3];
    latitude = (data[3] == "." || data[3] == "N") ? "0.0"  : data[3] ;  // если a > b, то с = 10. Если нет, то с = -20
   // longitude = data[5];
    longitude = (data[5] == "." || data[5] == "E") ? "0.0"  : data[3] ;  // если a > b, то с = 10. Если нет, то с = -20
    result = (float)sum / (float)count;
    count = 0;
    sum = 0;
    POST = "{\"password\":\"super\",\"value\":" + String(result) + ",\"latitude\":" + latitude + ",\"longitude\":" + longitude + ",\"mechanism_id\":" + mechanism_id + "}";
    sentPost(POST);
    Serial.println(POST);
  }

}



void splitBuffer (String buffer, char simbol) {
  int j = 0;
  for (int x = 0; x < 6; x++) {
    data[x] = "";
  }
  for (int i = 0; i < buffer.length(); i++) {
    boolean flag = true; // flag to remove 0 at the beginning
    if (buffer[i] == ',') {
      j++;
    }
    else {
      if (buffer[i] == '0' && flag) {
        continue;
      }
      else {
        data[j] += buffer[i];
        flag = false;
      }
    }
    if (j > 6) {
      break;
    }
  }
}

String sendData (String command , const int timeout) {
  String response = "";
  SimSerial.println(command);
  long int time = millis();
  int i = 0;
  while ( (time + timeout ) > millis()) {
    while (SimSerial.available()) {
      char c = char(SimSerial.read());
      response += c;
    }
  }
  //  Serial.print(response);
  return response;
}

void turnGPS() {
  ArduinoToSim("AT", 1000);
  ArduinoToSim("AT + CGPSPWR=1", 1000);
  ArduinoToSim("AT + CGPSRST=1", 1000); // 1 HOT; 2 WARM
  ArduinoToSim("AT + CGPSINF=2", 1000);
  ArduinoToSim("AT+CGNSSEQ=RMC", 1000);
  ArduinoToSim("AT + CGPSSTATUS?", 1000);
}

void registrationSim() {
  ArduinoToSim("AT", 100);
  ArduinoToSim("AT+CSQ", 100);
  ArduinoToSim("AT+CCID", 100);
  ArduinoToSim("AT + CIPSHUT", 100);
  ArduinoToSim("AT+CGATT=1", 100);
  ArduinoToSim("AT + CREG?", 100);
  ArduinoToSim("AT + SAPBR = 3,1, \"CONTYPE\", \"GPRS\"", 100);
  ArduinoToSim("AT+SAPBR=3,1,\"APN\",\"internet.mts.ru\"", 100);
  ArduinoToSim("AT+SAPBR=1,1", 1000);
  ArduinoToSim("AT+SAPBR=2,1", 1000);
  ArduinoToSim("AT+SAPBR=2,1", 1000);
  ArduinoToSim("AT+HTTPINIT", 1000);
  ArduinoToSim("AT+HTTPPARA=\"CID\",1", 100);
  ArduinoToSim("AT+HTTPPARA=\"URL\", \"http://35.241.126.216/api/v1.0/add_post\"", 1000);
  ArduinoToSim("AT+HTTPPARA=\"CONTENT\",\"application/json\"", 1000);
}

void sentPost(String msg) {
  ArduinoToSim("AT+HTTPDATA=" + String(msg.length()) + ",10000", 100);
  ArduinoToSim(msg, 500);
  ArduinoToSim("AT+HTTPACTION=1", 100);
  ArduinoToSim("AT+HTTPREAD", 100);
}

void ArduinoToSim(String command, const int wait) {
  SimSerial.println(command);
  delay(wait);
}

void updateSerial()
//message view function
{
  delay(2000);
  while (Serial.available())
  {
    SimSerial.write(Serial.read());
  }
  while (SimSerial.available())
  {
    Serial.write(SimSerial.read());
  }
}
