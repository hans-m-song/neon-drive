#version 330

layout(location = 0) in vec3 positionAttribute;
layout(location = 1) in vec3 normalAttribute;
layout(location = 2) in vec3 texCoordAttribute;

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

out VertexData {
    vec3 v2f_viewSpacePosition;
    vec3 v2f_viewSpaceNormal;
};

void main() {
    v2f_viewSpacePosition = (modelToViewTransform * vec4(positionAttribute, 1.0)).xyz;
    v2f_viewSpaceNormal = normalize(modelToViewNormalTransform * normalAttribute);
    gl_Position = modelToClipTransform * vec4(positionAttribute, 1.0);
}