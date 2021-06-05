#version 330

in VertexData {
    vec2 v2f_textureCoord;
    vec3 v2f_worldSpacePosition;
    mat4 v2f_cameraPosition;
};

uniform vec3 viewPosition;
uniform mat4 viewSpaceLightPosition;
uniform vec3 lightColourAndIntensity;
uniform vec3 ambientLightColourAndIntensity;
uniform float fogExtinctionCoeff;
uniform vec3 fogColor;

// overrides
uniform float texCoordScale;
uniform sampler2D groundTexture;
out vec4 fragmentColor;

void main() {
    vec3 groundColor = texture(groundTexture, v2f_worldSpacePosition.xz * texCoordScale).xyz;

    //Compute Fog
    float xDist = v2f_worldSpacePosition.x;
    float yDist = v2f_worldSpacePosition.y;
    float zDist = v2f_worldSpacePosition.z;
    float dist = sqrt(xDist * xDist + yDist * yDist + zDist * zDist);
    float fogAmount = 1.0 - exp(-dist * fogExtinctionCoeff);

    vec3 finalColor = mix(groundColor, fogColor, fogAmount);

    fragmentColor = vec4(finalColor, 1.0);
}