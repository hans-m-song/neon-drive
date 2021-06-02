#version 330

in VertexData {
    vec3 v2f_viewSpaceNormal;
    vec3 v2f_viewSpacePosition;
    vec2 v2f_texCoord;
};

uniform sampler2D tex;

out vec4 fragmentColor;

void main() {
    fragmentColor = texture(tex, v2f_texCoord);
}
