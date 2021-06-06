# flake8: noqa

import os

import OpenGL.GL as gl
from PIL import Image

from shader.utils import (
    bind_texture,
    build_shader,
    create_bind_vertex_attrib_array_float,
    load_glsl,
)
from utils.math import Mat3, Mat4


class ObjModel:
    RF_Transparent = 1
    RF_AlphaTested = 2
    RF_Opaque = 4
    RF_All = RF_Opaque | RF_AlphaTested | RF_Transparent

    AA_Position = 0
    AA_Normal = 1
    AA_TexCoord = 2
    AA_Tangent = 3
    AA_Bitangent = 4

    TU_Diffuse = 0
    TU_Opacity = 1
    TU_Specular = 2
    TU_Normal = 3
    TU_EnvMap = 4

    fileName = "ObjModel"

    def __init__(self, fileName):
        self.fileName = os.path.basename(fileName)
        self.defaultTextureOne = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.defaultTextureOne)
        gl.glTexImage2D(
            gl.GL_TEXTURE_2D,
            0,
            gl.GL_RGBA,
            1,
            1,
            0,
            gl.GL_RGBA,
            gl.GL_FLOAT,
            [1.0, 1.0, 1.0, 1.0],
        )

        self.defaultNormalTexture = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.defaultNormalTexture)
        gl.glTexImage2D(
            gl.GL_TEXTURE_2D,
            0,
            gl.GL_RGBA32F,
            1,
            1,
            0,
            gl.GL_RGBA,
            gl.GL_FLOAT,
            [0.5, 0.5, 0.5, 1.0],
        )
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

        self.overrideDiffuseTextureWithDefault = False
        self.load(fileName)

        self.defaultShader = build_shader(
            self.defaultVertexShader,
            self.defaultFragmentShader,
            self.getDefaultAttributeBindings(),
        )
        gl.glUseProgram(self.defaultShader)
        self.setDefaultUniformBindings(self.defaultShader)
        gl.glUseProgram(0)

    def load(self, fileName):
        basePath, _ = os.path.split(fileName)
        with open(fileName, "r", encoding="utf8") as inFile:
            self.loadObj(inFile.readlines(), basePath)

    def loadObj(self, objLines, basePath):
        positions = []
        normals = []
        uvs = []
        materialChunks = []
        materials = {}

        for l in objLines:
            # 1 standardize line
            if len(l) > 0 and l[:1] != "#":
                tokens = l.split()
                if len(tokens):
                    if tokens[0] == "mtllib":
                        assert len(tokens) >= 2
                        materialName = " ".join(tokens[1:])
                        materials = self.loadMaterials(
                            os.path.join(basePath, materialName), basePath
                        )
                    if tokens[0] == "usemtl":
                        assert len(tokens) >= 2
                        materialName = " ".join(tokens[1:])
                        if (
                            len(materialChunks) == 0
                            or materialChunks[-1][0] != materialName
                        ):
                            materialChunks.append([materialName, []])
                    elif tokens[0] == "v":
                        assert len(tokens[1:]) >= 3
                        positions.append([float(v) for v in tokens[1:4]])
                    elif tokens[0] == "vn":
                        assert len(tokens[1:]) >= 3
                        normals.append([float(v) for v in tokens[1:4]])
                    elif tokens[0] == "vt":
                        assert len(tokens[1:]) >= 2
                        uvs.append([float(v) for v in tokens[1:3]])
                    elif tokens[0] == "f":
                        materialChunks[-1][1] += self.parseFace(tokens[1:])

        self.numVerts = 0
        for mc in materialChunks:
            self.numVerts += len(mc[1])

        self.positions = [None] * self.numVerts
        self.normals = [None] * self.numVerts
        self.uvs = [[0.0, 0.0]] * self.numVerts
        self.tangents = [[0.0, 1.0, 0.0]] * self.numVerts
        self.bitangents = [[1.0, 0.0, 0.0]] * self.numVerts
        self.chunks = []

        start = 0
        end = 0

        for matId, tris in materialChunks:
            material = materials[matId]
            renderFlags = 0
            if material["alpha"] != 1.0:
                renderFlags |= self.RF_Transparent
            elif material["texture"]["opacity"] != -1:
                renderFlags |= self.RF_AlphaTested
            else:
                renderFlags |= self.RF_Opaque
            start = end
            end = start + int(len(tris) / 3)

            chunkOffset = start * 3
            chunkCount = len(tris)

            # De-index mesh and (TODO) compute tangent frame
            for k in range(0, len(tris), 3):
                for j in [0, 1, 2]:
                    p = positions[tris[k + j][0]]
                    oo = chunkOffset + k + j
                    self.positions[oo] = p
                    if tris[k + j][1] != -1:
                        self.uvs[oo] = uvs[tris[k + j][1]]
                    self.normals[oo] = normals[tris[k + j][2]]
            self.chunks.append(
                (material, chunkOffset, chunkCount, renderFlags)
            )

        self.vertexArrayObject = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vertexArrayObject)

        self.positionBuffer = create_bind_vertex_attrib_array_float(
            self.positions, self.AA_Position
        )
        self.normalBuffer = create_bind_vertex_attrib_array_float(
            self.normals, self.AA_Normal
        )
        self.uvBuffer = create_bind_vertex_attrib_array_float(
            self.uvs, self.AA_TexCoord
        )
        self.tangentBuffer = create_bind_vertex_attrib_array_float(
            self.tangents, self.AA_Tangent
        )
        self.biTangentBuffer = create_bind_vertex_attrib_array_float(
            self.bitangents, self.AA_Bitangent
        )

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
        gl.glBindVertexArray(0)

    def parseFloats(self, tokens, minNum):
        assert len(tokens) >= minNum
        return [float(v) for v in tokens[0:minNum]]

    def parseFaceIndexSet(self, s):
        inds = s.split("/")
        assert len(inds) == 3
        return [int(ind) - 1 if ind != "" else -1 for ind in inds]

    def parseFace(self, tokens):
        assert len(tokens) >= 3
        result = []
        v0 = self.parseFaceIndexSet(tokens[0])
        v1 = self.parseFaceIndexSet(tokens[1])
        for t in tokens[2:]:
            v2 = self.parseFaceIndexSet(t)
            result += [v0, v1, v2]
            v1 = v2
        return result

    def loadMaterials(self, materialFileName, basePath):
        materials = {}
        with open(materialFileName, "r", encoding="utf8") as inFile:
            currentMaterial = ""
            for l in inFile.readlines():
                tokens = l.split()
                if len(tokens):
                    if tokens[0] == "newmtl":
                        assert len(tokens) >= 2
                        currentMaterial = " ".join(tokens[1:])
                        materials[currentMaterial] = {
                            "color": {
                                "diffuse": [0.5, 0.5, 0.5],
                                "ambient": [0.5, 0.5, 0.5],
                                "specular": [0.5, 0.5, 0.5],
                                "emissive": [0.0, 0.0, 0.0],
                            },
                            "texture": {
                                "diffuse": -1,
                                "opacity": -1,
                                "specular": -1,
                                "normal": -1,
                            },
                            "alpha": 1.0,
                            "specularExponent": 22.0,
                            "offset": 0,
                        }
                    elif tokens[0] == "Ka":
                        materials[currentMaterial]["color"][
                            "ambient"
                        ] = self.parseFloats(tokens[1:], 3)
                    elif tokens[0] == "Ns":
                        materials[currentMaterial]["specularExponent"] = float(
                            tokens[1]
                        )
                    elif tokens[0] == "Kd":
                        materials[currentMaterial]["color"][
                            "diffuse"
                        ] = self.parseFloats(tokens[1:], 3)
                    elif tokens[0] == "Ks":
                        materials[currentMaterial]["color"][
                            "specular"
                        ] = self.parseFloats(tokens[1:], 3)
                    elif tokens[0] == "Ke":
                        materials[currentMaterial]["color"][
                            "emissive"
                        ] = self.parseFloats(tokens[1:], 3)
                    elif tokens[0] == "map_Kd":
                        materials[currentMaterial]["texture"][
                            "diffuse"
                        ] = self.loadTexture(
                            " ".join(tokens[1:]), basePath, True
                        )
                    elif tokens[0] == "map_Ks":
                        materials[currentMaterial]["texture"][
                            "specular"
                        ] = self.loadTexture(
                            " ".join(tokens[1:]), basePath, True
                        )
                    elif tokens[0] == "map_bump" or tokens[0] == "bump":
                        materials[currentMaterial]["texture"][
                            "normal"
                        ] = self.loadTexture(
                            " ".join(tokens[1:]), basePath, False
                        )
                    elif tokens[0] == "map_d":
                        materials[currentMaterial]["texture"][
                            "opacity"
                        ] = self.loadTexture(
                            " ".join(tokens[1:]), basePath, False
                        )
                    elif tokens[0] == "d":
                        materials[currentMaterial]["alpha"] = float(tokens[1])

        for id, m in materials.items():
            for ch in ["diffuse", "specular"]:
                if m["texture"][ch] != -1 and sum(m["color"][ch]) == 0.0:
                    m["color"][ch] = [1, 1, 1]
                if m["texture"][ch] != -1 and sum(m["color"][ch]) == 0.0:
                    m["color"][ch] = [1, 1, 1]
        return materials

    def loadTexture(self, fileName, basePath, srgb):
        fullFileName = os.path.join(basePath, fileName)

        width = 0
        height = 0
        channels = 0
        try:
            im = Image.open(fullFileName)
            texId = gl.glGenTextures(1)
            gl.glActiveTexture(gl.GL_TEXTURE0)
            gl.glBindTexture(gl.GL_TEXTURE_2D, texId)

            data = im.tobytes(
                "raw", "RGBX" if im.mode == "RGB" else "RGBA", 0, -1
            )
            gl.glTexImage2D(
                gl.GL_TEXTURE_2D,
                0,
                gl.GL_SRGB_ALPHA if srgb else gl.GL_RGBA,
                im.size[0],
                im.size[1],
                0,
                gl.GL_RGBA,
                gl.GL_UNSIGNED_BYTE,
                data,
            )
            gl.glGenerateMipmap(gl.GL_TEXTURE_2D)

            gl.glTexParameterf(
                gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR
            )
            gl.glTexParameterf(
                gl.GL_TEXTURE_2D,
                gl.GL_TEXTURE_MIN_FILTER,
                gl.GL_LINEAR_MIPMAP_LINEAR,
            )
            gl.glTexParameteri(
                gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT
            )
            gl.glTexParameteri(
                gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT
            )
            # gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAX_ANISOTROPY_EXT, 16);
            gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
            return texId
        except:
            print("WARNING: FAILED to load texture '%s'" % fileName)
            # print("Could not load image :(")

        return -1

    def render(self, shaderProgram=None, renderFlags=None, transforms={}):
        if not renderFlags:
            renderFlags = self.RF_All

        if not shaderProgram:
            shaderProgram = self.defaultShader

        chunks = [ch for ch in self.chunks if ch[3] & renderFlags]

        gl.glBindVertexArray(self.vertexArrayObject)
        gl.glUseProgram(shaderProgram)

        defaultTfms = {
            "modelToClipTransform": Mat4(),
            "modelToViewTransform": Mat4(),
            "modelToViewNormalTransform": Mat3(),
        }
        defaultTfms.update(transforms)
        for tfmName, tfm in defaultTfms.items():
            loc = gl.glGetUniformLocation(shaderProgram, tfmName)
            tfm._set_open_gl_uniform(loc)

        previousMaterial = None
        for material, chunkOffset, chunkCount, renderFlags in chunks:
            if material != previousMaterial:
                previousMaterial = material
                if self.overrideDiffuseTextureWithDefault:
                    bind_texture(
                        self.TU_Diffuse,
                        self.defaultTextureOne,
                        self.defaultTextureOne,
                    )
                else:
                    bind_texture(
                        self.TU_Diffuse,
                        material["texture"]["diffuse"],
                        self.defaultTextureOne,
                    )
                bind_texture(
                    self.TU_Opacity,
                    material["texture"]["opacity"],
                    self.defaultTextureOne,
                )
                bind_texture(
                    self.TU_Specular,
                    material["texture"]["specular"],
                    self.defaultTextureOne,
                )
                bind_texture(
                    self.TU_Normal,
                    material["texture"]["normal"],
                    self.defaultNormalTexture,
                )

                for k, v in material["color"].items():
                    gl.glUniform3fv(
                        gl.glGetUniformLocation(
                            shaderProgram, "material_%s_color" % k
                        ),
                        1,
                        v,
                    )
                gl.glUniform1f(
                    gl.glGetUniformLocation(
                        shaderProgram, "material_specular_exponent"
                    ),
                    material["specularExponent"],
                )
                gl.glUniform1f(
                    gl.glGetUniformLocation(shaderProgram, "material_alpha"),
                    material["alpha"],
                )

            gl.glDrawArrays(gl.GL_TRIANGLES, chunkOffset, chunkCount)

        gl.glUseProgram(0)

    def getDefaultAttributeBindings(self):
        return {
            "positionAttribute": self.AA_Position,
            "normalAttribute": self.AA_Normal,
            "texCoordAttribute": self.AA_TexCoord,
            "tangentAttribute": self.AA_Tangent,
            "bitangentAttribute": self.AA_Bitangent,
        }

    def setDefaultUniformBindings(self, shaderProgram):
        assert gl.glGetIntegerv(gl.GL_CURRENT_PROGRAM) == shaderProgram

        gl.glUniform1i(
            gl.glGetUniformLocation(shaderProgram, "diffuse_texture"),
            self.TU_Diffuse,
        )
        gl.glUniform1i(
            gl.glGetUniformLocation(shaderProgram, "opacity_texture"),
            self.TU_Opacity,
        )
        gl.glUniform1i(
            gl.glGetUniformLocation(shaderProgram, "specular_texture"),
            self.TU_Specular,
        )
        gl.glUniform1i(
            gl.glGetUniformLocation(shaderProgram, "normal_texture"),
            self.TU_Normal,
        )
        gl.glUniform1i(
            gl.glGetUniformLocation(shaderProgram, "cube_texture"),
            self.TU_EnvMap,
        )

    defaultVertexShader = load_glsl("objmodel_vertex")

    defaultFragmentShader = load_glsl("objmodel_fragment")
