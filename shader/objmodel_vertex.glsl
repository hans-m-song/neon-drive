#version 330

layout(location = 0) in vec3 positionAttribute;
layout(location = 1) in vec3 normalAttribute;
layout(location = 2) in vec2 texCoordAttribute;

uniform mat4 modelToClipTransform;
uniform mat4 modelToViewTransform;
uniform mat3 modelToViewNormalTransform;
uniform mat4 worldToViewTransform;
uniform mat4 viewToClipTransform;

out VertexData {
    vec3 v2f_viewSpaceNormal;
    vec2 v2f_texCoord;
    vec3 v2f_worldSpacePosition;
    vec3 v2f_viewSpacePosition;
};

void main() {
    gl_Position = modelToClipTransform * vec4(positionAttribute, 1.0);
    v2f_viewSpaceNormal = normalize(modelToViewNormalTransform * normalAttribute);
    v2f_viewSpacePosition = (modelToViewTransform * vec4(positionAttribute, 1.0)).xyz;
    v2f_texCoord = texCoordAttribute;
    v2f_worldSpacePosition = positionAttribute;
}