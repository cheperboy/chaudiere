import serial.tools.list_ports

STRING_PROG_PORT = 'Prog. Port'
STRING_ARDUINO_PORT = 'Arduino Due'

def find_usb_ports():
    ports = list(serial.tools.list_ports.comports())
    return ports

def find_arduino_ports():
    arduino_ports = []
    usb_ports = find_usb_ports()
    for p in usb_ports:
        if (str(p).find(STRING_ARDUINO_PORT) > 0):
            arduino_ports.append(str(find_portname(p)))
    return arduino_ports
    
def prog_port():
    usb_ports = find_usb_ports()
    for p in usb_ports:
        if (str(p).find(STRING_PROG_PORT) > 0):
            return str(find_portname(p))
        
def native_port():
    arduino_ports = find_arduino_ports()
    for p in arduino_ports:
        if (str(p).find(STRING_PROG_PORT) < 0):
            return str(find_portname(p))
        
def find_portname(port_info):
    port = str(port_info).split(' ')[0]
    return port

def print_ports():
    ports = find_usb_ports()
    print ('All Ports : ')
    for p in ports:
        print p
    print ('')

    ports = find_arduino_ports()
    print ('Arduino Ports : ')
    for p in ports:
        print p
    print ('')

    port = prog_port()
    print ('Prog port : ')
    print port
    print ('')

    port = native_port()
    print ('Native port : ')
    print (port)

if __name__ == '__main__':
    print_ports()