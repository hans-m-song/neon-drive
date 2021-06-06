#version 330

in vec3 positionAttribute;
in vec2 texCoordAttribute;

uniform mat4 modelToClipTransform;

out vec2 v2f_texCoord;

void main() {
  gl_Position = modelToClipTransform * vec4(positionAttribute, 1.0);
  v2f_texCoord = texCoordAttribute;
}