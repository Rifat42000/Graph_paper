import tkinter as tk

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Paper Paint Tool with Centered Axis and Reset")

        # Canvas size and axis range
        self.canvas_width = 830
        self.canvas_height = 650
        self.axis_min = -1
        self.axis_max = 1

        # Calculate grid box size to evenly distribute labels
        self.grid_box_size = min(self.canvas_width, self.canvas_height) // (self.axis_max - self.axis_min)

        # Set up the canvas with a grid background
        self.canvas = tk.Canvas(root, bg="white", width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

        # Draw graph paper grid, fixed axis lines, and axis labels
        self.draw_grid()
        self.draw_axes()
        self.draw_axis_labels_with_dots()

        # Bind mouse events for drawing
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.reset_draw)

        # Initialize drawing state
        self.last_x, self.last_y = None, None

        # Label to show coordinates
        self.coord_label = tk.Label(root, text="X: 0.0, Y: 0.0", font=("Arial", 12))
        self.coord_label.pack()

        # Reset button to clear canvas
        reset_button = tk.Button(root, text="Reset", command=self.clear_canvas)
        reset_button.pack()

    def draw_grid(self):
        """Draws grid lines on the canvas to resemble graph paper."""
        # Draw vertical lines
        for x in range(0, self.canvas_width, self.grid_box_size):
            self.canvas.create_line(x, 0, x, self.canvas_height, fill="#e0e0e0")

        # Draw horizontal lines
        for y in range(0, self.canvas_height, self.grid_box_size):
            self.canvas.create_line(0, y, self.canvas_width, y, fill="#e0e0e0")

    def draw_axes(self):
        """Draws fixed X and Y axis lines in the middle of the grid (representing zero)."""
        middle_x = self.canvas_width // 2
        middle_y = self.canvas_height // 2

        # Draw Y-axis (vertical line in the middle)
        self.canvas.create_line(middle_x, 0, middle_x, self.canvas_height, fill="blue", width=2)

        # Draw X-axis (horizontal line in the middle)
        self.canvas.create_line(0, middle_y, self.canvas_width, middle_y, fill="blue", width=2)

    def draw_axis_labels_with_dots(self):
        """Adds axis labels from -20 to 20 on both X and Y axes, aligned with grid boxes, with spacing and dots."""
        middle_x = self.canvas_width // 2
        middle_y = self.canvas_height // 2
        label_offset = 15  # Distance from axis line to label

        # Draw X-axis labels and dots
        for i in range(self.axis_min, self.axis_max + 1):
            if i != 0:  # Skip labeling zero at center
                x = middle_x + i * self.grid_box_size
                # Place label slightly below the x-axis line
                self.canvas.create_text(x, middle_y + label_offset, text=str(i), fill="black", font=("Arial", 10))
                # Draw dot at the point
                self.canvas.create_oval(x - 2, middle_y - 2, x + 2, middle_y + 2, fill="black")

        # Draw Y-axis labels and dots
        for i in range(self.axis_min, self.axis_max + 1):
            if i != 0:  # Skip labeling zero at center
                y = middle_y - i * self.grid_box_size
                # Place label slightly to the left of the y-axis line
                self.canvas.create_text(middle_x - label_offset, y, text=str(i), fill="black", font=("Arial", 10))
                # Draw dot at the point
                self.canvas.create_oval(middle_x - 2, y - 2, middle_x + 2, y + 2, fill="black")

    def start_draw(self, event):
        """Initialize starting point of the line."""
        self.last_x, self.last_y = event.x, event.y
        scaled_x, scaled_y = self.get_scaled_coordinates(event.x, event.y)
        self.update_coordinates(scaled_x, scaled_y)

    def draw(self, event):
        """Draw line segment and update coordinates."""
        x, y = event.x, event.y
        if self.last_x and self.last_y:
            # Draw a line segment from the last position to the current position
            self.canvas.create_line(self.last_x, self.last_y, x, y, fill="black", width=2)

            # Update scaled coordinates
            scaled_x, scaled_y = self.get_scaled_coordinates(x, y)
            self.update_coordinates(scaled_x, scaled_y)

            # Update last position
            self.last_x, self.last_y = x, y

    def reset_draw(self, event):
        """Reset the starting point when the mouse button is released."""
        self.last_x, self.last_y = None, None

    def update_coordinates(self, x, y):
        """Update the coordinate label with the scaled x, y position."""
        # Display coordinates with one decimal precision for clarity
        self.coord_label.config(text=f"X: {x:.1f}, Y: {y:.1f}")

        # Display the current coordinates near the drawing cursor
        coord_text_id = self.canvas.create_text(self.last_x + 20, self.last_y - 10, text=f"({x:.1f}, {y:.1f})", fill="red", font=("Arial", 10))
        # Remove the coordinate text after a short delay for readability
        self.canvas.after(500, self.canvas.delete, coord_text_id)

    def get_scaled_coordinates(self, x, y):
        """Convert pixel coordinates to a scaled axis range with floating-point precision."""
        # Calculate the center point on the canvas in pixels
        center_x = self.canvas_width / 2
        center_y = self.canvas_height / 2

        # Scale the x coordinate to -20 to 20 range
        scaled_x = (x - center_x) / self.grid_box_size

        # Scale the y coordinate to -20 to 20 range, inverting the direction
        scaled_y = (center_y - y) / self.grid_box_size

        return scaled_x, scaled_y

    def clear_canvas(self):
        """Clears all drawings from the canvas and redraws the grid and axes."""
        self.canvas.delete("all")
        self.draw_grid()
        self.draw_axes()
        self.draw_axis_labels_with_dots()

# Create the Tkinter root and run the app
root = tk.Tk()
app = PaintApp(root)
root.mainloop()
