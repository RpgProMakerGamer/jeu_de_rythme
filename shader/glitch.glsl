#version 330 core

in vec4 fragmentColor;
in vec2 fragmentTexCoord;
out vec4 color;


uniform sampler2D imageTexture;
const float shake_power = 0.008;

const float shake_rate  = 0.1;

const float shake_speed = 15.0;

const float shake_block_size = 40.5;

const float shake_color_rate  = 0.01;

uniform float time;

float random( float seed )
{
	return fract( 543.2543 * sin( dot( vec2( seed, seed ), vec2( 3525.46, -54.3415 ) ) ) );
}

void main( )
{
	float enable_shift = float(
		random( trunc( time * shake_speed ) )
	<	shake_rate
	);

	vec2 fixed_uv = fragmentTexCoord;
	fixed_uv.x += (
		random(
			( trunc( fragmentTexCoord.y * shake_block_size ) / shake_block_size )
		+	time
		) - 0.5
	) * shake_power * enable_shift;

	vec4 pixel_color = textureLod( imageTexture, fixed_uv, 0.0 );
	pixel_color.r = mix(
		pixel_color.r
	,	textureLod( imageTexture, fixed_uv + vec2( shake_color_rate, 0.0 ), 0.0 ).r
	,	enable_shift
	);
	pixel_color.b = mix(
		pixel_color.b
	,	textureLod( imageTexture, fixed_uv + vec2( -shake_color_rate, 0.0 ), 0.0 ).b
	,	enable_shift
	);
	pixel_color *=  pixel_color.r < 0.008 ? 0.0 : 1.0;
	color = pixel_color;
}