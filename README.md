# DiodeMatrix

High-precision tactile perception system leveraging structured photodiode arrays for intelligent robotic touch sensing and object interaction.

## Overview

DiodeMatrix is a robotic tactile sensing framework that enables precision manipulation and tactile feedback through optical diode matrix arrays. This project integrates with Universal Robots (UR) cobots to perform high-resolution contact sensing and scanning tasks.

## Features

✨ **Core Capabilities**
- 4x4 diode matrix scanning with configurable spacing
- Precision pose calculation for contact point transformation
- Real-time robot motion control via socket communication
- Support for both simulation and real robot environments
- Automated waypoint generation and execution

🤖 **Robot Integration**
- Universal Robots UR cobot compatibility
- Dual-mode operation: simulation and real hardware
- Configurable acceleration and velocity profiles
- Socket-based communication protocol (UR RTDE)

📊 **Data Management**
- CSV-based waypoint storage and export
- Pose transformation utilities
- Contact-to-TCP position conversion

## Project Structure

```
DiodeMatrix/
├── generate_path.py           # Generate 4x4 matrix scanning path
├── run_motion_diode.py        # Execute scanning motion on robot
├── pose_utils.py              # Pose transformation utilities
├── start_pose.py              # Initialize robot start position
├── go_home.py                 # Move robot to home position
├── stop.py                    # Emergency stop handler
├── diode_matrix_path.csv      # Generated waypoints (auto-created)
└── README.md                  # Project documentation
```

## Requirements

- **Python 3.7+**
- **NumPy** - Numerical computations
- **Pandas** - Data manipulation and CSV handling
- **SciPy** - Rotation transformations
- **Universal Robots UR**: Tested with UR5/UR10 cobots

### Python Dependencies

```
numpy>=1.19.0
pandas>=1.1.0
scipy>=1.5.0
```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/linhlaptrinh/DiodeMatrix.git
cd DiodeMatrix
```

### 2. Create Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install numpy pandas scipy
```

## Configuration

### Robot Connection

1) How to call the UR simulation docker
   
sudo docker run --rm -it -p 5900:5900 -p 6080:6080 universalrobots/ursim_e-series -p 29999:29999 -p 30002:30002 -p 30003:30003


Edit `pose_utils.py` to configure your robot parameters:

```python
# Simulation mode
A_sim = 0.5      # Acceleration (m/s²)
V_sim = 0.5      # Velocity (m/s)
HOST_sim = "172.17.0.2"

# Real hardware mode
A_real = 0.1     # Lower values for safety
V_real = 0.05
HOST_real = "192.168.0.153"  # Update with your robot IP
```

### Tool Calibration

Adjust the tool tip offset to match your actual diode array position:

```python
TOOL_TIP_OFFSET = np.array([0.0, 0.05, 0.0])  # [x, y, z] in meters
FIXED_ROTVEC = np.array([0.027, -2.229, 2.237])  # Rotation vector
```

### Matrix Parameters

In `generate_path.py`, customize the scanning pattern:

```python
x_corner = -0.13   # Starting X position
y_corner = -0.528  # Starting Y position
z_fixed = 0.2      # Fixed Z height
step = 0.01        # Grid spacing (1 cm, can adjust to 2.5mm)
offsets = [0, 1, 2, 3]  # 4x4 matrix
```

## Usage

### Step 1: Generate Scanning Path

Generate waypoints for the 4x4 diode matrix:

```bash
python generate_path.py
```

**Output:**
- `diode_matrix_path.csv` - Contains 16 waypoints with TCP positions and rotations
- Console output shows calculated point positions

### Step 2: Initialize Robot Position

Move robot to starting pose:

```bash
python start_pose.py
```

### Step 3: Execute Scanning Motion

Run the tactile sensing scan:

```bash
python run_motion_diode.py
```

Select mode when prompted:
- `sim` - Simulation mode (no hardware required)
- `real` - Real robot hardware

The robot will:
1. Load waypoints from `diode_matrix_path.csv`
2. Move to each point sequentially
3. Pause at each position for sensor data collection (3 seconds)
4. Log motion progress to console

