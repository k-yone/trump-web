#include <stdio.h>
#include <wiringPi.h>


#define LED     17

int main (void)
{
  int i;
  FILE *fp;

  if(wiringPiSetup () == -1)
    exit(1);

  pinMode (LED, OUTPUT);

  fp = fopen("light.conf", "r");
  if(fp == NULL){
      printf("could not open light config\n");
      exit(1);
  }
  fscanf(fp, "%d", &i);

  fclose(fp);

  if(i){
    digitalWrite (LED, HIGH) ;  // On
  }else{
    digitalWrite (LED, LOW) ;  // On
  }

  return 0 ;
}
