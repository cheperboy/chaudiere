#include "EmonLib.h" // https://github.com/openenergymonitor/EmonLib
#define NSENSORS 4
#define STARTPIN 5

EnergyMonitor emon[NSENSORS]; //declare un tab de 0 à 3. taille 4
int irms[NSENSORS];

const int const_voltage = 234;
//const int const_calib = 110;
const int const_calib = 29;// Current: input pin, calibration. Cur Const= Ratio/BurdenR. 1800/62 = 29
const int const_irms = 1480;  

void setup(){
	Serial.begin(9600);	// Programming USB
	delay(100);
    SerialUSB.begin(9600); 	// Native USB
	delay(100);
	for(int i=0; i<NSENSORS; i++) { 
		emon[i].current(STARTPIN + i, const_calib);
	}
	delete_first_readings();
}

void print_serial(){
	int crc = 0;
	
	for(int i=0; i<NSENSORS; i++) {
		irms[i] = int(emon[i].calcIrms(const_irms)*const_voltage);
		delay(20);
		crc += irms[i];
	}
	for(int i=0; i<NSENSORS; i++) {
		Serial.print(irms[i]);
		Serial.print(";");
		delay(100);
		SerialUSB.print(irms[i]);
		SerialUSB.print(";");
		delay(100);
	}
	Serial.print(crc);
	Serial.print(";");
	Serial.println();
	delay(100);
	SerialUSB.print(crc);
	SerialUSB.print(";");
	SerialUSB.println();
	delay(1000);
}

void delete_first_readings(){
	for(int j=0; j<12; j++) {
		for(int i=0; i<NSENSORS; i++) {
			irms[i] = int(emon[i].calcIrms(const_irms)*const_voltage);
			delay(20);
		}
		delay(300);
	}
}

void loop(){
	print_serial();
}


