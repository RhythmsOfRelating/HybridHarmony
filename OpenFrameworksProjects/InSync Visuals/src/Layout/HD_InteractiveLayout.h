#pragma once
#include "ofMain.h"
#include "HD_Layout.h"


const ofColor hubColor(ofColor(255, 255, 255));

class HD_InteractiveLayout: public HD_Layout {
public:
	
	void setup(int _width, int _height) override {
		HD_Layout::setup(_width, _height);
		
		colorR.resize(numPlayers,0);
		groupR = 0;
		highPair = {0,0};
		hub = -1;
		
		baseRadius = 0.02;
		power = 1.5;
	}
	
	void draw(int _x, int _y, int _w, int _h) override {
		HD_Mask::draw(_x, _y, _w, _h);
		ofPushStyle();
		ofPushView();
		ofTranslate(_x, _y);
		glm::vec2 scale = glm::vec2(_w, _h);
		ofEnableBlendMode(OF_BLENDMODE_DISABLED);
		
		for (int i=0; i<numPlayers; i++) {
			ofSetColor(colorColors[i]);
			ofDrawCircle(colorOrigins[i] * scale, windowHeight * baseRadius + windowHeight * colorRadius * powf(colorR[i], power));
		}
		ofSetColor(groupColor);
		ofDrawCircle(groupOrigin * scale, windowHeight * baseRadius + windowHeight * groupRadius * groupR);
		ofSetLineWidth(4);
		if (highPair.first != highPair.second) {
			ofDrawLine(colorOrigins[highPair.first] * scale , colorOrigins[highPair.second] * scale);
		}
		
		ofSetColor(hubColor);
		if (hub >= 0) {
			ofDrawCircle(colorOrigins[hub] * scale, windowHeight * baseRadius / 2.0);
			
		}
		ofPopView();
		ofPopStyle();
	}
	
	void setGroupR(float _value)	{ groupR = _value; }
	void setPurpleR(float _value)	{ colorR[0] = _value; }
	void setOrangeR(float _value)	{ colorR[1] = _value; }
	void setGreenR(float _value)	{ colorR[2] = _value; }
	void setBlueR(float _value)		{ colorR[3] = _value; }
	void setHub(string _value)		{ hub = -1; for (int i=0; i<numPlayers; i++) { if (_value	== colorNames[i]) { hub = i;} } }
	void setHighPair(pair<string, string> _pair) {
		for (int i=0; i<numPlayers; i++) {
			if (_pair.first		== colorNames[i]) {
				highPair.first = i;
			}
			if (_pair.second	== colorNames[i]) {
				highPair.second = i;
			}
		}
	}
	
private:
	vector<float>	colorR;
	float			groupR;
	int				hub;
	pair<int, int>	highPair;
	float			baseRadius;
	float			power;
};
