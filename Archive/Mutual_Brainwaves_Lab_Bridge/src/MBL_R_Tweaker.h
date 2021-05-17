#pragma once

#include "ofMain.h"
#include "HD_R_Tweaker.h"

class MBL_R_Tweaker : public HD_R_Tweaker{
	public:
	
	void setup(float _R_InitValue = 0.6) {
		initR = _R_InitValue;
		initHalfRange = 0.1;
		
		int averageSampleRate = 20;
		
		parameters.setName("tweaker");
		pInR.disableEvents();
		pSmoothInR.disableEvents();
		pSmoothOutR.disableEvents();
		parameters.add(pInR.set("input", 0, 0, 1));
		parameters.add(pInputWindow.set("input smooth window", 10, 0, 1 * averageSampleRate));
		parameters.add(pSmoothInR.set("smoothed input", 0, 0, 1));
		dataParameters.setName("range");
		dataParameters.add(pAutoRangeToggle.set("toggle auto range", false));
		dataParameters.add(pAutoRangeHalfTime.set("auto range half time", 10, 1, 60));
		dataParameters.add(pRange.set("normalization range", glm::vec2(0,1), glm::vec2(0), glm::vec2(1)));
		dataParameters.add(pNormalizedR.set("normalized input", 0, 0, 1));
		parameters.add(dataParameters);
		parameters.add(pOutputWindow.set("output smooth window", 30, 0, 4 * averageSampleRate));
		parameters.add(pPower.set("output power", 1, 1, 5));
		parameters.add(pSmoothOutR.set("output", 0, 0, 1));
				
		inputBuffer.resize(pInputWindow.getMax(), initR);
		outputBuffer.resize(pOutputWindow.getMax(), initR);
		reset();
	}
	
};
