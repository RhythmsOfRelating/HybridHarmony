//
//  epocSaveData.h
//  MWMData
//
//  Created by Ties East on 26/7/13.
//
//
#pragma once
#include "ofMain.h"
#include "ofxOsc.h"

class HD_Osc_Out
{
public:
	void setup(string _hostA = "localhost", int _portA = 9000, string _hostV = "localhost", int _portV = 9001) {
		oscSenderA.setup(_hostA, _portA);
		oscSenderV.setup(_hostV, _portV);
		ofLogNotice("sending osc Audio messages to adress: " + string(_hostA) + " @ port: " + ofToString(_portA));
		ofLogNotice("sending osc Video messages to adress: " + string(_hostV) + " @ port: " + ofToString(_portV));
		reset();
	}
	
	void	update() {
		bundle.clear();
		
		message.clear();
		message.setAddress("/HD/Status/Scene");
		message.addIntArg(scene);
		bundle.addMessage(message);
		
		message.clear();
		message.setAddress("/HD/Status/Time");
		message.addFloatArg(time);
		message.addFloatArg(position);
		bundle.addMessage(message);
		
		message.clear();
		message.setAddress("/HD/NumHeadsets");
		message.addIntArg(numHeadSets);
		bundle.addMessage(message);
		
		message.clear();
		message.setAddress("/HD/GroupR");
		message.addFloatArg(groupR);
		bundle.addMessage(message);
		
		message.clear();
		message.setAddress("/HD/ColorR");
		message.addFloatArg(purpleR);
		message.addFloatArg(orangeR);
		message.addFloatArg(greenR);
		message.addFloatArg(blueR);
		bundle.addMessage(message);
		
		message.clear();
		message.setAddress("/HD/Hub/R");
		message.addFloatArg(hubR);
		bundle.addMessage(message);
		
		message.clear();
		message.setAddress("/HD/Hub/Color");
		message.addStringArg(hubColor);
		bundle.addMessage(message);
		
		message.clear();
		message.setAddress("/HD/HighPair/R");
		message.addFloatArg(highR);
		bundle.addMessage(message);
		
		message.clear();
		message.setAddress("/HD/HighPair/Colors");
		message.addStringArg(highPair.first);
		message.addStringArg(highPair.second);
		bundle.addMessage(message);
		
		message.clear();
		message.setAddress("/HD/LowPair/R");
		message.addFloatArg(lowR);
		bundle.addMessage(message);
		
		message.clear();
		message.setAddress("/HD/LowPair/Colors");
		message.addStringArg(lowPair.first);
		message.addStringArg(lowPair.second);
		bundle.addMessage(message);
		
		oscSenderA.sendBundle(bundle);
		oscSenderV.sendBundle(bundle);
	}
	
	void	reset() {
		scene = 0;
		position = 0;
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
	
	void	setStatus(int _scene, float _time, float _position) {
		scene		= _scene;
		time		= _time;
		position	= _position;
	}
	
	void	setNumHeadsets(int _numHeadsets)		{ numHeadSets = _numHeadsets; }
	
	void	setGroupCorrelation(float _R)			{ groupR	= _R; }
	void 	setHubCorrelation(float _R)				{ hubR		= _R; }
	void 	setHighCorrelation(float _R)			{ highR		= _R; }
	void 	setLowCorrelation(float _R)				{ lowR		= _R; }
	void	setPurpleCorrelation(float _R)			{ purpleR	= _R; }
	void	setOrangeCorrelation(float _R)			{ orangeR	= _R; }
	void	setGreenCorrelation(float _R)			{ greenR	= _R; }
	void	setBlueCorrelation(float _R)			{ blueR		= _R; }
	
	void 	setHub(string _color)					{ hubColor	= _color; }
	void 	setHighPair(pair<string,string> _pair)	{ highPair	= _pair; }
	void 	setLowPair(pair<string,string> _pair)	{ lowPair	= _pair; }
	
protected:
	
	ofxOscSender	oscSenderA;
	ofxOscSender	oscSenderV;
	ofxOscMessage	message;
	ofxOscBundle	bundle;
	
	int		scene;
	float	time, position;
	int 	numHeadSets;
	
	float	groupR;
	float	orangeR, purpleR, blueR, greenR;
	float	hubR, highR, lowR;
	
	string	hubColor;
	pair<string,string>	highPair, lowPair;
	
};
