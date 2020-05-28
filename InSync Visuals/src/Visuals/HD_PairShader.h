
#pragma once

#include "ofMain.h"
#include "ftShader.h"

namespace flowTools {
	
	class HD_PairShader : public ftShader {
	public:
		HD_PairShader() {
			bInitialized = 1;
			if (ofIsGLProgrammableRenderer()) { glFour(); } else { glTwo(); }
			string shaderName = "HD_PairShader";
			if (bInitialized) { ofLogVerbose(shaderName + " initialized"); }
			else { ofLogWarning(shaderName + " failed to initialize"); }
		}
		
	protected:
		void glTwo() {
			fragmentShader = GLSL120(
									 uniform sampler2DRect tex_velocity;
									 uniform sampler2DRect tex_source;
									 uniform sampler2DRect tex_obstacle;
									 
									 uniform float timestep;
									 uniform float rdx;
									 uniform float dissipation;
									 uniform vec2  scale;
									 
									 void main(){
										 vec2 st = gl_TexCoord[0].st;
										 vec2 st2 = st * scale;
										 
										 float oC = texture2DRect(tex_obstacle, st2).x;
										 if (oC == 1.0) {
											 gl_FragColor = vec4(0.0);
										 } else {
											 vec2 velocity = texture2DRect(tex_velocity, st2).xy;
											 vec2 st_back = st - timestep * rdx * velocity / scale;
											 gl_FragColor = dissipation * texture2DRect(tex_source, st_back);
										 }
									 }
									 );
			
			bInitialized *= setupShaderFromSource(GL_FRAGMENT_SHADER, fragmentShader);
			bInitialized *= linkProgram();
		}
		
		void glFour() {
			fragmentShader = GLSL410(
									 precision mediump float;
									 precision mediump int;
									 
									 in vec2 texCoordVarying;
									 out vec4 glFragColor;
									 
									 uniform sampler2DRect den_tex;
									 
									 uniform vec2	point;
									 uniform vec4	colorA;
									 uniform vec4	colorB;
									 uniform float	force;
									 
									 void main(){
										 vec2 st = texCoordVarying;
										 vec4 den = texture(den_tex, st);
										 
										 float colorforceA = length(den * colorA);
										 float colorforceB = length(den * colorB);
										 vec4 addDenA = force * colorforceA * colorB;
										 vec4 addDenB = force * colorforceB * colorA;
										 den += addDenA + addDenB;
										 if (length(den) > 1 ) {
											 den = normalize(den) * 1;
										 }
										 glFragColor = den;
									 }
									 );
			
			bInitialized *= setupShaderFromSource(GL_VERTEX_SHADER, vertexShader);
			bInitialized *= setupShaderFromSource(GL_FRAGMENT_SHADER, fragmentShader);
			bInitialized *= bindDefaults();
			bInitialized *= linkProgram();
		}
		
	public:
		void update(ofFbo& _fbo, ofTexture& _backTex, glm::vec4 _colorA, glm::vec4 _colorB, float _force){
			_fbo.begin();
			begin();
			setUniform4f		("colorA",		_colorA);
			setUniform4f		("colorB",		_colorB);
			setUniform1f		("force",		_force);
			setUniformTexture	("den_tex",		_backTex,	1);
			renderFrame(_fbo.getWidth(), _fbo.getHeight());
			end();
			_fbo.end();
		}
	};
}



