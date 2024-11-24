#version 330 core

in vec2 fragmentTexCoord;
//uniform sampler2D imageTexture;

//uniform float time;

out vec4 color;

//const float SCALE_GLOW=.2f;
//const float SCALE_TIME=.05f;
uniform float time;

const float speed = 0.02;

void main()
{
    color = vec4(0.0);

// Precompute intensity, clamp to avoid branching
// Subtract intensity-scaled color
    float add = time*speed;
    color.a = mod(round((gl_FragCoord.y+add+2)/4), 2) * 0.4 ;

}
