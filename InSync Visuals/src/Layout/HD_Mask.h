#pragma once
#include "ofMain.h"
#include "ofxXmlSettings.h"

class HD_Mask
{
public:
	HD_Mask();
	~HD_Mask();
	
	virtual void setup(int _width, int _height);
	
	ofTexture& getMask() { return maskFbo.getTexture(); }
	
	ofMesh getMesh() { return maskMesh; }
	
	ofParameterGroup& getParameters()	{ return parameters; }
	
	bool getEditMode() { return pToggleEditMask.get(); }
	
protected:
	virtual void update();
	virtual void draw(int _x, int _y, int _w, int _h);
	
	ofMesh maskMesh;
	float width, height, windowWidth, windowHeight;
	ofParameterGroup parameters;
	ofParameterGroup maskTweakParameters;
	
private:
	void mouseMoved(ofMouseEventArgs& _event);
	void mouseDragged(ofMouseEventArgs& _event);
	void mousePressed(ofMouseEventArgs& _event);
	void windowResized(ofResizeEventArgs& _event);
	void keyPressed(ofKeyEventArgs& _event);
	
	void load();
	void save();
	

	glm::vec3 lastMousePos;
	
	int numVertices;
	int activeVertex;
	ofFbo maskFbo;
	
	int pointSize;
	ofxXmlSettings	maskXml;
	ofParameter<bool> pToggleEditMask;
	ofParameter<bool> pAddVertex;
	ofParameter<bool> pDeleteVertex;
	ofParameter<bool> pSaveMask;
	ofParameter<bool> pLoadMask;
	
	void pAddVertexListener(bool& _value);
	void pDeleteVertexListener(bool& _value);
	void pSaveMaskListener(bool& _value) { if (_value) {_value = false; save();} }
	void pLoadMaskListener(bool& _value) { if (_value) {_value = false; load();} }
	void moveVertex(bool _left, bool _right, bool _up, bool _down);
	
	ofParameter<bool> maskNudgeRight;
	ofParameter<bool> maskNudgeLeft;
	ofParameter<bool> maskNudgeUp;
	ofParameter<bool> maskNudgeDown;
	void maskNudgeRightListener(bool& _value)	{ _value = false; nudgeMask(1,0,0,0); }
	void maskNudgeLeftListener(bool& _value)	{ _value = false; nudgeMask(0,1,0,0); }
	void maskNudgeUpListener(bool& _value)		{ _value = false; nudgeMask(0,0,1,0); }
	void maskNudgeDownListener(bool& _value)	{ _value = false; nudgeMask(0,0,0,1); }
	
	void nudgeMask(bool _left, bool _right, bool _up, bool _down);
	
	void updateMaskListener(float& _value)		{ update(); }
	glm::vec3 MP2TP(glm::vec3 _mousPos);
};
