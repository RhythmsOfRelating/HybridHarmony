#pragma once
#include "ofMain.h"
#include "ofxOsc.h"

class HD_OSC_Receiver
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
			
			else if (adress == "/HD/GroupR") {
				groupR = message.getArgAsFloat(0);
			}
			
			else if (adress == "/HD/ColorR") {
				purpleR = message.getArgAsFloat(0);
				orangeR = message.getArgAsFloat(1);
				greenR = message.getArgAsFloat(2);
				blueR = message.getArgAsFloat(3);
			}
			
			else if (adress == "/HD/Hub/R") {
				hubR = message.getArgAsFloat(0);
			}
			
			else if (adress == "/HD/Hub/Color") {
				hubColor = message.getArgAsString(0);
			}
			
			else if (adress == "/HD/HighPair/R") {
				highR = message.getArgAsFloat(0);
			}
			
			else if (adress == "/HD/HighPair/Colors") {
				highPair.first = message.getArgAsString(0);
				highPair.second = message.getArgAsString(1);
			}
			
			else if (adress == "/HD/LowPair/R") {
				lowR = message.getArgAsFloat(0);
			}
			
			else if (adress == "/HD/LowPair/Colors") {
				lowPair.first = message.getArgAsString(0);
				lowPair.second = message.getArgAsString(1);
			}
		}
	}
	
	void	reset() {
		scene = 0;
		progress = 0;
		time = 0;
		numHeadSets = 0;
		
		groupR = 0;
		orangeR = 0;
		purpleR = 0;
		blueR = 0;
		greenR = 0;
		hubColor = "none";
		highPair.first = "none";
		highPair.second = "none";
		lowPair.first = "none";
		lowPair.second  = "none";
	}
	
	int		getScene()				{ return scene; }
	float	getTime()				{ return time; }
	float	getProgress()			{ return progress; }
	
	int		getNumHeadsets()		{ return numHeadSets; }
	
	float	getGroupCorrelation()	{ return groupR; }
	float	getHubCorrelation()		{ return hubR; }
	float	getHighCorrelation()	{ return highR; }
	float	getLowCorrelation()		{ return lowR; }
	float	getPurpleCorrelation()	{ return purpleR; }
	float	getOrangeCorrelation()	{ return orangeR; }
	float	getGreenCorrelation()	{ return greenR; }
	float	getBlueCorrelation()	{ return blueR; }
	
	string	getHub()					{ return hubColor; }
	pair<string,string>	getHighPair()	{ return highPair; }
	pair<string,string>	getLowPair()	{ return lowPair; }
	
protected:
	
	ofxOscReceiver	oscReceiver;
	ofxOscMessage	message;
	
	int		scene;
	float	time, progress;
	int		numHeadSets;
	
	float	groupR;
	float	orangeR, purpleR, blueR, greenR;
	float	hubR, highR, lowR;
	
	string	hubColor;
	pair<string,string>	highPair, lowPair;
	
};
