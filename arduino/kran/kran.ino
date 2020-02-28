#define sensor1 2
#define sensor2 3
#define sensor3 4
#define sensor4 5
#define sensor5 6
#define sensor6 7
#define sensor7 8
#define sensor8 9
/*
           море
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  ‾‾‾‾‾‾‾‾‾‾4-------------8‾‾‾‾‾‾‾‾‾‾
            3             7
            ┆             ┆
            ┆             ┆
            2             6
  __________1-------------5__________

  ==============================
*/

uint32_t Timer1, Timer2, Timer3, Timer4, Timer5, Timer6, Timer7, Timer8;
uint32_t TimerPrint, TimerLed;
int p90, p180; // один цикл 90 и один цикл 180
int halfTurn180; // оборот в одну сторону на 180 градусов
int p90Temp, p180Temp; // переменные для хранения предыдущих значений
String data, two_las_simvols;
int Led = 13;//LED pin

void setup()
{
  pinMode(Led, OUTPUT);
  pinMode(sensor1, INPUT_PULLUP);
  pinMode(sensor2, INPUT_PULLUP);
  pinMode(sensor3, INPUT_PULLUP);
  pinMode(sensor4, INPUT_PULLUP);
  pinMode(sensor5, INPUT_PULLUP);
  pinMode(sensor6, INPUT_PULLUP);
  pinMode(sensor7, INPUT_PULLUP);
  pinMode(sensor8, INPUT_PULLUP);
  Serial.begin(9600);
}

void loop()
{
  digitalWrite(Led, LOW);
  if (digitalRead(sensor1) == 0 && millis() - Timer1 > 2000)
  {
    Timer1 = millis();
    data += "1";
    LED();
  }

  if (digitalRead(sensor2) == 0 && millis() - Timer2 > 2000)
  {
    Timer2 = millis();
    data += "2";
    LED();
  }

  if (digitalRead(sensor3) == 0 && millis() - Timer3 > 2000)
  {
    Timer3 = millis();
    data += "3";
    LED();
  }
  if (digitalRead(sensor4) == 0 && millis() - Timer4 > 2000)
  {
    Timer4 = millis();
    data += "4";
    LED();
  }

  if (digitalRead(sensor5) == 0 && millis() - Timer5 > 2000)
  {
    Timer5 = millis();
    data += "5";
    LED();
  }

  if (digitalRead(sensor6) == 0 && millis() - Timer6 > 2000)
  {
    Timer6 = millis();
    data += "6";
    LED();
  }

  if (digitalRead(sensor7) == 0 && millis() - Timer7 > 2000)
  {
    Timer7 = millis();
    data += "7";
    LED();
  }

  if (digitalRead(sensor8) == 0 && millis() - Timer8 > 2000)
  {
    Timer8 = millis();
    data += "8";
    LED();
  }



  if (millis() - TimerPrint > 1000)
  {
    TimerPrint = millis();
    Serial.println(data + ":" + p90 + "-" + p180);

  }



  if (data.length() >= 4) {
    if (data == "1234" || data == "4321" || data == "5678" || data == "8765") {
      halfTurn180++; // половина цикла поворота  
    }

    if (data == "1221" || data == "3443" || data == "5665" || data == "7887") {
      p90++;
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

  if (data.length() >= 3) { // если оди датчик не сработал то скидываем data в положениях стрела на море или на штабель
    two_las_simvols = data.substring(data.length() - 2, data.length());
    if (two_las_simvols == "21" || two_las_simvols == "34" || two_las_simvols == "65" ||  two_las_simvols == "78") {
      data = "";
    }
  }


}


void LED() {
  digitalWrite(Led, HIGH);
  digitalWrite(Led, LOW);
}
