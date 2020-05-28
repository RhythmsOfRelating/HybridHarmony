#pragma once

#include "ofMain.h"
#include "ftUtil.h"
#include "ftFlow.h"
#include "ftMouseShader.h"


namespace flowTools {
	
	
	class HD_PlayerFlow : public ftFlow{
	public:
		
		void setup(int _width, int _height, ftFlowForceType _type);
		virtual void update(glm::vec4 _force);
		void reset() override;
		
		ofTexture&			getTexture()		{ return outputFbo.getTexture();}
		
		ftFlowForceType		getType()			{ return type; }
		float				getRadius()			{ return pRadius.get(); }
		float				getSmooth()			{ return pSmooth.get(); }
		float				getSpeed()			{ return pSpeed.get(); }
		
		void setRadius(float _value)			{ pRadius.set(_value); }
		void setSmooth(float _value)			{ pSmooth.set(_value) ;}
		void setSpeed(float _value)				{ pSpeed.set(_value); }
		
		void setName(string _name)				{ parameters.setName(_name); }
		
		void setPosition(glm::vec2 _value)		{ position	= _value; }
		
	protected:
		glm::vec2	position;
		
		ofParameter<float>		pSpeed;
		ofParameter<float>		pRadius;
		ofParameter<float>		pSmooth;
		
		ftFlowForceType		type;
		ftMouseShader		mouseShader;
		
		
	};
}


