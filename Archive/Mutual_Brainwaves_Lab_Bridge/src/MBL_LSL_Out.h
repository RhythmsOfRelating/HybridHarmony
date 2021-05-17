#pragma once

#include "ofMain.h"
#include "lsl_cpp.h"

class MBL_LSL_Out {
public:
	void setup() {
		lsl_info = lsl::stream_info("Session Time","Markers",1, lsl::IRREGULAR_RATE);
		lsl_outlet = new lsl::stream_outlet(lsl_info);
	}
	
	void update(float _sessionTime) {
		
		lsl_outlet->push_sample(&_sessionTime);
	}
	
private:
	
		lsl::stream_info 	lsl_info;
		lsl::stream_outlet*	lsl_outlet;
	};
