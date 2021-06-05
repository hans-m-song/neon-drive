#version 330

in vec2 v2f_textureCoord;

uniform samplerCube cubemap;

out vec4 fragmentColor;

void main() {
    fragmentColor = textureCube(cubemap, vec3(v2f_textureCoord, 1.0));
}