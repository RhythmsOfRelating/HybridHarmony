//
//  HD_Visuals.cpp
//  Visuals Simple
//
//  Created by Ties East on 04/03/2019.
//

#include "HD_Visuals.h"

const vector<string> sceneNames({"IDLE", "INTRO", "CORRELATE", "SCORE"});
enum scene{S_IDLE = 0, S_INTRO, S_CORRELATE, S_SCORE};

void HD_Visuals::setup(int _width, int _height) {
	numPlayers = 4;
	
	width = _width;
	height = _height;
	colorizedFbo.allocate(width, height, GL_RGBA32F);
	maskFbo.allocate(width, height, GL_R8);
	pairFbo.allocate(width, height, GL_RGBA32F);
	
	densityFlow	= new HD_PlayerFlow[4];
	velocityFlow= new HD_PlayerFlow[4];
	pressureFlow.setup(width, height, FT_PRESSURE);
	attractFlow.setup(width, height);
	pairFlow.setup(width, height);
	
	visColors	= new glm::vec4[4];
	
	centre		= glm::vec2(0.5, 0.5);
	origins		= new glm::vec2[4];
	directions	= new glm::vec2[4];
	velocities	= new glm::vec2[4];
	Rs			= new float[4];
	
	fluidFlow.setup(width, height);
//	velocityBridgeFlow.setup(width, height);
//	densityBridgeFlow.setup(width, height, width, height);
	
	flows.push_back(&fluidFlow);
//	flows.push_back(&velocityBridgeFlow);
//	flows.push_back(&densityBridgeFlow);
	
	for (int i=0; i<numPlayers; i++) {
		densityFlow[i].setup(width, height, FT_DENSITY);
		velocityFlow[i].setup(width, height, FT_VELOCITY);
		Rs[i] = 0;
		flows.push_back(&densityFlow[i]);
		flows.push_back(&velocityFlow[i]);
	}
	
	parameters.setName("Flow");
	
	visualizationParameters.setName("visualization");
	visualizationParameters.add(visualizationMode.set("mode", INPUT_DEN, INPUT_VEL, FLUID_DEN));
	visualizationParameters.add(visualizationName.set("name", "fluidFlow Density"));
	visualizationParameters.add(visualizationScale.set("scale", 1, 0.1, 10.0));
	visualizationParameters.add(toggleVisualizationScalar.set("show scalar", false));
	visualizationParameters.add(toggleSimpleVis.set("show simple visualisation", false));
	parameters.add(visualizationParameters);
	visualizationMode.addListener(this, &HD_Visuals::visualizationModeListener);
	toggleVisualizationScalar.addListener(this, &HD_Visuals::toggleVisualizationScalarListener);
	visualizationScale.addListener(this, &HD_Visuals::visualizationScaleListener);
	
	colorParameters.setName("colors");
	pPurpleColor.addListener(this, &HD_Visuals::colorListener);
	pOrangeColor.addListener(this, &HD_Visuals::colorListener);
	pGreenColor.addListener(this, &HD_Visuals::colorListener);
	pBlueColor.addListener(this, &HD_Visuals::colorListener);
	pColorRadius.addListener(this, &HD_Visuals::pColorRadiusListener);
	pColorSmooth.addListener(this, &HD_Visuals::pColorSmoothListener);
	colorParameters.add(pPurpleColor.set("purple",	ofFloatColor( 1.0, 0.0, .83, 1.0), ofFloatColor(0.0, 0.0, 0.0, 0.0), ofFloatColor(1.0, 1.0, 1.0, 1.0)));
	colorParameters.add(pOrangeColor.set("orange",	ofFloatColor( 1.0, .66, 0.0, 1.0), ofFloatColor(0.0, 0.0, 0.0, 0.0), ofFloatColor(1.0, 1.0, 1.0, 1.0)));
	colorParameters.add(pGreenColor.set("green",	ofFloatColor( 0.0, 1.0, .17, 1.0), ofFloatColor(0.0, 0.0, 0.0, 0.0), ofFloatColor(1.0, 1.0, 1.0, 1.0)));
	colorParameters.add(pBlueColor.set("blue",		ofFloatColor( 0.0, .33, 1.0, 1.0), ofFloatColor(0.0, 0.0, 0.0, 0.0), ofFloatColor(1.0, 1.0, 1.0, 1.0)));
	colorParameters.add(pColorRadius.set("radius",	.16, 0,	.3));
	colorParameters.add(pColorSmooth.set("smooth",	1.0, 0,	1));
	parameters.add(colorParameters);
	
	parameters.add(fluidFlow.getParameters());
	
	introParameters.setName("intro");
	introParameters.add(pIntroPassiveDensity.set("passive density"		, 0.09,	0,	0.5	));
	introParameters.add(pIntroActiveDensity.set("active density"		, 0.18,	0,	0.5	));
	parameters.add(introParameters);
	
	introColorActivated.resize(numPlayers, 0);
	
	RParameters.setName("correlate");
	RColorParameters.setName("color");
	RColorParameters.add(pRColorPassiveDensity.set("passive density"	, 0.02,	0,	1	));
	RColorParameters.add(pRColorActiveDensity.set("active density"		, 0.4,	0,	1	));
	RColorParameters.add(pRColorDensityPower.set("density power"		, 1.8,	1,	3	));
	RColorParameters.add(pRColorPassiveVelocity.set("passive velocity"	, 1,	0,	2	));
	RColorParameters.add(pRColorActiveVelocity.set("active velocity"	, 1,	0,	2	));
	RColorParameters.add(pRColorVelocityPower.set("velocity power"		, 1.618,1,	3	));
	RColorParameters.add(pRColorVelocityAngle.set("velocity angle"		, -.15,	-.5,.5	));
	RParameters.add(RColorParameters);
	
	RGroupParameters.setName("group");
	RGroupParameters.add(pRPressureRadius.set("pressure radius"			, .3,	.1,	1	));
	RGroupParameters.add(pRPressurePower.set("pressure power"			, 2,	1,	3	));
	RGroupParameters.add(pRPressureSpeed.set("pressure speed"			, -16,	-20,0	));
	RParameters.add(RGroupParameters);
	RParameters.add(pRFluidDissipation.set("fluid dissipation"			, .3,	0,	1	));
	
	RPairParameters.setName("pair");
	RPairParameters.add(pRAttractionForceStart.set(" attraction start"	, .2,	0,	1	));
	RPairParameters.add(pRAttractionForceEnd.set(" attraction end"		, 1,	0,	1	));
	RPairParameters.add(pRPairForceStart.set("color start"				, 0.002,	0,	0.02));
	RPairParameters.add(pRPairForceEnd.set("color end"					, 0.02,	0,	0.02	));
	RParameters.add(RPairParameters);
	
	parameters.add(RParameters);
	
	SParameters.setName("score");
	SColorParameters.setName("color");
	SColorParameters.add(pSColorPassiveDensity.set("passive density"	, 0.05,	0,	1	));
	SColorParameters.add(pSColorActiveDensity.set("active density"		, 0.05,	0,	1	));
	SColorParameters.add(pSColorDensityPower.set("density power"		, 2,	1,	3	));
	SColorParameters.add(pSColorPassiveVelocity.set("passive velocity"	, 0.5,	0,	2	));
	SColorParameters.add(pSColorActiveVelocity.set("active velocity"	, 0.5,	0,	2	));
	SColorParameters.add(pSColorVelocityPower.set("velocity power"		, 2,	1,	3	));
	SColorParameters.add(pSColorVelocityAngle.set("velocity angle"		, -.1, -.5,	.5	));
	SParameters.add(SColorParameters);
	SGroupParameters.setName("group");
	SGroupParameters.add(pSPressureRadius.set("pressure radius"			, .3,	.1,	1	));
	SGroupParameters.add(pSPressurePower.set("pressure power"			, 2,	1,	3	));
	SGroupParameters.add(pSPressureSpeed.set("pressure speed"			, -10,	-20, 20	));
	SParameters.add(SGroupParameters);
	SParameters.add(pSFluidDissipation.set("fluid dissipation"			, 0,	0,	1	));
	parameters.add(SParameters);
	
//	parameters.add(pressureFlow.getParameters());
//	parameters.add(attractFlow.getParameters());
	
	
}

