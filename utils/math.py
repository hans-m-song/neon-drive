import math
from typing import Union

import numpy as np
import OpenGL.GL as gl


def vec2(x, y=None):
    if y is None:
        return np.array([x, x], dtype=np.float32)
    return np.array([x, y], dtype=np.float32)


def vec3(x, y=None, z=None):
    if y is None:
        return np.array([x, x, x], dtype=np.float32)
    if z is None:
        return np.array([x, y, y], dtype=np.float32)
    return np.array([x, y, z], dtype=np.float32)


class Mat4:
    matData = None

    # Construct a Mat4 from a python array
    def __init__(
        self, p=[[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    ):
        if isinstance(p, Mat3):
            self.matData = np.matrix(np.identity(4))
            self.matData[:3, :3] = p.matData
        else:
            self.matData = np.matrix(p)

    # overload the multiplication operator to enable sane looking transformation expressions!
    def __mul__(self, other):
        # if it is a list, we let numpy attempt to convert the data
        # we then return it as a list also (the typical use case is
        # for transforming a vector). Could be made more robust...
        if isinstance(other, (np.ndarray, list)):
            return list(self.matData.dot(other).flat)
        # Otherwise we assume it is another Mat4 or something compatible, and just multiply the matrices
        # and return the result as a new Mat4
        return Mat4(self.matData.dot(other.matData))

    # Helper to get data as a contiguous array for upload to OpenGL
    def getData(self):
        return np.ascontiguousarray(self.matData, dtype=np.float32)

    # note: returns an inverted copy, does not change the object (for clarity use the global function instead)
    #       only implemented as a member to make it easy to overload based on matrix class (i.e. 3x3 or 4x4)
    def _inverse(self):
        return Mat4(np.linalg.inv(self.matData))

    def _transpose(self):
        return Mat4(self.matData.T)

    def _set_open_gl_uniform(self, loc):
        gl.glUniformMatrix4fv(loc, 1, gl.GL_TRUE, self.getData())

    def __str__(self):
        return str(self.matData.A)


class Mat3:
    matData = None

    # Construct a Mat4 from a python array
    def __init__(self, p=[[1, 0, 0], [0, 1, 0], [0, 0, 1]]):
        if isinstance(p, Mat4):
            self.matData = p.matData[:3, :3]
        else:
            self.matData = np.matrix(p)

    # overload the multiplication operator to enable sane looking
    # transformation expressions!
    def __mul__(self, other):
        # if it is a list, we let numpy attempt to convert the data
        # we then return it as a list also (the typical use case is
        # for transforming a vector). Could be made more robust...
        if isinstance(other, (np.ndarray, list)):
            return list(self.matData.dot(other).flat)
        # Otherwise we assume it is another Mat3 or something compatible, and
        # just multiply the matrices
        # and return the result as a new Mat3
        return Mat3(self.matData.dot(other.matData))

    # Helper to get data as a contiguous array for upload to OpenGL
    def getData(self):
        return np.ascontiguousarray(self.matData, dtype=np.float32)

    # note: returns an inverted copy, does not change the object (for clarity
    #       use the global function instead)
    #       only implemented as a member to make it easy to overload based on
    #       matrix class (i.e. 3x3 or 4x4)
    def _inverse(self):
        return Mat3(np.linalg.inv(self.matData))

    def _transpose(self):
        return Mat3(self.matData.T)

    def _set_open_gl_uniform(self, loc):
        gl.glUniformMatrix3fv(loc, 1, gl.GL_TRUE, self.getData())

    def __str__(self):
        return str(self.matData.A)


def mat_to_vec(m: Union[Mat4, Mat3]):
    if isinstance(m, (Mat3, Mat4)):
        data = m.getData()
        return [data[0][-1], data[1][-1], data[2][-1]]
    else:
        raise ValueError(f"value {m} is not Mat3 or Mat4")


# Turns a multidimensional array (up to 3d?) into a 1D array
def flatten(*lll):
    return [u for ll in lll for l in ll for u in l]


def inverse(mat):
    return mat._inverse()


def transpose(mat):
    return mat._transpose()


def normalize(v):
    norm = np.linalg.norm(v)
    return v / norm


def length(v):
    return np.linalg.norm(v)


def cross(a, b):
    return np.cross(a, b)


# Linearly interpolate from v0 to v1, t in [0,1] named to match GLSL
def mix(v0, v1, t):
    return v0 * (1.0 - t) + v1 * t


def dot(a, b):
    return np.dot(a, b)


def make_translation(x, y, z):
    return Mat4([[1, 0, 0, x], [0, 1, 0, y], [0, 0, 1, z], [0, 0, 0, 1]])


def make_scale(x, y, z):
    return Mat4([[x, 0, 0, 0], [0, y, 0, 0], [0, 0, z, 0], [0, 0, 0, 1]])


def make_rotation_y(angle):
    return Mat4(
        [
            [math.cos(angle), 0, -math.sin(angle), 0],
            [0, 1, 0, 0],
            [math.sin(angle), 0, math.cos(angle), 0],
            [0, 0, 0, 1],
        ]
    )


def make_rotation_x(angle):
    return Mat4(
        [
            [1, 0, 0, 0],
            [0, math.cos(angle), -math.sin(angle), 0],
            [0, math.sin(angle), math.cos(angle), 0],
            [0, 0, 0, 1],
        ]
    )


def make_rotation_z(angle):
    return Mat4(
        [
            [math.cos(angle), -math.sin(angle), 0, 0],
            [math.sin(angle), math.cos(angle), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )


def make_look_from(eye, direction, up):
    f = normalize(direction)
    U = np.array(up[:3])
    s = normalize(np.cross(f, U))
    u = np.cross(s, f)
    M = np.matrix(np.identity(4))
    M[:3, :3] = np.vstack([s, u, -f])
    T = make_translation(-eye[0], -eye[1], -eye[2])
    return Mat4(M) * T


# make_lookAt defines a view transform, i.e., from world to view space, using intuitive parameters. location of camera, point to aim, and rough up direction.
# this is basically the same as what we saw in Lexcture #2 for placing the car in the world, except the inverse! (and also view-space 'forwards' is the negative z-axis)
def make_look_at(eye, target, up):
    return make_look_from(
        eye,
        np.array(target[:3]) - np.array(eye[:3]),
        up,
    )


def make_perspective(yFovDeg, aspect, n, f):
    radFovY = math.radians(yFovDeg)
    tanHalfFovY = math.tan(radFovY / 2.0)
    sx = 1.0 / (tanHalfFovY * aspect)
    sy = 1.0 / tanHalfFovY
    zz = -(f + n) / (f - n)
    zw = -(2.0 * f * n) / (f - n)

    return Mat4([[sx, 0, 0, 0], [0, sy, 0, 0], [0, 0, zz, zw], [0, 0, -1, 0]])


def clamp(
    value: float,
    limit_max: float = 0.0,
    limit_min: float = 0.0,
) -> float:
    return max(min(value, limit_max), limit_min)


def transform_point(mat4x4, point):
    x, y, z, w = mat4x4 * [point[0], point[1], point[2], 1.0]
    return vec3(x, y, z) / w


def subdivide(dest, v0, v1, v2, level):
    if level:
        v3 = normalize(v0 + v1)
        v4 = normalize(v1 + v2)
        v5 = normalize(v2 + v0)

        subdivide(dest, v0, v3, v5, level - 1)
        subdivide(dest, v3, v4, v5, level - 1)
        subdivide(dest, v3, v1, v4, level - 1)
        subdivide(dest, v5, v4, v2, level - 1)
    else:
        dest.append(v0)
        dest.append(v1)
        dest.append(v2)


def create_sphere(numSubDivisionLevels):
    sphereVerts = []

    subdivide(
        sphereVerts,
        vec3(0, 1, 0),
        vec3(0, 0, 1),
        vec3(1, 0, 0),
        numSubDivisionLevels,
    )
    subdivide(
        sphereVerts,
        vec3(0, 1, 0),
        vec3(1, 0, 0),
        vec3(0, 0, -1),
        numSubDivisionLevels,
    )
    subdivide(
        sphereVerts,
        vec3(0, 1, 0),
        vec3(0, 0, -1),
        vec3(-1, 0, 0),
        numSubDivisionLevels,
    )
    subdivide(
        sphereVerts,
        vec3(0, 1, 0),
        vec3(-1, 0, 0),
        vec3(0, 0, 1),
        numSubDivisionLevels,
    )

    subdivide(
        sphereVerts,
        vec3(0, -1, 0),
        vec3(1, 0, 0),
        vec3(0, 0, 1),
        numSubDivisionLevels,
    )
    subdivide(
        sphereVerts,
        vec3(0, -1, 0),
        vec3(0, 0, 1),
        vec3(-1, 0, 0),
        numSubDivisionLevels,
    )
    subdivide(
        sphereVerts,
        vec3(0, -1, 0),
        vec3(-1, 0, 0),
        vec3(0, 0, -1),
        numSubDivisionLevels,
    )
    subdivide(
        sphereVerts,
        vec3(0, -1, 0),
        vec3(0, 0, -1),
        vec3(1, 0, 0),
        numSubDivisionLevels,
    )

    return sphereVerts
