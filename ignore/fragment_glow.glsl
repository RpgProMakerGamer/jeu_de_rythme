#version 330 core

in vec2 fragmentTexCoord;
uniform sampler2D imageTexture;

uniform float time;
uniform int rand;

out vec4 color;

const float SCALE_GLOW=.2f;
const float SCALE_TIME=.05f;

void main()
{
    vec4 color = texture(imageTexture, fragmentTexCoord);

// Precompute intensity, clamp to avoid branching
    float intensity = max(0.0, (sin(time * SCALE_TIME) + rand) * SCALE_GLOW);

// Subtract intensity-scaled color
    color -= intensity * vec4(1, 1, 1, 0);


}
