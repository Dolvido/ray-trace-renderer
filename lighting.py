'''
This file contains classes and functions related to the lighting model.
'''
import math
import random
class Light:
    def __init__(self, position, intensity):
        self.position = position
        self.intensity = intensity
class PointLight(Light):
    def __init__(self, position, intensity):
        super().__init__(position, intensity)
class DirectionalLight(Light):
    def __init__(self, direction, intensity):
        self.direction = direction
        super().__init__(None, intensity)
class AreaLight(Light):
    def __init__(self, position, normal, width, height, intensity):
        self.position = position
        self.normal = normal
        self.width = width
        self.height = height
        self.intensity = intensity
def calculate_shadows(point, light, scene):
    if isinstance(light, PointLight):
        shadow_ray = Ray(point, light.position - point)
        for object in scene.objects:
            if object.intersect(shadow_ray):
                return True
    elif isinstance(light, DirectionalLight):
        shadow_ray = Ray(point, -light.direction)
        for object in scene.objects:
            if object.intersect(shadow_ray):
                return True
    elif isinstance(light, AreaLight):
        num_samples = 10
        for i in range(num_samples):
            sample_point = sample_area_light(light)
            shadow_ray = Ray(point, sample_point - point)
            for object in scene.objects:
                if object.intersect(shadow_ray):
                    return True
    return False
def calculate_reflection(ray, intersection, scene, depth):
    if depth <= 0:
        return Color(0, 0, 0)
    if intersection.object.material.reflectivity == 0:
        return Color(0, 0, 0)
    reflection_direction = reflect(ray.direction, intersection.normal)
    reflection_ray = Ray(intersection.point, reflection_direction)
    reflection_color = trace_ray(reflection_ray, scene, depth - 1)
    return reflection_color * intersection.object.material.reflectivity
def calculate_refraction(ray, intersection, scene, depth):
    if depth <= 0:
        return Color(0, 0, 0)
    if intersection.object.material.transparency == 0:
        return Color(0, 0, 0)
    refraction_direction = refract(ray.direction, intersection.normal, intersection.object.material.refractive_index)
    refraction_ray = Ray(intersection.point, refraction_direction)
    refraction_color = trace_ray(refraction_ray, scene, depth - 1)
    return refraction_color * intersection.object.material.transparency
def sample_area_light(light):
    u = random.uniform(-light.width / 2, light.width / 2)
    v = random.uniform(-light.height / 2, light.height / 2)
    return light.position + u * light.u + v * light.v
def reflect(incident, normal):
    return incident - 2 * dot(incident, normal) * normal
def refract(incident, normal, refractive_index):
    cos_theta_i = -dot(incident, normal)
    sin_theta_i = math.sqrt(max(0, 1 - cos_theta_i * cos_theta_i))
    sin_theta_t = refractive_index * sin_theta_i
    if sin_theta_t >= 1:
        return None
    cos_theta_t = math.sqrt(max(0, 1 - sin_theta_t * sin_theta_t))
    return refractive_index * incident + (refractive_index * cos_theta_i - cos_theta_t) * normal
def dot(a, b):
    return a.x * b.x + a.y * b.y + a.z * b.z