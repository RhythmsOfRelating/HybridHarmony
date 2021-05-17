#pragma once

#include "ofMain.h"

#include "ofxGui.h"
#include "ofxMonitorInfo.h"

#include "MBL_OSC_Receiver.h"
#include "MBL_Visuals.h"


class ofApp : public ofBaseApp{
	
public:
	void setup();
	void update();
	void draw();
	
	MBL_OSC_Receiver oscReceiver;
	MBL_Visuals		visuals;
	
	ofParameterGroup settings;
	ofxPanel gui;
	ofParameter<bool> toggleGui;
	void setupGui();
	void minimizeGui(ofxGuiGroup* _group);
	ofxGuiGroup		inputs;
	ofParameter<float>	pCorrelation;
	ofParameter<int>	pScore;
	ofParameter<float>	pPower1;
	ofParameter<float>	pPower2;
	ofParameter<int>	pScene;
	ofParameter<float>	pPosition;
	
	ofxMonitorInfo screens;
	ofParameter<int> screenId;
	void screenIdListener(int& _value);
	ofParameter<bool> toggleFullscreen;
	void toggleFullscreenListener(bool& _value);
	float windowWidth, windowHeight;
	bool initFullScreen;
	ofParameter<bool>	toggleReset;
	void				toggleResetListener(bool& _value) { if (_value) { ; } }
	
	
	void keyPressed(int key);
	void keyReleased(int key);
	void mouseMoved(int x, int y );
	void mouseDragged(int x, int y, int button);
	void mousePressed(int x, int y, int button);
	void mouseReleased(int x, int y, int button);
	void mouseEntered(int x, int y);
	void mouseExited(int x, int y);
	void windowResized(int w, int h);
	void dragEvent(ofDragInfo dragInfo);
	void gotMessage(ofMessage msg);
	
};

