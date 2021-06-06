#version 330

layout(location = 0) in vec3 positionAttribute;
layout(location = 1) in vec3 normalAttribute;
layout(location = 2) in vec2 texCoordAttribute;

uniform mat4 modelToClipTransform;
uniform mat4 modelToViewTransform;
uniform mat3 modelToViewNormalTransform;
uniform vec3 lightColourAndIntensity;
uniform vec3 ambientLightColourAndIntensity;
uniform float fogExtinctionOffset;
uniform float fogExtinctionCoeff;
uniform vec3 fogColor;
uniform bool enableSrgb;

out VertexData {
    vec3 v2f_viewSpaceNormal;
    vec3 v2f_viewSpacePosition;
    vec2 v2f_textureCoordinate;
    vec3 v2f_worldSpacePosition;
};

void main() {
    gl_Position = modelToClipTransform * vec4(positionAttribute, 1.0);
    v2f_viewSpaceNormal = normalize(modelToViewNormalTransform * normalAttribute);
    v2f_viewSpacePosition = (modelToViewTransform * vec4(positionAttribute, 1.0)).xyz;
    v2f_textureCoordinate = texCoordAttribute;
    v2f_worldSpacePosition = positionAttribute;
}