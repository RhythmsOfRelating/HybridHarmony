#pragma once

#include "ofMain.h"

struct winnerStruct {
	pair<string,string> stringPair = {"none", "none"};
	int score = 0;;
};

class HD_String_Pair_Tweaker {
public:
	void setup() {
		parameters.setName("tweaker");
		pWindow.set("window (samples)", 10, 1, 50);
//		parameters.add(pWindow);
		pBias.set("winner bias (pct)", 5, 0, 10);
//		parameters.add(pBias);
		parameters.add(pInR.set("input", "none"));
		parameters.add(pOutR.set("output", "none"));
		
		smoothBuffer.resize(pWindow.getMax(), {"none", "none"});
		inStringPair	= {"none", "none"};
		outStringPair	= {"none", "none"};
		
		lastWinnerTime = 0;
		
		reset();
	}
	
	pair<string, string> update(pair<string, string> _stringPair) {
		inStringPair = _stringPair;
		
		updateSmoothBuffer(smoothBuffer, inStringPair);
		int windowSize = pWindow;
		float bias = (pBias / 100.0) * windowSize;
		outStringPair = getSmooth(smoothBuffer, windowSize, outStringPair, bias);
		
		pInR = inStringPair.first + " " + inStringPair.second;
		pOutR = outStringPair.first + " " + outStringPair.second;
		return outStringPair;
	}
	
	void reset() {
		inStringPair	= {"none", "none"};
		outStringPair	= {"none", "none"};
		pInR = "none none";
		pOutR = "non nonee";
		for (auto& s: smoothBuffer) { s = inStringPair; }
	}
	
	void	setWindow(float _value)		{ pWindow.set(_value); }
	void	setBias(float _value)		{ pBias.set(_value); }
	int		getWindow()					{ return pWindow.get(); }
	int		getBias() 					{ return pBias.get(); }
	
	ofParameterGroup& getParameters()	{ return parameters; }
	
private:
	ofParameterGroup		parameters;
	
	deque< pair<string, string> >	smoothBuffer;
	pair<string, string> 			inStringPair, outStringPair;
	float					lastWinnerTime;
	
	ofParameter<float>		pWindow;
	ofParameter<float>		pBias;
	ofParameter<string>		pInR;
	ofParameter<string>		pOutR;
	
	void updateSmoothBuffer(deque< pair<string, string> >& _buffer, pair<string, string> _value) {
		_buffer.pop_back();
		_buffer.push_front(_value);
	}
	
	pair<string, string> getSmooth(deque< pair<string, string> >& _buffer, int _size, pair<string, string> _biasStringPair, int _bias) {
		if (_size > _buffer.size()) { _size = _buffer.size(); }
		vector< winnerStruct > scoreVector;
		winnerStruct winnerBias;
		winnerBias.stringPair = _biasStringPair;
		winnerBias.score = _bias;
		scoreVector.push_back(winnerBias);
		for (int i=0; i<_size; i++) {
			pair<string, string> s = _buffer[i];
			bool stringFound = false;
			for (auto& score : scoreVector) {
				if (score.stringPair == s) {
					score.score++;
					stringFound = true;
					
				}
			}
			if (!stringFound) {
				winnerStruct winnerBias;
				winnerBias.stringPair = s;
				winnerBias.score = 1;
				scoreVector.push_back(winnerBias);
			}
		}
		
		pair<string, string> winnerStringPair = {"none", "none"};
		int winnerScore = 0;
		for (int i=0; i<scoreVector.size(); i++) {
			if (scoreVector[i].score > winnerScore) {
				winnerStringPair = scoreVector[i].stringPair;
				winnerScore = scoreVector[i].score;
			}
		}
		
		return winnerStringPair;
	}
	
};
