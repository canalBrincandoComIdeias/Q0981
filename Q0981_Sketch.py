#     AUTOR:    BrincandoComIdeias
#     APRENDA:  https://cursodearduino.net/
#     SKETCH:   Bluetooth
#     DATA:     16/01/23

from machine import Pin, PWM
from utime import sleep_ms as delay
from utime import sleep_us as delayMicroseconds
from utime import ticks_ms as millis
from machine import time_pulse_us as pulseIn

# Importando a comunicação Serial (UART)
from machine import UART

# Configurando Porta Serial na UART 0 - pinos 0 (TX) e 1 (RX)
Serial = UART(0, 9600)

# Configurando os pinos do HCSR04
pinTrig = Pin(17, Pin.OUT)
pinEcho = Pin(16, Pin.IN)

# Configurando pinos dos motores como OUTPUT
pinIn1 = Pin(5, Pin.OUT)
pinIn2 = Pin(4, Pin.OUT)
pinIn3 = Pin(3, Pin.OUT)
pinIn4 = Pin(2, Pin.OUT)

# Configurando PWM nos pinos dos motores
motorEsq1 = PWM(pinIn1)
motorEsq2 = PWM(pinIn2)
motorDir1 = PWM(pinIn3)
motorDir2 = PWM(pinIn4)

# Frequencia do PWM Arduino portas 3, 9, 10 e 11
motorEsq1.freq(490)
motorEsq2.freq(490)
motorDir1.freq(490)
motorDir2.freq(490)

# Equivalente a função map()
def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

# Função para converter a velocidade de 0 a 100 em pulso PWM 16 bits
def pulsoMotor(velocidade):
    return map(velocidade, 0, 100, 0, 65534)

# Funções para mover o robo
def paraFrente():
    pulso = pulsoMotor(35)
    
    motorEsq1.duty_u16(pulso)
    motorEsq2.duty_u16(0)
    
    motorDir1.duty_u16(pulso)
    motorDir2.duty_u16(0)

def parar():
    motorEsq1.duty_u16(0)
    motorEsq2.duty_u16(0)
    
    motorDir1.duty_u16(0)
    motorDir2.duty_u16(0)

def virar():
    pulso = pulsoMotor(55)
    
    parar()
    delay(200)
    
    motorEsq1.duty_u16(pulso)
    motorEsq2.duty_u16(0)
    
    motorDir1.duty_u16(0)
    motorDir2.duty_u16(pulso)
    
    delay(350)
    parar()
    delay(500)
    
# Função para ler a distancia
def medir():
    pinTrig.value(0)
    delayMicroseconds(5)
    pinTrig.value(1)
    delayMicroseconds(10)
    pinTrig.value(0)
    
    # Duração do pulso em uS
    duracao = pulseIn(pinEcho, 1, 20000)
    
    if duracao < 0:
        print("timeout")
        return (-1)
    
    # Tempo em Segundos
    tempo = duracao / 1000000
    
    # Distancia em CM
    dist = (tempo * 34000) / 2
    return round(dist, 1)

# Delay de 2 segundos para começar o "loop"
parar()
delay(2000)

tempo = 0

while True:
    if millis() - tempo > 250:
        distancia = medir()    
        Serial.write(f"Dist: {distancia}cm\n")
        tempo = millis()
    
    if distancia > 10:
        paraFrente()

    elif distancia > 0:
        virar()
        Serial.write("Objeto a frente!\n")
        
    else:
        parar()
        delay(500)
        Serial.write("Erro de leitura\n")
        