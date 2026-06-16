import socket
import time 
import pandas as pd
from pose_utils import A_sim, A_real, V_sim, V_real, pose_str


def scanning():
    mode = input("Select mode ('sim' or 'real'): ").strip().lower()
    if mode == "sim":
        HOST = "172.17.0.2"
        A = A_sim
        V = V_sim
    elif mode == "real":
        HOST = "192.168.0.153"
        A = A_real
        V = V_real
    else:
        print("Invalid mode. Exiting.")
        return

    PORT = 30003

    try: 
        df = pd.read_csv("diode_matrix_path.csv")
        print(f"Loaded {len(df)} waypoints from 'diode_matrix_path.csv'.")
    except FileNotFoundError:
        print("Error: 'diode_matrix_path.csv' not found. Please run 'generate_path.py' first.")
        return
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        print("Connected to robot")
    except Exception as e:
        print(f"Failed to connect to the robot: {e}")
        return
    
    try: 
        for index, row in df.iterrows():
            pose = [row['x'], row['y'], row['z'], row['rx'], row['ry'], row['rz']]
            pose_line = pose_str(pose)

            ur_script = f"movel(p[{pose_line}],  a={A}, v={V}, t=0, r=0)\n"

            print(f"Moving to waypoint {index + 1}/{len(df)}: {pose_line}")
            s.sendall(ur_script.encode('ascii'))
            time.sleep(3.0) 
    except Exception as e: 
        print(f"Error during scanning: {e}")
    finally:        
        s.close()
        print("Connection closed.")

if __name__ == "__main__":
    scanning()