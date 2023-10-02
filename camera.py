'''
This file contains classes and functions related to the camera system.
'''
import math
class Camera:
    def __init__(self, position, target, up, fov, width, height):
        self.position = position
        self.target = target
        self.up = up
        self.fov = fov
        self.width = width
        self.height = height
        self.right = normalize(cross(target - position, up))
    def move_camera(self, new_position):
        self.position = new_position
def cross(a, b):
    return Vector(a.y * b.z - a.z * b.y, a.z * b.x - a.x * b.z, a.x * b.y - a.y * b.x)
class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
    def __add__(self, other):
        return Color(self.r + other.r, self.g + other.g, self.b + other.b)
    def __mul__(self, scalar):
        return Color(self.r * scalar, self.g * scalar, self.b * scalar)
    def __rmul__(self, scalar):
        return self.__mul__(scalar)