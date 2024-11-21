#version 330 core

in vec4 fragmentColor;
in vec2 fragmentTexCoord;
out vec4 color;


uniform sampler2D imageTexture;
uniform float shake_power = 0.01;

uniform float shake_rate  = 0.2;

uniform float shake_speed = 5.0;

uniform float shake_block_size = 40.5;

uniform float shake_color_rate  = 0.01;

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
	//pixel_color = vec4(fragmentTexCoord.x) ;
	if( pixel_color.r > .1 && pixel_color.g > .1 && pixel_color.b > .1 )
	{
		color = vec4( 0.0 );
	}
	else
	{
		color = pixel_color;
	}

}