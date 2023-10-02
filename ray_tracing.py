'''
This file contains the core ray tracing algorithm.
'''
import math
class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction
def generate_rays(camera, width, height):
    rays = []
    aspect_ratio = width / height
    fov_tan = math.tan(math.radians(camera.fov / 2))
    for y in range(height):
        for x in range(width):
            normalized_x = (2 * ((x + 0.5) / width) - 1) * fov_tan * aspect_ratio
            normalized_y = (1 - 2 * ((y + 0.5) / height)) * fov_tan
            direction = normalize(camera.target - camera.position + normalized_x * camera.right + normalized_y * camera.up)
            rays.append(Ray(camera.position, direction))
    return rays
def intersect(ray, scene):
    closest_intersection = None
    for object in scene.objects:
        intersection = object.intersect(ray)
        if intersection and (not closest_intersection or intersection.distance < closest_intersection.distance):
            closest_intersection = intersection
    return closest_intersection
def shade(intersection, scene, lights):
    color = intersection.object.material.color
    for light in lights:
        if not is_shadowed(intersection.point, light, scene):
            color += calculate_lighting(intersection, light)
    return color
def is_shadowed(point, light, scene):
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
def calculate_lighting(intersection, light):
    normal = intersection.object.normal(intersection.point)
    light_direction = normalize(light.position - intersection.point)
    diffuse = max(dot(normal, light_direction), 0)
    specular = 0
    if diffuse > 0:
        view_direction = normalize(intersection.ray.origin - intersection.point)
        reflection_direction = reflect(-light_direction, normal)
        specular = pow(max(dot(view_direction, reflection_direction), 0), intersection.object.material.specular_exponent)
    return light.intensity * (intersection.object.material.diffuse * diffuse + intersection.object.material.specular * specular)
def trace_ray(ray, scene, depth):
    intersection = intersect(ray, scene)
    if intersection:
        color = shade(intersection, scene, scene.lights)
        reflection_color = calculate_reflection(ray, intersection, scene, depth)
        refraction_color = calculate_refraction(ray, intersection, scene, depth)
        return color + reflection_color + refraction_color
    return Color(0, 0, 0)
def render_scene(scene, camera, width, height, max_depth):
    image = [[Color(0, 0, 0) for _ in range(width)] for _ in range(height)]
    rays = generate_rays(camera, width, height)
    for y in range(height):
        for x in range(width):
            ray = rays[y * width + x]
            color = trace_ray(ray, scene, max_depth)
            image[y][x] = color
    return image
def normalize(vector):
    length = vector.length()
    return vector / length
def dot(a, b):
    return a.x * b.x + a.y * b.y + a.z * b.z