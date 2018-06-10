#include <wiringPi.h>

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(void)
{
  int i;
  FILE *fp;

  int pin = 18;
  if(wiringPiSetup () == -1)
    exit(1);

  pinMode(pin, PWM_OUTPUT);
  pwmSetMode(PWM_MODE_MS);
  pwmSetClock(400);
  pwmSetRange(1024);


  fp = fopen("servo.conf", "r");
  if(fp == NULL){
      printf("could not open servo config\n");
      exit(1);
  }
  fscanf(fp, "%d", &i);

  fclose(fp);

  pwmWrite(pin, i);
  sleep(1);
  digitalWrite(pin, 0);

  return 0;
}
