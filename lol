
c0nrad's corner

    Home
    Projects
    About Me

Welcome!

Welcome to c0nrad's c0rner! The website is still in it's very early stages of development, but please bear with me as I get it operational. When complete, this website should give you a view into the projects I'm working on, and hopefully inspire new projects to be started. If you have any questions or comments, please feel free to email me at poptarts4liffe@gmail.com.

View Current Project »
1-8-13 natas15

If anyone is into wargames, natas is a really fun way to brush up your skills. Each level consist of a little problem, and you have to "hack" your way through to find the next level's password. Currently there are 17 levels, and they get pretty difficult. (http://www.overthewire.org/wargames/natas/).

This source code is the solution to level 15. A blind sql injector. Since you can't just dump the password directly, you have to go through and figure it out character by character.
Sauce: sauce

12-30-12 c0nzip

Just wrote this little script to decompress arbitrary file compression types.
Usage:

Usage: c0nzip -f 

Options:
    -h, --help         show this help message and exit
    -f COMPRESSEDFILE  specify a compressed file
    -e FILEEXTENSION   specify the file extension
	  

Source Code
9-29-12 RC4 Implemnetation

A little while ago, a friend and I wrote our own RC4 implementations to communicate to each other publically without another friend knowing what we were saying. Here's the implementation in C++.

/******************************************************************
 * Project: RC4
 * Author: Stuart C. Larsen (with thanks to Kevin Vece for debug)
 *
 *    A simple RC4 implementation in C++. Reads a file from
 * either STDIN or from file and writes to STDOUT the encypted
 * or decrypted text.
 *
 * Usage:
 *    rc4 < infile > outfile
 *
 * Example:
 *    make
 *    rc4 < myPic.jpg > enc.data
 *    rc4 < enc.data > myOrigPic.jpg
 *******************************************************************/
#include iostream
#include cstdlib
#include cstring
#include fstream
using namespace std;

/* The key used to encrypt/decrypt files! */
char key[] = "cybears";

/* Some globals to simplify code */
unsigned char S[256];
int StreamSize;

void swap(unsigned char *s, int i, int j) {
	unsigned char temp = s[i];
	s[i] = s[j];
	s[j] = temp;
}

unsigned char* KSA(int sizeOfKey) {
	int i = 0, j = 0;
	for(i = 0; i < 256; ++i) {
		j = (j + S[i] + key[i % sizeOfKey]) % 256;
		swap(S,i, j);
	}
	return S;
}

unsigned char* PRGA(int lengthOfStream) {
	int i = 0,j = 0;
	unsigned char* output = new unsigned char[lengthOfStream];	
	for (int x = 0; x < lengthOfStream; ++x) {
		i = (i + 1) % 256;
		j = (j + S[i]) % 256;
		swap(S, i, j);
		output[x] = S[(S[i] + S[j]) % 256];
	}
	return output;
}

unsigned char* XOR(unsigned char* keyStream, const char* plainText) {
	unsigned char* output = new unsigned char[StreamSize];
	for (unsigned int x = 0; x < (unsigned int)StreamSize; ++x)
		output[x] = plainText[x] ^ keyStream[x];
	return output;
}

const char* readStdin() {
	char byte;
	string data = "";
	while(!cin.eof()) {
		cin.get(byte);
		data += byte;
	}
	data = data.substr(0, data.length() -1 ); // Annoying little fix
	return data.c_str();
}

const char* readFromFile(char* fileName) {
	char * data;

	ifstream file (fileName, ios::in|ios::binary|ios::ate);
	if (file.is_open()) {
		StreamSize = (int)file.tellg();
		data = new char [StreamSize];
		file.seekg (0, ios::beg);
		file.read (data, StreamSize);
		file.close();
	} else 
		cout << "Unable to open file";
	return data;
}
		
int main(int argc, char* argv[]) {
	const char* plainText;
	if (argc >= 2) {
		plainText = readFromFile(argv[1]);
	} else
		plainText = readStdin();

	for (int x = 0; x < 256; ++x)
		S[x] = x;

	KSA(strlen(key));
	unsigned char* prga = PRGA(StreamSize);
	unsigned char* encrypted = XOR(prga, plainText);

	for (unsigned int x = 0; x < (unsigned int)StreamSize ; ++x)
		cout << encrypted[x];

	return 0;
}
			

6-22-12 Motors came in!

I ordered some small hobbiest DC motors a little awhile ago ([1.4,4.5], [12,24], [12,30], [6, 24])V, and they finally game in. I also found some knex parts that sort of looks like tank treads. So, I put them together and wha-lah! Possibly Wilfred will be using tank treads in the new future.

The wheel/chain are moving, hence the slight blur.
6-18-12 New Project: ConWatch

Just started a new project, ConWatch. I'm having fun programming the MSP430, and decided to build something with it. As of right now, I am able to control one 7-seg display.
6-15-12 Wilfred Frustration

Maybe I'm just retarded, but I'm having a really hard time getting the arduino IDE to work correctly with my Bluetooth slave. I can't upload code without physically unplugging the bluetooth module, and even then uploading code is iffy. The bluetooth module says it's connected to something, (I think it's connected to my phone), but it says it isn't recieving any information. This is the arduino code I'm using:

#include "MotorDriver.h"

char mDirection = 0, mSpeed = 5, nullByte;

// Must be PWM pins
int RIGHT_MOTOR_PIN_1 = 5;
int RIGHT_MOTOR_PIN_2 = 6;
int LEFT_MOTOR_PIN_1 = 10;
int LEFT_MOTOR_PIN_2 = 11;

MotorDriver rightMotorDriver(RIGHT_MOTOR_PIN_1, RIGHT_MOTOR_PIN_2);
MotorDriver leftMotorDriver(LEFT_MOTOR_PIN_1, LEFT_MOTOR_PIN_2);

void setup() {
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    mDirection = Serial.read();
    mSpeed = Serial.read();
    nullByte = Serial.read();
    
    switch (mDirection) {
      case 'F':
	rightMotorDriver.rotateForwardFull();
	//rightMotorDriver.rotateForward((mSpeed - '0') * 25);
	leftMotorDriver.rotateForward((mSpeed - '0') * 25);
	break;
      case 'R':
	rightMotorDriver.rotateForward((mSpeed - '0') * 25);
	leftMotorDriver.rotateReverse((mSpeed - '0') * 25);
	 break;
      case 'L':
	 rightMotorDriver.rotateReverse((mSpeed - '0') * 25);
	 leftMotorDriver.rotateForward((mSpeed - '0') * 25); 
	 break;
      case 'B':
	  rightMotorDriver.rotateReverse((mSpeed - '0') * 25);
	  leftMotorDriver.rotateReverse((mSpeed - '0') * 25);
	  break;
    }
    delay(100);
  
  }
}
			

6-13-12 Website is up

c0nrad's c0rner is up!

© c0nrad's Corner