void HD_Visuals::update() {
	
	bool sceneChanged = false;
	if (scene != prev_scene) {
		sceneChanged = true;
		prev_scene = scene;
	}
	
	if (sceneChanged) {
		for(auto& a : introColorActivated) {a = 0;}
		
		pressureFlow.reset();
		attractFlow.reset();
		for (int i=0; i<numPlayers; i++) {
			velocityFlow[i].reset();
			densityFlow[i].reset();
		}
	}
	
	
	if (scene == S_IDLE) {
		for (int i=0; i<numPlayers; i++) {
//			densityFlow[i].update(playerDensities[i] * pIntroPassiveDensity.get());
//			fluidFlow.addDensity(densityFlow[i].getTexture());
			fluidFlow.setDensityDissipation(1);
			fluidFlow.setVelocityDissipation(1);
		}
	}
	
	if (scene == S_INTRO) {
		for (int i=0; i<numPlayers; i++) {
			if (Rs[i] > 0) { introColorActivated[i] = 1; }
			densityFlow[i].update(playerDensities[i] * (introColorActivated[i] * pIntroPassiveDensity + Rs[i] * pIntroActiveDensity));
			fluidFlow.addDensity(densityFlow[i].getTexture());
			
			fluidFlow.setDensityDissipation(1);
			fluidFlow.setVelocityDissipation(1);
		}
	}
	
	if (scene == S_CORRELATE) {
		// COLOR
		for (int i=0; i<numPlayers; i++) {
			densityFlow[i].update(playerDensities[i] * (pRColorPassiveDensity + powf(Rs[i], pRColorDensityPower) * pRColorActiveDensity));
			
			float angle = lfo(3.3, pRColorVelocityAngle.get(), -1.0 * pRColorVelocityAngle.get());
			glm::vec2 rotatedVelocity = glm::rotate(directions[i], angle);
			float velocityForce = pRColorPassiveVelocity + powf(Rs[i], pRColorVelocityPower) * pRColorActiveVelocity;
			velocities[i] = rotatedVelocity * velocityForce;
			velocityFlow[i].update(glm::vec4(velocities[i], 0.0, 0.0));
			
			fluidFlow.addVelocity(velocityFlow[i].getTexture());
			fluidFlow.addDensity(densityFlow[i].getTexture());
		}
		
		// GROUP
		pressureFlow.setSpeed(pRPressureSpeed);
		pressureFlow.setRadius(pRPressureRadius);
		pressureFlow.update(glm::vec4(powf(1.0 - groupR, pRPressurePower.get()), 0, 0, 0));
		fluidFlow.addPressure(pressureFlow.getTexture(), 1.0);
		
		// PAIR
		if (highPair.first != highPair.second) {
			attractFlow.reset();
			attractFlow.setInput(fluidFlow.getDensity());
			float aForce = pRAttractionForceStart + (pRAttractionForceEnd - pRAttractionForceStart) * progress;
			attractFlow.setForce(aForce);
			attractFlow.update(origins[highPair.first], playerDensities[highPair.second]);
			attractFlow.update(origins[highPair.second], playerDensities[highPair.first]);
			fluidFlow.addVelocity(attractFlow.getTexture());

			pairFlow.setInput(fluidFlow.getDensity());
			float pForce = pRPairForceStart + (pRPairForceEnd - pRPairForceStart) * progress;
			pairFlow.setForce(pForce);
			pairFlow.update(playerDensities[highPair.first], playerDensities[highPair.second]);
			fluidFlow.setDensity(pairFlow.getTexture());
//			fluidFlow.setDensity(pairFlow.getInput());
		}
		
		fluidFlow.setDensityDissipation(pRFluidDissipation);
		fluidFlow.setVelocityDissipation(pRFluidDissipation);
	}
	
	if (scene == S_SCORE) {
		// COLOR
		for (int i=0; i<numPlayers; i++) {
			densityFlow[i].update(playerDensities[i] * (pSColorPassiveDensity + powf(Rs[i], pSColorDensityPower) * pSColorActiveDensity));
			
			velocities[i] = glm::rotate(directions[i], pSColorVelocityAngle.get()) * (pSColorPassiveVelocity + powf(Rs[i], pSColorVelocityPower) * pSColorActiveVelocity);
			velocityFlow[i].update(glm::vec4(velocities[i], 0.0, 0.0));
			
			fluidFlow.addVelocity(velocityFlow[i].getTexture());
			fluidFlow.addDensity(densityFlow[i].getTexture());
		}
		
		// GROUP
		float cp = 0.9;
		float t = 0;
		float p = 0;
		if (progress < cp) {
			t = progress / cp;
			p = 1.0 - powf(t, 2.0);
		}
		else {
			t = 1.0 - ((progress - cp) / (1.0 - cp));
			p = (1.0 - powf(t, 2.0)) * 5;
		}
		
		pressureFlow.setSpeed(pSPressureSpeed * p);
		pressureFlow.setRadius(pSPressureRadius);
		pressureFlow.update(glm::vec4(powf(groupR, pRPressurePower.get()), 0, 0, 0));
		fluidFlow.addPressure(pressureFlow.getTexture(), 1.0);
		
		fluidFlow.setDensityDissipation(pSFluidDissipation);
		fluidFlow.setVelocityDissipation(pSFluidDissipation);
	}
	
	fluidFlow.update(1.0 / 60.0);
	
}

