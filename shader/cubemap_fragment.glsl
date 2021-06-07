#version 330

in VertexData {
    vec3 v2f_textureCoord;
    vec3 v2f_viewSpacePosition;
};

uniform samplerCube cubemap;
uniform vec3 fogColor;

out vec4 fragmentColor;

void main() {
    vec4 color = texture(cubemap, v2f_textureCoord);

    // fog
    float fogAmount = exp(3 * -v2f_textureCoord.y);

    vec3 finalColor = mix(vec3(color), fogColor, fogAmount);

    fragmentColor = vec4(finalColor, 1.0);
}