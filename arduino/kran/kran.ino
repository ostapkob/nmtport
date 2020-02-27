#define sensor1 2
#define sensor2 3
#define sensor3 4
#define sensor4 5
/*
           море
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

‾‾‾‾‾‾‾‾‾‾2-----3‾‾‾‾‾‾‾‾‾‾
          |     |
__________1-----4__________

==============================
*/

uint32_t Timer1, Timer2, Timer3, Timer4, TimerPrint;
int p90, p180; // один цикл 90 и один цикл 180
int halfTurn180; // оборот в одну сторону на 180 градусов
int p90Temp, p180Temp; // переменные для хранения предыдущих значений
String data; 
int Led = 13;//LED pin

void setup()
{
  pinMode(Led, OUTPUT);
  pinMode(sensor1, INPUT_PULLUP);
  pinMode(sensor2, INPUT_PULLUP);
  pinMode(sensor3, INPUT_PULLUP);
  pinMode(sensor4, INPUT_PULLUP);
  Serial.begin(9600);
}

void loop()
{
  if (digitalRead(sensor1) == LOW && millis() - Timer1 > 2000)
  {
    Timer1 = millis();
    data += "1";
    LED();
  }

  if (digitalRead(sensor2) == LOW && millis() - Timer2 > 2000)
  {
    Timer2 = millis();
    data += "2";
    LED();
  }

  if (digitalRead(sensor3) == 1 && millis() - Timer3 > 2000)
  {
    Timer3 = millis();
    data += "3";
    LED();
  }
  if (digitalRead(sensor4) == 1 && millis() - Timer4 > 2000)
  {
    Timer4 = millis();
    data += "4";
    LED();
  }


  if (millis() - TimerPrint > 500)
  {
    TimerPrint = millis();
    Serial.println(data + ":" + p90 + "-" + p180);
  }

  if (data.length() > 1) {
    if (data == "11" || data == "22" || data == "33" || data == "44")  { // выгружает вагоны
      p90 += 1;
    }
    if (data == "12" || data == "21" || data == "34" || data == "43")  { // поворачивается на параход
      halfTurn180 += 1;
    }
    data = "";
    p180 = halfTurn180 / 2; // цикл считается когда кран повернулся на 180 туда и обратно
    if (p90 - p90Temp == 1) { // если новое значение больше старого 
      Serial.println(" отправляем на сервер 90 градусов" + p90);
    }
    if (p180 - p180Temp == 1) {// если новое значение больше старого 
      Serial.println(" отправляем на сервер 180 градусов" +  p180);
    }
    p90Temp = p90;
    p180Temp = p180;

  }
}


void LED() {
  digitalWrite(Led, HIGH);
  delay(200);
  digitalWrite(Led, LOW);
}
