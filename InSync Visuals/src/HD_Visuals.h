#pragma once
#include "ofMain.h"
#include "ofxFlowTools.h"
#include "HD_PlayerFlow.h"
#include "HD_ColorizeShader.h"
#include "ftInverseShader.h"
#include "HD_AttractFlow.h"
#include "HD_PairFlow.h"

using namespace flowTools;

const vector<string> cNames({"Purple", "Orange", "Green", "Blue"});
const vector<glm::vec4> playerDensities({ glm::vec4(1,0,0,0), glm::vec4(0,1,0,0), glm::vec4(0,0,1,0), glm::vec4(0,0,0,1)});
//const vector<glm::vec4> visColors({ glm::vec4(1,0,.83,1), glm::vec4(1,.66,0,1), glm::vec4(0,1,.17,1), glm::vec4(0,.33,1,1)});

enum visualizationTypes{ INPUT_VEL = 0, INPUT_DEN, INPUT_PRS, OBSTACLE, FLUID_BUOY, FLUID_VORT, FLUID_TMP, FLUID_DIVE, FLUID_PRS, FLUID_VEL, FLUID_DEN };

const vector<string> visualizationNames({"velocity", "density", "pressure", "obstacle", "fluid buoyancy", "fluid vorticity", "fluid temperature", "fluid divergence", "fluid pressure", "fluid velocity", "fluid density"});

class HD_Visuals
{
public:
	
	void	setup(int _width, int _height);
	void	update();
	
	void	setMask(ofTexture& _tex);
	void	draw(int _x, int _y, int _w, int _h);
	
	void	reset() { fluidFlow.reset(); }
	
	void	setScene(int _value)		{ scene = _value; }
	void	setProgress(float _value)	{ progress = _value; }
	
	void	setCentre(glm::vec2 _value)			{ pressureFlow.setPosition(_value * glm::vec2(width, height)); centre = _value; }
	void	setPurpleOrigin(glm::vec2 _value)	{ setOrigin(0, _value); }
	void	setOrangeOrigin(glm::vec2 _value)	{ setOrigin(1, _value); }
	void	setGreenOrigin(glm::vec2 _value)	{ setOrigin(2, _value); }
	void	setBlueOrigin(glm::vec2 _value)		{ setOrigin(3, _value); }
	
	void	setGroupR(float _value)		{ groupR	= _value; }
	void	setPurpleR(float _value)	{ Rs[0]		= _value; }
	void	setOrangeR(float _value)	{ Rs[1]		= _value; }
	void	setGreenR(float _value)		{ Rs[2]		= _value; }
	void	setBlueR(float _value)		{ Rs[3]		= _value; }
	
	void	setHub(string _value);
	void	setHighPair(pair<string, string> _pair);
	
	int		getWidth()	{ return width; }
	int		getHeight()	{ return height; }
	
	ofParameterGroup&	getParameters()	{ return parameters; }
	
protected:
	ofParameterGroup		parameters;
	
	ofParameterGroup		visualizationParameters;
	ofParameter<int>		visualizationMode;
	ofParameter<string>		visualizationName;
	ofParameter<float>		visualizationScale;
	ofParameter<bool>		toggleVisualizationScalar;
	ofParameter<bool>		toggleSimpleVis;
	void visualizationModeListener(int& _value)				{ visualizationName.set(visualizationNames[_value]); }
	void visualizationScaleListener(float& _value)			{ for (auto flow : flows) { flow->setVisualizationScale(_value); } }
	void toggleVisualizationScalarListener(bool &_value)	{ for (auto flow : flows) { flow->setVisualizationToggleScalar(_value); } }
	
