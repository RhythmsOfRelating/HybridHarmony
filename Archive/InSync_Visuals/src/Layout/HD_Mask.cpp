//
//  HD_Mask.cpp
//  Visuals Simple
//
//  Created by Ties East on 28/02/2019.
//

#include "HD_Mask.h"

HD_Mask::HD_Mask() {
	ofAddListener(ofEvents().mouseMoved, this, &HD_Mask::mouseMoved);
	ofAddListener(ofEvents().mouseDragged, this, &HD_Mask::mouseDragged);
	ofAddListener(ofEvents().mousePressed, this, &HD_Mask::mousePressed);
	ofAddListener(ofEvents().windowResized, this, &HD_Mask::windowResized);
	ofAddListener(ofEvents().keyPressed, this, &HD_Mask::keyPressed);
}

HD_Mask::~HD_Mask() {
	ofRemoveListener(ofEvents().mouseMoved, this, &HD_Mask::mouseMoved);
	ofRemoveListener(ofEvents().mouseDragged, this, &HD_Mask::mouseDragged);
	ofRemoveListener(ofEvents().mousePressed, this, &HD_Mask::mousePressed);
	ofRemoveListener(ofEvents().windowResized, this, &HD_Mask::windowResized);
}

void HD_Mask::setup(int _width, int _height) {
	width = _width;
	height = _height;
	windowWidth = ofGetWindowWidth();
	windowHeight = ofGetWindowHeight();
	
	maskMesh.setMode(OF_PRIMITIVE_TRIANGLE_FAN);
	//	maskMesh.setupIndicesAuto();
	maskMesh.disableColors();
	maskMesh.disableNormals();
	maskMesh.disableIndices();
	activeVertex = -1;
	lastMousePos = glm::vec3(0);
	
	
	maskFbo.allocate(width, height, GL_RGB);
	
	load();
	
	pointSize = 10;
	
	parameters.setName("table mask");
	parameters.add(pToggleEditMask.set("edit", false));
	//	parameters.add(pToggleEditMask.set("edit (E)", false));
	//	parameters(pAddVertex.set("add (A)", false));
	//	parameters(pDeleteVertex.set("delete (D)", false));
	parameters.add(pSaveMask.set("save", false));
	parameters.add(pLoadMask.set("load", false));
	
	maskTweakParameters.setName("tweak");
	maskTweakParameters.add(maskNudgeRight.set("nudge right", false));
	maskTweakParameters.add(maskNudgeLeft.set("nudge left", false));
	maskTweakParameters.add(maskNudgeUp.set("nudge up", false));
	maskTweakParameters.add(maskNudgeDown.set("nudge down", false));
	maskNudgeRight.addListener(this, &HD_Mask::maskNudgeRightListener);
	maskNudgeLeft.addListener(this, &HD_Mask::maskNudgeLeftListener);
	maskNudgeUp.addListener(this, &HD_Mask::maskNudgeUpListener);
	maskNudgeDown.addListener(this, &HD_Mask::maskNudgeDownListener);
	parameters.add(maskTweakParameters);
	
	pAddVertex.addListener(this, &HD_Mask::pAddVertexListener);
	pDeleteVertex.addListener(this, &HD_Mask::pDeleteVertexListener);
	pSaveMask.addListener(this, &HD_Mask::pSaveMaskListener);
	pLoadMask.addListener(this, &HD_Mask::pLoadMaskListener);
}


//--------------------------------------------------------------
void HD_Mask::load() {
	maskXml.load("mask.xml");
	numVertices = maskXml.getNumTags("vertex");
	maskMesh.clear();
	for (int i=0; i<numVertices; i++) {
		maskXml.pushTag("vertex", i);
		maskMesh.addVertex(glm::vec3(maskXml.getValue("x", .5), maskXml.getValue("y", .5), 0));
		maskXml.popTag();
	}
	update();
}

void HD_Mask::save() {
	if (pToggleEditMask.get()) {
		maskXml.clear();
		for (int i=0; i<numVertices; i++) {
			maskXml.addTag("vertex");
			maskXml.pushTag("vertex", i);
			maskXml.addValue("x", maskMesh.getVertex(i).x);
			maskXml.addValue("y", maskMesh.getVertex(i).y);
			maskXml.popTag();
		}
		maskXml.saveFile();
	}
}

void HD_Mask::update() {
	maskFbo.begin();
	ofClear(0, 0, 0, 255);
	ofPushMatrix();
	ofScale(width, height);
	maskMesh.draw();
	ofPopMatrix();
	maskFbo.end();
}

void HD_Mask::draw(int _x, int _y, int _w, int _h) {
	maskFbo.draw(_x, _y, _w, _h);
	
	ofPushStyle();
	ofPushView();
	ofEnableBlendMode(OF_BLENDMODE_DISABLED);
	ofTranslate(_x, _y);	
	
	if (pToggleEditMask.get()) {
		ofPushStyle();
		ofSetColor(255, 0, 0);
		glm::vec2 scale = glm::vec2(_w, _h);
		ofDrawCircle(maskMesh.getVertex(0) * scale, pointSize);
		ofSetColor(128, 128, 128);
		for(int i=1; i<numVertices; i++) {
			ofDrawCircle(maskMesh.getVertex(i) * scale, pointSize);
		}
		ofSetColor(0, 255, 0);
		if (activeVertex > 0) {
			ofDrawCircle(maskMesh.getVertex(activeVertex) * scale, pointSize);
		}
		ofSetColor(255, 255, 255);
		for(int i=0; i<numVertices; i++) {
			ofDrawBitmapString(ofToString(i), maskMesh.getVertex(i) * scale + glm::vec2(-8,4));
		}
		ofPopStyle();
	}
	ofPopView();
	ofPopStyle();
}

