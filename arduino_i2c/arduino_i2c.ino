#include <Wire.h>

#define SLAVE_ADDRESS 0x12
int dataReceived = 0;

void setup() {
    delay(1*1000);
    Serial.begin(9600);		// /tty/ACM0
    SerialUSB.begin(9600); 	// /tty/AMA0
    Wire.begin(SLAVE_ADDRESS);
    Wire.onReceive(receiveData);
    Wire.onRequest(sendData);
}

void loop() {
    delay(100);
    Serial.println("Prog port up");
    delay(100);
    SerialUSB.println("Native port up");
}

void receiveData(int byteCount){
    while(Wire.available()) {
        dataReceived = Wire.read();
        Serial.print("Donnee recue : ");
        Serial.println(dataReceived);
    }
}

void sendData(){
    int envoi = dataReceived + 1;
    Wire.write(envoi);
}
