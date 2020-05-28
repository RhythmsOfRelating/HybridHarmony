#pragma once
#include "ofMain.h"
#include "HD_Mask.h"


const vector<string> colorNames({"Purple", "Orange", "Green", "Blue"});
const vector<ofColor> colorColors({ ofColor(255, 0, 212), ofColor(255, 170, 0), ofColor(0, 255, 43),  ofColor(0, 85, 255)});
const ofColor groupColor(ofColor(0, 0, 0));

class HD_Layout: public HD_Mask {
public:
	
	void setup(int _width, int _height) override {
		HD_Mask::setup(_width, _height);
		parameters.setName("layout");
		parameters.add(pColorOrigin.set("color origin",	0.0,	0.0,	0.5));
		pColorOrigin.addListener(this, &HD_Layout::updateMaskListener);
		
		colorRadius = 0.05;
		groupRadius = 0.1;
		numPlayers = colorNames.size();
		colorOrigins.resize(numPlayers);
		
		
		update();
	}
	
	void draw(int _x, int _y, int _w, int _h) override {
		ofPushStyle();
		ofPushView();
		ofEnableBlendMode(OF_BLENDMODE_DISABLED);
		ofTranslate(_x, _y);
		glm::vec2 scale = glm::vec2(_w, _h);
		
		for (int i=0; i<numPlayers; i++) {
			ofSetColor(colorColors[i]);
			ofDrawCircle(colorOrigins[i] * scale, windowHeight * colorRadius);
		}
		ofSetColor(groupColor);
		ofDrawCircle(groupOrigin * scale, windowHeight * groupRadius);
		ofPopView();
		ofPopStyle();
	}
	
	void drawMask(int _x, int _y, int _w, int _h) {
		HD_Mask::draw(_x, _y, _w, _h);
	}
	
	glm::vec2 getCentre()	{ return groupOrigin; }
	glm::vec2 getPurple()	{ return colorOrigins[0]; }
	glm::vec2 getOrange()	{ return colorOrigins[1]; }
	glm::vec2 getGreen()	{ return colorOrigins[2]; }
	glm::vec2 getBlue()		{ return colorOrigins[3]; }

protected:
	void update() override {
		HD_Mask::update();
		
		glm::vec3 C = maskMesh.getVertex(0);
		for (int i=0; i<numPlayers; i++) {
			int i1 = i*2+2;
			int i2 = i*2+3;
			colorOrigins[i] = triangulate(maskMesh.getVertex(i1), maskMesh.getVertex(i2), C);
		}
		groupOrigin = maskMesh.getVertex(0);
	}
	
	int numPlayers;
	vector<glm::vec3> colorOrigins;
	glm::vec3 groupOrigin;
	
	ofParameterGroup	playerParameters;
	ofParameter<float>	pColorOrigin;
	float	colorRadius;
	float	groupRadius;
	
	void updateMaskListener(float& _value)		{ update(); }
	
	
	glm::vec3 triangulate(glm::vec3 _A, glm::vec3 _B, glm::vec3 _C) {
		glm::vec3 P1 = (_A + _B) / 2.0;
		return (1.0 - pColorOrigin) * P1 + pColorOrigin.get() * _C;
	}
};
