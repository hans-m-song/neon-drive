#version 330

layout(location = 0) in vec3 worldPositionAttr;
layout(location = 1) in vec2 textureCoordAttr;

uniform mat4 modelToClipTransform;
uniform mat4 modelToViewTransform;
uniform mat3 modelToViewNormalTransform;
uniform mat4 worldToViewTransform;
uniform mat4 viewToClipTransform;

out vec2 v2f_textureCoord;

void main() {
    v2f_textureCoord = textureCoordAttr;
    gl_Position = modelToClipTransform * vec4(worldPositionAttr, 1.0);
}