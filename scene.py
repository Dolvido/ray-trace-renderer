'''
This file contains classes and functions related to scene representation.
'''
import math
class Object:
    def __init__(self):
        pass
class Sphere(Object):
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material
    def intersect(self, ray):
        oc = ray.origin - self.center
        a = ray.direction.dot(ray.direction)
        b = 2.0 * oc.dot(ray.direction)
        c = oc.dot(oc) - self.radius * self.radius
        discriminant = b * b - 4 * a * c
        if discriminant > 0:
            t1 = (-b - math.sqrt(discriminant)) / (2 * a)
            t2 = (-b + math.sqrt(discriminant)) / (2 * a)
            if t1 > 0:
                return Intersection(t1, self, ray)
            elif t2 > 0:
                return Intersection(t2, self, ray)
        return None
    def normal(self, point):
        return (point - self.center).normalize()
class Plane(Object):
    def __init__(self, position, normal, material):
        self.position = position
        self.normal = normal
        self.material = material
    def intersect(self, ray):
        denom = ray.direction.dot(self.normal)
        if abs(denom) > 0.0001:
            t = (self.position - ray.origin).dot(self.normal) / denom
            if t > 0:
                return Intersection(t, self, ray)
        return None
    def normal(self, point):
        return self.normal
class Triangle(Object):
    def __init__(self, v0, v1, v2, material):
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2
        self.material = material
        self.normal = (v1 - v0).cross(v2 - v0).normalize()
    def intersect(self, ray):
        edge1 = self.v1 - self.v0
        edge2 = self.v2 - self.v0
        h = ray.direction.cross(edge2)
        a = edge1.dot(h)
        if abs(a) < 0.0001:
            return None
        f = 1 / a
        s = ray.origin - self.v0
        u = f * s.dot(h)
        if u < 0 or u > 1:
            return None
        q = s.cross(edge1)
        v = f * ray.direction.dot(q)
        if v < 0 or u + v > 1:
            return None
        t = f * edge2.dot(q)
        if t > 0:
            return Intersection(t, self, ray)
        return None
    def normal(self, point):
        return self.normal
class Material:
    def __init__(self, color, reflectivity, transparency, refractive_index):
        self.color = color
        self.reflectivity = reflectivity
        self.transparency = transparency
        self.refractive_index = refractive_index
class Intersection:
    def __init__(self, distance, object, ray):
        self.distance = distance
        self.object = object
        self.ray = ray
        self.point = ray.origin + ray.direction * distance
class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction.normalize()
class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar, self.z * scalar)
    def __truediv__(self, scalar):
        return Vector(self.x / scalar, self.y / scalar, self.z / scalar)
    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z
    def cross(self, other):
        return Vector(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )
    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
    def normalize(self):
        length = self.length()
        return Vector(self.x / length, self.y / length, self.z / length)