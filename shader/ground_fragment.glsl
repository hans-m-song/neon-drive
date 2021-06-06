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
uniform vec3 viewSpaceLightDirection;
uniform vec3 lightColourAndIntensity;
uniform vec3 ambientLightColourAndIntensity;
uniform float fogExtinctionOffset;
uniform float fogExtinctionCoeff;
uniform vec3 fogColor;
uniform bool enableSrgb;

// overrides
uniform float texCoordScale;
uniform sampler2D groundTexture;

out vec4 fragmentColor;

void main() {
    vec3 groundColor = texture(groundTexture, v2f_worldSpacePosition.xz * texCoordScale).xyz;

    float xDist = v2f_viewSpacePosition.x;
    float yDist = v2f_viewSpacePosition.y;
    float zDist = v2f_viewSpacePosition.z;
    float dist = sqrt(xDist * xDist + yDist * yDist + zDist * zDist);
    float fogAmount = 1 - exp((-dist + fogExtinctionOffset) * fogExtinctionCoeff);

    vec3 finalColor = mix(groundColor, fogColor, fogAmount);

    fragmentColor = vec4(finalColor, 1.0);
}