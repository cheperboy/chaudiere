import smbus2 as smbus
import time

# Remplacer 0 par 1 si nouveau Raspberry
bus = smbus.SMBus(1)
address = 0x12

print "1 + 1 = "
bus.write_byte(address, 1)
# Pause de 1 seconde pour laisser le temps au traitement de se faire
time.sleep(1)
reponse = bus.read_byte(address)
print "La reponse de l'arduino : ", reponse
