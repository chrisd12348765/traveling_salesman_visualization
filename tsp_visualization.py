import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider
from itertools import permutations
import sys

frames_per_update_var = 500

def calculate_distance(path, points):
    """Calculate the total distance of a path."""
    total_distance = 0
    for i in range(len(path) - 1):
        total_distance += np.linalg.norm(points[path[i]] - points[path[i + 1]])
    # Add distance from last point back to start
    total_distance += np.linalg.norm(points[path[-1]] - points[path[0]])
    return total_distance

def generate_random_points(n_points, seed=None):
    """Generate random points for the TSP."""
    if seed is not None:
        np.random.seed(seed)
    return np.random.rand(n_points, 2) * 100

def update(frame, ax, points, all_paths, distances, best_path_info, n_cities):
    """Update function for animation."""
    try:
        ax.clear()
        
        # Plot all points
        ax.scatter(points[:, 0], points[:, 1], c='red', s=100)
        
        # Plot current path
        current_path = all_paths[frame]
        current_distance = distances[frame]
        
        # Update best path if current path is better
        if current_distance < best_path_info['distance']:
            best_path_info['path'] = current_path
            best_path_info['distance'] = current_distance
        
        # Create path points array correctly
        path_points = np.zeros((len(current_path) + 1, 2))
        for i, city_idx in enumerate(current_path):
            path_points[i] = points[city_idx]
        # Close the path by adding the first point again
        path_points[-1] = points[current_path[0]]
        
        # Plot the current path
        ax.plot(path_points[:, 0], path_points[:, 1], 'b-', alpha=0.5)
        
        # Add point labels
        for i, (x, y) in enumerate(points):
            ax.annotate(f'City {i}', (x, y), xytext=(5, 5), textcoords='offset points')
        
        # Update title with current distance, best distance, and number of cities
        ax.set_title(f'Cities: {n_cities} | Current Distance: {current_distance:.2f}\nBest Distance: {best_path_info["distance"]:.2f}')
        
        # Set axis limits with some padding
        ax.set_xlim(-10, 110)
        ax.set_ylim(-10, 110)
        
        return ax,
    except Exception as e:
        print(f"Error in update function: {e}")
        return ax,

def update_cities(val, fig, ax, points_var, all_paths_var, distances_var, best_path_info_var, anim_var, n_cities_var):
    """Update the number of cities when the slider changes."""
    try:
        # Get the new number of cities
        n_cities = int(val)
        n_cities_var[0] = n_cities
        
        # Generate new random points
        points = generate_random_points(n_cities)
        points_var[0] = points
        
        # Generate all possible permutations
        all_paths = list(permutations(range(n_cities)))
        all_paths_var[0] = all_paths
        
        # Calculate distances for all paths
        distances = [calculate_distance(path, points) for path in all_paths]
        distances_var[0] = distances
        
        # Find the best path and distance
        best_path_idx = np.argmin(distances)
        best_path = all_paths[best_path_idx]
        best_distance = distances[best_path_idx]
        
        # Update best path info
        best_path_info_var[0] = {
            'path': best_path,
            'distance': best_distance
        }
        
        # Update the animation
        anim_var[0].event_source.stop()
        anim_var[0] = FuncAnimation(
            fig, update,
            frames=len(all_paths),
            fargs=(ax, points, all_paths, distances, best_path_info_var[0], n_cities),
            interval=frames_per_update_var, 
            blit=False
        )
        
        # Redraw the figure
        fig.canvas.draw_idle()
        
    except Exception as e:
        print(f"Error updating cities: {e}")

def update_speed(val, fig, anim_var, all_paths, ax, points, distances, best_path_info_var, n_cities):
    """Update the speed/frames per update when the slider changes."""

    global frames_per_update_var
    frames_per_update_var = int(val)

    try:
        # Update the animation
        anim_var[0].event_source.stop()
        anim_var[0] = FuncAnimation(
            fig, update,
            frames=len(all_paths),
            fargs=(ax, points, all_paths, distances, best_path_info_var[0], n_cities),
            interval=frames_per_update_var,  
            blit=False
        )
        
        # Redraw the figure
        fig.canvas.draw_idle()
        
    except Exception as e:
        print(f"Error changing speed: {e}")

def main():
    try:
        # Set the backend to TkAgg for better compatibility
        plt.switch_backend('TkAgg')
        
        # Initial number of cities
        n_cities = 4
        
        print("Generating random points...")
        points = generate_random_points(n_cities)
        
        print("Generating permutations...")
        all_paths = list(permutations(range(n_cities)))
        
        print("Calculating distances...")
        distances = [calculate_distance(path, points) for path in all_paths]
        
        # Find the best path and distance
        best_path_idx = np.argmin(distances)
        best_path = all_paths[best_path_idx]
        best_distance = distances[best_path_idx]
        
        # Initialize best path info
        best_path_info = {
            'path': best_path,
            'distance': best_distance
        }
        
        print("Creating visualization...")
        # Create figure and axis
        fig = plt.figure(figsize=(10, 10))
        
        # Create main plot area
        ax = fig.add_subplot(111)
        
        # Create slider axis
        city_slider_ax = fig.add_axes([0.2, 0.05, 0.6, 0.03])
        speed_slider_ax = fig.add_axes([0.2, 0.01, 0.6, 0.03])
        
        # Create slider for cities
        slider = Slider(
            ax=city_slider_ax,
            label='Number of Cities',
            valmin=3,
            valmax=8,
            valinit=n_cities,
            valstep=1
        )

        #Create slider for speed
        speed_slider = Slider(
            ax=speed_slider_ax,
            label='Frames per Update',
            valmin=100,
            valmax=1000,
            valinit=500,
            valstep=100
        )
        
        # Create variables to store data that needs to be updated
        points_var = [points]
        all_paths_var = [all_paths]
        distances_var = [distances]
        best_path_info_var = [best_path_info]
        anim_var = [None]
        n_cities_var = [n_cities]
        
        # Create animation
        anim = FuncAnimation(
            fig, update,
            frames=len(all_paths),
            fargs=(ax, points, all_paths, distances, best_path_info, n_cities),
            interval=frames_per_update_var,  # 1 second between frames
            blit=False
        )
        
        # Store animation in variable
        anim_var[0] = anim
        
        # Connect slider to update function
        slider.on_changed(lambda val: update_cities(val, fig, ax, points_var, all_paths_var, distances_var, best_path_info_var, anim_var, n_cities_var))
        speed_slider.on_changed(
    lambda val: update_speed(val, fig, anim_var, all_paths_var[0], ax, points_var[0], distances_var[0], best_path_info_var, n_cities_var[0])
)

        print("Starting animation...")
        plt.show()
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 