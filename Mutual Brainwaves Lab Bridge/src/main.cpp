#include "ofMain.h"
#include "ofApp.h"

//========================================================================
int main( ){
	
	ofGLFWWindowSettings windowSettings;
	windowSettings.setPosition(glm::vec2(340, 22));
	windowSettings.setSize(320, 1080-22);
	windowSettings.windowMode = OF_WINDOW;
	
	ofCreateWindow(windowSettings);
	ofRunApp(new ofApp());
	
}

