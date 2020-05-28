#include "ofApp.h"

//--------------------------------------------------------------
void ofApp::setup(){
	
	ofSetDataPathRoot("../Resources");
	ofSetFrameRate(30);
	
	numPlayers = 2;
	numScenes = sceneNames.size();
	
	R_InitValue = .4;
	
	currentScene = SCENE_IDLE;
	nextScene = SCENE_IDLE;
	scenePosition = 0;
	sceneStartTime = 0;
	sceneTime = 0;
	
	lslInput.setup(numPlayers, R_InitValue);
	correlationType = R_THETA;
	
	correlation = R_InitValue;
	score = 0;
	powers.resize(numPlayers, 1.0);
	
	RTweaker.setup(R_InitValue);
	
	lslOutput.setup();
	oscOutput.setup("192.168.0.127", 9000);
	
	setupGui();
}

//--------------------------------------------------------------
void ofApp::update(){
	
	// NEXT SCENE IF CURRENT SCENE IS PAST DURATION
	bool forceNextScene = true;
	if (currentScene != SCENE_IDLE) {
		sceneTime = ofGetElapsedTimef() - sceneStartTime;
		if (pFastMode) {sceneTime *= 20; }
		if (sceneTime >= sceneDuration * 60) {
			nextScene = (currentScene == SCENE_SCORE)? SCENE_IDLE : currentScene + 1;
			forceNextScene = false;
		}
	}
	
	// GO TO NEXT SCENE
	if (nextScene != currentScene) {
		if (pContinuousMode && !forceNextScene) { nextScene = currentScene; }
		switch (nextScene) {
			case SCENE_IDLE:
				reset();
				sceneDuration = 1;
				break;
			case SCENE_INTRO:
				reset();
				sceneDuration = pIntroDuration.get();
				break;
			case SCENE_CORRELATE:
				reset();
				sceneDuration = pCorrelateDuration.get();
				break;
			case SCENE_SCORE:
				sceneDuration = pScoreDuration.get();
				break;
			default:
				reset();
				sceneDuration = 1;
				break;
		}
		currentScene = nextScene;
		sceneStartTime = ofGetElapsedTimef();
		sceneTime = 0;
		sceneSampleStart = lslInput.getSampleCount();
		pSceneName.set(sceneNames[currentScene]);
	}
	scenePosition = (sceneTime == 0)? 0 : sceneTime / (sceneDuration * 60.0);
	pSceneProgress.set(scenePosition * 100);
	pSceneSampleCount = lslInput.getSampleCount() - sceneSampleStart;
	
	lslInput.update();
	int numConnectedHeadsets = lslInput.getNumHeadsets();
	oscOutput.setNumHeadsets(numConnectedHeadsets);
	
	if (currentScene == SCENE_IDLE) {
		pSceneSampleCount	= 0;
		correlation			= 0.0;
	}
	
	if (currentScene == SCENE_INTRO) {
		powers[0] = 0.5 + lfo(1.1) * 0.5;
		powers[1] = 0.5 + lfo(2.2) * 0.5;
		score = 0;
	}
	
	if (currentScene == SCENE_CORRELATE) {
		if (numConnectedHeadsets == 0) {
			reset();
		}
		if (numConnectedHeadsets == numPlayers && lslInput.getSampleCount() > 0) {
			correlation = RTweaker.update(lslInput.getGroupCorrelation(correlationType));
			correlation = ofClamp(correlation * 1.05, 0, 1);
			if (correlation >= 1) {
				score += 1.0;
			}
		}
		powers[0] 			= 1.0;
		powers[1] 			= 1.0;
	}
	
	if (currentScene == SCENE_SCORE) {
	}
	
	
	pCorrelation	= int(correlation * 100) / 100.0;
	pScore			= score;
	pPower1			= int(powers[0] * 100) / 100.0;
	pPower2			= int(powers[1] * 100) / 100.0;
	
	lslOutput.update(sceneTime);
	
	int oscScene = 0;
	switch (currentScene) {
		case SCENE_IDLE:
			oscScene = 0;
			break;
		case SCENE_INTRO:
			oscScene = 1;
			break;
		case SCENE_CORRELATE:
			oscScene = 2;
			break;
		case SCENE_SCORE:
			oscScene = 3;
			break;
		default:
			break;
	}
	oscOutput.setStatus(oscScene, sceneTime, scenePosition);
	
	oscOutput.setCorrelation(correlation);
	oscOutput.setScore(score);
	oscOutput.setPower1(powers[0]);
	oscOutput.setPower2(powers[1]);
	oscOutput.update();
	
}

