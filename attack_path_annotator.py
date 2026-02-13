#!/usr/bin/env python3
"""
IEC 62443 Attack Path Annotator
Tool for marking network diagrams with attack paths for risk assessments
"""

import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
from PIL import Image, ImageGrab, ImageTk, ImageDraw, ImageFont
import os
import io


class Arrow:
    """Represents an attack path arrow"""

    def __init__(self, start_x, start_y, end_x, end_y, label=""):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.label = label
        self.canvas_items = []  # Store canvas item IDs for deletion


class AttackPathAnnotator:
    def __init__(self, root):
        self.root = root
        self.root.title("IEC 62443 Attack Path Annotator")
        self.root.geometry("1400x900")

        # Image and display
        self.original_image = None
        self.display_image = None
        self.photo_image = None
        self.canvas_image_id = None

        # Arrow drawing state
        self.arrows = []
        self.drawing_arrow = False
        self.arrow_start_x = None
        self.arrow_start_y = None
        self.temp_line = None
        self.temp_crosshairs = []  # Store temporary crosshair IDs

        # Display offsets
        self.image_x = 0
        self.image_y = 0
        self.scale_factor = 1.0

        # Attack path labels - can be customized
        self.attack_labels = [
            "Zone Boundary Breach",
            "Lateral Movement",
            "Privilege Escalation"
        ]

        # Setup UI
        self.setup_ui()
        self.load_from_clipboard()

        # Bind resize event
        self.root.bind('<Configure>', self.on_window_resize)

    def setup_ui(self):
        # Top frame for instructions and controls
        top_frame = tk.Frame(self.root, bg='#f0f0f0', padx=10, pady=10)
        top_frame.pack(fill=tk.X)

        instruction = tk.Label(
            top_frame,
            text="Right-click for menu | Left-click and drag to create attack path arrows",
            font=('Arial', 11),
            bg='#f0f0f0'
        )
        instruction.pack(side=tk.LEFT)

        # Buttons on the right
        button_container = tk.Frame(top_frame, bg='#f0f0f0')
        button_container.pack(side=tk.RIGHT)

        reload_btn = tk.Button(
            button_container,
            text="Reload from Clipboard",
            command=self.load_from_clipboard,
            font=('Arial', 10),
            padx=15,
            pady=5
        )
        reload_btn.pack(side=tk.LEFT, padx=5)

        finish_btn = tk.Button(
            button_container,
            text="Finish & Save PDF",
            command=self.finish_and_save,
            font=('Arial', 10, 'bold'),
            bg='#4CAF50',
            fg='white',
            padx=15,
            pady=5
        )
        finish_btn.pack(side=tk.LEFT, padx=5)

        # Canvas for image display and annotation
        canvas_frame = tk.Frame(self.root)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Add scrollbars
        h_scroll = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        v_scroll = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas = tk.Canvas(
            canvas_frame,
            bg='white',
            xscrollcommand=h_scroll.set,
            yscrollcommand=v_scroll.set
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        h_scroll.config(command=self.canvas.xview)
        v_scroll.config(command=self.canvas.yview)

        # Bind events
        self.canvas.bind('<Button-3>', self.show_context_menu)  # Right-click
        self.canvas.bind('<Button-1>', self.on_left_click)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_release)

        # Create context menu
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Create Arrow", command=self.start_arrow_mode)
        self.context_menu.add_command(label="Delete Arrow", command=self.delete_arrow_at_cursor)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Clear All Arrows", command=self.clear_all_arrows)

        # Store last right-click position
        self.last_right_click_x = 0
        self.last_right_click_y = 0

    def load_from_clipboard(self):
        """Load image from clipboard"""
        try:
            image = ImageGrab.grabclipboard()

            if image is None:
                messagebox.showerror(
                    "No Image",
                    "No image found in clipboard. Please copy an image first."
                )
                return

            if not isinstance(image, Image.Image):
                messagebox.showerror(
                    "Invalid Data",
                    "Clipboard does not contain a valid image."
                )
                return

            self.original_image = image

            # Clear existing arrows when loading new image
            self.clear_all_arrows()

            self.display_image_on_canvas()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image from clipboard:\n{str(e)}")

    def display_image_on_canvas(self):
        """Display the image on canvas"""
        if self.original_image is None:
            return

        # Get canvas dimensions
        self.canvas.update()
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Use original size or scale down if too large
        img_width, img_height = self.original_image.size

        # Scale to fit if needed, but prefer original size
        scale_w = canvas_width / img_width if img_width > canvas_width else 1.0
        scale_h = canvas_height / img_height if img_height > canvas_height else 1.0
        scale = min(scale_w, scale_h, 1.0)  # Don't scale up

        if scale < 1.0:
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            self.display_image = self.original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        else:
            new_width = img_width
            new_height = img_height
            self.display_image = self.original_image.copy()

        self.scale_factor = scale

        # Convert to PhotoImage
        self.photo_image = ImageTk.PhotoImage(self.display_image)

        # Clear canvas
        self.canvas.delete('all')

        # Position image
        self.image_x = 10
        self.image_y = 10

        # Display image
        self.canvas_image_id = self.canvas.create_image(
            self.image_x, self.image_y,
            anchor=tk.NW,
            image=self.photo_image
        )

        # Configure scroll region
        self.canvas.configure(scrollregion=(0, 0, new_width + 20, new_height + 20))

    def show_context_menu(self, event):
        """Show context menu on right-click"""
        self.last_right_click_x = event.x
        self.last_right_click_y = event.y
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def start_arrow_mode(self):
        """Start drawing an arrow from the last right-click position"""
        self.drawing_arrow = True
        self.arrow_start_x = self.last_right_click_x
        self.arrow_start_y = self.last_right_click_y
        self.root.config(cursor="crosshair")

    def on_left_click(self, event):
        """Handle left click"""
        if self.drawing_arrow:
            # Starting point already set, this is the end point
            pass

    def on_drag(self, event):
        """Handle drag motion"""
        if self.drawing_arrow and self.arrow_start_x is not None:
            # Delete previous temporary elements
            if self.temp_line:
                self.canvas.delete(self.temp_line)
            for crosshair in self.temp_crosshairs:
                self.canvas.delete(crosshair)
            self.temp_crosshairs.clear()

            # Draw temporary line
            self.temp_line = self.canvas.create_line(
                self.arrow_start_x, self.arrow_start_y,
                event.x, event.y,
                fill='red',
                width=2,
                arrow=tk.LAST,
                arrowshape=(10, 12, 5)  # Small arrowhead
            )

            # Draw crosshairs at start point
            crosshair_size = 10
            # Vertical line at start
            ch1 = self.canvas.create_line(
                self.arrow_start_x, self.arrow_start_y - crosshair_size,
                self.arrow_start_x, self.arrow_start_y + crosshair_size,
                fill='blue',
                width=1,
                dash=(2, 2)
            )
            # Horizontal line at start
            ch2 = self.canvas.create_line(
                self.arrow_start_x - crosshair_size, self.arrow_start_y,
                self.arrow_start_x + crosshair_size, self.arrow_start_y,
                fill='blue',
                width=1,
                dash=(2, 2)
            )

            # Draw crosshairs at current (end) point
            # Vertical line at end
            ch3 = self.canvas.create_line(
                event.x, event.y - crosshair_size,
                event.x, event.y + crosshair_size,
                fill='blue',
                width=1,
                dash=(2, 2)
            )
            # Horizontal line at end
            ch4 = self.canvas.create_line(
                event.x - crosshair_size, event.y,
                event.x + crosshair_size, event.y,
                fill='blue',
                width=1,
                dash=(2, 2)
            )

            # Store crosshair IDs for cleanup
            self.temp_crosshairs.extend([ch1, ch2, ch3, ch4])

    def on_release(self, event):
        """Handle mouse release"""
        if self.drawing_arrow and self.arrow_start_x is not None:
            # Delete temporary elements
            if self.temp_line:
                self.canvas.delete(self.temp_line)
                self.temp_line = None

            # Delete crosshairs
            for crosshair in self.temp_crosshairs:
                self.canvas.delete(crosshair)
            self.temp_crosshairs.clear()

            # Create arrow
            end_x = event.x
            end_y = event.y

            # Minimum arrow length check
            import math
            distance = math.sqrt((end_x - self.arrow_start_x) ** 2 + (end_y - self.arrow_start_y) ** 2)

            if distance < 10:  # Too short, ignore
                self.drawing_arrow = False
                self.arrow_start_x = None
                self.arrow_start_y = None
                self.root.config(cursor="")
                return

            # Prompt for label
            label = self.prompt_for_label()

            if label is not None:  # User didn't cancel
                # Create arrow object
                arrow = Arrow(self.arrow_start_x, self.arrow_start_y, end_x, end_y, label)
                self.arrows.append(arrow)

                # Draw the arrow
                self.draw_arrow(arrow)

            # Reset state
            self.drawing_arrow = False
            self.arrow_start_x = None
            self.arrow_start_y = None
            self.root.config(cursor="")

    def prompt_for_label(self):
        """Show dialog to select attack path label"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Attack Path Type")
        dialog.geometry("400x200")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Select Attack Path Type:", font=('Arial', 11, 'bold')).pack(pady=10)

        selected_label = tk.StringVar(value=self.attack_labels[0])

        for label in self.attack_labels:
            rb = tk.Radiobutton(
                dialog,
                text=label,
                variable=selected_label,
                value=label,
                font=('Arial', 10)
            )
            rb.pack(anchor=tk.W, padx=30, pady=5)

        result = [None]  # Use list to capture result from nested function

        def ok_clicked():
            result[0] = selected_label.get()
            dialog.destroy()

        def cancel_clicked():
            result[0] = None
            dialog.destroy()

        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=15)

        ok_btn = tk.Button(button_frame, text="OK", command=ok_clicked, padx=20, pady=5, bg='#4CAF50', fg='white')
        ok_btn.pack(side=tk.LEFT, padx=10)

        cancel_btn = tk.Button(button_frame, text="Cancel", command=cancel_clicked, padx=20, pady=5)
        cancel_btn.pack(side=tk.LEFT, padx=10)

        # Wait for dialog to close
        self.root.wait_window(dialog)

        return result[0]

    def draw_arrow(self, arrow):
        """Draw an arrow on the canvas"""
        # Draw the arrow line
        line_id = self.canvas.create_line(
            arrow.start_x, arrow.start_y,
            arrow.end_x, arrow.end_y,
            fill='red',
            width=2,
            arrow=tk.LAST,
            arrowshape=(10, 12, 5),  # Small arrowhead
            tags='arrow'
        )
        arrow.canvas_items.append(line_id)

        # Draw the label
        if arrow.label:
            # Calculate midpoint
            mid_x = (arrow.start_x + arrow.end_x) / 2
            mid_y = (arrow.start_y + arrow.end_y) / 2

            # Calculate if arrow is horizontal-ish (offset text upward)
            import math
            dx = arrow.end_x - arrow.start_x
            dy = arrow.end_y - arrow.start_y
            angle = abs(math.atan2(dy, dx))

            # If angle is close to horizontal (less than 30 degrees from horizontal)
            if angle < math.pi / 6 or angle > 5 * math.pi / 6:
                # Offset text upward
                mid_y -= 12

            # Create text without background box
            text_id = self.canvas.create_text(
                mid_x, mid_y,
                text=arrow.label,
                fill='red',
                font=('Arial', 9, 'bold'),
                tags='arrow'
            )
            arrow.canvas_items.append(text_id)

    def delete_arrow_at_cursor(self):
        """Delete arrow near the last right-click position"""
        delete_threshold = 15  # pixels

        arrows_to_delete = []

        for arrow in self.arrows:
            # Check distance from cursor to arrow start point
            import math
            distance = math.sqrt(
                (self.last_right_click_x - arrow.start_x) ** 2 +
                (self.last_right_click_y - arrow.start_y) ** 2
            )

            if distance <= delete_threshold:
                arrows_to_delete.append(arrow)

        if arrows_to_delete:
            for arrow in arrows_to_delete:
                # Delete from canvas
                for item_id in arrow.canvas_items:
                    self.canvas.delete(item_id)

                # Remove from list
                self.arrows.remove(arrow)

            messagebox.showinfo("Deleted", f"Deleted {len(arrows_to_delete)} arrow(s)")
        else:
            messagebox.showinfo("No Arrow", "No arrow found near cursor position")

    def clear_all_arrows(self):
        """Clear all arrows from the canvas"""
        if self.arrows:
            response = messagebox.askyesno(
                "Clear All",
                f"Delete all {len(self.arrows)} arrow(s)?"
            )

            if response:
                for arrow in self.arrows:
                    for item_id in arrow.canvas_items:
                        self.canvas.delete(item_id)

                self.arrows.clear()
        else:
            # Silent clear if no arrows (used when loading new image)
            self.arrows.clear()

    def finish_and_save(self):
        """Capture the annotated image and save as PDF"""
        if self.original_image is None:
            messagebox.showerror("No Image", "No image loaded")
            return

        try:
            # Create a new image with the original image plus arrows
            # We'll draw on the original-sized image, not the display image
            annotated_image = self.original_image.copy()
            draw = ImageDraw.Draw(annotated_image)

            # Try to load a font, fall back to default if not available
            try:
                font = ImageFont.truetype("arial.ttf", 12)
            except:
                font = ImageFont.load_default()

            # Draw all arrows on the original image
            for arrow in self.arrows:
                # Convert coordinates from display to original image coordinates
                orig_start_x = int((arrow.start_x - self.image_x) / self.scale_factor)
                orig_start_y = int((arrow.start_y - self.image_y) / self.scale_factor)
                orig_end_x = int((arrow.end_x - self.image_x) / self.scale_factor)
                orig_end_y = int((arrow.end_y - self.image_y) / self.scale_factor)

                # Draw the arrow line
                draw.line(
                    [(orig_start_x, orig_start_y), (orig_end_x, orig_end_y)],
                    fill='red',
                    width=3
                )

                # Draw arrowhead
                self.draw_arrowhead(
                    draw,
                    orig_start_x, orig_start_y,
                    orig_end_x, orig_end_y
                )

                # Draw label
                if arrow.label:
                    mid_x = (orig_start_x + orig_end_x) // 2
                    mid_y = (orig_start_y + orig_end_y) // 2

                    # Calculate if arrow is horizontal-ish (offset text upward)
                    import math
                    dx = orig_end_x - orig_start_x
                    dy = orig_end_y - orig_start_y
                    angle = abs(math.atan2(dy, dx))

                    # If angle is close to horizontal (less than 30 degrees from horizontal)
                    if angle < math.pi / 6 or angle > 5 * math.pi / 6:
                        # Offset text upward (scale the offset for original image)
                        mid_y -= int(15 / self.scale_factor)

                    # Draw text without background box
                    draw.text(
                        (mid_x, mid_y),
                        arrow.label,
                        fill='red',
                        font=font,
                        anchor='mm'
                    )

            # Prompt for save location
            from tkinter import filedialog
            filepath = filedialog.asksaveasfilename(
                title="Save Annotated Network Diagram",
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                initialfile="network_attack_path.pdf"
            )

            if not filepath:
                return

            # Convert to RGB if needed
            if annotated_image.mode == 'RGBA':
                rgb_image = Image.new('RGB', annotated_image.size, (255, 255, 255))
                rgb_image.paste(annotated_image, mask=annotated_image.split()[3])
                annotated_image = rgb_image
            elif annotated_image.mode != 'RGB':
                annotated_image = annotated_image.convert('RGB')

            # Save as PDF
            annotated_image.save(filepath, 'PDF', resolution=100.0)

            messagebox.showinfo(
                "Success",
                f"Attack path diagram saved successfully!\n\n{filepath}"
            )

        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save PDF:\n\n{str(e)}")
            import traceback
            traceback.print_exc()

    def draw_arrowhead(self, draw, x1, y1, x2, y2):
        """Draw an arrowhead at the end of a line"""
        import math

        # Calculate angle
        angle = math.atan2(y2 - y1, x2 - x1)

        # Arrowhead size
        arrow_length = 15
        arrow_width = 8

        # Calculate arrowhead points
        left_x = x2 - arrow_length * math.cos(angle - math.pi / 6)
        left_y = y2 - arrow_length * math.sin(angle - math.pi / 6)

        right_x = x2 - arrow_length * math.cos(angle + math.pi / 6)
        right_y = y2 - arrow_length * math.sin(angle + math.pi / 6)

        # Draw arrowhead as polygon
        draw.polygon(
            [(x2, y2), (left_x, left_y), (right_x, right_y)],
            fill='red',
            outline='red'
        )

    def on_window_resize(self, event):
        """Handle window resize event - redraw image and arrows at new scale"""
        # Only respond to canvas resize events, not other widget events
        if event.widget != self.root:
            return

        # Debounce resize events - only redraw after a short delay
        if hasattr(self, '_resize_timer'):
            self.root.after_cancel(self._resize_timer)

        self._resize_timer = self.root.after(100, self.redraw_with_arrows)

    def redraw_with_arrows(self):
        """Redraw the image and all arrows after resize"""
        if self.original_image is None:
            return

        # Store arrow data in original image coordinates before redraw
        original_arrows = []
        for arrow in self.arrows:
            orig_arrow = {
                'start_x': int((arrow.start_x - self.image_x) / self.scale_factor),
                'start_y': int((arrow.start_y - self.image_y) / self.scale_factor),
                'end_x': int((arrow.end_x - self.image_x) / self.scale_factor),
                'end_y': int((arrow.end_y - self.image_y) / self.scale_factor),
                'label': arrow.label
            }
            original_arrows.append(orig_arrow)

        # Redraw the image at new scale
        self.display_image_on_canvas()

        # Recreate arrows at new scale
        self.arrows.clear()
        for orig_arrow in original_arrows:
            # Convert from original coordinates to new display coordinates
            new_start_x = int(orig_arrow['start_x'] * self.scale_factor + self.image_x)
            new_start_y = int(orig_arrow['start_y'] * self.scale_factor + self.image_y)
            new_end_x = int(orig_arrow['end_x'] * self.scale_factor + self.image_x)
            new_end_y = int(orig_arrow['end_y'] * self.scale_factor + self.image_y)

            # Create new arrow with scaled coordinates
            arrow = Arrow(new_start_x, new_start_y, new_end_x, new_end_y, orig_arrow['label'])
            self.arrows.append(arrow)
            self.draw_arrow(arrow)


def main():
    root = tk.Tk()
    app = AttackPathAnnotator(root)
    root.mainloop()


if __name__ == '__main__':
    main()