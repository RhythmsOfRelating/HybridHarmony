//
//  HD_LSL_R.cpp
//  Core
//
//  Created by Ties East on 08/02/2019.
//

#include "HD_LSL_R.h"


void HD_LSL_R::setup(int _preferredNumHeadsets, float _R_InitValue) {
	lslIn.start();
	
	numWaves = (int)R_AVERAGE + 1;
	sampleCount = 0;
	R_InitValue = _R_InitValue;
	
	groupR.resize(numWaves, R_InitValue);
	highR.resize(numWaves, R_InitValue);
	lowR.resize(numWaves, R_InitValue);
	highPairMapIndex.resize(numWaves);
	lowPairMapIndex.resize(numWaves);
	hub.resize(numWaves, "none");
	hubR.resize(numWaves, R_InitValue);
	
	parameters.setName("headsets");
	parameters.add(pNumHeadsets.set("number", 0, 0, _preferredNumHeadsets));
	parameters.add(pHeadsetColors.set("colors", "none"));
	parameters.add(pHeadsetNames.set("names", "none"));
	parameters.add(pSamplesReceived.set("samples received", 0, 0, 1));
	parameters.add(pSPS.set("samples per second", 0, 0, 30));

	dataParameters.setName("EEG Raw");
	vector<string> waveNames = {"delta", "theta", "alpha", "beta", "average"};
	groupParameters.setName("group correlation");
	hubParameters.setName("hub correlation");
	highParameters.setName("high correlation");
	lowParameters.setName("low correlation");
	
	pHubR.resize(numWaves);
	pHub.resize(numWaves);
	pGroupR.resize(numWaves);
	pHighR.resize(numWaves);
	pLowR.resize(numWaves);
	pHighPair.resize(numWaves);
	pLowPair.resize(numWaves);
	for (int w=0; w<numWaves; w++) {
		groupParameters.add(pGroupR[w].set(waveNames[w] + " R", 0, 0, 1));
		hubParameters.add(pHub[w].set(waveNames[w] + " hub", "none"));
		hubParameters.add(pHubR[w].set(waveNames[w] + " R", 0, 0, 1));
		highParameters.add(pHighPair[w].set(waveNames[w] + " pair", "none"));
		highParameters.add(pHighR[w].set(waveNames[w] + " R", 0, 0, 1));
		lowParameters.add(pLowPair[w].set(waveNames[w] + " pair", "none"));
		lowParameters.add(pLowR[w].set(waveNames[w] + " R", 0, 0, 1));
	}
	dataParameters.add(groupParameters);
	dataParameters.add(hubParameters);
	dataParameters.add(highParameters);
	dataParameters.add(lowParameters);
}

