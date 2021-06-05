#version 330

in vec2 v2f_textureCoord;

uniform samplerCube cubemap;

out vec4 fragmentColor;

void main() {
    fragmentColor = texture(cubemap, v2f_textureCoord);
}