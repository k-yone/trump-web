from flask import Flask, render_template, request, jsonify
import subprocess

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
            duty = DUTY_MAX - 1.0*(position-POS_MIN)*(DUTY_MAX-DUTY_MIN)/(POS_MAX-POS_MIN)
            self.duty = int(round(duty))

    def get_duty(self):
        return self.duty

    def to_position(self):
        position = POS_MIN + 1.0*(DUTY_MAX-self.duty)*(POS_MAX-POS_MIN)/(DUTY_MAX-DUTY_MIN)
        return int(round(position))

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/servo")
def servo_route():
    position = request.args.get('position')
    duty = int(float(open('/var/www/html/servo.conf', 'r').read()))
    servo = Servo(duty)
    if (position):
        servo.set_position(int(position))
        open('/var/www/html/servo.conf', 'w').write('{}'.format(servo.get_duty()))
        subprocess.call('/var/www/html/pwm')
        ret = {'duty': '{}'.format(servo.get_duty()),
               'position': '{}'.format(servo.to_position())}
    else:
        ret = {'duty': '{}'.format(servo.get_duty()),
               'position': '{}'.format(servo.to_position())}
    return jsonify(ResultSet=ret)

@app.route("/light")
def light_route():
    mode = request.args.get('mode')
    if (mode):
        open('/var/www/html/light.conf', 'w').write('{}'.format(mode))
        subprocess.call('/var/www/html/light')
        ret = {'mode': '{}'.format(mode)}
    else:
        mode = int(float(open('/var/www/html/light.conf', 'r').read()))
        ret = {'mode': '{}'.format(mode)}
    return jsonify(ResultSet=ret)

if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=11113)
