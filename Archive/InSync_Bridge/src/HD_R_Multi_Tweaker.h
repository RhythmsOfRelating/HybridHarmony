#pragma once

#include "ofMain.h"

class HD_R_Multi_Tweaker : public HD_R_Tweaker{
public:
	
	void setup(vector<string> _inputNames,  float _R_InitValue = 0.6) {
		HD_R_Tweaker::setup(_R_InitValue);
		multiSize = _inputNames.size();
		
		dataParameters.clear();
		dataParameters.setName("info");
		multiParameters.resize(multiSize);
		pInRs.resize(multiSize);
		pSmoothInRs.resize(multiSize);
		pNormalizedRs.resize(multiSize);
		pSmoothOutRs.resize(multiSize);
		
		dataParameters.add(pRange.set("normalization range", glm::vec2(0,1), glm::vec2(0), glm::vec2(1)));
		
		for (int i=0; i<multiSize; i++) {
			multiParameters[i].setName(_inputNames[i]);
			multiParameters[i].add(pInRs[i].set("input", 0, 0, 1));
			multiParameters[i].add(pSmoothInRs[i].set("smooth", 0, 0, 1));
			multiParameters[i].add(pNormalizedRs[i].set("normalized", 0, 0, 1));
			multiParameters[i].add(pSmoothOutRs[i].set("out", 0, 0, 1));
			dataParameters.add(multiParameters[i]);
		}
		parameters.add(dataParameters);
		
		inputBuffers.resize(multiSize);
		outputBuffers.resize(multiSize);
		for (int i=0; i<multiSize; i++) {
			inputBuffers[i].resize(pInputWindow.getMax(), initR);
			outputBuffers[i].resize(pOutputWindow.getMax(), initR);
		}
		reset();
		
	}
	
	vector<float> update(vector<float> _R) {
		for (int i=0; i<multiSize; i++) {
			updateSmoothBuffer(inputBuffers[i], _R[i]);
			smoothInRs[i] = getSmooth(inputBuffers[i], pInputWindow);
		}
		
		rangeMax = 0;
		rangeMin = 1;
		for (int i=0; i<multiSize; i++) {
			if (smoothInRs[i] > rangeMax) { rangeMax = smoothInRs[i]; }
			if (smoothInRs[i] < rangeMin) { rangeMin = smoothInRs[i]; }
		}
		pRange.set( glm::vec2(rangeMin, rangeMax) );
		
		if (rangeMin >= rangeMax) { rangeMin = rangeMax - 0.01; }
		
		for (int i=0; i<multiSize; i++) {
			normalizedRs[i] = normalize(smoothInRs[i], rangeMin, rangeMax);
			updateSmoothBuffer(outputBuffers[i], normalizedRs[i]);
			smoothOutRs[i] = getSmooth(outputBuffers[i], pOutputWindow);
			smoothOutRs[i] = powf(smoothOutRs[i], pPower.get());
		}
		
		for (int i=0; i<multiSize; i++) {
			pInRs[i] = _R[i];
			pSmoothInRs[i] = smoothInRs[i];
			pNormalizedRs[i] = normalizedRs[i];
			pSmoothOutRs[i] = smoothOutRs[i];
		}
		
		return smoothOutRs;
	}
	
	void reset() {
		HD_R_Tweaker::reset();
		
		smoothInRs.clear();
		smoothInRs.resize(multiSize, initR);
		normalizedRs.clear();
		normalizedRs.resize(multiSize, initR);
		smoothOutRs.clear();
		smoothOutRs.resize(multiSize, initR);
		
		for (int i=0; i<multiSize; i++) {
			for (auto& s: inputBuffers[i]) { s = initR; }
			for (auto& s: outputBuffers[i]) { s = initR; }
			pInRs[i] = initR;
			pSmoothInRs[i] = initR;
			pNormalizedRs[i] = initR;
			pSmoothOutRs[i] = initR;
		}
	}
	
private:
	ofParameterGroup		parameters;
	int 					multiSize;
	vector< deque<float> >	inputBuffers;
	vector< deque<float> >	outputBuffers;
	
	vector<float>			smoothInRs, normalizedRs, smoothOutRs;
	
	vector<ofParameterGroup >		multiParameters;
	vector< ofParameter<float>	>	pInRs, pSmoothInRs, pNormalizedRs, pSmoothOutRs;
	
};
