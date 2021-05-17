
#include "HD_R_Tweaker.h"

void HD_R_Tweaker::setup(float _R_InitValue) {
	initR = _R_InitValue;
	initHalfRange = 0.1;
	
	int averageSampleRate = 20;
	
	parameters.setName("tweaker");
	parameters.add(pInputWindow.set("in window", 10, 0, 1 * averageSampleRate));
	parameters.add(pOutputWindow.set("out window", 10, 0, 4 * averageSampleRate));
	parameters.add(pAutoRangeToggle.set("toggle auto range", true));
	parameters.add(pAutoRangeHalfTime.set("auto range half time", 10, 1, 60));
	parameters.add(pPower.set("power", 1, 1, 5));
	parameters.add(pSmoothOutR.set("output", 0, 0, 1));
	
	dataParameters.setName("info");
	dataParameters.add(pInR.set("input", 0, 0, 1));
	pInR.disableEvents();
	dataParameters.add(pSmoothInR.set("smooth", 0, 0, 1));
	dataParameters.add(pRange.set("normalization range", glm::vec2(0,1), glm::vec2(0), glm::vec2(1)));
	dataParameters.add(pNormalizedR.set("normalized", 0, 0, 1));
	dataParameters.add(pSmoothOutR);
	parameters.add(dataParameters);
	
	inputBuffer.resize(pInputWindow.getMax(), initR);
	outputBuffer.resize(pOutputWindow.getMax(), initR);
	reset();
}


float HD_R_Tweaker::update(float _R) {
	updateSmoothBuffer(inputBuffer, _R);
//	int windowSize = pWindow;
	smoothInR = getSmooth(inputBuffer, pInputWindow);
	
	if (pAutoRangeToggle.get()) {
		float halfTime = pAutoRangeHalfTime;
		rangeMin = getMinRangeDecay(minDecayBase, minDecayTime, halfTime, smoothInR);
		rangeMax = getMaxRangeDecay(maxDecayBase, maxDecayTime, halfTime, smoothInR);
		pRange.set( glm::vec2(rangeMin, rangeMax) );
	}
	else {
		rangeMin = pRange.get().x;
		rangeMax = pRange.get().y;
	}
	
	if (rangeMax <= rangeMin) { rangeMax = rangeMin + 0.01; }
	
	normalizedR = normalize(smoothInR, rangeMin, rangeMax);
	updateSmoothBuffer(outputBuffer, normalizedR);
	smoothOutR = getSmooth(outputBuffer, pOutputWindow);
	smoothOutR = powf(smoothOutR, pPower.get());
	
	pInR = _R;
	pSmoothInR = smoothInR;
	pNormalizedR = normalizedR;
	pSmoothOutR = smoothOutR;
	
	return smoothOutR;
}


void HD_R_Tweaker::reset() {
	smoothInR = initR;
	normalizedR = initR;
	smoothOutR = initR;
	for (auto& s: inputBuffer) { s = initR; }
	for (auto& s: outputBuffer) { s = initR; }
	if (pAutoRangeToggle.get()) {
		minDecayBase = 0;
		maxDecayBase = 0;
		minDecayTime = ofGetElapsedTimef();
		maxDecayTime = ofGetElapsedTimef();
		pRange = glm::vec2(initR - initHalfRange, initR + initHalfRange);
	}
	pInR = initR;
	pSmoothInR = initR;
	pNormalizedR = initR;
	pSmoothOutR = initR;
}


float HD_R_Tweaker::getSmooth(deque<float>& _buffer, int _size) {
	if (_size > _buffer.size()) { _size = _buffer.size(); }
	float outValue = 0;
	for (int i=0; i<_size; i++) { outValue += _buffer[i]; }
	outValue /= _size;
	return outValue;
}


float HD_R_Tweaker::getMinRangeDecay(float& _decayBase, float& _decayTime, float _halfTime, float _value) {
	float minRangeMax = .99;
	float rangeValue = ofClamp(1.0 - (_value / minRangeMax), 0.0, 1.0);
	float minRange = getRangeDecay(_decayBase, _decayTime, _halfTime, rangeValue);
	return (1.0 - minRange) * minRangeMax;
}


float HD_R_Tweaker::getMaxRangeDecay(float& _decayBase, float& _decayTime, float _halfTime, float _value) {
	float maxRangeMin = 0.01;
	float rangeValue = ofClamp((_value - maxRangeMin) / (1.0 - maxRangeMin), 0.0, 1.0);
	float maxRange = getRangeDecay(_decayBase, _decayTime, _halfTime, rangeValue);
	return maxRangeMin + maxRange * (1.0 - maxRangeMin);
}


float HD_R_Tweaker::getRangeDecay(float& _decayBase, float& _decayTime, float _halfTime, float _value) {
	float decayedValue = decay(_decayBase, ofGetElapsedTimef() - _decayTime, _halfTime);
	if (_value < decayedValue) { return decayedValue; }
	else {
		_decayBase = _value;
		_decayTime = ofGetElapsedTimef();
		return _decayBase;
	}
}


float HD_R_Tweaker::decay(float _value, float _timePassed, float _halfTime) {
	return _value * powf(2.0, - _timePassed / float(_halfTime));
}


float HD_R_Tweaker::normalize(float _val, float _min, float _max) {
	float normalizedVal =_val - _min;
	normalizedVal /= _max - _min;
	normalizedVal = ofClamp(normalizedVal, 0, 1);
	return normalizedVal;
}

