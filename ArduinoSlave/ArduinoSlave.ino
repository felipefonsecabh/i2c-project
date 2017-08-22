// Wire Slave Receiver
// by Nicholas Zambetti <http://www.zambetti.com>

// Demonstrates use of the Wire library
// Receives data as an I2C/TWI slave device
// Refer to the "Wire Master Writer" example for use with this

// Created 29 March 2006

// This example code is in the public domain.

#include <Wire.h>
byte data[12];
int command;

typedef struct processData{
  float temp1;
  float temp2;
  float temp3;
  float temp4;
  float vazao_quente;
  float vazao_fria;
  byte pump_speed;
  //bool  pump_status;
  byte bstatus;
  //bool heater_status;
  byte chksum;
};

typedef union I2C_Send{
  processData data;
  byte I2C_packet[sizeof(processData)];
};

//declaracao da variável de envio
I2C_Send send_info;


void parseValues(byte data[]){
  union float_tag{
    byte b[4];
    float fval;
  }ft;

  ft.b[0] =data[1];
  ft.b[1] = data[2];
  ft.b[2] = data[3];
  ft.b[3] = data[4];

  Serial.println(ft.fval);
}

int num;

//função para testar valores
void setrnddata();

void setup()
{
  Wire.begin(12);                // join i2c bus with address #4
  Wire.onReceive(receiveEvent); // register event
  Wire.onRequest(requestEvent);
  Serial.begin(9600);           // start serial for output
  setrnddata();
}

void loop()
{
  delay(100);
}

// function that executes whenever data is received from master
// this function is registered as an event, see setup()
void receiveEvent(int howMany)
{
  command = Wire.read();
  if (command==1){
    int i=0;
    while(1 <= Wire.available()) // loop through all but the last
    {
      data[i] = Wire.read(); // receive byte as a character
      i = i+1;
    }
    parseValues(data);
  }
}
  
void requestEvent()
{
    if(command==2){
      Wire.write(send_info.I2C_packet,sizeof(processData));
    }
}

void setrnddata(){
  send_info.data.temp1 = 10.2;
  send_info.data.temp2 = 5.3;
  send_info.data.temp3 = 4.8;
  send_info.data.temp4 = 10.7;
  send_info.data.vazao_quente = 25.1;
  send_info.data.vazao_fria = 12.4;
  send_info.data.pump_speed = 58;
  bitSet(send_info.data.bstatus,0);
  bitSet(send_info.data.bstatus,1);
  send_info.data.chksum = 27;
}

