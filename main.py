from ursina import * # pyright: ignore[reportWildcardImportFromLibrary]
from math import atan2, degrees
import logging
import random
from panda3d.core import loadPrcFileData
loadPrcFileData('', 'load-display pandagl')

logging.getLogger('ursina').setLevel(logging.CRITICAL)

app = Ursina()
application.development_mode = False # pyright: ignore[reportAttributeAccessIssue]

window.color = color.white
window.exit_button.visible = False
window.fps_counter.enabled = False
window.collider_counter.enabled = False
window.entity_counter.enabled = False

camera.clip_plane_far = 100000

Sky()

DirectionalLight(rotation=(45, -45, 0), intensity=1)
AmbientLight(color=color.white)

MAP_SCALE = 1000
MAP_BOUND = MAP_SCALE / 2.5
PLANE_SCALE = 1

visual_map = Entity(
    model='assets/map/object.glb',
    scale=MAP_SCALE, # pyright: ignore[reportArgumentType]
    position=(0, 0, 0) # pyright: ignore[reportArgumentType]
)

ground = Entity(
    model='plane',
    scale=(MAP_SCALE, 1, MAP_SCALE), # pyright: ignore[reportArgumentType]
    position=(0, 0, 0), # pyright: ignore[reportArgumentType]
    collider='box',
    visible=False
)

wall_thickness = 10
wall_height = 200

walls = [
    Entity(model='cube', scale=(wall_thickness, wall_height, MAP_SCALE*2), position=( MAP_BOUND, wall_height/2, 0), collider='box', visible=False), # pyright: ignore[reportArgumentType]
    Entity(model='cube', scale=(wall_thickness, wall_height, MAP_SCALE*2), position=(-MAP_BOUND, wall_height/2, 0), collider='box', visible=False), # pyright: ignore[reportArgumentType]
    Entity(model='cube', scale=(MAP_SCALE*2, wall_height, wall_thickness), position=(0, wall_height/2,  MAP_BOUND), collider='box', visible=False), # pyright: ignore[reportArgumentType]
    Entity(model='cube', scale=(MAP_SCALE*2, wall_height, wall_thickness), position=(0, wall_height/2, -MAP_BOUND), collider='box', visible=False), # pyright: ignore[reportArgumentType]
]

plane = Entity(
    model='assets/airplane/object.glb',
    scale=PLANE_SCALE, # pyright: ignore[reportArgumentType]
    position=(0, 20, 0), # pyright: ignore[reportArgumentType]
    collider='box',
    rotation=(0, 180, 0) # pyright: ignore[reportArgumentType]
)

camera.look_at(plane)
camera.parent = plane
camera.position = (0, 5, -20)
camera.rotation = (0, 0, 0)
camera.fov = 70

min_zoom = -10
max_zoom = -200
zoom_speed = 80

speed = 0
max_speed = 7
acceleration = 6
deceleration = 6
lift_factor = 2.5
gravity = 15
vertical_speed = 0
roll = 0
max_roll = 45
started = False

def hud(text, pos, size=1.6):
    return Text(text=text, position=pos, scale=size, parent=camera.ui, background=True)

speed_text = hud('Speed: 0 m/s', (-0.75, 0.45))
altitude_text = hud('Altitude: 20 m', (-0.75, 0.30))
v_speed_text = hud('V-Speed: 0 m/s', (-0.75, 0.15))
compass_text = hud('Compass: 0°', (-0.75, 0))
roll_text = hud('Roll: 0°', (-0.75, -0.15))
status_text = hud('Press W to Start', (0, -0.05), 2)

def update():
    global speed, vertical_speed, started, roll
    dt = time.dt # pyright: ignore[reportAttributeAccessIssue]

    # Camera zoom
    if held_keys['q']: # pyright: ignore[reportIndexIssue]
        camera.position.z += zoom_speed * dt
    if held_keys['e']: # pyright: ignore[reportIndexIssue]
        camera.position.z -= zoom_speed * dt
    camera.position.z = clamp(camera.position.z, max_zoom, min_zoom)

    if not started:
        status_text.visible = True
        if held_keys['w']: # pyright: ignore[reportIndexIssue]
            started = True
            status_text.visible = False
        return

    # Forward/backward
    if held_keys['w']: # pyright: ignore[reportIndexIssue]
        speed = max(speed + acceleration * dt, max_speed)
    elif held_keys['s']: # pyright: ignore[reportIndexIssue]
        speed = max(speed - deceleration * dt, -max_speed)
    else:
        speed *= 0.98

    # Yaw left/right
    if held_keys['a']: # pyright: ignore[reportIndexIssue]
        plane.rotation_y -= 80 * dt
    if held_keys['d']: # pyright: ignore[reportIndexIssue]
        plane.rotation_y += 80 * dt

    # Roll gradual auto-level + induced by altitude changes
    target_roll = 0
    if held_keys['z']: # pyright: ignore[reportIndexIssue]
        target_roll = -max_roll
    elif held_keys['x']: # pyright: ignore[reportIndexIssue]
        target_roll = max_roll

    # Add gradual roll from altitude control
    altitude_input = 0
    if held_keys['r']: # pyright: ignore[reportIndexIssue]
        altitude_input = 1
    elif held_keys['t']: # pyright: ignore[reportIndexIssue]
        altitude_input = -1

    vertical_speed += altitude_input * dt * 5  # r/t changes climb/fall
    target_roll += altitude_input * 15  # small tilt effect
    roll += (target_roll - roll) * dt * 2  # smooth interpolation
    plane.rotation_z = roll

    # Pitch
    pitch = 0
    if held_keys['up']: # pyright: ignore[reportIndexIssue]
        pitch = 35
    if held_keys['down']: # pyright: ignore[reportIndexIssue]
        pitch = -35
    plane.rotation_x = pitch * dt

    # Move forward
    forward = Vec3(plane.forward.x, 0, plane.forward.z).normalized()
    plane.position += forward * speed * dt

    # Gravity + lift
    vertical_speed -= gravity * dt
    vertical_speed += speed * lift_factor * dt * 0.01
    plane.position.y += vertical_speed * dt

    # Collisions
    hit = plane.intersects()
    if hit.hit:
        plane.position += hit.normal * 1.5
        speed *= -0.4
        vertical_speed *= -0.3
        plane.rotation_y += random.uniform(-25, 25)
        plane.rotation_z += random.uniform(-20, 20)

    # Compass & HUD
    compass = degrees(atan2(plane.forward.x, plane.forward.z))
    if compass < 0:
        compass += 360

    speed_text.text = f'Speed: {speed:.1f} m/s'
    altitude_text.text = f'Altitude: {plane.position.y:.1f} m'
    v_speed_text.text = f'V-Speed: {vertical_speed:.1f} m/s'
    compass_text.text = f'Compass: {compass:.0f}°'
    roll_text.text = f'Roll: {roll:.1f}°'

app.run() # pyright: ignore[reportAttributeAccessIssue]
