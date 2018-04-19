#include "EmonLib.h" // https://github.com/openenergymonitor/EmonLib
#define NSENSORS 3
#define STARTPIN 6

EnergyMonitor emon[STARTPIN-NSENSORS];
int irms[STARTPIN-NSENSORS];

const int const_voltage = 234;
const int const_calib = 110;
const int const_irms = 1480;

void setup(){
	Serial.begin(9600);		// Programming USB
    SerialUSB.begin(9600); 	// Native USB
	for(int i=STARTPIN; i<STARTPIN+NSENSORS; i++) {
		emon[i].current(i, const_calib);
	}
}

void loop(){
	int crc = 0;
	
	for(int i=STARTPIN; i<STARTPIN+NSENSORS; i++) {
		irms[i] = int(emon[i].calcIrms(const_irms)*const_voltage);
		crc += irms[i];
	}
	for(int i=STARTPIN; i<STARTPIN+NSENSORS; i++) {
		Serial.print(irms[i]);
		Serial.print(";");
		SerialUSB.print(irms[i]);
		SerialUSB.print(";");
	}
	Serial.print(crc);
	Serial.print(";");
	Serial.println();
	SerialUSB.print(crc);
	SerialUSB.print(";");
	SerialUSB.println();
	delay(700);
}


