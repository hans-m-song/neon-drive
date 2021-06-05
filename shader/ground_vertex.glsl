#version 330

layout(location = 0) in vec3 worldPositionAttr;
layout(location = 1) in vec2 textureCoordAttr;

uniform mat4 modelToClipTransform;
uniform mat4 modelToViewTransform;
uniform mat3 modelToViewNormalTransform;
uniform mat4 worldToViewTransform;
uniform mat4 viewToClipTransform;

// overrides
uniform float texCoordScale;

out VertexData {
    vec2 v2f_textureCoord;
    vec3 v2f_worldSpacePosition;
    vec3 v2f_viewSpacePosition;
};

void main() {
    v2f_worldSpacePosition = worldPositionAttr;
    v2f_textureCoord = textureCoordAttr * texCoordScale - (texCoordScale - 1.0) / 2.0;
    v2f_viewSpacePosition = (modelToViewTransform * vec4(worldPositionAttr, 1.0)).xyz;
    gl_Position = modelToClipTransform * vec4(worldPositionAttr, 1.0);
}