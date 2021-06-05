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
    mat4 v2f_cameraPosition;
};

void main() {
    v2f_worldSpacePosition = worldPositionAttr;
    v2f_cameraPosition = worldToViewTransform;
    v2f_textureCoord = textureCoordAttr * texCoordScale - (texCoordScale - 1.0) / 2.0;
    gl_Position = modelToClipTransform * vec4(worldPositionAttr, 1.0);
}