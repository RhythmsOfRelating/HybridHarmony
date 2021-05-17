// HALLO SUUZ

#pragma once

#include "ofMain.h"
#include "ofxGui.h"
#include "ofxOsc.h"

#include "MBL_LSL_R.h"
#include "MBL_R_Tweaker.h"

#include "MBL_LSL_Out.h"
#include "MBL_Osc_Out.h"

const vector<string> tweakNames({"hub", "high", "low", "group"});
const vector<string> sceneNames({"IDLE", "INTRO", "CORRELATE", "SCORE"});
enum scene{SCENE_IDLE = 0, SCENE_INTRO, SCENE_CORRELATE, SCENE_SCORE};

class ofApp : public ofBaseApp{
//	use git.lfs to include apps in repository
	
	
	public:
	void setup();
	void update();
	void reset();
	
	void draw();
	void keyPressed(int key);
		
	MBL_LSL_R	lslInput;
	MBL_LSL_Out	lslOutput;
	MBL_Osc_Out	oscOutput;
	
	int		numPlayers;
	float	R_InitValue;
	
	rType	correlationType;
	
	float			correlation;
	float			score;
	vector<float>	powers;
	
	MBL_R_Tweaker	RTweaker;
	
	// GUI
	void				setupGui();
	
	ofxGuiGroup			sessionGui;
	void				drawGui();
	void				minimizeGui(ofxGuiGroup* _group);
	void				minimizeSubGroups(ofxGuiGroup* _group);
	void				switchGuiColor(ofxGuiGroup& _panel, bool _switch);
	void				oneDecimalsListener(float& _value) { _value = int(_value * 10) / 10.0; }
	void				twoDecimalsListener(float& _value) { _value = int(_value * 100) / 100.0; }
	
	ofParameter<bool>	pToggleIdle;
	
	int					numScenes;
	int 				currentScene;
	int 				nextScene;
	float				scenePosition;
	float 				sceneStartTime;
	float 				sceneTime;
	float 				sceneDuration;
	float 				sceneSampleStart;
	
	// BASIC GUI
	ofxGuiGroup			infoGui;
	ofParameter<bool>	pToggleStart;
	ofParameter<bool>	pToggleStop;
	ofParameter<bool>	pToggleEditMode;
	void				pToggleStartListener(bool & _value)	{ if (_value) {_value = false; if (currentScene == SCENE_IDLE) nextScene = SCENE_INTRO; } }
	void				pToggleStopListener(bool & _value)	{ if (_value) {_value = false; nextScene = 0;} }
	void				pToggleEditModeListener(bool & _value);
	
	// BASIC INFO - SCENE
	ofParameterGroup 	sceneInfoParameters;
	ofParameter<string>	pSceneName;
	ofParameter<int>	pSceneProgress;
	ofParameter<int>	pSceneSampleCount;
	
	// BASIC INFO - CORRELATION
	ofParameterGroup	correlationParameters;
	ofParameter<float>	pCorrelation;
	ofParameter<float>	pScore;
	ofParameter<float>	pPower1;
	ofParameter<float>	pPower2;
	
	// EDIT GUI
	ofxPanel			editGui;
	ofParameter<float>	pFPS;
	
	// EDIT GUI - SCENE
	ofParameterGroup	sceneParameters;
	void				pEditModeListener(bool& _value)	{ if (!pToggleEditMode.get()) { _value = false; } }
	ofParameter<bool>	pFastMode;
	ofParameter<bool>	pToggleNextScene;
	void				pToggleNextSceneListener(bool& _value);
	ofParameter<bool>	pContinuousMode;
	ofParameter<bool>	pToggleReset;
	void				pToggleResetListener(bool& _value) { if (_value) { _value = false; reset(); } }
	ofParameterGroup	durationParameters;
	ofParameter<float>	pIntroDuration;
	ofParameter<float>	pCorrelateDuration;
	ofParameter<float>	pScoreDuration;
	
	ofParameterGroup	RParameters;
	
	ofxGuiGroup			editInfo;
	
	float	decimal2MinSec(float _value)	{ return int(_value / 60.0) + fmod(_value / 60.0, 1.0) / 100.0 * 60.0; }
	float 	lfo(float _duration = 1.0)		{ return sin(ofGetElapsedTimef() * M_PI / _duration) / 2.0 + 0.5; }
};

