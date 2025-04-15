#define DIR_DRIVE_1 10
#define DIR_DRIVE_2 12
#define SPEED_DRIVE 11

#define DIR_PUNCH_1 5
#define DIR_PUNCH_2 4
#define SPEED_PUNCH 3


#include "GyverPID.h"

unsigned long time1;
bool switcher = 0;

//GyverPID regulator(0.5, 0.001, 0,  100);
// 2.5 2 0.8
const float Pi = 2.5, Ii = 2, Di = 0.8; // 1.5, Ii = 2, Di = 0.8; 150 good | 1.5 1.7 0.8 100
GyverPID regulator_plus(Pi, Ii, Di,  150);

void setup() {
  Serial.begin(38400);
  Serial.setTimeout(50);
  regulator_plus.setLimits(-150, 150);
  pinMode(DIR_DRIVE_1, OUTPUT);
  pinMode(DIR_DRIVE_2, OUTPUT);
  pinMode(SPEED_DRIVE, OUTPUT);
  pinMode(DIR_PUNCH_1, OUTPUT);
  pinMode(DIR_PUNCH_2, OUTPUT);
  pinMode(SPEED_PUNCH, OUTPUT);
}

void loop() {
  int x, x_ball, punch;
  if (Serial.available()>0){
    String s = Serial.readStringUntil('\n');
    Serial.println(s);
    byte ind = s.indexOf(',');
    byte ind1 = s.indexOf(';');
    String s1 = s.substring(0,ind);
    String s2 = s.substring(ind+1,ind1);
    String s3 = s.substring(ind1+1,s.length());
    x = s2.toInt();
    x_ball = s3.toInt();
    punch = s1.toInt();
    regulator_plus.setpoint = x_ball;
    regulator_plus.input = x;

    if (x == 0 and x_ball == 0){
      Motor(0);
    } else {
      regulator_plus.setDirection(NORMAL);
      regulator_plus.getResult();
      //if (abs(regulator_plus.output) > 40){
        Motor(regulator_plus.output); 
      //}
    }
  }
  if (punch == 1 && switcher == 0){
    PunchMotor(255);
    time1 = millis();
    switcher = 1;
  }
  if (millis() - time1 > 500 && switcher == 1){
    PunchMotor(-50);
    delay(10);
    PunchMotor(0);
    switcher = 0;
  } 
}

void Motor(int speed1){
  int dir1 = 0;
  int dir2 = 0;
  if (speed1 <= 0){
     dir1 = 1;
     dir2 = 0;
  } else {
     dir1 = 0;
     dir2 = 1;
  }
  if (speed1 == 0){
    dir1 = 0;
    dir2 = 0;
  }
  digitalWrite(DIR_DRIVE_1, dir1); 
  digitalWrite(DIR_DRIVE_2, dir2); 
  speed1 = abs(speed1);
  speed1 = constrain(speed1, 50, 255);
  analogWrite(SPEED_DRIVE, speed1);
}

void PunchMotor(int speed2){
  int dir1_1 = 0;
  int dir2_1 = 0;
  if (speed2 <= 0){
     dir1_1 = 1;
     dir2_1 = 0;
  } else {
     dir1_1 = 0;
     dir2_1 = 1;
  }
  if (speed2 == 0){
    dir1_1 = 0;
    dir2_1 = 0;
  }
  digitalWrite(DIR_PUNCH_1, dir1_1);
  digitalWrite(DIR_PUNCH_2, dir2_1);
  speed2 = abs(speed2);
  speed2 = constrain(speed2, 0, 255);
  analogWrite(SPEED_PUNCH, speed2);
}