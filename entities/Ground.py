from typing import Any

import OpenGL.GL as gl

from entities.Entity import Entity
from renderer.View import View
from shader.Shader import Shader
from shader.utils import (
    create_vertex_obj,
    prepare_index_data_buffer,
    prepare_vertex_data_buffer,
)
from utils.math import (
    Mat3,
    Mat4,
    cross,
    inverse,
    normalize,
    transpose,
    vec2,
    vec3,
)


class Ground(Entity):
    TU_Diffuse = 0
    TU_Opacity = 1
    TU_Specular = 2
    TU_Normal = 3

    rotation = Mat4()
    size = 4
    scale = 1
    height = 0

    vertices: list[Any]
    normals: list[Any]
    indices: list[Any]

    vertex_obj: Any
    shader: Shader

    def __init__(self):
        super().__init__(name="Ground")

        self.generate_mesh()
        self.upload_data()
        self.shader = Shader()

    def generate_mesh(self):
        vertices = []
        for y in range(self.size):
            for x in range(self.size):
                offset = (y * self.size + x) * 4
                pos = vec2(x, y) * self.scale + offset
                vertices.append(vec3(*pos, self.height))

        normals = [vec3(0.0, 0.0, 1.0)] * self.size * self.size
        for y in range(1, self.size - 1):
            for x in range(1, self.size - 1):
                vxP = vertices[y * self.size + x - 1]
                vxN = vertices[y * self.size + x + 1]
                dx = vxP - vxN

                vyP = vertices[(y - 1) * self.size + x]
                vyN = vertices[(y + 1) * self.size + x]
                dy = vyP - vyN

                nP = normalize(cross(dx, dy))

                vdxyP = vertices[(y - 1) * self.size + x - 1]
                vdxyN = vertices[(y + 1) * self.size + x + 1]
                dxy = vdxyP - vdxyN

                vdyxP = vertices[(y - 1) * self.size + x + 1]
                vdyxN = vertices[(y + 1) * self.size + x - 1]
                dyx = vdyxP - vdyxN

                nD = normalize(cross(dxy, dyx))

                normals[y * self.size + x] = normalize(nP + nD)

        indices = [0] * 2 * 3 * (self.size - 1) * (self.size - 1)
        for y in range(self.size - 1):
            for x in range(self.size - 1):
                qInds = [
                    y * self.size + x,
                    y * self.size + x + 1,
                    (y + 1) * self.size + x,
                    (y + 1) * self.size + x + 1,
                ]
                out_offset = 3 * 2 * (y * (self.size - 1) + x)

                indices[out_offset + 0] = qInds[0]
                indices[out_offset + 1] = qInds[1]
                indices[out_offset + 2] = qInds[2]

                indices[out_offset + 3] = qInds[2]
                indices[out_offset + 4] = qInds[1]
                indices[out_offset + 5] = qInds[3]

        self.vertices = vertices
        self.normals = normals
        self.indices = indices

    def upload_data(self):
        self.vertex_obj = create_vertex_obj()

        prepare_vertex_data_buffer(
            self.vertex_obj,
            self.vertices,
            0,
        )

        prepare_vertex_data_buffer(
            self.vertex_obj,
            self.normals,
            1,
        )

        prepare_index_data_buffer(
            self.vertex_obj,
            self.indices,
        )

    def render(self, view: View = None):
        super().render(view=view)

        model_to_world = Mat4()

        model_to_clip_transform = (
            view.view_to_clip_transform
            * view.world_to_view_transform
            * model_to_world
        )
        model_to_view_transform = view.world_to_view_transform * model_to_world
        model_to_view_normal_transform = inverse(
            transpose(Mat3(model_to_view_transform))
        )

        self.shader.use()
        self.shader.set_uniforms(
            {
                "modelToClipTransform": model_to_clip_transform,
                "modelToViewTransform": model_to_view_transform,
                "modelToViewNormalTransform": model_to_view_normal_transform,
                "worldToViewTransform": view.world_to_view_transform,
                "viewToClipTransform": view.view_to_clip_transform,
            }
        )

        gl.glBindVertexArray(self.vertex_obj)
        gl.glDrawElements(
            gl.GL_TRIANGLES,
            len(self.indices),
            gl.GL_UNSIGNED_INT,
            None,
        )
        gl.glBindVertexArray(0)
        gl.glUseProgram(0)
