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

class MBL_Osc_Out
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
		message.addFloatArg(progress);
		bundle.addMessage(message);
		
		message.clear();
		message.setAddress("/HD/NumHeadsets");
		message.addIntArg(numHeadSets);
		bundle.addMessage(message);
		
		message.clear();
		message.setAddress("/HD/Correlation");
		message.addFloatArg(correlation);
		bundle.addMessage(message);
		
		message.clear();
		message.setAddress("/HD/Score");
		message.addFloatArg(score);
		bundle.addMessage(message);
		
		message.clear();
		message.setAddress("/HD/Power");
		message.addFloatArg(power1);
		message.addFloatArg(power2);
		bundle.addMessage(message);
		
		oscSenderA.sendBundle(bundle);
		oscSenderV.sendBundle(bundle);
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
	
	void	setStatus(int _scene, float _time, float _progress) {
		scene		= _scene;
		time		= _time;
		progress	= _progress;
	}
	
	void	setNumHeadsets(int _numHeadsets)	{ numHeadSets = _numHeadsets; }
	
	void	setCorrelation(float _value)		{ correlation	= _value; }
	void 	setScore(float _value)				{ score			= _value; }
	void 	setPower1(float _value)				{ power1		= _value; }
	void 	setPower2(float _value)				{ power2		= _value; }
	
protected:
	
	ofxOscSender	oscSenderA;
	ofxOscSender	oscSenderV;
	ofxOscMessage	message;
	ofxOscBundle	bundle;
	
	int		scene;
	float	time, progress;
	int		numHeadSets;
	
	float	correlation;
	int		score;
	float	power1, power2;
	
};
