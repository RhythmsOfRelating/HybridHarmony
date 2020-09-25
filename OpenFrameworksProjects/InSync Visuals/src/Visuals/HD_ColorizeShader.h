
#pragma once

#include "ofMain.h"
#include "ftShader.h"

namespace flowTools {
	
	class HD_ColorizeShader : public ftShader {
	public:
		HD_ColorizeShader() {
			bInitialized = 1;
			if (ofIsGLProgrammableRenderer()) { glFour(); } else { glTwo(); }
			string shaderName = "HD_ColorizeShader";
			if (bInitialized) { ofLogVerbose(shaderName + " initialized"); }
			else { ofLogWarning(shaderName + " failed to initialize"); }
		}
		
	protected:
		void glTwo() {
			fragmentShader = GLSL120(
									 uniform vec4	restColor;
									 
									 void main(){
										 gl_FragColor = restColor;
										 
									 }
									 
									 );
			
			setupShaderFromSource(GL_FRAGMENT_SHADER, fragmentShader);
			linkProgram();
			
		}
		
		void glFour() {
			
			fragmentShader = GLSL410(
									 uniform sampler2DRect SourceTexture;
									 uniform vec4	PurpleColor;
									 uniform vec4	OrangeColor;
									 uniform vec4	GreenColor;
									 uniform vec4	BlueColor;
									 
									 in vec2 texCoordVarying;
									 out vec4 fragColor;
									 
									 void main(){
										 vec2 st = texCoordVarying;
										 vec4 srcCol = texture(SourceTexture, st);
										 vec4 purple = srcCol.x * PurpleColor;
										 vec4 orange = srcCol.y * OrangeColor;
										 vec4 green = srcCol.z * GreenColor;
										 vec4 blue = srcCol.w * BlueColor;
										 
										 fragColor = purple + orange + green + blue;
									 }
									 );
			
			setupShaderFromSource(GL_VERTEX_SHADER, vertexShader);
			setupShaderFromSource(GL_FRAGMENT_SHADER, fragmentShader);
			bindDefaults();
			linkProgram();
		}
		
	public:
		
		void update(ofFbo& _fbo, ofTexture _srcTex, glm::vec4 _pColor, glm::vec4 _oColor, glm::vec4 _gColor, glm::vec4 _bColor){
			_fbo.begin();
			begin();
			setUniformTexture("SourceTexture", _srcTex, 0);
			setUniform4f("PurpleColor",	_pColor);
			setUniform4f("OrangeColor",	_oColor);
			setUniform4f("GreenColor",	_gColor);
			setUniform4f("BlueColor",	_bColor);
			renderFrame(_fbo.getWidth(), _fbo.getHeight());
			end();
			_fbo.end();
		}
	};
}



