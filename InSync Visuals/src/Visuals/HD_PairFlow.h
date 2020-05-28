#pragma once

#include "ofMain.h"
#include "ftUtil.h"
#include "ftFlow.h"
#include "HD_PairShader.h"


namespace flowTools {
	
	
	class HD_PairFlow : public ftFlow{
	public:
		
		void setup(int _width, int _height){
			allocate(_width, _height, GL_RGBA32F, _width, _height, GL_RGBA32F);
			parameters.setName("pair");
			parameters.add(pMaxForce.set("force (max)", 1, 0, 1));
			parameters.add(pStepForce.set("step (pct)", 1, 0, 1));
		}
					
		virtual void update(glm::vec4 _colorA, glm::vec4 _colorB) {
			pairShader.update(outputFbo.get(), inputFbo.getTexture(), _colorA, _colorB, pMaxForce.get());
		}
		
		ofTexture&	getTexture()		{ return outputFbo.getTexture();}
		
		float	getForce()				{ return pMaxForce.get(); }
		
		void	setForce(float _value)	{ pMaxForce.set(_value); }
		
		void	setName(string _name)	{ parameters.setName(_name); }
		
	protected:
		glm::vec2	position;
		
		ofParameter<float>	pStepForce;
		ofParameter<float>	pMaxForce;
		
		ftFlowForceType		type;
		HD_PairShader		pairShader;
		
		
	};
}


