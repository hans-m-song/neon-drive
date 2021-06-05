#version 330

in VertexData {
    vec3 v2f_viewSpaceNormal;
    vec2 v2f_texCoord;
    vec3 v2f_worldSpacePosition;
};

uniform vec3 material_diffuse_color;
uniform float material_alpha;
uniform vec3 material_specular_color;
uniform vec3 material_emissive_color;
uniform float material_specular_exponent;
uniform float fogExtinctionCoeff;
uniform vec3 fogColor;

uniform sampler2D diffuse_texture;
uniform sampler2D opacity_texture;
uniform sampler2D specular_texture;
uniform sampler2D normal_texture;
uniform bool enableSrgb;

uniform vec3 origin;

uniform vec3 viewSpaceLightDirection;

out vec4 fragmentColor;

vec3 toSrgb(vec3 color) {
    return pow(color, vec3(1.0 / 2.2));
}

void main() {
    if(texture(opacity_texture, v2f_texCoord).r < 0.5) {
        discard;
    }

    vec3 materialDiffuse = texture(diffuse_texture, v2f_texCoord).xyz * material_diffuse_color;
    vec3 color = materialDiffuse * (0.1 + 0.9 * max(0.0, dot(v2f_viewSpaceNormal, -viewSpaceLightDirection))) + material_emissive_color;

    //Compute Fog
    float xDist = v2f_worldSpacePosition.x - origin.x;
    float yDist = v2f_worldSpacePosition.z - origin.z;
    float dist = sqrt(xDist * xDist + yDist * yDist);
    float fogAmount = 1.0 - exp(-dist * fogExtinctionCoeff);

    vec3 finalColor = mix(color, fogColor, fogAmount);

    if(enableSrgb) {
        finalColor = toSrgb(finalColor);
    }

    fragmentColor = vec4(finalColor, material_alpha);
}