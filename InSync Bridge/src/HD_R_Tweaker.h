#pragma once

#include "ofMain.h"

class HD_R_Tweaker {
public:
	void setup(float _R_InitValue = 0.6);
	
	float update(float _R);
	
	void reset();
	
	void setInputWindow(int _value)			{ pInputWindow.set(_value); }
	void setOutputWindow(int _value)		{ pOutputWindow.set(_value); }
	void setPower(float _value)				{ pPower.set(_value); }
	void setAutoRange(bool _value)			{ pAutoRangeToggle.set(_value); }
	void setAutoRangeHalfTime(float _value)	{ pAutoRangeHalfTime.set(_value); }
	
	int		getInputWindow()				{ return pInputWindow.get(); }
	int		getOutputWindow()				{ return pOutputWindow.get(); }
	float	getPower()						{ return pPower.get(); }
	bool	getAutoRange()					{ return pAutoRangeToggle.get(); }
	float	getAutoRangeHalfTime()			{ return pAutoRangeHalfTime.get(); }
	
	int		getBufferSize() 				{ return outputBuffer.size(); }
	
	ofParameterGroup& getParameters()		{ return parameters; }
	ofParameterGroup& getParametersInfo()	{ return dataParameters; }
	
protected:
	deque<float>			inputBuffer;
	deque<float>			outputBuffer;
	ofParameter<float>		pInR, pSmoothInR, pNormalizedR, pSmoothOutR;
	float					smoothInR, normalizedR, smoothOutR;

	ofParameterGroup		parameters;
	float 					initR, initHalfRange;
	ofParameter<int>		pInputWindow, pOutputWindow;
	ofParameter<bool>		pAutoRangeToggle;
	ofParameter<float>		pAutoRangeHalfTime;
	ofParameter<float>		pPower;
	
	ofParameterGroup		dataParameters;
	
	ofParameter<glm::vec2>	pRange;
	
	float					rangeMin;
	float					rangeMax;
	float					minDecayBase;
	float					maxDecayBase;
	float					minDecayTime;
	float					maxDecayTime;
	
	void updateSmoothBuffer(deque<float>& _buffer, float _value) { _buffer.pop_back(); _buffer.push_front(_value); }
	
	float getSmooth(deque<float>& _buffer, int _size);
	
	float getMinRangeDecay(float& _decayBase, float& _decayTime, float _halfTime, float _value);
	
	float getMaxRangeDecay(float& _decayBase, float& _decayTime, float _halfTime, float _value);
	
	float getRangeDecay(float& _decayBase, float& _decayTime, float _halfTime, float _value);
	
	float decay(float _value, float _timePassed, float _halfTime);
	
	float normalize(float _val, float _min, float _max);
	
};