//--------------------------------------------------------------
void HD_LSL_R::update() {
	if (!lslIn.isConnected()) {
		reset();
	}
	else {
		if (numHeadsets == 0) {
			updateMapping(lslIn.getMapping());
		}
		
//		stabilities = lslIn.getStability();
//		
//		for (auto &stab: stabilities) {
//			cout << stab.color;
//			for (auto &s: stab.sample) {
//				cout << s;
//			}
//			cout << endl;
//		}
		
		vector<ofxLSLSample> buffer = lslIn.flush();
		if(buffer.size()) {
			sampleCount = (sampleCount + buffer.size());
			float timeCode = buffer.back().timestamp;
			timeCodeHistory.push_back(timeCode);
			auto rValues = buffer.back().sample; // 2DO use all samples
			
			// AVERAGE CORRELATION
			int chunkCounter = 0;
			for (int i=0; i<numMaps; i++) {
				vector<float>::const_iterator first = rValues.begin() + chunkCounter;
				vector<float>::const_iterator last = rValues.begin() + chunkCounter + 16;
				vector<float> subVec(first, last);
				updateWavelengths(subVec, pairR[i]);
				chunkCounter+=16;
			}
			
			// GROUP CORRELATION
			groupR[4] = 0;
			for (int i=0; i<4; i++) {
				groupR[i] = 0;
				int counter = 0;
				for (auto pair: pairR) {
					groupR[i] += pair[i];
					counter++;
				}
				groupR[i] /= counter;
				groupR[4] += groupR[i];
			}
			groupR[4] /= 4.0;
			
			// HIGH & LOW CORRELATION
			if (numHeadsets == 2) {
				for (int w=0; w<numWaves; w++) {
					highR[w] = groupR[w];
					lowR[w] = groupR[w];
					highPairMapIndex[w] = 0;
					lowPairMapIndex[w] = 0;
				}
			}
			else {
				for (int w=0; w<numWaves; w++) {
					float high = 0;
					float low = 1;
					int highIndex = 0;
					int lowIndex = 0;
					for (int i=0; i < pairR.size(); i++) {
						float R = pairR[i][w];
						if (R > high) { high = R; highIndex = i; }
						if (R < low)  { low = R;  lowIndex = i; }
					}
					highR[w] = high;
					highPairMapIndex[w] = highIndex;
					lowR[w] = low;
					lowPairMapIndex[w] = lowIndex;
				}
			}
			
			// COLOR & HUB CORRELATION
			
			if (numHeadsets == 2) {
				for (int w=0; w<numWaves; w++) {
					_colorR[0][w] = groupR[w];
					_colorR[1][w] = groupR[w];
					hubR[w] = groupR[w];
					hub[w] = getColorFromIndex(0); // or 1, whatever
				}
			}
			else {
				for (int i=0; i<numHeadsets; i++) {
					for (int w=0; w<numWaves; w++) {
						_colorR[i][w] = 0;
						for (int j=0; j<numHeadsets; j++) {
							pair<int, int> _indices = make_pair(i, j);
							if (i !=j ) {
								_colorR[i][w] += getPairCorrelation(_indices, (rType)w);
							}
						}
						_colorR[i][w] /= numHeadsets - 1.0;
					}
				}
				
				vector<float>	hub_HighCorrelation;
				vector<int>		hub_HighCorrelationIndex;
				hub_HighCorrelation.resize(numWaves, 0);
				hub_HighCorrelationIndex.resize(numWaves, 0);
				// select highest
				for (int i=0; i<numHeadsets; i++) {
					for (int w=0; w<numWaves; w++) {
						if (_colorR[i][w] > hub_HighCorrelation[w]) {
							hub_HighCorrelationIndex[w] = i;
							hub_HighCorrelation[w] = _colorR[i][w];
						}
					}
				}
				for (int w=0; w<numWaves; w++) {
					hubR[w] = hub_HighCorrelation[w];
					hub[w] = getColorFromIndex(hub_HighCorrelationIndex[w]);
				}
			}
			
			// PARAMETERS
			
			float mostRecentTime = timeCodeHistory.back();
			for (int i=timeCodeHistory.size()-1; i>=0; i--) {
				if (timeCodeHistory[i] < mostRecentTime - 1.0) timeCodeHistory.erase(timeCodeHistory.begin() + i);
			}
			pSPS = timeCodeHistory.size();
			
			
			for (int w=0; w<numWaves; w++) {
				pGroupR[w] = groupR[w];
				pHubR[w] = hubR[w];
				pHighR[w] = highR[w];
				pLowR[w] = lowR[w];
				
				pHub[w] = hub[w];
				pair<string, string> ss;
				ss = getHighCorrelationPair((rType)w);
				pHighPair[w] = ss.first + " & " + ss.second;
				ss = getLowCorrelationPair((rType)w);
				pLowPair[w] = ss.first + " & " + ss.second;
				
			}
		}
		pNumHeadsets = numHeadsets;
		pHeadsetColors = "";
		for (auto &c : headSetColors)	{ pHeadsetColors += c + " "; }
		pHeadsetNames = "";
		for (auto &c : headSetNames)	{ pHeadsetNames+= c + " "; }
		pSamplesReceived = sampleCount;
	}
}

void HD_LSL_R::reset() {
	sampleCount = 0;
	numHeadsets = 0;
	pNumHeadsets = numHeadsets;
	pHeadsetColors = "";
	pHeadsetNames = "";
}

//--------------------------------------------------------------
//-- averages the correlation from 4 x 4 nodes over 4 wavelengths
void HD_LSL_R::updateWavelengths(vector<float> &_input, vector<float> &_output) {
	
	float avgDelta = 0;
	float avgTheta = 0;
	float avgAlpha = 0;
	float avgBeta  = 0;
//	for (int n=0; n<4; n++) {
//		avgDelta += fabs(_input[n * 4 + 0]);
//		avgTheta += fabs(_input[n * 4 + 1]);
//		avgAlpha += fabs(_input[n * 4 + 2]);
//		avgBeta  += fabs(_input[n * 4 + 3]);
//	}
//
//	avgDelta /= 4.0;
//	avgTheta /= 4.0;
//	avgAlpha /= 4.0;
//	avgBeta /= 4.0;
	for (int n=1; n<3; n++) {
		avgDelta += fabs(_input[n * 4 + 0]);
		avgTheta += fabs(_input[n * 4 + 1]);
		avgAlpha += fabs(_input[n * 4 + 2]);
		avgBeta  += fabs(_input[n * 4 + 3]);
	}
	
	avgDelta /= 2.0;
	avgTheta /= 2.0;
	avgAlpha /= 2.0;
	avgBeta /= 2.0;
	
	if (isnan(avgDelta)) { avgDelta = R_InitValue; }
	if (isnan(avgTheta)) { avgTheta = R_InitValue; }
	if (isnan(avgAlpha)) { avgAlpha = R_InitValue; }
	if (isnan(avgBeta))  { avgBeta = R_InitValue;  }
	
	_output[0] = avgDelta;
	_output[1] = avgTheta;
	_output[2] = avgAlpha;
	_output[3] = avgBeta;
	_output[4] = (avgDelta + avgTheta + avgAlpha + avgBeta) / 4.0;
}

