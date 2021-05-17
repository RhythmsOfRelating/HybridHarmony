
#pragma once

#include "ofMain.h"
#include "ftShader.h"

namespace flowTools {
	
	class HD_AttractShader : public ftShader {
	public:
		HD_AttractShader() {
			bInitialized = 1;
			if (ofIsGLProgrammableRenderer()) { glFour(); } else { glTwo(); }
			string shaderName = "HD_AttractShader";
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
									 
									 uniform sampler2DRect vel_tex;
									 uniform sampler2DRect den_tex;
									 
									 uniform vec2	point;
									 uniform vec4	color;
									 uniform float	force;
									 
									 void main(){
										 vec2 st = texCoordVarying;
										 vec4 den = texture(den_tex, st);
										 vec2 vel = texture(vel_tex, st).xy;
//										 if (distance(normalize(den), color) < 0.1) {
//											 float colorforce = 1.0 - distance(den, color);
//											 vec2 attraction = normalize(point - st) * force * colorforce;
//											 vel += attraction;
//										 }
										 
										 float colorforce = length(den * color);
										 vec2 attraction = normalize(point - st) * force * colorforce;
										 vel += attraction;
										 
										 glFragColor = vec4(vel, 0.0, 0.0);
									 }
									 );
			
			bInitialized *= setupShaderFromSource(GL_VERTEX_SHADER, vertexShader);
			bInitialized *= setupShaderFromSource(GL_FRAGMENT_SHADER, fragmentShader);
			bInitialized *= bindDefaults();
			bInitialized *= linkProgram();
		}
		
	public:
		void update(ofFbo& _fbo, ofTexture& _backTex, ofTexture& _denTex, glm::vec2 _point, glm::vec4 _color, float _force){
			_fbo.begin();
			begin();
			setUniform2f		("point",		_point);
			setUniform4f		("color",		_color);
			setUniform1f		("force",		_force);
			setUniformTexture	("vel_tex",		_backTex,	0);
			setUniformTexture	("den_tex",		_denTex,	1);
			renderFrame(_fbo.getWidth(), _fbo.getHeight());
			end();
			_fbo.end();
		}
	};
}



