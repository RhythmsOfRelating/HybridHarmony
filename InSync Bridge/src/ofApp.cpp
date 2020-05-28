#include "ofApp.h"

//--------------------------------------------------------------
void ofApp::setup(){
	
	ofSetDataPathRoot("../Resources");
	ofSetFrameRate(30);
	
	numPlayers = 4;
	numScenes = sceneNames.size();
	numTweakers = tweakNames.size();
	
	R_InitValue = .4;
	
	currentScene = SCENE_IDLE;
	nextScene = SCENE_IDLE;
	scenePosition = 0;
	sceneStartTime = 0;
	sceneTime = 0;
	
	lslInput.setup(numPlayers, R_InitValue);
	correlationType = correlationType;
	
	groupR = R_InitValue;
	colorR.resize(numPlayers, R_InitValue);
	scoreR.resize(numPlayers, 0);
	normalizedScoreR.resize(numPlayers, 0);
	hubR = R_InitValue;
	highR = R_InitValue;
	lowR = R_InitValue;
	hub = "none";
	highPair = {"none", "none"};
	lowPair = {"none", "none"};
	
	RTweakers.resize(numTweakers);
	for (auto &t : RTweakers) { t.setup(R_InitValue); }
	colorTweaker.setup(rColorNames, R_InitValue);
	hubTweaker.setup();
	highTweaker.setup();
	lowTweaker.setup();
	
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
			case SCENE_PURPLE:
			case SCENE_ORANGE:
			case SCENE_GREEN:
			case SCENE_BLUE:
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
		pSceneSampleCount = 0;
	}
	
	if (currentScene == SCENE_PURPLE) {
		colorR[R_PURPLE] = 0.5 + lfo(1.1) * 0.5;
	}
	if (currentScene == SCENE_ORANGE) {
		colorR[R_ORANGE] = 0.5 + lfo(2.2) * 0.5;
	}
	if (currentScene == SCENE_GREEN) {
		colorR[R_GREEN] = 0.5 + lfo(3.3) * 0.5;
	}
	if (currentScene == SCENE_BLUE) {
		colorR[R_BLUE] = 0.5 + lfo(4.4) * 0.5;
	}
	
	if (currentScene == SCENE_CORRELATE) {
		if (numConnectedHeadsets == 0) {
			reset();
		}
		if (numConnectedHeadsets == 4 && lslInput.getSampleCount() > 0) {
		
			groupR		= RTweakers[3].update(lslInput.getHubCorrelation(correlationType));
			
			for (int i=0; i<numPlayers; i++) { colorR[i] = lslInput.getColorCorrelation((rColor)i, correlationType); }
			colorR = colorTweaker.update(colorR);
			
			hub 		= hubTweaker.update(lslInput.getHub(correlationType));
			hubR		= RTweakers[0].update(lslInput.getHubCorrelation(correlationType));
			highPair	= highTweaker.update(lslInput.getHighCorrelationPair(correlationType));
			highR		= RTweakers[1].update(lslInput.getHighCorrelation(correlationType));
			lowPair		= lowTweaker.update(lslInput.getLowCorrelationPair(correlationType));
			lowR		= RTweakers[2].update(lslInput.getLowCorrelation(correlationType));
			
			float highScore = 0;
			for (int i=0; i<numPlayers; i++) { scoreR[i] += colorR[i]; }
			for (auto s : scoreR) { if (s > highScore) { highScore = s; } }
			for (int i=0; i<numPlayers; i++) { normalizedScoreR[i] = scoreR[i] / highScore; }
		}
	}
	
	if (currentScene == SCENE_SCORE) {
		
		groupR				= 1.0;
		colorR[R_PURPLE]	= normalizedScoreR[R_PURPLE];
		colorR[R_ORANGE]	= normalizedScoreR[R_ORANGE];
		colorR[R_GREEN]		= normalizedScoreR[R_GREEN];
		colorR[R_BLUE]		= normalizedScoreR[R_BLUE];
		
		for (int i=0; i<numPlayers; i++) {
			if (normalizedScoreR[i] == 1) {
				hub = rColorNames[i];
			}
		}
		hubR = 1;
		
		highPair	= {"none", "none"};
		highR		= 0;
		lowPair		= {"none", "none"};
		lowR		= 0;
	}
	
	
	pGroupR		= groupR;
	pPurpleR	= colorR[R_PURPLE];
	pOrangeR	= colorR[R_ORANGE];
	pGreenR		= colorR[R_GREEN];
	pBlueR		= colorR[R_BLUE];
	pHubR		= hubR;
	pHub		= hub;
	pHighR		= highR;
	pHighPair	= highPair.first + " " + highPair.second;
	pLowR		= lowR;
	pLowPair	= lowPair.first + " " + lowPair.second;
	pPurpleS	= normalizedScoreR[R_PURPLE];
	pOrangeS	= normalizedScoreR[R_ORANGE];
	pGreenS		= normalizedScoreR[R_GREEN];
	pBlueS		= normalizedScoreR[R_BLUE];
	
	
	lslOutput.update(sceneTime);
	
	int oscScene = 0;
	switch (currentScene) {
		case SCENE_IDLE:
			oscScene = 0;
			break;
		case SCENE_PURPLE:
		case SCENE_ORANGE:
		case SCENE_GREEN:
		case SCENE_BLUE:
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
	
	oscOutput.setGroupCorrelation(groupR);
	oscOutput.setPurpleCorrelation(colorR[0]);
	oscOutput.setOrangeCorrelation(colorR[1]);
	oscOutput.setGreenCorrelation(colorR[2]);
	oscOutput.setBlueCorrelation(colorR[3]);
	oscOutput.setHubCorrelation(hubR);
	oscOutput.setHub(hub);
	oscOutput.setHighCorrelation(highR);
	oscOutput.setHighPair(highPair);
	oscOutput.setLowCorrelation(lowR);
	oscOutput.setLowPair(lowPair);
	oscOutput.update();
	
}