void HD_Visuals::draw(int _x, int _y, int _w, int _h) {
	
	ofEnableBlendMode(OF_BLENDMODE_ALPHA);
	switch(visualizationMode.get()) {
		case INPUT_VEL:		drawInputVelocity(			_x, _y, _w, _h); break;
		case INPUT_DEN:		drawInputDensity(			_x, _y, _w, _h); break;
		case INPUT_PRS:		pressureFlow.draw(			_x, _y, _w, _h); break;
		case OBSTACLE:		fluidFlow.drawObstacle(		_x, _y, _w, _h); break;
		case FLUID_BUOY:	fluidFlow.drawBuoyancy(		_x, _y, _w, _h); break;
		case FLUID_VORT:	fluidFlow.drawVorticity(	_x, _y, _w, _h); break;
		case FLUID_DIVE:	fluidFlow.drawDivergence(	_x, _y, _w, _h); break;
		case FLUID_TMP:		fluidFlow.drawTemperature(	_x, _y, _w, _h); break;
		case FLUID_PRS:		fluidFlow.drawPressure(		_x, _y, _w, _h); break;
		case FLUID_VEL:		fluidFlow.drawVelocity(		_x, _y, _w, _h); break;
		case FLUID_DEN:		drawFluid(					_x, _y, _w, _h); break;
		default: break;
	}
	
	if (toggleSimpleVis.get()) {
		drawSimpleVis(_x, _y, _w, _h);
	}
	
}