//--------------------------------------------------------------
void HD_LSL_R::updateMapping(std::vector<pair<string, string> > _mapping) {
	numMaps = (int)_mapping.size();
	numHeadsets = getNumberOfHeadSetsFromMapping((int)_mapping.size());
	
	_colorR.clear();
	_colorR.resize(numHeadsets);
	for (int i=0; i<numHeadsets; i++) {
		_colorR[i].resize(numWaves, R_InitValue);
	}
		
	pairR.clear();
	pairR.resize(numMaps);
	pairColorIDs.clear();
	pairColorIDs.resize(numMaps);
	pairNameIDs.clear();
	pairNameIDs.resize(numMaps);
	for (int i=0; i<numMaps; i++) {
		pairR[i].resize(numWaves, R_InitValue);
		vector<std::string> splitString;
		string a = _mapping[i].first;
		splitString = ofSplitString(a, "-");
		pairNameIDs[i].first = splitString[3];
		pairColorIDs[i].first = splitString[0];
		string b = _mapping[i].second;
		splitString = ofSplitString(b, "-");
		pairNameIDs[i].second = splitString[3];
		pairColorIDs[i].second = splitString[0];
		cout << pairColorIDs[i].first << " " << pairColorIDs[i].second << endl;
	}
//	cout << "update mapping " << numHeadsets << endl;
	
	headSetNames.clear();
	headSetColors.clear();
	
	if (numHeadsets == 0) {
		ofLogWarning("updateMapping") << "mapping size = 0";
		return;
	}
	
	headSetColors.push_back(pairColorIDs[0].first);
	headSetNames.push_back(pairNameIDs[0].first);
	for (int i=0; i<numHeadsets-1; i++) {
		headSetColors.push_back(pairColorIDs[i].second);
		headSetNames.push_back(pairNameIDs[i].second);
	}
	
//	pNumHeadsetsConnected = numHeadsets;
//	for (int i=0; i<maxNumberOfHeadsets; i++) {
//		pHeadsetCNs[i].set(getColorFromIndex(i) + " " + getNameFromIndex(i));
//	}
//	
//	for (int i=0; i<numMaps; i++) {
//		pair<int, int> cPair = getPairFromMapIndex(i);
//		int mi = getMapIndexFromPair(cPair);
//		cout << i << " " << mi << " " << getColorFromIndex(cPair.first) << " "  << getColorFromIndex(cPair.second) << endl;
//	}
}

//--------------------------------------------------------------
vector<int> HD_LSL_R::getStability(std::string _color, vector<ofxStability> _stab) {
	for (auto& s: _stab) {
		if (s.color == _color) {
			return s.sample;
		}
	}
	vector<int> emptyVector;
	return emptyVector;
}

//--------------------------------------------------------------

float HD_LSL_R::getColorCorrelation(rColor _color, rType _type) {
	return getColorCorrelation(rColorNames[_color], _type);
}

float HD_LSL_R::getColorCorrelation(string _color, rType _type) {
	if (getColorActive(_color)) {
		int index = getIndexFromColor(_color);
		return _colorR[index][_type];
	}
	return R_InitValue;
}

//--------------------------------------------------------------

float HD_LSL_R::getPairCorrelation(string _colorA, string _colorB, rType _type){
	pair<string, string> cPair = make_pair (_colorA, _colorB);
	return getPairCorrelation(cPair, _type);
}

float HD_LSL_R::getPairCorrelation(pair<string, string> _color, rType _type) {
	pair<int, int> cPair = make_pair (getIndexFromColor(_color.first), getIndexFromColor(_color.second));
	return getPairCorrelation(cPair, _type);
	
}

