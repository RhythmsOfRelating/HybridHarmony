#pragma once

#include "ofMain.h"

class MBL_Visuals {
public:

	void	setup(int _width, int _height);
	
	void	setStatus(int _scene, float _time, float _progress)	{ scene = _scene; time = _time; progress = _progress; }
	void	setCorrelation(float _value)			{ correlation = _value; }
	void	setScore(int _value)					{ score = _value; }
	void	setPower1(float _value)					{ power1 = _value; }
	void	setPower2(float _value)					{ power2 = _value; }
	
	void	update();
	void	draw() { draw(0, 0, visualFbo.getWidth(), visualFbo.getHeight()); }
	void	draw(int _x, int _y, int _width, int _height);
	
	ofParameterGroup& getParameters() { return parameters; }
	
private:
	ofImage	headImage1, headImage2;
	ofFbo	visualFbo, headFbo1, headFbo2;
	
	ofTrueTypeFont headFont;
	
	int		scene;
	float	time;
	float	progress;
	
	float	correlation;
	int		score;
	float	power1, power2;
	
	int		width, height;
	
	ofParameterGroup	parameters;
	ofParameter<float>	scale;
	ofParameter<float>	start;
	ofParameter<float>	end;
	ofParameter<bool>	flip1;
	ofParameter<bool>	flip2;
	void flipListener(bool& _value);
	ofParameter<float>	fontSize;
	void fontSizeListener(float& _value) { headFont.load("Arial Narrow.ttf", fontSize.get() * scale.get()); }
	ofParameter<float>	fontY;

	void	fit(ofFbo& _dst, ofTexture& _tex, bool _flip);
};
