import numpy as np
import OpenGL.GL as gl

from utils.math import Mat3, Mat4


def get_shader_info_log(obj):
    logLength = gl.glGetShaderiv(obj, gl.GL_INFO_LOG_LENGTH)
    return gl.glGetShaderInfoLog(obj).decode() if logLength > 0 else ""


def compile_and_attach_shader(shaderProgram, shaderType, sources):
    shader = gl.glCreateShader(shaderType)
    gl.glShaderSource(shader, sources)
    gl.glCompileShader(shader)

    compileOk = gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS)

    if not compileOk:
        shaderTypeStr = {
            gl.GL_VERTEX_SHADER: "VERTEX",
            gl.GL_FRAGMENT_SHADER: "FRAGMENT",
            gl.GL_COMPUTE_SHADER: "COMPUTE",
        }
        err = get_shader_info_log(shader)
        print(
            "%s SHADER COMPILE ERROR: '%s'"
            % (shaderTypeStr.get(shaderType, "??"), err)
        )
        return False

    gl.glAttachShader(shaderProgram, shader)
    gl.glDeleteShader(shader)
    return True


def build_shader(
    vertex_shader_sources,
    fragment_shader_sources,
    attrib_locs,
    frag_data_locs={},
):
    shader = gl.glCreateProgram()

    if compile_and_attach_shader(
        shader, gl.GL_VERTEX_SHADER, vertex_shader_sources
    ) and compile_and_attach_shader(
        shader, gl.GL_FRAGMENT_SHADER, fragment_shader_sources
    ):
        for name, loc in attrib_locs.items():
            gl.glBindAttribLocation(shader, loc, name)
        for name, loc in frag_data_locs.items():
            gl.glBindFragDataLocation(shader, loc, name)

        gl.glLinkProgram(shader)
        linkStatus = gl.glGetProgramiv(shader, gl.GL_LINK_STATUS)
        if not linkStatus:
            err = gl.glGetProgramInfoLog(shader).decode()
            print("SHADER LINKER ERROR: '%s'" % err)
            gl.glDeleteProgram(shader)
            return None
        return shader
    else:
        gl.glDeleteProgram(shader)
        return None


def set_uniform(shaderProgram, uniformName, value):
    loc = gl.glGetUniformLocation(shaderProgram, uniformName)
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
        assert False  # If this happens the type was not supported, check your argument types and either add a new else case above or change the type
