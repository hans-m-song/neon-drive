#version 330

in VertexData {
    vec3 v2f_viewSpacePosition;
    vec3 v2f_viewSpaceNormal;
};

uniform vec3 sphereColour;

out vec4 fragmentColor;

void main() {
    float shading = max(0.0, dot(normalize(-v2f_viewSpacePosition), v2f_viewSpaceNormal));
    fragmentColor = vec4(sphereColour.xyz * shading, 1.0);

}