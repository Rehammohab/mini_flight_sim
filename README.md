# Ursina Airplane Simulator

## Overview

This is a simple 3D airplane simulation built with the **Ursina Engine**. It allows players to control an airplane in a limited 3D environment with basic physics, camera zoom, and HUD indicators for speed, altitude, roll, vertical speed, and compass direction.

## Features

* **3D Map**: Loaded from a GLB model (`assets/map/object.glb`) with invisible walls to prevent leaving the play area.
* **Controllable Airplane**: Loaded from a GLB model (`assets/airplane/object.glb`) with smooth forward motion, roll, pitch, and yaw.
* **Camera**: Third-person view that follows the plane, adjustable zoom with `Q` and `E`.
* **HUD**: Displays real-time speed, altitude, vertical speed, compass, roll, and game status.
* **Physics**: Basic gravity, lift, collision response, and acceleration/deceleration.
* **Controls**:

  * `W` - Increase speed / Start game
  * `S` - Decrease speed
  * `A` - Yaw left
  * `D` - Yaw right
  * `Q` - Zoom out
  * `E` - Zoom in
  * `R` - Ascend
  * `T` - Descend
  * `Z` - Roll left
  * `X` - Roll right

## Installation

1. Install Python 3.10+.
2. Install required libraries:

```bash
pip install -r requirements.txt
```

## Usage

Run the simulator with:

```bash
python main.py
```

The game starts paused. Press `W` to start controlling the airplane.

## Notes

* The simulation currently has invisible walls to prevent the airplane from leaving the map.
* Collisions with walls or ground will affect speed, vertical speed, and rotation randomly to simulate impact.
* Camera zoom is limited between -10 and -200 units.

## License

This project is open-source and free to use. Textures and models should comply with their respective licenses.

---

**Disclaimer**: The plane may sink into the map or behave unpredictably if collision detection fails. Apologies for any rough textures or placeholder models.
