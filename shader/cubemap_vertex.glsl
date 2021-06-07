#version 330

layout(location = 0) in vec3 positionAttribute;

uniform mat4 modelToClipTransform;
uniform mat4 modelToViewTransform;
uniform mat3 modelToViewNormalTransform;

out VertexData {
    vec3 v2f_textureCoord;
    vec3 v2f_viewSpacePosition;
};

void main() {
    v2f_textureCoord = positionAttribute;
    v2f_viewSpacePosition = (modelToViewTransform * vec4(positionAttribute, 1.0)).xyz;
    gl_Position = modelToClipTransform * vec4(positionAttribute, 1.0);
}