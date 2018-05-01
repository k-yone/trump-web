import falcon
import json
import subprocess

DUTY_BIN = 25
DUTY_MAX = 225
DUTY_MIN = 100

class RootResource:
    def on_get(self, req, resp):
        action = req.get_param('action')
        duty = int(open('/var/www/api/servo.conf', 'r').read())
        if(action == 'swing-left'):
            duty += DUTY_BIN
            if(duty > DUTY_MAX):
                duty = DUTY_MAX
        if(action == 'swing-right'):
            duty -= DUTY_BIN
            if(duty < DUTY_MIN):
                duty = DUTY_MIN
        open('/var/www/api/servo.conf', 'w').write('{}'.format(duty))
        subprocess.call('/var/www/api/pwm')
        resp.media = {'duty': '{}'.format(duty)}

api = falcon.API()
api.add_route('/', RootResource())

if __name__ == '__main__':
  from wsgiref import simple_server
  httpd = simple_server.make_server("127.0.0.1", 11112, api)
  httpd.serve_forever()

