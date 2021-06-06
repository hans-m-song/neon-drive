#version 330

in vec3 positionIn;
in vec3 normalIn;

uniform mat4 modelToClipTransform;
uniform mat4 modelToViewTransform;
uniform mat3 modelToViewNormalTransform;

out VertexData {
    vec3 v2f_viewSpacePosition;
    vec3 v2f_viewSpaceNormal;
};

void main() {
    v2f_viewSpacePosition = (modelToViewTransform * vec4(positionIn, 1.0)).xyz;
    v2f_viewSpaceNormal = normalize(modelToViewNormalTransform * normalIn);
    gl_Position = modelToClipTransform * vec4(positionIn, 1.0);
}