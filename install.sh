#!/bin/sh
gcc -Wall -o ./html/pwm ./src/pwm.c -lwiringPi -lpthread
gcc -Wall -o ./html/light ./src/light.c -lwiringPi -lpthread

chown :pi ./html/pwm
chown :pi ./html/light

chmod ug+s ./html/pwm
chmod ug+s ./html/light

echo 175 > ./html/servo.conf
echo 0 > ./html/light.conf

chmod a+r ./html/servo.conf
chmod a+r ./html/light.conf

cp -r ./html /var/