//--------------------------------------------------------------
void HD_Mask::pDeleteVertexListener(bool &_value) {
	if (pToggleEditMask.get()) {
		if (_value) {
			_value = false;
			if(activeVertex > 2 && activeVertex < numVertices) {
				maskMesh.removeVertex(activeVertex);
				numVertices--;
				activeVertex--;
			}
			update();
		}
	}
};

void HD_Mask::pAddVertexListener(bool &_value) {
	if (pToggleEditMask.get()) {
		if (_value) {
			_value = false;
			
			maskMesh.addVertex(glm::vec3(0.0));
			activeVertex++;
			for (int i=numVertices; i>activeVertex; i--) {
				maskMesh.setVertex(i, maskMesh.getVertex(i-1));
			}
			glm::vec3 newVertex = (maskMesh.getVertex(activeVertex-1) + maskMesh.getVertex((activeVertex+1)%(numVertices+1))) / 2.0;
			maskMesh.setVertex(activeVertex, newVertex);
			numVertices++;
			
			update();
		}
	}
};

void HD_Mask::moveVertex(bool _left, bool _right, bool _up, bool _down){
	if (pToggleEditMask.get()) {
		float x = (_right - _left) * (1.0 / windowWidth);
		float y = (_down - _up) * (1.0 / windowWidth);
		
		if (activeVertex >= 0 && activeVertex < numVertices) {
			maskMesh.setVertex(activeVertex, maskMesh.getVertex(activeVertex) + glm::vec3(x, y, 0));
			if (activeVertex == 9) { maskMesh.setVertex(1, maskMesh.getVertex(9)); }
		}
		
		update();
	}
}

//--------------------------------------------------------------
void HD_Mask::nudgeMask(bool _left, bool _right, bool _up, bool _down){
	if (pToggleEditMask.get()) {
		float x = (_right - _left) * (1.0 / windowWidth);
		float y = (_down - _up) * (1.0 / windowWidth);
		
		for (int i=0; i<numVertices; i++) {
			maskMesh.setVertex(i, maskMesh.getVertex(i) + glm::vec3(x, y, 0));
		}
		update();
	}
}

//--------------------------------------------------------------
void HD_Mask::mouseMoved(ofMouseEventArgs& _event) {
	lastMousePos = glm::vec3(_event.x / windowWidth, _event.y / windowHeight, 0);
	lastMousePos = MP2TP(lastMousePos);
}

void HD_Mask::mouseDragged(ofMouseEventArgs& _event) {
	glm::vec3 mousePos = glm::vec3(_event.x / windowWidth, _event.y / windowHeight, 0);
	mousePos = MP2TP(mousePos);
	if (pToggleEditMask.get()) {
		if (activeVertex >= 0 && activeVertex < numVertices) {
			glm::vec3 mouseDif = mousePos - lastMousePos;
			maskMesh.setVertex(activeVertex, maskMesh.getVertex(activeVertex) + mouseDif);
			if (activeVertex == 9) { maskMesh.setVertex(1, maskMesh.getVertex(9)); }
			update();
		}
	}
	lastMousePos = mousePos;
	
}

void HD_Mask::mousePressed(ofMouseEventArgs& _event){
	if (pToggleEditMask.get()) {
		glm::vec3 mP = glm::vec3(_event.x / windowWidth, _event.y / windowHeight, 0);
		glm::vec3 tP = MP2TP(mP);
		
		float maxDistance = (pointSize * 2.0) / windowWidth;
		activeVertex = -1;
		for (int i=0; i<numVertices; i++) {
			if (glm::distance(maskMesh.getVertex(i), tP) < maxDistance) {
				activeVertex = i;
			}
		}
	}
}

glm::vec3 HD_Mask::MP2TP(glm::vec3 _mousPos) {
	float wRatio = windowWidth / windowHeight;
	float tRatio = width / height;
	float x, y, w, h;
	if (wRatio > tRatio) {
		_mousPos.x *= wRatio / tRatio;
		_mousPos.x -= (wRatio - tRatio) / 2.0;
	}
	else {
		_mousPos.y *= tRatio / wRatio;
		_mousPos.y += ((1.0/tRatio) - (1.0/wRatio)) / 2.0;
	}
	return _mousPos;
}

void HD_Mask::windowResized(ofResizeEventArgs& _event){
	windowWidth = _event.width;
	windowHeight = _event.height;
//	maskFbo.allocate(_event.width, _event.height, GL_RGB);
	update();
}

void HD_Mask::keyPressed(ofKeyEventArgs &_event) {
	int key = _event.key;
	
	switch (key) {
//		case 'E':
//			pToggleEditMask = !pToggleEditMask;
//			break;
//		case 'A':
//			pAddVertex = !pAddVertex;
//			break;
//		case 'D':
//			pDeleteVertex = !pDeleteVertex;
//			break;
//		case 'S':
//			pSaveMask = !pSaveMask;
//			break;
//		case 'L':
//			pLoadMask = !pLoadMask;
//			break;
		case OF_KEY_LEFT:
			moveVertex(1, 0, 0, 0);
			break;
		case OF_KEY_RIGHT:
			moveVertex(0, 1, 0, 0);
			break;
		case OF_KEY_UP:
			moveVertex(0, 0, 1, 0);
			break;
		case OF_KEY_DOWN:
			moveVertex(0, 0, 0, 1);
			break;
		default:
			break;
	}
	
}
