# GSOF_3dWireFrame
Simple and basic 3D Wire-Frame drawing program.
- Loads .stl or .json object files.
- Supports assembly containers to manipulate object in their own frame of reference.
- Supports line connection between objects in assembly (visual links).
- Uses 4x4 transformation matrices under the hood.
- Uses PyGame to line drawing only.

## Running instructions
## Using pip (recommened)
- run `pip install GSOF_3dWireFrame`
- run `pip install pymeshlab` (if you want to use stl files)

## Manual install
- Clone
- Install requirements `pip install -r requirements.txt`
- run `pip install .`
- run `pip install pymeshlab` (if you want to use stl files)
- Open and run one of the code examples (e.g. `Example_staticWorld.py`)

![alt text](./Documentation/3DWireFrame_quadcopter.gif "Animation")

![alt text](./Documentation/3DWireFrame_interactive.gif "Animation")

![alt text](./Documentation/3DWireFrame_flex.gif "Screenshot")

## This project is licensed under MIT LICENSE, see LICENSE file for more info.