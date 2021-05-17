#pragma once
#include "ofMain.h"
#include "ofxOsc.h"

class MBL_OSC_Receiver
{
public:
	void setup(int _port = 9001) {
		oscReceiver.setup(_port);
		ofLog() << "listening for osc messages on port " << _port;
	}
	
	void	update() {
		
		while(oscReceiver.hasWaitingMessages()){
			oscReceiver.getNextMessage(message);
			
			string adress = message.getAddress();
			
			if (adress == "/HD/Status/Scene") {
				scene = message.getArgAsInt(0);
			}
			
			else if (adress == "/HD/Status/Time") {
				time = message.getArgAsFloat(0);
				progress = message.getArgAsFloat(1);
			}
			
			else if (adress == "/HD/NumHeadsets") {
				numHeadSets = message.getArgAsInt32(0);
			}
			
			else if (adress == "/HD/Correlation") {
				correlation = message.getArgAsFloat(0);
			}
			
			else if (adress == "/HD/Score") {
				score = message.getArgAsFloat(0);
			}
			
			else if (adress == "/HD/Power") {
				power1 = message.getArgAsFloat(0);
				power2 = message.getArgAsFloat(1);
			}
		}
	}
	
	void	reset() {
		scene = 0;
		progress = 0;
		time = 0;
		numHeadSets = 0;
		
		correlation = 0;
		score = 0;
		power1 = 0;
		power2 = 0;
	}
	
	int		getScene()			{ return scene; }
	float	getTime()			{ return time; }
	float	getProgress()		{ return progress; }
	
	int		getNumHeadsets()	{ return numHeadSets; }
	
	float	getCorrelation()	{ return correlation; }
	float	getScore()			{ return score; }
	float	getPower1()			{ return power1; }
	float	getPower2()			{ return power2; }
	
protected:
	
	ofxOscReceiver	oscReceiver;
	ofxOscMessage	message;
	
	int		scene;
	float	time, progress;
	int		numHeadSets;
	
	float	correlation;
	int		score;
	float	power1, power2;
	
};
