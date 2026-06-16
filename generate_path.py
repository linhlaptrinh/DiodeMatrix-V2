import pandas as pd
import numpy as np
from pose_utils import contact_to_tcp_position, FIXED_ROTVEC

def generate_diode_matrix():
    print(" Generating path for 4x4 matrix...")
    
    x_corner = -0.13  
    y_corner = -0.528
    z_fixed = 0.2
    
    step = 0.01 #1cm sau nay chuyen thanh 2.5mm    
    
    offsets = [0, 1, 2, 3]
    
    waypoints = []
    point_count = 1
    
    for i in offsets:     
        for j in offsets:
           
            target_x = x_corner - (i * step)
            target_y = y_corner - (j * step)
            contact_xyz = [target_x, target_y, z_fixed]
            
            #pose_utils
            tcp_xyz = contact_to_tcp_position(contact_xyz)
            
            full_pose = np.concatenate([tcp_xyz, FIXED_ROTVEC])
            waypoints.append(full_pose)
            
            print(f"  Point {point_count}: Centre at: [{target_x:.6f}, {target_y:.6f}, {z_fixed:.6f}]")
            point_count += 1

    df = pd.DataFrame(waypoints, columns=['x', 'y', 'z', 'rx', 'ry', 'rz'])
    df.to_csv("diode_matrix_path.csv", index=False)
    print(" Data points exported to file 'diode_matrix_path.csv'!")

if __name__ == "__main__":
    generate_diode_matrix()