### Step 4: Return to Home

After scanning completes:

```bash
python go_home.py
```

### Emergency Stop

If needed, stop the robot immediately:

```bash
python stop.py
```

## Core Modules

### `generate_path.py`
Generates a structured 4x4 scanning pattern for the diode matrix.

**Key Functions:**
- `generate_diode_matrix()` - Creates waypoint grid with TCP-corrected positions
- Calculates contact points to TCP offset using `contact_to_tcp_position()`
- Exports waypoints to CSV format

### `run_motion_diode.py`
Executes motion commands on the UR robot via socket communication.

**Features:**
- Mode selection (sim/real)
- Waypoint loading from CSV
- Sequential motion execution
- Real-time status feedback

**Motion Parameters:**
- `a` (acceleration) - 0.1 m/s² for real, 0.5 m/s² for simulation
- `v` (velocity) - 0.05 m/s for real, 0.5 m/s for simulation
- `t` (time) - 0 (no time-based movement)
- `r` (blend radius) - 0 (sharp corners at waypoints)

### `pose_utils.py`
Utility functions for pose transformations and robot kinematics.

**Key Functions:**
- `contact_to_tcp_position(contact_xyz, rotvec, tip_offset)` - Converts contact point to TCP frame
- `rotvec_to_matrix(rotvec)` - Converts rotation vector to rotation matrix
- `pose_str(p)` - Formats pose array for UR script

**Constants:**
- `TOOL_TIP_OFFSET` - Offset from TCP to contact point
- `FIXED_ROTVEC` - Tool orientation
- Motion profiles for simulation and real modes

## Technical Details

### Coordinate Frames

The system uses multiple coordinate frames:

1. **Contact Frame** - Where the diode array touches the object
2. **TCP Frame** - Robot tool center point (UR convention)
3. **Robot Base** - UR robot base coordinates

**Transformation:**
```
tcp_position = contact_position - Rotation_Matrix × tip_offset
```

### Motion Protocol

Uses UR's native scripting language over socket connection:

```
Protocol: TCP/IP
Port: 30003 (UR RTDE)
Command: movel(pose, a=acceleration, v=velocity)
Format: movel(p[x, y, z, rx, ry, rz], a=A, v=V, t=0, r=0)\n
```

### Data Format

Waypoints are stored as CSV with 6 DOF:

```csv
x,y,z,rx,ry,rz
-0.130000,-.528000,0.200000,0.027000,-2.229000,2.237000
...
```

## Troubleshooting

### Connection Issues

**Error:** "Failed to connect to the robot"

**Solutions:**
1. Verify robot IP address in code matches your setup
2. Ensure robot is powered and network-connected
3. Check firewall allowing port 30003
4. Use `172.17.0.2` for simulation, `192.168.0.153` for real hardware

### Waypoint Generation Issues

**Error:** "diode_matrix_path.csv not found"

**Solution:** Run `python generate_path.py` before executing motion

### Motion Accuracy

**Low precision contact:**
1. Recalibrate `TOOL_TIP_OFFSET`
2. Verify `FIXED_ROTVEC` orientation
3. Reduce `step` parameter for finer grid
4. Check TCP frame calibration on robot

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit changes (`git commit -m 'Add YourFeature'`)
4. Push to branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Citation

If you use DiodeMatrix in your research, please cite:

```bibtex
@software{diodematrix2026,
  title={DiodeMatrix: Structured Optical Tactile Sensing for Robotic Manipulation},
  author={The Linh Do},
  year={2026},
  url={https://github.com/linhlaptrinh/DiodeMatrix}
}
```

## Contact & Support

For issues, questions, or suggestions:
- **GitHub Issues:** [Open an issue](https://github.com/yourusername/DiodeMatrix/issues)
- **Email:** thelinh2911@gmail.com

## Acknowledgments

- Universal Robots for UR cobot platform
- SciPy and NumPy communities for numerical computing

---

**Status:** Active Development

**Last Updated:** 2024

**Version:** 1.0.0
