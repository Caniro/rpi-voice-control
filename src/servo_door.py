from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory

class ServoDoor:
    def __init__(self, pin):
        factory = PiGPIOFactory(host='localhost')
        self.servo = AngularServo(pin, pin_factory=factory,
                            min_angle=90, max_angle=-90,
                            min_pulse_width=0.00045, max_pulse_width=0.0023)

    def open(self):
        self.servo.angle = 90
        print('문을 열었습니다.')

    def close(self):
        self.servo.angle = 0
        print('문을 닫았습니다.')
