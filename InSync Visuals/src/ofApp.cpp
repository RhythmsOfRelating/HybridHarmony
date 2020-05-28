#include "ofApp.h"

//--------------------------------------------------------------
void ofApp::setup(){
	ofSetDataPathRoot("../Resources");
	
	screens.getMonitorsInfo();
	windowWidth = ofGetWindowWidth();
	windowHeight = ofGetWindowHeight();
	
	oscReceiver.setup();
	tableLayout.setup(1200, 1200);
	
	visuals.setup(1200, 1200);
	
	gui.setup("settings");
	gui.add(toggleGui.set("show gui (G)", false));
	toggleFullscreen.addListener(this, &ofApp::toggleFullscreenListener);
	gui.add(toggleFullscreen.set("full screen (F)", false));
	screenId.addListener(this, &ofApp::screenIdListener);
	gui.add(screenId.set("select screen", 0, 0, screens.getCount() - 1));
	gui.add(toggleReset.set("reset (R)", false));
	toggleReset.addListener(this, &ofApp::toggleResetListener);
	gui.add(toggleSimpleMode.set("simple mode (S)", false));
	gui.add(tableLayout.getParameters());
	
	gui.add(visuals.getParameters());
	
	gui.loadFromFile("settings.xml");
	minimizeGui(&gui);
	
	toggleFullscreen.set(false);
	toggleFullscreen.set(true);
	toggleSimpleMode.set(true);
//	toggleGui.set(false);
	
	updateLayout();
}

void ofApp::minimizeGui(ofxGuiGroup* _group) {
	for (int i=0; i< _group->getNumControls(); i++) {
		ofxGuiGroup * subGroup  = dynamic_cast<ofxGuiGroup*>(_group->getControl(i));
		if (subGroup) {
			minimizeGui(subGroup);
			_group->minimizeAll();
		}
	}
}
//--------------------------------------------------------------
void ofApp::screenIdListener(int& _value) {
	if((screens.getCount() - 1) < _value) _value = screens.getCount() - 1;
}

void ofApp::toggleFullscreenListener(bool& _value) {
	if (_value) {
		ofSetWindowPosition(screens.getX(screenId.get()), screens.getY(screenId.get()));
		ofSetFullscreen(true);
		gui.setPosition((windowWidth / 2.0) - (gui.getWidth() / 2.0), (windowHeight / 2.0) - (gui.getHeight() / 2.0));
		toggleGui.set(false);
	}
	else {
		ofSetFullscreen(false);
		ofSetWindowPosition(100, 100);
		gui.setPosition(10, 10);
		toggleGui.set(true);
	}
}



//--------------------------------------------------------------
void ofApp::update(){
	oscReceiver.update();
	
	if (tableLayout.getEditMode()) {
		toggleSimpleMode.set(true);
		updateLayout();
	}
	else if (oscReceiver.getScene() != 0 ) {
		toggleSimpleMode.set(false);
	}
	
	if (toggleSimpleMode) {
		tableLayout.setGroupR(oscReceiver.getGroupCorrelation());
		tableLayout.setPurpleR(oscReceiver.getPurpleCorrelation());
		tableLayout.setOrangeR(oscReceiver.getOrangeCorrelation());
		tableLayout.setGreenR(oscReceiver.getGreenCorrelation());
		tableLayout.setBlueR(oscReceiver.getBlueCorrelation());
		tableLayout.setHighPair(oscReceiver.getHighPair());
		tableLayout.setHub(oscReceiver.getHub());
	}
		
	if (!toggleSimpleMode) {
		visuals.setScene(oscReceiver.getScene());
		visuals.setProgress(oscReceiver.getProgress());
		visuals.setGroupR(oscReceiver.getGroupCorrelation());
		visuals.setPurpleR(oscReceiver.getPurpleCorrelation());
		visuals.setOrangeR(oscReceiver.getOrangeCorrelation());
		visuals.setGreenR(oscReceiver.getGreenCorrelation());
		visuals.setBlueR(oscReceiver.getBlueCorrelation());
		visuals.setHighPair(oscReceiver.getHighPair());
		visuals.setHub(oscReceiver.getHub());
		visuals.update();
	}
}

void ofApp::updateLayout() {
	visuals.setCentre(tableLayout.getCentre());
	visuals.setPurpleOrigin(tableLayout.getPurple());
	visuals.setOrangeOrigin(tableLayout.getOrange());
	visuals.setGreenOrigin(tableLayout.getGreen());
	visuals.setBlueOrigin(tableLayout.getBlue());
	visuals.setMask(tableLayout.getMask());
}

//--------------------------------------------------------------
void ofApp::draw(){
	ofClear(0,0);
	
	float wRatio = windowWidth / windowHeight;
	float texRatio = float(visuals.getWidth()) / float(visuals.getHeight());
	float x, y, w, h;
	if (wRatio > texRatio) { h = windowHeight; w = h * texRatio; }
	else { w = windowWidth; h = w / texRatio; }
	x = (windowWidth - w) / 2;
	y = (windowHeight - h) / 2;
	
	if (toggleSimpleMode) {
		tableLayout.drawMask(x, y, w, h);
		tableLayout.draw(x, y, w, h);
	}
	else {
		visuals.draw(x, y, w, h);
	}
	
	if (toggleGui) { gui.draw(); }
}

//--------------------------------------------------------------
void ofApp::keyPressed(int key){

	switch (key) {
		case 'F':
			toggleFullscreen = !toggleFullscreen;
			break;
		case 'G':
			toggleGui = !toggleGui;
			break;
		case 'R':
			toggleReset = !toggleReset;
			break;
		default:
			break;
	}
}

//--------------------------------------------------------------
void ofApp::keyReleased(int key){

}

//--------------------------------------------------------------
void ofApp::mouseMoved(int x, int y ){

}

//--------------------------------------------------------------
void ofApp::mouseDragged(int x, int y, int button){

}

//--------------------------------------------------------------
void ofApp::mousePressed(int x, int y, int button){

}

//--------------------------------------------------------------
void ofApp::mouseReleased(int x, int y, int button){

}

//--------------------------------------------------------------
void ofApp::mouseEntered(int x, int y){

}

//--------------------------------------------------------------
void ofApp::mouseExited(int x, int y){

}

//--------------------------------------------------------------
void ofApp::windowResized(int w, int h){

	windowWidth = w;
	windowHeight = h;
}

//--------------------------------------------------------------
void ofApp::gotMessage(ofMessage msg){

}

//--------------------------------------------------------------
void ofApp::dragEvent(ofDragInfo dragInfo){ 

}
