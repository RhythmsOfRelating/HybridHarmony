#pragma once

#include "ofMain.h"
#include "ftUtil.h"
#include "ftFlow.h"
#include "HD_AttractShader.h"


namespace flowTools {
	
	
	class HD_AttractFlow : public ftFlow{
	public:
		
		void setup(int _width, int _height){
			allocate(_width, _height, GL_RGBA32F, _width, _height, GL_RG32F);
			parameters.setName("attraction");
			parameters.add(pMaxForce.set("force (max)", 1, 0, 1));
			parameters.add(pStepForce.set("step (pct)", 1, 0, 1));
		}
					
		virtual void update(glm::vec2 _pos, glm::vec4 _color) {
			outputFbo.swap();
			attractShader.update(outputFbo.get(), outputFbo.getBackTexture(), inputFbo.getTexture(), _pos, _color, pMaxForce.get());
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
		HD_AttractShader	attractShader;
		
		
	};
}


