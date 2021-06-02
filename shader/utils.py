from ctypes import c_float, c_uint
from functools import cache
from typing import Any

import numpy as np
import OpenGL.GL as gl

from utils.log import get_logger
from utils.math import Mat3, Mat4, flatten

logger = get_logger()


def get_shader_info_log(obj):
    logLength = gl.glGetShaderiv(obj, gl.GL_INFO_LOG_LENGTH)
    return gl.glGetShaderInfoLog(obj).decode() if logLength > 0 else ""


def compile_and_attach_shader(program, type, sources):
    shader = gl.glCreateShader(type)
    gl.glShaderSource(shader, sources)
    gl.glCompileShader(shader)

    compile_success = gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS)

    if not compile_success:
        err = get_shader_info_log(shader)
        raise RuntimeError(err)

    gl.glAttachShader(program, shader)
    gl.glDeleteShader(shader)


Program = Any


def build_shader(
    vertex_shader_sources,
    fragment_shader_sources,
    attrib_locs,
    frag_data_locs={},
) -> Program:
    shader = gl.glCreateProgram()

    compile_and_attach_shader(
        shader,
        gl.GL_VERTEX_SHADER,
        vertex_shader_sources,
    )

    compile_and_attach_shader(
        shader,
        gl.GL_FRAGMENT_SHADER,
        fragment_shader_sources,
    )

    for name, loc in attrib_locs.items():
        gl.glBindAttribLocation(shader, loc, name)

    for name, loc in frag_data_locs.items():
        gl.glBindFragDataLocation(shader, loc, name)

    gl.glLinkProgram(shader)
    link_success = gl.glGetProgramiv(shader, gl.GL_LINK_STATUS)
    if not link_success:
        err = gl.glGetProgramInfoLog(shader).decode()
        raise RuntimeError(err)

    return shader


def set_uniform(program, name, value):
    loc = gl.glGetUniformLocation(program, name)
    if isinstance(value, float):
        gl.glUniform1f(loc, value)
    elif isinstance(value, int):
        gl.glUniform1i(loc, value)
    elif isinstance(value, (np.ndarray, list)):
        if len(value) == 2:
            gl.glUniform2fv(loc, 1, value)
        if len(value) == 3:
            gl.glUniform3fv(loc, 1, value)
        if len(value) == 4:
            gl.glUniform4fv(loc, 1, value)
    elif isinstance(value, (Mat3, Mat4)):
        value._set_open_gl_uniform(loc)
    else:
        raise ValueError(f"invalid uniform value: '{name}': {value}")


ShaderSource = Any


@cache
def load_glsl(filename) -> ShaderSource:
    with open(f"shader/{filename}.glsl", "r") as f:
        return f.read()


def create_vertex_obj():
    return gl.glGenVertexArrays(1)


def prepare_vertex_data_buffer(vertex_array_object, data, attribute_index):
    gl.glBindVertexArray(vertex_array_object)
    buffer = gl.glGenBuffers(1)
    flat_data = flatten(data)
    data_buffer = (c_float * len(flat_data))(*flat_data)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)
    gl.glBufferData(gl.GL_ARRAY_BUFFER, data_buffer, gl.GL_STATIC_DRAW)
    gl.glVertexAttribPointer(
        attribute_index,
        len(data[0]),
        gl.GL_FLOAT,
        gl.GL_FALSE,
        0,
        None,
    )
    gl.glEnableVertexAttribArray(attribute_index)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
    gl.glBindVertexArray(0)

    return buffer


def prepare_index_data_buffer(vertex_array_object, data):
    gl.glBindVertexArray(vertex_array_object)
    buffer = gl.glGenBuffers(1)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)
    data_buffer = (c_uint * len(data))(*data)
    gl.glBufferData(gl.GL_ARRAY_BUFFER, data_buffer, gl.GL_STATIC_DRAW)
    gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, buffer)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
    gl.glBindVertexArray(0)

    return buffer


Texture = Any


def create_default_texture(data) -> Texture:
    texture = gl.glGenTextures(1)
    gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
    gl.glTexImage2D(
        gl.GL_TEXTURE_2D,
        0,
        gl.GL_RGBA,
        1,
        1,
        0,
        gl.GL_RGBA,
        gl.GL_FLOAT,
        data,
    )
    gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

    return texture
