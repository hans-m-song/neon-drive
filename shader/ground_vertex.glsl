#version 330
layout(location = 0) in vec3 worldPositionAttr;
layout(location = 1) in vec2 textureCoordAttr;

uniform float texCoordScale;
uniform mat4 worldToClipTransform;

out vec2 v2f_textureCoord;

void main() {
    v2f_textureCoord = textureCoordAttr * texCoordScale - (texCoordScale - 1.0) / 2.0;
    gl_Position = worldToClipTransform * vec4(worldPositionAttr, 1.0);
}