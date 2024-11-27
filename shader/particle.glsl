#version 330 core

in vec3 fragmentColor;
in vec2 fragmentTexCoord;
out vec4 color;

uniform vec3 pixel_color;


void main( )
{
	color.rgb = pixel_color;
    color.a = 1.0;
}