float HD_LSL_R::getPairCorrelation(pair<int,int> _indices, rType _type) {
	int mapIndex = getMapIndexFromPair(_indices);
	return (pairR[mapIndex][_type]);
}

pair<string, string> HD_LSL_R::getHighCorrelationPair(rType _type) {
	return getColorPairFromMapIndex(highPairMapIndex[_type]);
}

pair<string, string> HD_LSL_R::getLowCorrelationPair(rType _type) {
	return getColorPairFromMapIndex(lowPairMapIndex[_type]);
}

//--------------------------------------------------------------
int HD_LSL_R::getMapIndexFromPair(pair<int, int> _pair) {
	int low = min(_pair.first, _pair.second);
	int high = max(_pair.first, _pair.second);
	
	if (high >= numHeadsets) {
		ofLogWarning("HD_LSL_R::getMapIndexFromPair") << high << " out of range of " << numHeadsets;
		return R_InitValue;
	}
	if (low == high) { return 1; } // correlation with self // why 1??
	
	int mapIndex = 0;
	for (int i=0; i<low; i++) {
		mapIndex += numHeadsets - 1 - i;
	}
	mapIndex += high - low - 1;
	
	return mapIndex;
}

//--------------------------------------------------------------
pair<int, int> HD_LSL_R::getPairFromMapIndex(int _index) {
	
	pair<int, int> cPair = make_pair(0,0);
	if (_index >= numMaps) {
		ofLogWarning("HD_LSL_R::getPairIndexFromMapIndex") << _index << " out of range of " << numMaps;
		return cPair;
	}
	
	if (numHeadsets <1) {
		cout << "AAAAAHHHHHH" << endl;
		return cPair;
	}
	int fP = 0;
	int currentLevel = 0;
	int nextLevel = numHeadsets - 1;
	for (int i=0; _index >= nextLevel; i++) {
		fP++;
		currentLevel = nextLevel;
		nextLevel += numHeadsets -2 -i ;
	}
	cPair.first = fP;
	cPair.second = _index - currentLevel + 1 + fP;
	
//	int sP = 0;
//	for (int i=0; i<fP; i++) {
//		sP += numHeadsets -1 -i ;
//	}
//	cPair.second = _index - sP + 1 + fP;
	
	return cPair;
}

pair<string, string> HD_LSL_R::getColorPairFromMapIndex(int _index) {
	pair<int, int> ip = getPairFromMapIndex(_index);
	pair<string, string> cp = {getColorFromIndex(ip.first), getColorFromIndex(ip.second)};
	return cp;
}

//--------------------------------------------------------------
int HD_LSL_R::getNumberOfHeadSetsFromMapping(int _size){
	
	int numHeadsets = 1;
	int nextLevel = 1;
	int sizeLeft = _size;
	for (int i=0; sizeLeft > 0; i++) {
		if (sizeLeft >= nextLevel) {
			numHeadsets ++;
			sizeLeft -= nextLevel;
			nextLevel++;
		}
		else {
			ofLogWarning("getNumberOfHeadSetsFromMapping") << "this does not make sense";
			return 0;
		}
	}
	if (numHeadsets < 2) { return 0; }
	return numHeadsets;
}

//--------------------------------------------------------------
string HD_LSL_R::getNameFromIndex(int _value) {
	if (_value >= numHeadsets) {
		ofLogVerbose("HD_LSL_R::getNameFromIndex") << "index " << _value << " out of range, 0.." << numHeadsets;
		return "no_name";
	}
	return headSetNames[_value];
}

string HD_LSL_R::getColorFromIndex(int _value) {
	if (_value >= numHeadsets) {
		ofLogVerbose("HD_LSL_R::getColorFromIndex") << "index " << _value << " out of range, 0.." << numHeadsets;
		return "no_color";
	}
	return headSetColors[_value];
}

int HD_LSL_R::getIndexFromName(string _value) {
	for (int i=0; i<headSetNames.size(); i++) {
		if (_value == headSetNames[i]) {
			return i;
		}
	}
	ofLogVerbose("HD_LSL_R::getIndexFromName") << "name " << _value << " not found";
	return 0;
}

int HD_LSL_R::getIndexFromColor(string _value) {
	for (int i=0; i<headSetColors.size(); i++) {
		if (_value == headSetColors[i]) {
			return i;
		}
	}
	ofLogVerbose("HD_LSL_R::getIndexFromColor") << "color " << _value << " not found";
	return 0;
}

bool HD_LSL_R::getColorActive(string _value) {
	for (int i=0; i<headSetColors.size(); i++) {
		if (_value == headSetColors[i]) {
			return true;
		}
	}
	return false;
}