	ofParameterGroup			colorParameters;
	ofParameter<ofFloatColor>	pPurpleColor;
	ofParameter<ofFloatColor>	pOrangeColor;
	ofParameter<ofFloatColor>	pGreenColor;
	ofParameter<ofFloatColor>	pBlueColor;
	ofParameter<float>			pColorRadius;
	ofParameter<float>			pColorSmooth;
	void pColorRadiusListener(float &_value) { for(int i=0; i<numPlayers; i++) { densityFlow[i].setRadius(_value); velocityFlow[i].setRadius(_value);} }
	void pColorSmoothListener(float &_value) { for(int i=0; i<numPlayers; i++) { densityFlow[i].setSmooth(_value); velocityFlow[i].setSmooth(_value);} }
	void colorListener(ofFloatColor& _value);
	
	ofParameterGroup		introParameters;
	ofParameter<float>		pIntroActiveDensity;
	ofParameter<float>		pIntroPassiveDensity;
	vector<int>				introColorActivated;
	
	ofParameterGroup		RParameters;
	ofParameterGroup		RColorParameters;
	ofParameter<float>		pRColorPassiveDensity;
	ofParameter<float>		pRColorActiveDensity;
	ofParameter<float>		pRColorDensityPower;
	ofParameter<float>		pRColorVelocityAngle;
	ofParameter<float>		pRColorPassiveVelocity;
	ofParameter<float>		pRColorActiveVelocity;
	ofParameter<float>		pRColorVelocityPower;
	
	ofParameterGroup		RGroupParameters;
	ofParameter<float>		pRPressureRadius;
	ofParameter<float>		pRPressurePower;
	ofParameter<float>		pRPressureSpeed;
	
	ofParameterGroup		RPairParameters;
	ofParameter<float>		pRAttractionForceStart;
	ofParameter<float>		pRAttractionForceEnd;
	ofParameter<float>		pRPairForceStart;
	ofParameter<float>		pRPairForceEnd;
	
	ofParameter<float>		pRFluidDissipation;
	
	ofParameterGroup		SParameters;
	ofParameterGroup		SColorParameters;
	ofParameter<float>		pSColorPassiveDensity;
	ofParameter<float>		pSColorActiveDensity;
	ofParameter<float>		pSColorDensityPower;
	ofParameter<float>		pSColorVelocityAngle;
	ofParameter<float>		pSColorPassiveVelocity;
	ofParameter<float>		pSColorActiveVelocity;
	ofParameter<float>		pSColorVelocityPower;
	
	ofParameterGroup		SGroupParameters;
	ofParameter<float>		pSPressureRadius;
	ofParameter<float>		pSPressurePower;
	ofParameter<float>		pSPressureSpeed;
	
	ofParameter<float>		pSFluidDissipation;
	
	int		numPlayers;
	int		width, height;
	
	ofFbo	playerFbo;
	ofFbo	colorizedFbo;
	ofFbo	maskFbo;
	ofFbo	pairFbo;
	HD_ColorizeShader	colorShader;
	ftInverseShader	inverseShader;
	
	glm::vec4*				visColors;
	
	vector< ftFlow* >		flows;
	HD_PlayerFlow*			densityFlow;
	HD_PlayerFlow*			velocityFlow;
	HD_PlayerFlow			pressureFlow;
//	ftVelocityBridgeFlow	velocityBridgeFlow;
//	ftDensityBridgeFlow		densityBridgeFlow;
	ftFluidFlow				fluidFlow;
	
	HD_AttractFlow			attractFlow;
	HD_PairFlow				pairFlow;
	
	int				scene;
	int				prev_scene;
	float			progress;
	
	glm::vec2		centre;
	glm::vec2*		origins;
	glm::vec2*		directions;
	glm::vec2*		velocities;
	float*			Rs;
	float			groupR;
	
	int				hub;
	pair<int, int>	highPair;
	
	void	setOrigin(int _index, glm::vec2 _origin);
	
	void	drawInputDensity(int _x, int _y, int _w, int _h);
	void	drawInputVelocity(int _x, int _y, int _w, int _h);
	void	drawFluid(int _x, int _y, int _w, int _h);
	void	drawSimpleVis(int _x, int _y, int _w, int _h);
	
	float	lfo(float _duration = 1.0, float _rangeMin = 0.0, float _rangeMax = 1.0);
};
	
