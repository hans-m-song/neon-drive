#version 330

in vec2 v2f_texCoord;

uniform sampler2D tex;

out vec4 fragmentColor;

void main() {
    fragmentColor = texture(tex, v2f_texCoord);
}
