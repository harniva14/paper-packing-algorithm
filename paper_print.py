import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0

    def fits_inside(self, bin_width, bin_height):
        return self.width <= bin_width and self.height <= bin_height

    def place(self, x, y):
        self.x = x
        self.y = y

    def rotate(self):
        """Rotate the rectangle by swapping its width and height."""
        self.width, self.height = self.height, self.width


class Bin:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.rectangles = []

    def can_place(self, rectangle):
        for placed_rect in self.rectangles:
            if (rectangle.x < placed_rect.x + placed_rect.width and
                rectangle.x + rectangle.width > placed_rect.x and
                rectangle.y < placed_rect.y + placed_rect.height and
                rectangle.y + rectangle.height > placed_rect.y):
                return False
        return True

    def place(self, rectangle):
        # Try placing the rectangle in its current orientation
        if self._attempt_place(rectangle):
            return True
        
        # If it doesn't fit, try rotating and placing again
        rectangle.rotate()
        if self._attempt_place(rectangle):
            return True
        
        # If it still doesn't fit, rotate it back to its original orientation
        rectangle.rotate()
        return False

    def _attempt_place(self, rectangle):
        """Helper method to attempt placing the rectangle in its current orientation."""
        if not self.rectangles:
            if rectangle.fits_inside(self.width, self.height):
                rectangle.place(0, 0)
                self.rectangles.append(Rectangle(rectangle.width, rectangle.height))
                self.rectangles[-1].place(0, 0)
                return True
            return False

        last_rect = self.rectangles[-1]
        if (last_rect.y + last_rect.height + rectangle.height <= self.height and
            last_rect.width == rectangle.width):
            # Place below the last rectangle if widths are the same
            rectangle.place(last_rect.x, last_rect.y + last_rect.height)
        else:
            # Start a new column
            new_x = last_rect.x + last_rect.width
            if new_x + rectangle.width <= self.width:
                rectangle.place(new_x, 0)
            else:
                return False

        if self.can_place(rectangle):
            self.rectangles.append(Rectangle(rectangle.width, rectangle.height))
            self.rectangles[-1].place(rectangle.x, rectangle.y)
            return True
        return False


    def visualize(self, ax, bin_index):
        # Draw the bin
        ax.add_patch(patches.Rectangle((0, 0), self.width, self.height, edgecolor='black', facecolor='none'))
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)
        ax.set_title(f"Paper {bin_index + 1}")

        # Draw each rectangle in the bin
        for rect in self.rectangles:
            ax.add_patch(patches.Rectangle((rect.x, rect.y), rect.width, rect.height, edgecolor='black', facecolor='gray'))
            ax.text(rect.x + rect.width/2, rect.y + rect.height/2, f"{rect.width}x{rect.height}", ha='center', va='center', color='white')



def pack(rectangles, bin_width, bin_height):
    bins = []
    for rectangle in sorted(rectangles, key=lambda r: r.width * r.height, reverse=True):
        placed = False
        for b in bins:
            if b.place(rectangle):
                placed = True
                break
        if not placed:
            new_bin = Bin(bin_width, bin_height)
            if new_bin.place(rectangle):
                bins.append(new_bin)
    return bins

def visualize_bins(bins):
    fig, axs = plt.subplots(1, len(bins), figsize=(5 * len(bins), 5))
    if len(bins) == 1:
        axs = [axs]
    for i, b in enumerate(bins):
        b.visualize(axs[i], i)
    plt.tight_layout()
    plt.show()

# Example usage:
rectangles = [
    Rectangle(5, 10), 
    Rectangle(3, 7), 
    Rectangle(8, 8), 
    Rectangle(6, 6), 
    Rectangle(6, 6),
    Rectangle(2, 1), 
    Rectangle(6, 4), 
    Rectangle(3, 3), 
    Rectangle(3, 3),
    Rectangle(8, 4),
    Rectangle(8, 1)
    ]
bins = pack(rectangles, 20, 10)
print(f"Used {len(bins)} papers.")
visualize_bins(bins)
