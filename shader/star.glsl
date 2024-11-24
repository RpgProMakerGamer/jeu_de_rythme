#version 330 corein vec3 fragmentColor;in vec2 fragmentTexCoord;out vec4 color;uniform sampler2D imageTexture;uniform float time; // Time in seconds since the shader started runninguniform vec2 dimensions = vec2(1024.0, 600.0); // Resolution of ColorRect in pixelsuniform float small_stars = 50.0; // Number of small stars. Rows for horizontally scrolling stars or columns for vertically scrolling stars.uniform float small_stars_far_size  = 0.5;uniform float small_stars_near_size  = 1.0;uniform float large_stars = 8.0; // Number of large stars. Rows for horizontally scrolling stars or columns for vertically scrolling stars.uniform float large_stars_far_size  = 0.5;uniform float large_stars_near_size  = 0.7;// Replace the below references to 'source_color' with 'hint_color' if you are using a version of Godot before 4.uniform vec4 far_stars_color  = vec4(0.65, 1, 0.85, 1.0);uniform vec4 near_stars_color  = vec4(0.2, 0.65, 0.4, 1.0);uniform float base_scroll_speed  = 0.005;uniform float additional_scroll_speed  = 0.005;float greater_than(float x, float y) {	return max(sign(x - y), 0.0);}void main() {	color = textureLod(imageTexture, fragmentTexCoord, 0.0);	color.a = 1.0;// The below line will scroll the stars from right to left or from bottom to top.// To make the stars scroll in the opposite direction change the line to://	float time = 10000.0 - time;// Alternatively you can comment out the below line and add a new uniform above as:// uniform float time = 10000.0;// You can then update the time uniform from your _physics_process function by adding or subtracting delta. You can also pause the scrolling by not changing the time uniform.	 float time = 10000.0 + time/100;// Comment out the following two lines if you are not applying the shader to a TextureRect://	color = texture(TEXTURE,fragmentTexCoord); // This line is only required if you are using a version of Godot before 4.//	vec2 dimensions = 1.0 / TEXTURE_PIXEL_SIZE;// Horizontal scrolling:	float small_star_rn = fract(sin(floor(fragmentTexCoord.y * small_stars)) * dimensions.y);	float large_star_rn = fract(sin(floor(fragmentTexCoord.y * large_stars)) * dimensions.y);	vec2 small_star_uv = vec2(fract(fragmentTexCoord.x + (base_scroll_speed + small_star_rn * additional_scroll_speed) * time) * small_stars * dimensions.x / dimensions.y, fract(fragmentTexCoord.y * small_stars)) * 2.0 - 1.0;	vec2 large_star_uv = vec2(fract(fragmentTexCoord.x + (base_scroll_speed + large_star_rn *	additional_scroll_speed) * time) * large_stars * dimensions.x /	dimensions.y, fract(fragmentTexCoord.y * large_stars)) * 2.0 - 1.0;// Vertical scrolling://	float small_stars_rn = fract(sin(floor(fragmentTexCoord.x * small_stars)) * dimensions.x);//	float large_stars_rn = fract(sin(floor(fragmentTexCoord.x * large_stars)) * dimensions.x);//	vec2 small_stars_uv = vec2(fract(fragmentTexCoord.x * small_stars), fract(fragmentTexCoord.y + (base_scroll_speed + small_stars_rn * additional_scroll_speed) * time) * small_stars * dimensions.y / dimensions.x) * 2.0 - 1.0;//	vec2 large_stars_uv = vec2(fract(fragmentTexCoord.x * large_stars), fract(fragmentTexCoord.y + (base_scroll_speed + large_stars_rn * additional_scroll_speed) * time) * large_stars * dimensions.y / dimensions.x) * 2.0 - 1.0;	vec4 star_color = mix(far_stars_color, near_stars_color, small_star_rn);	float star_size = small_stars_far_size + (small_stars_near_size - small_stars_far_size) * small_star_rn;// Render small stars as circles with soft edges:	color.rgb = mix(color.rgb, star_color.rgb, max((star_size - length(small_star_uv)) / star_size, 0.0) * star_color.a);// Render small stars as circles with hard edges://	color.rgb = mix(color.rgb, star_color.rgb, greater_than(star_size, length(small_star_uv)) * star_color.a);// Render small stars as crosses with soft edges://	color.rgb = mix(color.rgb, star_color.rgb, max((star_size - length(small_star_uv)) / star_size, 0.0) * (max(greater_than(star_size / 10.0, abs(small_star_uv.x)), greater_than(star_size / 10.0, abs(small_star_uv.y)))) * star_color.a);// Render small stars as crosses with hard edges://	color.rgb = mix(color.rgb, star_color.rgb, max(greater_than(star_size / 5.0, abs(small_star_uv.x)) * greater_than(star_size, abs(small_star_uv.y)), greater_than(star_size / 5.0, abs(small_star_uv.y)) * greater_than(star_size, abs(small_star_uv.x))) * star_color.a);// Render small stars as squares://	color.rgb = mix(color.rgb, star_color.rgb, greater_than(star_size, abs(small_star_uv.x)) * greater_than(star_size, abs(small_star_uv.y)) * star_color.a);// Render small stars as diamonds://	color.rgb = mix(color.rgb, star_color.rgb, greater_than(star_size, abs(small_star_uv.y) + abs(small_star_uv.x)) * star_color.a);// Render small stars using the 'small_stars_texture':// The 'small_stars_texture' must have a border of blank transparent pixels.//	vec4 small_stars_texture_pixel = texture(small_stars_texture, (small_star_uv / (small_stars_far_size + (small_stars_near_size - small_stars_far_size) * small_star_rn) + 1.0) / 2.0) * mix(far_stars_color, near_stars_color, small_star_rn);//	color.rgb = mix(color.rgb, small_stars_texture_pixel.rgb, small_stars_texture_pixel.a);	star_color = mix(far_stars_color, near_stars_color, large_star_rn);	star_size = large_stars_far_size + (large_stars_near_size - large_stars_far_size) * large_star_rn;// Render large stars as circles with soft edges://	color.rgb = mix(color.rgb, star_color.rgb, max((star_size - length(large_star_uv)) / star_size, 0.0) * star_color.a);// Render large stars with circles and crosses with smooth edges:	 color.rgb = mix(color.rgb, star_color.rgb, (max((star_size / 1.7 - length(large_star_uv)) / star_size, 0.0) +	 max((star_size - length(large_star_uv)) / star_size / 2.0, 0.0) * (max(greater_than(star_size / 10.0, abs	 (large_star_uv.x)), greater_than(star_size / 10.0, abs(large_star_uv.y))))) * star_color.a);	color.a = color.r+color.g+color.b;// Render large stars as circles with hard edges://	color.rgb = mix(color.rgb, star_color.rgb, greater_than(star_size, length(large_star_uv)) * star_color.a);// Render large stars as crosses with soft edges://	color.rgb = mix(color.rgb, star_color.rgb, max((star_size - length(large_star_uv)) / star_size, 0.0) * (max(greater_than(star_size / 10.0, abs(large_star_uv.x)), greater_than(star_size / 10.0, abs(large_star_uv.y)))) * star_color.a);// Render large stars as crosses with hard edges://	color.rgb = mix(color.rgb, star_color.rgb, max(greater_than(star_size / 5.0, abs(large_star_uv.x)) * greater_than(star_size, abs(large_star_uv.y)), greater_than(star_size / 5.0, abs(large_star_uv.y)) * greater_than(star_size, abs(large_star_uv.x))) * star_color.a);// Render large stars as squares://	color.rgb = mix(color.rgb, star_color.rgb, greater_than(star_size, abs(large_star_uv.x)) * greater_than(star_size, abs(large_star_uv.y)) * star_color.a);// Render large stars as diamonds://	color.rgb = mix(color.rgb, star_color.rgb, greater_than(star_size, abs(large_star_uv.y) + abs(large_star_uv.x)) * star_color.a);// Render large stars using the 'large_stars_texture':// The 'large_stars_texture' must have a border of blank transparent pixels.//	vec4 large_stars_texture_pixel = texture(large_stars_texture, (large_star_uv / (large_stars_far_size + (large_stars_near_size - large_stars_far_size) * large_star_rn) + 1.0) / 2.0) * mix(far_stars_color, near_stars_color, large_star_rn);//	color.rgb = mix(color.rgb, large_stars_texture_pixel.rgb, large_stars_texture_pixel.a);}