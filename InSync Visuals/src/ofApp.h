#pragma once

#include "ofMain.h"

#include "ofxGui.h"
#include "ofxMonitorInfo.h"

#include "HD_OSC_Receiver.h"
#include "HD_InteractiveLayout.h"

#include "HD_Visuals.h"

class ofApp : public ofBaseApp{
	
public:
	void setup();
	void update();
	void draw();
	
	void updateLayout();
	
	HD_OSC_Receiver oscReceiver;
	HD_InteractiveLayout tableLayout;
	
	HD_Visuals visuals;
	
	ofParameterGroup settings;
	ofxPanel gui;
	ofParameter<bool> toggleGui;
	void setupGui();
	void minimizeGui(ofxGuiGroup* _group);
	
	ofxMonitorInfo screens;
	ofParameter<int> screenId;
	void screenIdListener(int& _value);
	ofParameter<bool> toggleFullscreen;
	void toggleFullscreenListener(bool& _value);
	float windowWidth, windowHeight;
	bool initFullScreen;
	ofParameter<bool>	toggleReset;
	void				toggleResetListener(bool& _value) { if (_value) { _value = false; visuals.reset(); visuals.setMask(tableLayout.getMask());} }
	ofParameter<bool>	toggleSimpleMode;
	
	
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

