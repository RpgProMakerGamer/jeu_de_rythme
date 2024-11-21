#version 330 core

in vec2 fragmentTexCoord;
//uniform sampler2D imageTexture;

//uniform float time;

out vec4 color;

//const float SCALE_GLOW=.2f;
//const float SCALE_TIME=.05f;

void main()
{
    color = vec4(0.0);

// Precompute intensity, clamp to avoid branching
// Subtract intensity-scaled color
    color.a = mod(round(gl_FragCoord.y/2), 2) * 0.4 ;

}
