import open3d as o3d

def convert_pcd_to_ply(pcd_file, ply_file):
    # Read PCD file
    pcd = o3d.io.read_point_cloud(pcd_file)

    # Write PLY file
    o3d.io.write_point_cloud(ply_file, pcd)

# Specify the paths of the PCD and PLY files
pcd_file = "sur0.pcd"
ply_file = "sur0.ply"

# Convert PCD to PLY
convert_pcd_to_ply(pcd_file, ply_file)
pcd_file = "sur1.pcd"
ply_file = "sur1.ply"

# Convert PCD to PLY
convert_pcd_to_ply(pcd_file, ply_file)