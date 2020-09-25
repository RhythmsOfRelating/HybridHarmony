#pragma once

#include "ofMain.h"
#include "ofxLSL.h"


enum rType{R_DELTA = 0, R_THETA, R_ALPHA, R_BETA, R_AVERAGE};
enum rColor{R_PURPLE = 0, R_ORANGE, R_GREEN, R_BLUE,};
const vector<string> rColorNames({"Purple", "Orange", "Green", "Blue"});

class HD_LSL_R {
public:
	void setup(int _preferredNumHeadsets = 10, float _R_InitValue = 0.6);
	
	void update();
	
	int		getNumHeadsets()			{ return numHeadsets; }
	vector<string> getHeadsetColors()	{ return headSetColors; }
	vector<string> getHeadsetNames()	{ return headSetNames; }
	int		getSampleCount()			{ return sampleCount; }
	
	float	getGroupCorrelation(rType _type = R_AVERAGE){ return groupR[_type]; }
	float	getHighCorrelation(rType _type = R_AVERAGE)	{ return highR[_type]; }
	float	getLowCorrelation(rType _type = R_AVERAGE)	{ return lowR[_type]; }
	float	getHubCorrelation(rType _type = R_AVERAGE)	{ return hubR[_type]; }
	string	getHub(rType _type = R_AVERAGE)				{ return hub[_type]; }
	
	float 	getColorCorrelation(rColor _color, rType _type = R_AVERAGE);
	float	getColorCorrelation(string _color, rType _type = R_AVERAGE);
	float	getPairCorrelation(string _colorA, string _colorB, rType _type = R_AVERAGE);
	float	getPairCorrelation(pair<string,string> _color, rType _type = R_AVERAGE);
	pair<string, string>	getHighCorrelationPair(rType _type = R_AVERAGE);
	pair<string, string>	getLowCorrelationPair(rType _type = R_AVERAGE);
	
	void reset();
	
	ofParameterGroup& getParameters() { return parameters; }
	ofParameterGroup& getDataParameters() { return dataParameters; }
	
private:
	ofxLSL	lslIn;
	unsigned long	sampleCount;
	float			R_InitValue;
	int				SPS; // sample per second
	vector<float>	timeCodeHistory;
	int 			numHeadsets;
	int 			maxNumberOfHeadsets;
	int 			numWaves;
	int 			numMaps;
	vector<string> 	headSetNames;
	vector<string> 	headSetColors;
	
	vector< vector<float> >	pairR;					// each pair, each wavelength
	vector< vector<float> > _colorR;					// each device, each wavelength
	vector< pair<string, string> > pairColorIDs;
	vector< pair<string, string> > pairNameIDs;
	vector< float >	groupR;
	vector< float >	highR;		// for each wavelength
	vector< float >	lowR;			// for each wavelength
	vector< int >	highPairMapIndex;
	vector< int >	lowPairMapIndex;
	vector< float >	hubR;			// for each wavelength
	vector< string >hub;			// for each wavelength
	
	vector< ofxStability > stabilities;
	vector<int> getStability(string _color, vector< ofxStability > _stab);
	
	void			updateMapping(std::vector< pair<string, string> > _mapping);
	void			updateStability(std::vector< ofxStability> _stabilities);
	void			updateWavelengths(vector<float> &_input, vector<float> &_output);
	
	int				getNumberOfHeadSetsFromMapping(int _size);
	int				getMapIndexFromPair(pair<int, int>);
	pair<int, int>	getPairFromMapIndex(int _index);
	pair<string, string>	getColorPairFromMapIndex(int _index);
	
	float	getPairCorrelation(pair<int,int> _indices, rType _type = R_AVERAGE);
	string	getNameFromIndex(int _value);
	string	getColorFromIndex(int _value);
	int		getIndexFromName(string _value);
	int		getIndexFromColor(string _value);
	bool	getColorActive(string _value);
	
	ofParameterGroup				parameters;
	ofParameter<int>				pNumHeadsets;
	ofParameter<string> 			pHeadsetColors;
	ofParameter<string> 			pHeadsetNames;
	ofParameter<int>				pSPS;
	ofParameter<unsigned long>		pSamplesReceived;
	
	ofParameterGroup				dataParameters;
	ofParameterGroup				groupParameters;
	vector< ofParameter<float> >	pGroupR;
	ofParameterGroup				hubParameters;
	vector< ofParameter<float> >	pHubR;
	vector< ofParameter<string> >	pHub;
	ofParameterGroup				highParameters;
	vector< ofParameter<float> >	pHighR;
	vector< ofParameter<string> >	pHighPair;
	ofParameterGroup				lowParameters;
	vector< ofParameter<float> >	pLowR;
	vector< ofParameter<string> >	pLowPair;
	};
