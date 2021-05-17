/*  ************************************************************************************
 *
 *  HD_PlayerFlow
 *
 *  Created by Matthias Oostrik on 03/16/14.
 *  Copyright 2014 http://www.MatthiasOostrik.com All rights reserved.
 *
 *  Redistribution and use in source and binary forms, with or without
 *  modification, are permitted provided that the following conditions are met:
 *
 *     * Redistributions of source code must retain the above copyright
 *       notice, this list of conditions and the following disclaimer.
 *     * Redistributions in binary form must reproduce the above copyright
 *       notice, this list of conditions and the following disclaimer in the
 *       documentation and/or other materials provided with the distribution.
 *     * Neither the name of the author nor the names of its contributors
 *       may be used to endorse or promote products derived from this software
 *       without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 *  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
 *  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 *  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
 *  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 *  (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
 *  OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
 *  OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
 *  OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
 *  OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 *  ************************************************************************************ */

#include "HD_PlayerFlow.h"

namespace flowTools {
	
	//--------------------------------------------------------------
	void HD_PlayerFlow::setup(int _width, int _height, ftFlowForceType _type) {
		if (_type < FT_DENSITY || _type > FT_OBSTACLE) {
			ofLogWarning("HD_PlayerFlow") << "Type " << ftFlowForceNames[_type] << " not supported";
			return;
		}
		type = _type;
		GLint internalFormat = ftUtil::getInternalFormatFromType(type);
		ftFlow::allocate(_width, _height, internalFormat, _width, _height, internalFormat);
		
		parameters.setName(ftFlowForceNames[type]);
		parameters.add(pSpeed.set("speed", .3, -10, 10));
		parameters.add(pRadius.set("radius", 0.035, 0, 3.0));
		parameters.add(pSmooth.set("smooth", 1.0, 0, 1));
	}
	
	//--------------------------------------------------------------
	void HD_PlayerFlow::update(glm::vec4 _force) {
		ftFlow::reset();
				
		float radius = pRadius.get() * inputWidth;
		
		ofPushStyle();
		ofEnableBlendMode(OF_BLENDMODE_DISABLED);
		mouseShader.update(inputFbo.get(),
						   _force,
						   position,
						   radius,
						   pSmooth.get());
		
		resetOutput();
		float areaForce = .1 / pRadius.get();
		
		add(outputFbo, inputFbo.getTexture(), pSpeed.get() * areaForce);
		
		ofPopStyle();
		
	}
	
	//--------------------------------------------------------------
	void HD_PlayerFlow::reset() {
		ftFlow::reset();
	}
	
}