//--------------------------------------------------------------
void ofApp::reset() {
	
	for(auto& R : powers) { R = 0.0;}
	correlation		= 0.0;
	score		= 0.0;
	
	RTweaker.reset();
	
	sceneSampleStart = lslInput.getSampleCount();
}

//--------------------------------------------------------------
void ofApp::draw(){
	drawGui();
}

//--------------------------------------------------------------
void ofApp::setupGui() {
	
	bool s = true;
	int guiWidth = 300;
	
	// BASIC GUI
	sessionGui.setDefaultWidth(guiWidth);
	switchGuiColor(sessionGui, s = !s);
	sessionGui.setup("session");
	sessionGui.add(pToggleStart.set("start (SPACE)", false));
	sessionGui.add(pToggleStop.set("stop", false));
	sessionGui.add(pToggleEditMode.set("edit mode", false));
	pToggleStart.addListener(this, &ofApp::pToggleStartListener);
	pToggleStop.addListener(this, &ofApp::pToggleStopListener);
	pToggleEditMode.addListener(this, &ofApp::pToggleEditModeListener);
	
	// ----------------------------
	// BASIC INFO
	infoGui.setDefaultWidth(guiWidth);
	switchGuiColor(infoGui, s = !s);
	infoGui.setup("session info");
	
	// BASIC INFO - SCENE
	sceneInfoParameters.setName("scene");
	sceneInfoParameters.add(pSceneName.set("current scene", sceneNames[0]));
	sceneInfoParameters.add(pSceneProgress.set("scene progress (pct)", 0, 0, 100));
	sceneInfoParameters.add(pSceneSampleCount.set("scene sample count", 0, 0, 1));
	infoGui.add(sceneInfoParameters);
	
	// BASIC INFO - LSL INPUT
	infoGui.add(lslInput.getParameters());
	
	// BASIC INFO - CORRELATION
	correlationParameters.setName("Correlation");
	correlationParameters.add(pCorrelation.set("correlation", 0.0, 0.0, 1.0));
	correlationParameters.add(pScore.set("score", 0.0, 0.0, 100.0));
	correlationParameters.add(pPower1.set("power 1", 0.0, 0.0, 1.0));
	correlationParameters.add(pPower2.set("power 2", 0.0, 0.0, 1.0));
	infoGui.add(correlationParameters);

	// ----------------------------
	// EDIT GUI
	string editGuiFile = "edit_settings.xml";
	editGui.setDefaultWidth(guiWidth);
	switchGuiColor(editGui, s = !s);
	editGui.setup("edit", editGuiFile);
	editGui.add(pFPS.set("average FPS", 0, 0, 30));
	
	// EDIT GUI - SCENE
	sceneParameters.setName("scene");
	sceneParameters.add(pFastMode.set("fast mode (F)", false));
	sceneParameters.add(pToggleNextScene.set("start / next scene (S)", false));
	sceneParameters.add(pContinuousMode.set("continous mode (C)", false));
	sceneParameters.add(pToggleReset.set("reset (R)", false));
	pFastMode.addListener(this, &ofApp::pEditModeListener);
	pToggleNextScene.addListener(this, &ofApp::pToggleNextSceneListener);
	pContinuousMode.addListener(this, &ofApp::pEditModeListener);
	pToggleReset.addListener(this, &ofApp::pToggleResetListener);
	
	// EDIT GUI - SCENE - DURATION
	durationParameters.setName("duration");
	durationParameters.add(pIntroDuration.set("intro duration (m)", 2, 0, 10));
	durationParameters.add(pCorrelateDuration.set("correlation duration (m)", 7, 0, 10));
	durationParameters.add(pScoreDuration.set("score duration (m)", 1, 0, 10));
	pIntroDuration.addListener(this, &ofApp::oneDecimalsListener);
	pCorrelateDuration.addListener(this, &ofApp::oneDecimalsListener);
	pScoreDuration.addListener(this, &ofApp::oneDecimalsListener);
	sceneParameters.add(durationParameters);
	
	// EDIT GUI - SCENE
	editGui.add(sceneParameters);
	
	// EDIT GUI - CORRELATION TWEAK
	RParameters.setName("correlation tweak");
	RParameters.add(RTweaker.getParameters());
	editGui.add(RParameters);
	
	// EDIT GUI
	if (!ofFile(editGuiFile)) { editGui.saveToFile(editGuiFile); }
	editGui.loadFromFile(editGuiFile);
	
	// ----------------------------
	// EDIT INFO - LOAD & LISTENERS
	
//	editInfo.setDefaultWidth(guiWidth);
//	switchGuiColor(editInfo, s = !s);
//	editInfo.setup("edit info");
//	ofParameterGroup &pHub = hubTweaker.getParameters();
//	pHub.setName("hub tweak");
//	editInfo.add(pHub);
//	ofParameterGroup &pHigh = highTweaker.getParameters();
//	pHigh.setName("high pair tweak");
//	editInfo.add(pHigh);
//	ofParameterGroup &pLow = lowTweaker.getParameters();
//	pLow.setName("low pair tweak");
//	editInfo.add(pLow);
//	int c = 0;
//	for (auto &t : RTweakers) {
//		ofParameterGroup &p = t.getParametersInfo();
//		p.setName(tweakNames[c] + " R Tweaker"); c++;
//		editInfo.add(p);
//	}
//	ofParameterGroup &pColor = colorTweaker.getParametersInfo();
//	pColor.setName("color R Tweaker"); c++;
//	editInfo.add(pColor);
//	minimizeGui(&editInfo);
}

