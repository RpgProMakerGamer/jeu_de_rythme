#version 330
in vec3 fragmentColor;
in vec2 fragmentTexCoord;
out vec4 color;

uniform sampler2D imageTexture;
uniform float ShakeStrength = 0.4;
uniform float time;
uniform vec2 FactorA  = vec2(100.0,100.0);
uniform vec2 FactorB  = vec2(1.0,1.0);
uniform vec2 magnitude = vec2(0.01,0.01);


void main() {
    vec2 uv = fragmentTexCoord;
	uv -= 0.5;
    uv *= 1.0 - 2.0 * magnitude.x;
    uv += 0.5;
	vec2 dt = vec2(0.0, 0.0);
	dt.x = sin(time * FactorA.x+FactorB.x) * magnitude.x;
	dt.y = cos(time *FactorA.y+ FactorB.y) * magnitude.y;
	color = texture(imageTexture, uv + (dt*ShakeStrength));
    color.r += color.a;
}