#pragma once

#include "ofMain.h"

class HD_String_Tweaker {
public:
	void setup() {
		parameters.setName("tweaker");
		pWindow.set("window (samples)", 10, 1, 50);
//		parameters.add(pWindow);
		pBias.set("winner bias (pct)", 5, 0, 10);
//		parameters.add(pWinnerBias);
		parameters.add(pInR.set("input", "none"));
		parameters.add(pOutR.set("output", "none"));
		
		smoothBuffer.resize(pWindow.getMax(), "none");
		outString = "none";
		
		reset();
	}
	
	string update(string _string) {
		inString = _string;
		
		updateSmoothBuffer(smoothBuffer, inString);
		int windowSize = pWindow;
		int bias = (pBias / 100.0) * windowSize;
		outString = getSmooth(smoothBuffer, windowSize, outString, bias);
		
		pInR = inString;
		pOutR = outString;
		return outString;
	}
	
	void reset() {
		pInR = "none";
		pOutR = "none";
		for (auto& s: smoothBuffer) { s = "none"; }
	}
	
	void	setWindow(float _value)		{ pWindow.set(_value); }
	void	setBias(float _value)		{ pBias.set(_value); }
	int		getWindow()					{ return pWindow.get(); }
	int		getBias() 					{ return pBias.get(); }
	
	ofParameterGroup& getParameters()	{ return parameters; }
	
private:
	ofParameterGroup		parameters;
	
	deque<string>			smoothBuffer;
	string 					inString, outString;
	
	ofParameter<float>		pWindow;
	ofParameter<float>		pBias;
	ofParameter<string>		pInR;
	ofParameter<string>		pOutR;
	
	void updateSmoothBuffer(deque<string>& _buffer, string _value) {
		_buffer.pop_back();
		_buffer.push_front(_value);
	}
	
	string getSmooth(deque<string>& _buffer, int _size, string _biasString, int _bias) {
		if (_size > _buffer.size()) { _size = _buffer.size(); }
		vector< pair<string, int> > scoreVector;
		scoreVector.push_back(pair<string, int>{_biasString, _bias});
		for (int i=0; i<_size; i++) {
			string s = _buffer[i];
			bool stringFound = false;
			for (auto& score : scoreVector) {
				if (score.first == s) {
					score.second++;
					stringFound = true;
					
				}
			}
			if (!stringFound) {
				scoreVector.push_back(pair<string, int>{s, 1});
			}
		}
		
		string winnerString = "none";
		int winnerScore = 0;
		for (int i=0; i<scoreVector.size(); i++) {
			if (scoreVector[i].second > winnerScore) {
				winnerString = scoreVector[i].first;
				winnerScore = scoreVector[i].second;
			}
		}
		
		return winnerString;
	}
	
};