void HD_Visuals::drawInputVelocity(int _x, int _y, int _w, int _h) {
	for (int i=0; i<numPlayers; i++) {
		velocityFlow[i].draw(_x, _y, _w, _h);
	}
}

void HD_Visuals::drawInputDensity(int _x, int _y, int _w, int _h) {
	for (int i=0; i<numPlayers; i++) {
		colorShader.update(colorizedFbo, densityFlow[i].getTexture(), visColors[0], visColors[1], visColors[2], visColors[3]);
		colorizedFbo.draw(_x, _y, _w, _h);
	}
}

void HD_Visuals::drawFluid(int _x, int _y, int _w, int _h) {
	colorShader.update(colorizedFbo, fluidFlow.getDensity(), visColors[0], visColors[1], visColors[2], visColors[3]);
	colorizedFbo.draw(_x, _y, _w, _h);
}


void HD_Visuals::drawSimpleVis(int _x, int _y, int _w, int _h) {
	ofPushStyle();
	if (highPair.first != highPair.second) {
		pairFbo.begin();
		ofClear(0);
		ofSetLineWidth(40);
		ofDrawLine(origins[highPair.first], origins[highPair.second]);
		ofDrawCircle(centre * glm::vec2(width, height), groupR * 33);
		ofNoFill();
		ofDrawCircle(centre * glm::vec2(width, height), 33);
		ofDrawCircle(origins[hub], 33);
		
		pairFbo.end();
		ofEnableBlendMode(OF_BLENDMODE_ADD);
		pairFbo.draw(_x, _y, _w, _h);
	}
	ofPopStyle();
}

void HD_Visuals::setMask(ofTexture &_tex) {
	inverseShader.update(maskFbo, _tex);
	fluidFlow.setObstacle(maskFbo.getTexture());
}

void HD_Visuals::setOrigin(int _index, glm::vec2 _origin)	{
	origins[_index] = _origin * glm::vec2(width, height);
	directions[_index] = glm::normalize(centre - _origin);
	densityFlow[_index].setPosition(_origin * glm::vec2(width, height));
	velocityFlow[_index].setPosition(_origin * glm::vec2(width, height));
}

void HD_Visuals::setHub(string _value) {
	hub = -1;
	for (int i=0; i<numPlayers; i++) {
		if (_value	== cNames[i]) {
			hub = i;}
	}
}

void HD_Visuals::setHighPair(pair<string, string> _pair) {
	highPair.first = 0;
	highPair.second = 0;
	for (int i=0; i<numPlayers; i++) {
		if (_pair.first		== cNames[i]) {
			highPair.first = i;
		}
		if (_pair.second	== cNames[i]) {
			highPair.second = i;
		}
	}
}

void HD_Visuals::colorListener(ofFloatColor &_value) {
	visColors[0] = glm::vec4(pPurpleColor.get().r,	pPurpleColor.get().g,	pPurpleColor.get().b,	pPurpleColor.get().a);
	visColors[1] = glm::vec4(pOrangeColor.get().r,	pOrangeColor.get().g,	pOrangeColor.get().b,	pOrangeColor.get().a);
	visColors[2] = glm::vec4(pGreenColor.get().r,	pGreenColor.get().g,	pGreenColor.get().b,	pGreenColor.get().a);
	visColors[3] = glm::vec4(pBlueColor.get().r,	pBlueColor.get().g,		pBlueColor.get().b,		pBlueColor.get().a);
}

float HD_Visuals::lfo(float _duration, float _rangeMin, float _rangeMax) {
	float nLFO = sin(ofGetElapsedTimef() * M_PI / _duration) / 2.0 + 0.5;
	float r = _rangeMax - _rangeMin;
	return nLFO * r + _rangeMin;
}
