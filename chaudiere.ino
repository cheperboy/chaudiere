#include "EmonLib.h" // https://github.com/openenergymonitor/EmonLib
#define NSENSORS 3
#define STARTPIN 6

EnergyMonitor emon[STARTPIN-NSENSORS];
int irms[STARTPIN-NSENSORS];

const int const_voltage = 234;
const int const_calib = 110;
const int const_irms = 1480;

void setup(){
	Serial.begin(9600);
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
	}
	Serial.print(crc);
	Serial.print(";");
	Serial.println();
	delay(700);
}


