#version 330

in VertexData {
    vec3 v2f_viewSpaceNormal;
    vec3 v2f_viewSpacePosition;
    vec2 v2f_textureCoordinate;
    vec3 v2f_worldSpacePosition;
};

uniform mat4 modelToClipTransform;
uniform mat4 modelToViewTransform;
uniform mat3 modelToViewNormalTransform;
uniform mat3 viewToWorldRotationTransform;
uniform float attenuationLinear;
uniform float attenuationQuadratic;
uniform vec3 lightPositionL;
uniform vec3 lightColourAndIntensityL;
uniform vec3 lightPositionR;
uniform vec3 lightColourAndIntensityR;
uniform vec3 ambientLightColourAndIntensity;
uniform float fogExtinctionOffset;
uniform float fogExtinctionCoeff;
uniform vec3 fogColor;
uniform bool enableSrgb;

uniform vec3 material_diffuse_color;
uniform float material_alpha;
uniform vec3 material_specular_color;
uniform vec3 material_emissive_color;
uniform float material_specular_exponent;
uniform sampler2D diffuse_texture;
uniform sampler2D opacity_texture;
uniform sampler2D specular_texture;
uniform sampler2D normal_texture;

// overrides
uniform float texCoordScale;
uniform sampler2D groundTexture;

out vec4 fragmentColor;

vec3 toSrgb(vec3 color) {
    return pow(color, vec3(1.0 / 2.2));
}

// float attenuate(float dist) {
//     return 1.0 / (1.0 + attenuationLinear * dist +
//         attenuationQuadratic * (dist * dist));
// }

// float lightDist = length(viewSpaceDirToLight);
// float attenuated = incomingIntensity * attenuate(length(viewSpaceDirToLight))

vec3 calculateLight(vec3 lightPosition, vec3 lightColourAndIntensity) {
    vec3 viewSpaceDirToLight = normalize(lightPosition - v2f_viewSpacePosition);
    vec3 viewSpaceNormal = normalize(v2f_viewSpaceNormal);
    float incomingIntensity = max(0.0, dot(viewSpaceNormal, viewSpaceDirToLight));
    return incomingIntensity * lightColourAndIntensity;
}

void main() {
    vec3 groundColor = texture(groundTexture, v2f_worldSpacePosition.xz * texCoordScale).xyz;

    // light
    vec3 totalLight = ambientLightColourAndIntensity +
        calculateLight(lightPositionL, lightColourAndIntensityL) +
        calculateLight(lightPositionR, lightColourAndIntensityR);

    // merge colours
    vec3 outgoingLight = totalLight * groundColor;

    float dist = length(v2f_viewSpacePosition);
    float fogAmount = 1 - exp((-dist + fogExtinctionOffset) * fogExtinctionCoeff);

    vec3 finalColor = mix(outgoingLight, fogColor, fogAmount);

    if(enableSrgb) {
        finalColor = toSrgb(finalColor);
    }

    fragmentColor = vec4(finalColor, 1.0);
}