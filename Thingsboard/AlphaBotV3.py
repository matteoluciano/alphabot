import RPi.GPIO as GPIO
import time


class AlphaBot(object):

    def __init__(self, in1=12, in2=13, ena=6, in3=20, in4=21, enb=26,
                 ir_left=19, ir_right=16):
        self.IN1 = in1
        self.IN2 = in2
        self.IN3 = in3
        self.IN4 = in4
        self.ENA = ena
        self.ENB = enb
        self.IR_LEFT  = ir_left
        self.IR_RIGHT = ir_right

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        for pin in (self.IN1, self.IN2, self.IN3, self.IN4,
                    self.ENA, self.ENB):
            GPIO.setup(pin, GPIO.OUT)
        GPIO.setup(self.IR_LEFT,  GPIO.IN)
        GPIO.setup(self.IR_RIGHT, GPIO.IN)

        self.PWMA = GPIO.PWM(self.ENA, 500)
        self.PWMB = GPIO.PWM(self.ENB, 500)
        self.PWMA.start(50)
        self.PWMB.start(50)

    # ── Movimento continuo (t=0 → non si ferma da solo) ─────────────────────

    def forward(self, t=0):
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
        if t:
            time.sleep(t)
            self.stop()

    def backward(self, t=0):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        if t:
            time.sleep(t)
            self.stop()

    def left(self, t=0):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
        if t:
            time.sleep(t)
            self.stop()

    def right(self, t=0):
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        if t:
            time.sleep(t)
            self.stop()

    def stop(self):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)

    # ── PWM ─────────────────────────────────────────────────────────────────

    def setPWMA(self, value):
        self.PWMA.ChangeDutyCycle(value)

    def setPWMB(self, value):
        self.PWMB.ChangeDutyCycle(value)

    def setMotor(self, left, right):
        if 0 <= right <= 100:
            GPIO.output(self.IN1, GPIO.HIGH)
            GPIO.output(self.IN2, GPIO.LOW)
            self.PWMA.ChangeDutyCycle(right)
        elif -100 <= right < 0:
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.HIGH)
            self.PWMA.ChangeDutyCycle(-right)
        if 0 <= left <= 100:
            GPIO.output(self.IN3, GPIO.HIGH)
            GPIO.output(self.IN4, GPIO.LOW)
            self.PWMB.ChangeDutyCycle(left)
        elif -100 <= left < 0:
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.HIGH)
            self.PWMB.ChangeDutyCycle(-left)

    # ── Sensori IR ───────────────────────────────────────────────────────────

    def left_sensor(self):
        """True se ostacolo rilevato a sinistra."""
        return GPIO.input(self.IR_LEFT) == 0

    def right_sensor(self):
        """True se ostacolo rilevato a destra."""
        return GPIO.input(self.IR_RIGHT) == 0

    # ── Figure (versione non-bloccante con t fisso) ──────────────────────────

    def cerchio(self):
        for _ in range(16):
            self.forward(0.6)
            self.left(0.2)

    def quadrato(self):
        for _ in range(4):
            self.forward(2)
            self.left(0.28)

    def triangolo(self):
        for _ in range(3):
            self.forward(2)
            self.left(0.42)