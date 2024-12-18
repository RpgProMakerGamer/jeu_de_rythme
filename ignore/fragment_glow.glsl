#version 330 core

in vec2 fragmentTexCoord;
uniform sampler2D imageTexture;

//uniform float time;
uniform float rand;

out vec4 color;

//const float SCALE_GLOW=.2f;
//const float SCALE_TIME=.05f;

void main()
{
    color = texture(imageTexture, fragmentTexCoord);

// Precompute intensity, clamp to avoid branching
    float intensity = max(0.0, (rand-1) * -1);
// Subtract intensity-scaled color
    color -= intensity * vec4(1, 1, 1, 0);

}
