#!/bin/sh
gcc -Wall -o ./html/pwm ./src/pwm.c -lwiringPi -lpthread
gcc -Wall -o ./html/light ./src/light.c -lwiringPi -lpthread

echo 175 > ./html/servo.conf
echo 0 > ./html/light.conf

cp -r ./html /var/www/

chown :pi /var/www/html/pwm
chown :pi /var/www/html/light
chown :pi /var/www/html/servo.conf
chown :pi /var/www/html/light.conf

chmod ug+s /var/www/html/pwm
chmod ug+s /var/www/html/light

chmod a+r /var/www/html/servo.conf
chmod a+r /var/www/html/light.conf

