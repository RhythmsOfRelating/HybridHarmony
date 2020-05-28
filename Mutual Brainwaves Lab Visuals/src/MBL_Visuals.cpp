//
//  MBL_Visuals.cpp
//  Mutual Brainwaves Lab Bridge
//
//  Created by Ties East on 25/04/2019.
//

#include "MBL_Visuals.h"


void MBL_Visuals::setup(int _width, int _height) {
	width = _width;
	height = _height;
	
	visualFbo.allocate(_width, _height, GL_RGBA);
	headImage1.load("headA.png");
	headImage2.load("headB.png");
	headFbo1.allocate(_width/2.0, _height, GL_RGBA);
	headFbo2.allocate(_width/2.0, _height, GL_RGBA);
	
	parameters.setName("visuals");
	parameters.add(scale.set("scale", 0.8, 0.2, 1));
	parameters.add(start.set("start", 0.0, -.1, .1));
	parameters.add(end.set("end", 0.5, 0.4, .6));
	parameters.add(flip1.set("flip1", false));
	parameters.add(flip2.set("flip2", true));
	flip1.addListener(this, &MBL_Visuals::flipListener);
	flip2.addListener(this, &MBL_Visuals::flipListener);
	parameters.add(fontSize.set("font Size", 160, 100, 200));
	fontSize.addListener(this, &MBL_Visuals::fontSizeListener);
	scale.addListener(this, &MBL_Visuals::fontSizeListener);
	parameters.add(fontY.set("font Y", .4, 0, 1));
	
	headFont.load("Arial Narrow.ttf", fontSize.get() * scale.get());
	fit(headFbo1, headImage1.getTexture(), flip1.get());
	fit(headFbo2, headImage2.getTexture(), flip2.get());
}

void MBL_Visuals::update() {
	
	float headWidth = visualFbo.getWidth() * 0.5 * scale.get();
	float headHeight = visualFbo.getHeight() * scale.get();
	float hHW = headWidth * 0.5;
	float hHH = headHeight * 0.5;
	
	float aniStart = start + (scale.get() * .25);
	float aniEnd = end;
	float aniRange = aniEnd - aniStart;
	
	float R = correlation;
	float P1 = power1;
	float P2 = power2;
	if (scene == 0) {
		P1 = .7;
		P2 = .7;
	}
	if (scene == 1) {
		float t = ofClamp(time / 10, 0, 1);
		P1 = .7 * (1.0 - t) + t * power1;
		P2 = .7 * (1.0 - t) + t * power2;
	}
	if (scene == 2) {
		float t = ofClamp(time / 2.22, 0, 1);
		R = t * correlation;
	}
	if (scene == 3) {
		R = ofClamp(correlation + time, 0, 1);
		P1 = ofClamp(power1 + time, 0, 1);
		P2 = ofClamp(power2 + time, 0, 1);
	}
	
	float aniCorr = aniStart + aniRange * R;
	
	float CentreX1 = width * aniCorr;
	float CentreX2 = width - CentreX1;
	float CentreY = height * 0.45;
	
	visualFbo.begin();
	ofPushStyle();
	ofEnableBlendMode(OF_BLENDMODE_ALPHA);
	ofClear(0);
	ofSetColor(P1 * 255);
	headFbo1.draw(CentreX1 - hHW, CentreY - hHH, headWidth, headHeight);
	ofSetColor(P2 * 255);
	headFbo2.draw(CentreX2 - hHW, CentreY - hHH, headWidth, headHeight);
	ofPopStyle();
	
	ofPushStyle();
	if (scene > 0 && scene < 3) {
		ofSetColor(255 * 0.6);
		ofDrawRectangle(width * 0.03, height * 0.94, width * 0.94 * (1.0 - progress), 12);
	}
	if (scene == 3) {
		float b = ofClamp(time / 3, 0, 1) * ((sin(ofGetElapsedTimef() / 0.26) + 1.0) / 2.6 + 0.3);
		b = ofClamp(b, 0, 1);
		ofSetColor(0,0,0, b * 255);
		string ss = ofToString(score);
		float centreS = ss.size() * fontSize.get() * scale.get() * 0.3;
		headFont.drawString(ofToString(score), width * 0.5 - centreS, CentreY - hHH + fontY * headHeight);
//		headFont.drawString(ofToString(score), width * 0.5 - centreS, height * 0.4);
	}
	ofPopStyle();
	
	visualFbo.end();
}

void MBL_Visuals::draw(int _x, int _y, int _width, int _height) {
	float srcWidth = visualFbo.getWidth();
	float srcHeight = visualFbo.getHeight();
	float dstWidth = _width;
	float dstHeight = _height;
	
	float srcRatio = srcWidth / srcHeight;   // 0.5625
	float dstRatio = dstWidth / dstHeight;   // 1.3333
	
	float drawX, drawY, drawWidth, drawHeight;
	
	if (srcRatio > dstRatio) {
		drawHeight = dstHeight;
		drawWidth = drawHeight * srcRatio;
	}
	else {
		drawWidth = dstWidth;
		drawHeight = drawWidth / srcRatio;
	}
	
	drawX = _x + (dstWidth - drawWidth) / 2.0;
	drawY = _y + (dstHeight - drawHeight) / 2.0;
	
	ofPushStyle();
	ofEnableBlendMode(OF_BLENDMODE_DISABLED);
	visualFbo.draw(drawX, drawY, drawWidth, drawHeight);
	ofPopStyle();
}

void MBL_Visuals::fit(ofFbo& _dst, ofTexture& _tex, bool _flip) {
	
	float meRatio = float(_dst.getWidth()) / float(_dst.getHeight());   // 0.5625
	float texRatio = float(_tex.getWidth()) / float(_tex.getHeight());   // 1.3333
	
	float width, height;
	float x0, y0, x1, y1;
	
	if (meRatio > texRatio) {
		height = _dst.getHeight();
		width = height * texRatio;
		
	}
	else {
		width = _dst.getWidth();
		height = width / texRatio;
	}
	
	x0 = (_dst.getWidth() - width) / 2;
	x1 = x0 + width;
	y0 = (_dst.getHeight() - height) / 2;
	y1 = y0 + height;
	
	ofMesh quad;
	quad.setMode(OF_PRIMITIVE_TRIANGLE_FAN);
	
	quad.addVertex(glm::vec3(x0,y0,0));
	quad.addVertex(glm::vec3(x1,y0,0));
	quad.addVertex(glm::vec3(x1,y1,0));
	quad.addVertex(glm::vec3(x0,y1,0));
	
	if (_flip) {
		quad.addTexCoord(glm::vec2(_tex.getWidth(),0));
		quad.addTexCoord(glm::vec2(0,0));
		quad.addTexCoord(glm::vec2(0,_tex.getHeight()));
		quad.addTexCoord(glm::vec2(_tex.getWidth(),_tex.getHeight()));
	} else {
		quad.addTexCoord(glm::vec2(0,0));
		quad.addTexCoord(glm::vec2(_tex.getWidth(),0));
		quad.addTexCoord(glm::vec2(_tex.getWidth(),_tex.getHeight()));
		quad.addTexCoord(glm::vec2(0,_tex.getHeight()));
	}
	
	_dst.begin();
	ofClear(0,0);
	_tex.bind();
	quad.draw();
	_tex.unbind();
	_dst.end();
}

void MBL_Visuals::flipListener(bool &_value) {
	fit(headFbo1, headImage1.getTexture(), flip1.get());
	fit(headFbo2, headImage2.getTexture(), flip2.get());
}
