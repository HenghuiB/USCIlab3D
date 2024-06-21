import open3d as o3d

def icp_align(source, target):
    icp_result = o3d.pipelines.registration.registration_icp(
        source, target, max_correspondence_distance=0.05,
        estimation_method=o3d.pipelines.registration.TransformationEstimationPointToPoint(),
        criteria=o3d.pipelines.registration.ICPConvergenceCriteria()
    )
    source.transform(icp_result.transformation)
    return source

def merge_point_clouds_with_icp(files):
    merged_cloud = o3d.geometry.PointCloud()
    merged_cloud += o3d.io.read_point_cloud(files[0])
    for file in files[1:]:
        cloud = o3d.io.read_point_cloud(file)
        cloud = icp_align(cloud, merged_cloud)
        merged_cloud += cloud
    return merged_cloud

# List of point cloud files to merge
files_to_merge = ["p1.pcd", "p2.pcd"]

# Merge point clouds with ICP alignment
merged_cloud = merge_point_clouds_with_icp(files_to_merge)

# Save merged point cloud
o3d.io.write_point_cloud("merged_cloud_icp_aligned.ply", merged_cloud)
