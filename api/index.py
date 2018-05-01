import falcon
import json
import subprocess

DUTY_BIN = 25
DUTY_MAX = 225
DUTY_MIN = 100
POS_MIN = -5
POS_MAX = 5

class Servo:
    def __init__(self, duty=DUTY_MIN):
        self.duty = duty

    def set_duty(self, duty):
        if(duty >= DUTY_MIN and duty <= DUTY_MAX):
            self.duty = duty

    def set_position(self, position):
        if(position >= POS_MIN and position <= POS_MAX):
            duty = DUTY_MIN + (position-POS_MIN)*(DUTY_MAX-DUTY_MIN)/(POS_MAX-POS_MIN)
            self.duty = duty

    def get_duty(self):
        return self.duty

    def to_position(self):
        position = POS_MIN + (self.duty-DUTY_MIN)*(POS_MAX-POS_MIN)/(DUTY_MAX-DUTY_MIN)
        return position

class RootResource:
    def on_get(self, req, resp):
        position = req.get_param('position')
        duty = int(open('/var/www/api/servo.conf', 'r').read())
        servo = Servo(duty)
        if (position):
            servo.set_position(position)
            open('/var/www/api/servo.conf', 'w').write('{}'.format(servo.to_duty()))
            subprocess.call('/var/www/api/pwm')
            resp.media = {'duty': '{}'.format(servo.get_duty()),
                          'position': '{}'.format(servo.to_position())}
        else:
            resp.media = {'duty': '{}'.format(duty),
                          'position': '{}'.format(position)}

api = falcon.API()
api.add_route('/', RootResource())

if __name__ == '__main__':
  from wsgiref import simple_server
  httpd = simple_server.make_server("127.0.0.1", 11112, api)
  httpd.serve_forever()
