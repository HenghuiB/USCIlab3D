import numpy as np

def count_colored_points(ply_file):
    """
    Count the number of points in a PLY file that have a color other than (0, 0, 0).
    
    Args:
        ply_file (str): The path to the PLY file.
        
    Returns:
        int: The number of colored points.
    """
    # Read the PLY file
    with open(ply_file, 'r') as f:
        lines = f.readlines()
    
    # Find the start of the vertex data
    start_idx = next(i for i, line in enumerate(lines) if line.startswith('end_header')) + 1
    
    # Extract the vertex data
    vertex_data = np.array([line.split() for line in lines[start_idx:]], dtype=float)
    print(vertex_data.shape)
    num_colored_points = np.sum(np.any(vertex_data[:, 3:6] != 0, axis=1))
    num_not_colored_points = np.sum(np.all(vertex_data[:, 3:6] == 0, axis=1))
    print(num_not_colored_points)
    return num_colored_points

# Example usage
num_colored = count_colored_points('point_cloud_dense.ply')
print(f"Number of colored points: {num_colored}")