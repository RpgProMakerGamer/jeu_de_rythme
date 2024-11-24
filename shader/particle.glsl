#version 330 core

in vec3 fragmentColor;
in vec2 fragmentTexCoord;
out vec4 color;

uniform vec4 pixel_color;


void main( )
{
	color = pixel_color;
}