#version 330

in VertexData {
    vec3 v2f_viewSpaceNormal;
    vec3 v2f_viewSpacePosition;
    vec2 v2f_texCoord;
};

uniform vec3 material_diffuse_color;
uniform float material_alpha;
uniform vec3 material_specular_color;
uniform vec3 material_emissive_color;
uniform float material_specular_exponent;

uniform sampler2D diffuse_texture;
uniform sampler2D opacity_texture;
uniform sampler2D specular_texture;

uniform vec3 viewSpaceLightPosition;
uniform vec3 lightColourAndIntensity;
uniform vec3 ambientLightColourAndIntensity;

uniform mat3 viewToWorldRotationTransform;

uniform float fogExtinctionCoeff;

out vec4 fragmentColor;

vec3 fresnelSchick(vec3 r0, float cosAngle) {
    return r0 + (vec3(1.0) - r0) * pow(1.0 - cosAngle, 5.0);
}

void main() {
    if(texture(opacity_texture, v2f_texCoord).r < 0.5) {
        discard;
    }

    vec3 materialDiffuse = texture(diffuse_texture, v2f_texCoord).xyz * material_diffuse_color;
    vec3 materialSpecular = texture(specular_texture, v2f_texCoord).xyz * material_specular_color;

    vec3 viewSpaceDirToLight = normalize(viewSpaceLightPosition - v2f_viewSpacePosition);
    vec3 viewSpaceNormal = normalize(v2f_viewSpaceNormal);
    vec3 viewSpaceDirToEye = normalize(-v2f_viewSpacePosition);

    float incomingIntensity = max(0.0, dot(viewSpaceNormal, viewSpaceDirToLight));
    vec3 incommingLight = incomingIntensity * lightColourAndIntensity;

    vec3 halfVector = normalize(viewSpaceDirToEye + viewSpaceDirToLight);

    float specularNormalizationFactor = ((material_specular_exponent + 2.0) / (2.0));
    float specularIntensity = specularNormalizationFactor * pow(max(0.0, dot(halfVector, viewSpaceNormal)), material_specular_exponent);
    vec3 fresnelSpecular = fresnelSchick(materialSpecular, max(0.0, dot(viewSpaceDirToLight, halfVector)));

    vec3 worldSpaceReflectionDir = viewToWorldRotationTransform * reflect(-viewSpaceDirToEye, viewSpaceNormal);

    vec3 fresnelSpecularEye = fresnelSchick(materialSpecular, max(0.0, dot(viewSpaceDirToEye, viewSpaceNormal)));

    vec3 outgoingLight = (incommingLight + ambientLightColourAndIntensity) * materialDiffuse +
        incommingLight * specularIntensity * fresnelSpecular +
        fresnelSpecularEye +
        material_emissive_color;

    // float xDist = v2f_worldSpacePosition.x - cameraViewPosition.x;
    // float yDist = v2f_worldSpacePosition.y - cameraViewPosition.y;
    // float dist = sqrt(xDist * xDist + yDist * yDist);
    // float fogAmount = 1.0 - exp(-dist * fogExtinctionCoeff);
    // vec3 fogColor = sunLightColour + globalAmbientLight;
    // vec3 finalLight = mix(reflectedLight, fogColor, fogAmount);

    // fragmentColor = vec4(toSrgb(finalLight), 1.0);

    fragmentColor = vec4(outgoingLight, material_alpha);
}
