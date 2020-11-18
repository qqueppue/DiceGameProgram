#-*- coding:utf-8 -*-
from flask import Flask, render_template
import RPi.GPIO as GPIO
import time
import datetime
import random

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

#Switch
GPIO.setup(14, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
#LED
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)

@app.route("/")
def inputPin():
    mean = 0            #Swtich Press Value
    win = 0             #Dice Game Winner Value
    ERROR = "Pin Error" #except Value
    
    GPIO.output(17, False)
    GPIO.output(27, False)
    
    #Dice Number Random Value
    rand1 = random.randrange(1,7)
    rand2 = random.randrange(1,7)
    
    #Dice, Select Winner
    if rand1 > rand2:
        win = 'player1win'
    elif rand1 < rand2:
        win = 'player2win'
    else:
        win = 'draw'

    #Switch, Select Winner
    if GPIO.input(14):
        try:
            mean = 'player2win'
        except:
            ERROR
    elif GPIO.input(18):
        try:
            mean = 'draw'
        except:
            ERROR  
    elif GPIO.input(23):
        try:
            mean = 'player1win'
        except:
            ERROR    
    else:
        mean = 'No Signal'
    
    #LED Control (Corrct -> Green LED on / Incorrect -> Red LED on)
    if mean == win:
        response = "True"
        GPIO.output(17, True)
        time.sleep(1)
        GPIO.output(17, False)
    else:
        response = "False"
        GPIO.output(27, True)
        time.sleep(1)
        GPIO.output(27, False)
        
    templateData = {
        'rand1' : rand1,
        'rand2' : rand2,
        'win' : win,
        'response' : response,
        'mean' : mean
    }
    return render_template('dice.html', **templateData)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
