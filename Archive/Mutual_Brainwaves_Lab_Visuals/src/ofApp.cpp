#include "ofApp.h"

//--------------------------------------------------------------
void ofApp::setup(){
	ofSetDataPathRoot("../Resources");
	
	screens.getMonitorsInfo();
	windowWidth = ofGetWindowWidth();
	windowHeight = ofGetWindowHeight();
	
	oscReceiver.setup();
	
	
	visuals.setup(1920, 1080);
	
	gui.setup("settings");
	gui.add(toggleGui.set("show gui (G)", false));
	toggleFullscreen.addListener(this, &ofApp::toggleFullscreenListener);
	gui.add(toggleFullscreen.set("full screen (F)", false));
	screenId.addListener(this, &ofApp::screenIdListener);
	gui.add(screenId.set("select screen", 0, 0, screens.getCount() - 1));
//	gui.add(toggleReset.set("reset (R)", false));
//	toggleReset.addListener(this, &ofApp::toggleResetListener);
	gui.add(visuals.getParameters());
	
	
	if (!ofFile("settings.xml")) { gui.saveToFile("settings.xml"); }
	gui.loadFromFile("settings.xml");
	
	inputs.setName("input");
	inputs.add(pScene.set("scene", 0, 0, 3));
	inputs.add(pPosition.set("position", 0, 0, 1));
	inputs.add(pCorrelation.set("correlation", 0, 0, 1));
	inputs.add(pScore.set("score", 0, 0, 100));
	inputs.add(pPower1.set("power1", 0, 0, 1));
	inputs.add(pPower2.set("power2", 0, 0, 1));
	
////	toggleFullscreen.set(false);
//	toggleFullscreen.set(true);
//	toggleGui.set(false);
	
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
	
	visuals.setStatus(oscReceiver.getScene(), oscReceiver.getTime(), oscReceiver.getProgress());
	visuals.setCorrelation(oscReceiver.getCorrelation());
	visuals.setScore(oscReceiver.getScore());
	visuals.setPower1(oscReceiver.getPower1());
	visuals.setPower2(oscReceiver.getPower2());
	
	visuals.update();
	
	pScene.set(oscReceiver.getScene());
	pPosition.set(oscReceiver.getProgress());
	pCorrelation.set(oscReceiver.getCorrelation());
	pScore.set(oscReceiver.getScore());
	pPower1.set(oscReceiver.getPower1());
	pPower2.set(oscReceiver.getPower2());
}

//--------------------------------------------------------------
void ofApp::draw(){
	ofClear(0,0);
	
	visuals.draw(0,0,windowWidth, windowHeight);
	
	if (toggleGui) {
		gui.draw();
		inputs.setPosition(gui.getPosition().x, gui.getPosition().y + gui.getHeight() + 10);
		inputs.draw();
	}
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
