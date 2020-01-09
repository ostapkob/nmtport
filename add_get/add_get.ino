#include <SoftwareSerial.h>
#define lever 12
#define led  13
#include<stdio.h>
#include<string.h>

// Rx of GSM —> pin 9 of Arduino | Tx of GSM –> pin 8 of Arduino
SoftwareSerial SimSerial(8, 9); 

unsigned long timer, timerSent;
String data[6], dataGPS, POST, GET, statusSim;
String latitude, longitude;
String const ip_addr = "http://35.241.126.216";
String const api = "/api/v1.0/add_get?";
String const mechanism_id = "32772";
int count, sum;
float  result;

//helper variable
boolean flag = true;


void setup() {
  Serial.begin(9600);
  SimSerial.begin(9600);
  SimSerial.setTimeout(3000);
  turnOnShield();
  turnOnGPS();
  //  updateSerial();
  registrationSim();
  //  updateSerial();
  pinMode (lever, INPUT_PULLUP);
  pinMode(led, OUTPUT);
    ArduinoToSim("AT+GSMBUSY=1", 1000); //Reject incoming call
  //  ArduinoToSim("ATE0", 1000);// echo
}


void loop() {

  if (millis() - timer > 100 ) {
    timer = millis();
    count ++;
    if (digitalRead(lever) == 1) { //push or not push
      sum++;
      digitalWrite(led, 1);
    }
    else {
      digitalWrite(led, 0);
    }
  }

  if (millis() - timerSent >= 60000 ) {
    timerSent = millis();
    statusShield();
    dataGPS = sendData("AT + CGPSINF=2", 2000);
    ParseGPS(dataGPS);
    result = (float)sum / (float)count;
    count = 0;
    sum = 0;
    GET = ip_addr + api + "mechanism_id=" + mechanism_id + "&password=super_pass" + "&value=" + String(result) + "&latitude=" + latitude + "&longitude=" + longitude;
    Serial.println(GET);
    sentGet(GET);
    //    POST = "{\"password\":\"super_pass\",\"value\":" + String(result) + ",\"latitude\":" + latitude + ",\"longitude\":" + longitude + ",\"mechanism_id\":" + mechanism_id + "}";
    //    sentPost(POST);
    //    Serial.println(POST);
  }
}

void(* resetFunc) (void) = 0;

void statusShield() { // if Shild is turn of then turn on
  updateSerial(); // clear Serial
  statusSim = sendData("AT", 500);
  if (statusSim.indexOf("OK") < 0) {

    resetFunc();
//    turnOnShield();
//    turnOnGPS();
//    registrationSim();
  }
}

void turnOnShield() {
  digitalWrite(11, HIGH);
  delay(1000);
  digitalWrite(11, LOW);
  delay(3000); // give time to register Sim online
}



void ParseGPS(String str) {
  int v0, v1, v2, v3,  v4, v5;
  v0 = str.indexOf("CGPSINF:");
  v1 = str.indexOf(",", v0 + 1);
  v2 = str.indexOf(",", v1 + 1);
  v3 = str.indexOf(",", v2 + 1);
  v4 = str.indexOf(",", v3 + 1);
  v5 = str.indexOf(",", v4 + 1);

  latitude = str.substring(v2 + 3, v3);
  longitude = str.substring(v4 + 3, v5);
  if (latitude == "00.0000") {
    latitude = "0"; // because server gets it how last data
    longitude = "0";
  }
}

void sentGet(String msg) {
  String add_get;
  add_get = "AT+HTTPPARA=\"URL\", \"" +msg+ "\"";
  ArduinoToSim("AT+HTTPPARA=\"CID\",1", 100);
  ArduinoToSim(add_get, 100);
  ArduinoToSim("AT+HTTPACTION=0", 100);
  ArduinoToSim("AT+HTTPREAD", 100);
  ArduinoToSim("AT+HTTPTERM", 100);
}

String sendData (String command , const int timeout) { // sent data to serial port return ansver
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
  return response;
}

void turnOnGPS() {
  ArduinoToSim("AT", 1000);
  ArduinoToSim("AT + CGPSPWR=1", 1000);
  ArduinoToSim("AT + CGPSRST=2", 1000); // 1 HOT; 2 WARM
  ArduinoToSim("AT + CGPSINF=2", 1000);
  ArduinoToSim("AT+CGNSSEQ=RMC", 1000);
  ArduinoToSim("AT + CGPSSTATUS?", 1000);
}





void registrationSim() {
  ArduinoToSim("AT", 100);// Status Shild
  ArduinoToSim("AT+CSQ", 100);//Signal quality test, 0-31
  ArduinoToSim("AT+CCID", 100);// SIM card information
  ArduinoToSim("AT + CIPSHUT", 100);//Break all connections
  ArduinoToSim("AT+CGATT=1", 100);// GPRS attach or deatach
  ArduinoToSim("AT + CREG?", 100);// is module in network
  ArduinoToSim("AT + SAPBR = 3,1, \"CONTYPE\", \"GPRS\"", 1000);
  ArduinoToSim("AT+SAPBR=3,1,\"APN\",\"internet.mts.ru\"", 1000);
  ArduinoToSim("AT+SAPBR=1,1", 2000);
  ArduinoToSim("AT+SAPBR=2,1", 1000);
  ArduinoToSim("AT+SAPBR=2,1", 1000);
  ArduinoToSim("AT+HTTPINIT", 1000);

}

void sentPost(String msg) {
  ArduinoToSim("AT+HTTPPARA=\"CID\",1", 100);
  ArduinoToSim("AT+HTTPPARA=\"URL\", \"http://35.241.126.216/api/v1.0/add_post\"", 100);
  ArduinoToSim("AT+HTTPPARA=\"CONTENT\",\"application/json\"", 100);
  ArduinoToSim("AT+HTTPDATA=" + String(msg.length()) + ",10000", 100);
  ArduinoToSim(msg, 500);
  ArduinoToSim("AT+HTTPACTION=1", 100);
  ArduinoToSim("AT+HTTPREAD", 100);
  ArduinoToSim("AT+HTTPTERM", 100);
}

void ArduinoToSim(String command, const int wait) { //it is more comfortable
  SimSerial.println(command);
  delay(wait);
}

void updateSerial()
//message view function
{
  delay(1000);
  while (Serial.available())
  {
    SimSerial.write(Serial.read());
  }
  while (SimSerial.available())
  {
    Serial.write(SimSerial.read());
  }
}
