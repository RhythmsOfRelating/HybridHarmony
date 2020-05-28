// HALLO SUUZ

#pragma once

#include "ofMain.h"
#include "ofxGui.h"
#include "ofxOsc.h"

#include "HD_LSL_R.h"
#include "HD_R_Tweaker.h"
#include "HD_R_Multi_Tweaker.h"
#include "HD_String_Tweaker.h"
#include "HD_String_Pair_Tweaker.h"

#include "HD_LSL_Out.h"
#include "HD_Osc_Out.h"

const vector<string> tweakNames({"hub", "high", "low", "group"});
const vector<string> sceneNames({"IDLE", "INTRO PURPLE", "INTRO ORANGE", "INTRO GREEN", "INTRO BLUE", "CORRELATE", "SCORE"});
enum scene{SCENE_IDLE = 0, SCENE_PURPLE, SCENE_ORANGE, SCENE_GREEN, SCENE_BLUE, SCENE_CORRELATE, SCENE_SCORE};

class ofApp : public ofBaseApp{
//	use git.lfs to include apps in repository
	
	
	public:
	void setup();
	void update();
	void reset();
	
	void draw();
	void keyPressed(int key);
		
	HD_LSL_R	lslInput;
	HD_LSL_Out	lslOutput;
	HD_Osc_Out	oscOutput;
	
	int		numPlayers;
	float	R_InitValue;
	
	rType	correlationType;
	
	float	groupR;
	vector<float>	colorR;
	float	hubR;
	float	highR;
	float	lowR;
	string	hub;
	pair<string,string> highPair;
	pair<string,string> lowPair;
	vector<float> scoreR;
	vector<float> normalizedScoreR;
	
	int						numTweakers;
	HD_String_Tweaker		hubTweaker;
	HD_String_Pair_Tweaker	highTweaker;
	HD_String_Pair_Tweaker	lowTweaker;
	vector<HD_R_Tweaker>	RTweakers;
	HD_R_Multi_Tweaker		colorTweaker;
	
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
	void				pToggleStartListener(bool & _value)	{ if (_value) {_value = false; if (currentScene == SCENE_IDLE) nextScene = SCENE_PURPLE; } }
	void				pToggleStopListener(bool & _value)	{ if (_value) {_value = false; nextScene = 0;} }
	void				pToggleEditModeListener(bool & _value);
	
	// BASIC INFO - SCENE
	ofParameterGroup 	sceneInfoParameters;
	ofParameter<string>	pSceneName;
	ofParameter<int>	pSceneProgress;
	ofParameter<int>	pSceneSampleCount;
	
	// BASIC INFO - CORRELATION
	ofParameterGroup	correlationParameters;
	ofParameter<float>	pGroupR;
	ofParameter<float>	pPurpleR;
	ofParameter<float>	pOrangeR;
	ofParameter<float>	pGreenR;
	ofParameter<float>	pBlueR;
	ofParameter<string>	pHub;
	ofParameter<float>	pHubR;
	ofParameter<string> pHighPair;
	ofParameter<float>	pHighR;
	ofParameter<string>	pLowPair;
	ofParameter<float>	pLowR;
	
	// BASIC INFO - SCORE
	ofParameterGroup	scoreParameters;
	ofParameter<float>	pPurpleS;
	ofParameter<float>	pOrangeS;
	ofParameter<float>	pGreenS;
	ofParameter<float>	pBlueS;
	
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
	
	ofParameterGroup	colorParameters;
	ofParameter<int>	pColorWindow;
	ofParameter<int>	pColorBias;
	ofParameterGroup	RParameters;
	ofParameter<int>	pRInWindow;
	ofParameter<int>	pRHalfTime;
	ofParameter<int>	pROutWindow;
	ofParameter<float>	pRPower;
	void pColorWindowListener(int &_value)	{ hubTweaker.setWindow(_value); highTweaker.setWindow(_value); lowTweaker.setWindow(_value); }
	void pColorBiasListener(int &_value)	{ hubTweaker.setBias(_value); highTweaker.setBias(_value); lowTweaker.setBias(_value); }
	void pRInWindowListener(int &_value)	{ for (auto &t : RTweakers) { t.setInputWindow(_value); } colorTweaker.setInputWindow(_value); }
	void pROutWindowListener(int &_value)	{ for (auto &t : RTweakers) { t.setOutputWindow(_value); } colorTweaker.setOutputWindow(_value); }
	void pRHalfTimeListener(int &_value)	{ for (auto &t : RTweakers) { t.setAutoRangeHalfTime(_value); }; }
	void pRPowerListener(float &_value)		{ for (auto &t : RTweakers) { t.setPower(_value); } colorTweaker.setPower(_value); }
	
	ofxGuiGroup			editInfo;
	
	float	decimal2MinSec(float _value)	{ return int(_value / 60.0) + fmod(_value / 60.0, 1.0) / 100.0 * 60.0; }
	float 	lfo(float _duration = 1.0)		{ return sin(ofGetElapsedTimef() * M_PI / _duration) / 2.0 + 0.5; }
};