//--------------------------------------------------------------
void ofApp::drawGui() {
	pFPS = (int)(ofGetFrameRate() + 0.5);
	
	ofPushStyle();
	ofEnableBlendMode(OF_BLENDMODE_ALPHA);
	
	ofPoint	gPos = ofPoint(10, 10);
	
	sessionGui.setPosition(gPos);
	sessionGui.draw();
	gPos += ofPoint(0, sessionGui.getHeight() + 10);
	infoGui.setPosition(gPos);
	infoGui.draw();
	if (pToggleEditMode) {
		gPos = ofPoint(infoGui.getPosition().x + infoGui.getWidth() + 10, 10);
		editGui.setPosition(gPos);
		editGui.draw();
		gPos += ofPoint(0, editGui.getHeight() + 10);
		editInfo.setPosition(gPos);
		editInfo.draw();
	}
	ofPopStyle();
}

//--------------------------------------------------------------
void ofApp::switchGuiColor(ofxGuiGroup &_panel, bool _switch) {
	ofColor bColor[2];
	bColor[0].set(120, 120, 60, 255);
	bColor[1].set(60, 120, 120, 255);
	ofColor hColor[2];
	hColor[0].set(120, 120, 60, 255);
	hColor[1].set(60, 120, 120, 255);
	ofColor fColor[2];
	fColor[0].set(120, 120, 60, 255);
	fColor[1].set(60, 120, 120, 255);
	
	_panel.setHeaderBackgroundColor(bColor[_switch]);
	_panel.setDefaultHeaderBackgroundColor(hColor[_switch]);
	_panel.setDefaultFillColor(fColor[_switch]);

}

//--------------------------------------------------------------
void ofApp::minimizeGui(ofxGuiGroup* _group) {
	for (int i=0; i< _group->getNumControls(); i++) {
		ofxGuiGroup * subGroup  = dynamic_cast<ofxGuiGroup*>(_group->getControl(i));
		if (subGroup) {
			minimizeSubGroups(subGroup);
			_group->minimizeAll();
		}
	}
}

//--------------------------------------------------------------
void ofApp::minimizeSubGroups(ofxGuiGroup* _group) {
	for (int i=0; i< _group->getNumControls(); i++) {
		ofxGuiGroup * subGroup  = dynamic_cast<ofxGuiGroup*>(_group->getControl(i));
		if (subGroup) {
			minimizeSubGroups(subGroup);
			_group->minimizeAll();
		}
	}
}

//--------------------------------------------------------------
void ofApp::keyPressed(int key){
	switch (key) {
		default: break;
		case ' ': pToggleNextScene.set(true); break;
		case 'F': pFastMode.set(!pFastMode.get()); break;
		case 'S': pToggleNextScene.set(true); break;
		case 'C': pContinuousMode.set(!pContinuousMode.get()); break;
		case 'R': reset(); break;
	}
}

void ofApp::pToggleEditModeListener(bool &_value) {
	if (_value) {
		glm::vec2 size = ofGetWindowSize();
		ofSetWindowShape(630, size.y);
	} else {
		glm::vec2 size = ofGetWindowSize();
		ofSetWindowShape(320, size.y);
		pFastMode.set(false);
		pContinuousMode.set(false);
	 }
}


void ofApp::pToggleNextSceneListener(bool &_value)  {
	if (_value) {
		_value = false;
		if (pToggleEditMode) {
			nextScene = (currentScene == SCENE_SCORE)? SCENE_IDLE : currentScene + 1;
		}
	}
}

