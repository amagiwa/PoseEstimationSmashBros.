#include <SoftwareSerial.h>
#include <NintendoSwitchControlLibrary.h>

int len = 0;
int input = -1;

void selectController() {
  pushButton(Button::L, 100);
  pushButton(Button::R, 100);
  pushButton(Button::A, 3000);
}

void selectCharacter(){
  tiltLeftStick(Stick::MIN, Stick::NEUTRAL, 350);
  tiltLeftStick(Stick::NEUTRAL, Stick::MIN, 700);
  pushButton(Button::A, 1000);
  pushButton(Button::A, 1000);
}

void setup() {
  // put your setup code here, to run once:
  Serial1.begin(9600);
  while(!Serial1){}
  pushButton(Button::L, 500, 5);
  selectController();
  selectCharacter();
}

void loop() {
  // put your main code here, to run repeatedly:
  len = Serial1.available();                         
  for(int i = 0; i < len-1; ++i){
     input = Serial1.read();
  }
  if(len-1 <= 0){
    input = Serial1.read();
  }
  if(input != -1){
    switch(input){
      case '1':
          tiltLeftStick(Stick::MAX, Stick::NEUTRAL, 500);
          break;
      case '2':
          tiltLeftStick(Stick::MIN, Stick::NEUTRAL, 500);
          break;
      case '3':
        pushButton(Button::A, 500);
        break;
      case '4':
        pushButton(Button::Y, 500);
        break;
      default: break;
    }
  }
}