//--------------------------------------------------------------
void ofApp::reset() {
	
	for(auto& R : colorR) { R = 0.0;}
	groupR		= 0.0;
	hub 		= "none";
	hubR 		= 0.0;
	highPair	= {"none", "none"};
	highR		= 0;
	lowPair		= {"none", "none"};
	lowR		= 0;
	for(auto& S : scoreR) { S = 0.0;}
//	for(auto& S : normalizedScoreR) { S = 0.0;}
	
	for (auto &t : RTweakers) { t.reset(); }
	hubTweaker.reset();
	highTweaker.reset();
	lowTweaker.reset();
	
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
	correlationParameters.add(pHub.set("hub", "none"));
	correlationParameters.add(pHubR.set("hub R", 0.0, 0.0, 1.0));
	correlationParameters.add(pHighPair.set("high Pair", "none none"));
	correlationParameters.add(pHighR.set("high R", 0.0, 0.0, 1.0));
	correlationParameters.add(pLowPair.set("low Pair", "none none"));
	correlationParameters.add(pLowR.set("low R", 0.0, 0.0, 1.0));
	correlationParameters.add(pGroupR.set("group R", 0.0, 0.0, 1.0));
	correlationParameters.add(pPurpleR.set("purple R", 0.0, 0.0, 1.0));
	correlationParameters.add(pOrangeR.set("orange R", 0.0, 0.0, 1.0));
	correlationParameters.add(pGreenR.set("green R", 0.0, 0.0, 1.0));
	correlationParameters.add(pBlueR.set("blue R", 0.0, 0.0, 1.0));
	
	// BASIC INFO - SCORE
	scoreParameters.setName("Score");
	scoreParameters.add(pPurpleS.set("purple", 0.0, 0.0, 1.0));
	scoreParameters.add(pOrangeS.set("orange", 0.0, 0.0, 1.0));
	scoreParameters.add(pGreenS.set("green", 0.0, 0.0, 1.0));
	scoreParameters.add(pBlueS.set("blue", 0.0, 0.0, 1.0));
	correlationParameters.add(scoreParameters);
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
	
	// EDIT GUI - HUB & PAIR TWEAK
	colorParameters.setName("hub & pair tweak");
	pColorWindow.addListener(this, &ofApp::pColorWindowListener);
	pColorBias.addListener(this, &ofApp::pColorBiasListener);
	colorParameters.add(pColorWindow.set("color window (samples)", 66, 1, 100));
	colorParameters.add(pColorBias.set("color winner bias (pct)", 5, 1, 10));
	editGui.add(colorParameters);
	
	// EDIT GUI - CORRELATION TWEAK
	RParameters.setName("correlation tweak");
	pRInWindow.addListener(this, &ofApp::pRInWindowListener);
	pROutWindow.addListener(this, &ofApp::pROutWindowListener);
	pRHalfTime.addListener(this, &ofApp::pRHalfTimeListener);
//	pRPower.addListener(this, &ofApp::pRPowerListener);
	RParameters.add(pRInWindow.set("R in window (samples)", 10, 1, 50));
	RParameters.add(pRHalfTime.set("R half time (seconds)", 40, 1, 60));
	RParameters.add(pROutWindow.set("R out window (samples)", 30, 1, 50));
//	RParameters.add(pRPower.set("R power (for random data)", 1, 1, 5));
	editGui.add(RParameters);
	
	// EDIT GUI
	if (!ofFile(editGuiFile)) { editGui.saveToFile(editGuiFile); }
	editGui.loadFromFile(editGuiFile);
	
	// ----------------------------
	// EDIT INFO - LOAD & LISTENERS
	
	editInfo.setDefaultWidth(guiWidth);
	switchGuiColor(editInfo, s = !s);
	editInfo.setup("edit info");
	ofParameterGroup &pHub = hubTweaker.getParameters();
	pHub.setName("hub tweak");
	editInfo.add(pHub);
	ofParameterGroup &pHigh = highTweaker.getParameters();
	pHigh.setName("high pair tweak");
	editInfo.add(pHigh);
	ofParameterGroup &pLow = lowTweaker.getParameters();
	pLow.setName("low pair tweak");
	editInfo.add(pLow);
	int c = 0;
	for (auto &t : RTweakers) {
		ofParameterGroup &p = t.getParametersInfo();
		p.setName(tweakNames[c] + " R Tweaker"); c++;
		editInfo.add(p);
	}
	ofParameterGroup &pColor = colorTweaker.getParametersInfo();
	pColor.setName("color R Tweaker"); c++;
	editInfo.add(pColor);
	minimizeGui(&editInfo);
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

