"""
HIT137 Group Assignment 3
Spot the Difference Desktop Application
This application demonstrates:
-Object-Oriented Programming
-Tkinter GUI development
-OpenCV image processing
-Random non-overlapping image differences
"""


import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
import random
from PIL import Image, ImageTk




#Base (Parent) class defining a common interface for all image effects (Polymorphism).
class DifferenceEffect:
    """Parent class for all image alteration effects."""

    def apply(self, image, region):
        """
        Apply an effect to a region of the image.
        Child classes override this method.
        """
        raise NotImplementedError("Subclasses must implement apply method")


class ColourShiftEffect(DifferenceEffect):
    """Applies a subtle colour shift to a rectangular region."""

    def apply(self, image, region):
        x, y, w, h = region
        roi = image[y:y + h, x:x + w]

        shift = np.array([random.randint(-30, 30),
                          random.randint(-30, 30),
                          random.randint(-30, 30)])

        altered = np.clip(roi.astype(np.int16) + shift, 0, 255).astype(np.uint8)
        image[y:y + h, x:x + w] = altered


class BlurEffect(DifferenceEffect):
    """Applies slight blur to a region."""

    def apply(self, image, region):
        x, y, w, h = region
        roi = image[y:y + h, x:x + w]
        blurred = cv2.GaussianBlur(roi, (15, 15), 0)
        image[y:y + h, x:x + w] = blurred


class BrightnessEffect(DifferenceEffect):
    """Changes brightness in a selected region."""

    def apply(self, image, region):
        x, y, w, h = region
        roi = image[y:y + h, x:x + w]

        factor = random.uniform(0.5, 1.5)
        altered = np.clip(roi.astype(np.float32) * factor, 0, 255).astype(np.uint8)

        image[y:y + h, x:x + w] = altered


class ShapeEffect(DifferenceEffect):
    """Draws a subtle small shape inside the selected region."""

    def apply(self, image, region):
        x, y, w, h = region

        center = (x + w // 2, y + h // 2)
        radius = max(12, min(w, h) // 2)

        colour = (
            random.randint(80, 180),
            random.randint(80, 180),
            random.randint(80, 180)
        )

        cv2.circle(image, center, radius, colour, 2)

#NEW EFFECT 1 (Border Highlight)
class BorderEffect(DifferenceEffect):
    def apply(self, image, region):
        x, y, w, h = region
        cv2.rectangle(image, (x, y), (x+w, y+h), (80, 80, 80), 1)



#NEW EFFECT 2 (Invert Color)
class InvertEffect(DifferenceEffect):
    def apply(self, image, region):
        x, y, w, h = region
        roi = image[y:y + h, x:x + w]
        image[y:y + h, x:x + w] = 255 - roi


#NEW EFFECT 3 (Grayscale Patch)
class GrayEffect(DifferenceEffect):
    def apply(self, image, region):
        x, y, w, h = region
        roi = image[y:y + h, x:x + w]

        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        gray = (gray * 0.8).astype(np.uint8)

        image[y:y + h, x:x + w] = gray


#NEW EFFECT 4 (Pixelation)
class PixelateEffect(DifferenceEffect):
    def apply(self, image, region):
        x, y, w, h = region
        roi = image [y:y +h, x:x + w]
         # pixelate
        small = cv2.resize(roi, (8, 8), interpolation=cv2.INTER_LINEAR)
        pixelated = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)

        image[y:y+h, x:x+w] = pixelated

#NEW EFFECT 5 (Noisy Patch)
class NoiseEffect(DifferenceEffect):
    def apply(self, image, region):
        x, y, w, h = region
        roi = image[y:y+h, x:x+w]

        noise = np.random.randint(0, 40, roi.shape, dtype='uint8')
        noisy = cv2.add(roi, noise)

        image[y:y+h, x:x+w] = noisy

#NEW EFFECT 6 (Dark Patch effect)
class DarkPatchEffect(DifferenceEffect):
    def apply(self, image, region):
        x, y, w, h = region
        roi = image[y:y+h, x:x+w]

        dark = (roi * 0.7).astype(np.uint8)
        image[y:y+h, x:x+w] = dark

#NEW EFFECT 7 (Canny Edge effect)      
class CannyEdgeEffect(DifferenceEffect):
    def apply(self, image, region):
        x, y, w, h = region
        roi = image[y:y+h, x:x+w]

        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 180, 250)
        edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        blended = cv2.addWeighted(roi, 0.9, edges_colored, 0.1, 0)

        image[y:y+h, x:x+w] = blended



#Data Class for Difference Regions
class DifferenceRegion:
    """Stores the position and status of a hidden difference."""

    def __init__(self, x, y, width, height):
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__found = False

    def get_region(self):
        return self.__x, self.__y, self.__width, self.__height

    def is_found(self):
        return self.__found

    def mark_found(self):
        self.__found = True

    def contains_click(self, click_x, click_y, tolerance=20):
        """
        Checks if click is inside or near the difference region.
        Tolerance gives reasonable proximity.
        """
        return (
            self.__x - tolerance <= click_x <= self.__x + self.__width + tolerance
            and self.__y - tolerance <= click_y <= self.__y + self.__height + tolerance
        )

    def overlaps(self, other_region, padding=25):
        #Prevents difference regions from overlapping.
        x1, y1, w1, h1 = self.get_region()
        x2, y2, w2, h2 = other_region.get_region()

        return not (
            x1 + w1 + padding < x2 or
            x2 + w2 + padding < x1 or
            y1 + h1 + padding < y2 or
            y2 + h2 + padding < y1
        )
    def __str__(self):
        return f"DifferenceRegion(found={self.__found})"

#Image Processing Class
class ImageProcessor:
    #Handles image loading, cloning, difference generation, and marking.

    DIFFERENCE_COUNT = 5

    def __init__(self):
        #Collection of polymorphic image effects applied randomly to difference regions.
        self.effects = [
            ColourShiftEffect(),
            BlurEffect(),
            BrightnessEffect(),
            ShapeEffect(),
            BorderEffect(),
            InvertEffect(),
            GrayEffect(),
            PixelateEffect(),
            NoiseEffect(),
            DarkPatchEffect(),
            CannyEdgeEffect()

        ]

    def load_image(self, file_path):
        image = cv2.imread(file_path)

        if image is None:
            raise ValueError("Unsupported or invalid image file.")

        return image

    def create_modified_image(self, original_image):
        modified_image = original_image.copy()
        regions = self.__generate_non_overlapping_regions(original_image)

        for region_obj in regions:
            effect = random.choice(self.effects)
            #randomly selects an effect for each hidden region.
            effect.apply(modified_image, region_obj.get_region())

        return modified_image, regions
    
#Generates random non-overlapping regions for differences.
    def __generate_non_overlapping_regions(self, image):
        height, width = image.shape[:2]
        regions = []
        attempts = 0

        while len(regions) < self.DIFFERENCE_COUNT and attempts < 1000:
            attempts += 1

            region_width = random.randint(max(30, width // 12), max(45, width // 7))
            region_height = random.randint(max(30, height // 12), max(45, height // 7))

            if region_width >= width or region_height >= height:
                region_width = max(20, width // 8)
                region_height = max(20, height // 8)

            x = random.randint(0, width - region_width)
            y = random.randint(0, height - region_height)

            new_region = DifferenceRegion(x, y, region_width, region_height)

            if all(not new_region.overlaps(existing) for existing in regions):
                regions.append(new_region)

        if len(regions) < self.DIFFERENCE_COUNT:
            raise RuntimeError("Could not generate five non-overlapping regions.")

        return regions

    def draw_circle(self, image, region, colour):
        x, y, w, h = region
        center = (x + w // 2, y + h // 2)
        radius = int(max(w, h) / 2) + 10
        cv2.circle(image, center, radius, colour, 4)

    def resize_for_display(self, image, max_width=700, max_height=500):
        height, width = image.shape[:2]
        scale = min(max_width / width, max_height / height)

        new_width = int(width * scale)
        new_height = int(height * scale)

        resized = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)

        return resized, scale

    def convert_to_tk_image(self, cv_image):
        rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_image)
        return ImageTk.PhotoImage(pil_image)



#Game Logic Class

class DifferenceGame:
    #Controls game state, scoring, mistakes, and reveal logic.

    MAX_MISTAKES = 3

    def __init__(self):
        self.regions = []
        self.mistakes = 0
        self.locked = False

    def start_new_round(self, regions):
        self.regions = regions
        self.mistakes = 0
        self.locked = False

    def remaining_count(self):
        return sum(1 for region in self.regions if not region.is_found())

    def found_count(self):
        return sum(1 for region in self.regions if region.is_found())

    def check_click(self, x, y):
        if self.locked:
            return None

        for region in self.regions:
            if not region.is_found() and region.contains_click(x, y):
                region.mark_found()
                return region

        self.mistakes += 1

        if self.mistakes >= self.MAX_MISTAKES:
            self.locked = True

        return None

    def reveal_all(self):
        for region in self.regions:
            if not region.is_found():
                region.mark_found()

        self.locked = True



#Tkinter GUI Class

class SpotDifferenceApp:

    def __init__(self, root):
        self.root = root
        self.root.title("HIT137 Spot the Difference Game")

        self.root.geometry("1200x820")
        self.root.configure(bg="#1e1e2f")
        self.root.minsize(1100, 750)
        self.root.resizable(True, True)

        self.processor = ImageProcessor()
        self.game = DifferenceGame()

        self.original_image = None
        self.modified_image = None

        self.original_tk = None
        self.modified_tk = None

        self.placeholder_label = None

        #  NEW FEATURES
        self.score = 0
        self.start_time = None
        self.timer_running = False

        self.__build_gui()

    def __build_gui(self):


       #Header with title and custom font, background color, and padding for a polished look.
        header = tk.Frame(self.root, bg="#12121c", height=30)
        header.pack(fill="x")
        tk.Label(header, text="🎮 SPOT THE DIFFERENCE",
                 font=("Segoe UI Black", 28, "bold"),
                 bg="#12121c", fg="#00ffe0").pack(pady=15)
        

        button_frame = tk.Frame(self.root, bg="#1e1e2f")
        button_frame.pack(pady=5)

        load_btn = tk.Button(button_frame, text="📂 Load Image",
                             font=("Segoe UI", 12, "bold"),
                             width=15, bg="#3498db", fg="white",
                             relief="flat", command=self.load_image)
        load_btn.grid(row=0, column=0, padx=10)

        reveal_btn = tk.Button(button_frame, text="👁 Reveal Differences",
                               font=("Segoe UI", 12, "bold"),
                               width=18, bg="#e67e22", fg="white",
                               relief="flat", command=self.reveal_differences)
        reveal_btn.grid(row=0, column=1, padx=10)


        #Hover effects for buttons
        def add_hover(w, normal, hover):
            w.bind("<Enter>", lambda e: w.config(bg=hover, fg="black"))
            w.bind("<Leave>", lambda e: w.config(bg=normal, fg="white"))

        add_hover(load_btn, "#3498db", "#5dade2")
        add_hover(reveal_btn, "#e67e22", "#f39c12")

        self.info_label = tk.Label(self.root, text="Load an image to start the game.",
                                  font=("Segoe UI", 12),
                                  bg="#1e1e2f", fg="#dcdde1")
        self.info_label.pack(pady=5)

        #HUD Frame for status 
        hud = tk.Frame(self.root, bg="#1e1e2f")
        hud.pack(pady=5)
        self.status_label = tk.Label(hud, text="Remaining: 5 | Mistakes: 0/3 | Found: 0",
                                     font=("Segoe UI", 12, "bold"), 
                                     bg="#2f3640", fg="#00ffcC", padx=20 , pady=6)
        self.status_label.grid(row=0, column=0, padx=10)
        self.timer_label = tk.Label(hud, text="Time: 0s | Score: 0",
                                     font=("Segoe UI", 12, "bold"), 
                                        bg="#2f3640", fg="#f1c40f", padx=20 , pady=6)
        self.timer_label.grid(row=0, column=1, padx=10)



        image_frame = tk.Frame(self.root, bg="#1e1e2f")
        image_frame.pack(pady=10, fill="both", expand=True)
        image_frame.grid_columnconfigure(0, weight=1)
        image_frame.grid_columnconfigure(1, weight=1)
        

        left_frame = tk.Frame(image_frame, bg="#2f3640", padx=12, pady=12)
        left_frame.grid(row=0, column=0, padx=20, sticky="e")

        right_frame = tk.Frame(image_frame, bg="#2f3640", padx=12, pady=12)
        right_frame.grid(row=0, column=1, padx=20, sticky="w")

        tk.Label(left_frame, text="Original Image",
                 font=("Segoe UI", 14, "bold"),
                 bg="#2f3640", fg="white").pack(pady=5)

        tk.Label(right_frame, text="Modified Image - Click Here",
                 font=("Segoe UI", 14, "bold"),
                 bg="#2f3640", fg="#ffdd59").pack(pady=5)

        self.original_label = tk.Label(left_frame, bg="#111111",
                                      
                                      relief="solid", bd=2)
        self.original_label.pack(pady=5)

        self.modified_label = tk.Label(right_frame, bg="#111111",
                                      
                                      relief="solid", bd=2,
                                      cursor="crosshair")
        self.modified_label.pack(pady=5)

        self.modified_label.bind("<Button-1>", self.handle_click)

        #WELCOME PLACEHOLDER
        self.placeholder_label = tk.Label(
        self.root,
    text="🎮 WELCOME PLAYER\n\n"
         "🔍 Find 5 hidden differences\n"
         "❌ Only 3 mistakes allowed\n\n"
         "👉 Click 'Load Image' to begin",
    font=("Segoe UI", 16, "bold"),
    bg="#12121c",
    fg="#00ffe0",
    justify="center",
    padx=30,
    pady=20
        )
        self.placeholder_label.place(relx=0.5, rely=0.6, anchor="center")

        footer = tk.Label(
            self.root,
            text="HIT137 Assignment 3 • © Spot the Difference • 2026",
            font=("Segoe UI", 10),
            bg="#1e1e2f", fg="#95a5a6")
        footer.pack(side="bottom", fill="x", pady=6)
    
        #FUNCTION FOR FEEDBACK ANIMATION
    def show_feedback(self, symbol, color, x, y, is_correct=True):
        label = tk.Label(self.modified_label, 
                         text=symbol, 
                         font=("Segoe UI Symbol", 18, "bold"),
                         fg=color, 
                          bg=self.modified_label.cget("bg"), bd = 0,
                          highlightthickness=0)
        label.place(x=x, y=y, anchor="center")  
        self.modified_label.after(400, label.destroy)  
        if is_correct:
            def pop(size=14):
                if size > 22:
                 self.modified_label.after(100, label.destroy)
                 return
                label.config(font=("Segoe UI Symbol", size, "bold")  )
                self.root.after(30, lambda: pop(size + 2))
            pop()
        else:
            def shake(step=0):
                if step > 6:
                    label.destroy()
                    return
                offset = 5 if step % 2 == 0 else -5
                label.place(x=x + offset, y=y)
                self.root.after(30, lambda: shake(step+1))
            shake()

    

    #TIMER FUNCTION
    def update_timer(self):
        if not self.timer_running:
            return

        import time
        elapsed = int(time.time() - self.start_time)
        self.timer_label.config(text=f"Time: {elapsed}s | Score: {self.score}")
        if self.timer_running:
           self.root.after(1000, self.update_timer)

    def load_image(self):
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.tiff *.webp")]
        )
        if not file_path:
            return

        try:
            if self.placeholder_label:
                self.placeholder_label.destroy()
                self.placeholder_label = None

            import time
            self.score = 0
            self.start_time = time.time()
            self.timer_running = True
            self.update_timer()

            self.info_label.config(text="Find the hidden differences!")
            
            self.original_image = self.processor.load_image(file_path)
            self.modified_image, regions = self.processor.create_modified_image(self.original_image)

            self.game.start_new_round(regions)

            self.update_display()
            self.update_status()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    
    
    #Updates the displayed images after loading or finding differences.
    def update_display(self):
        if self.original_image is None or self.modified_image is None:
         return

        self.original_display, self.display_scale = self.processor.resize_for_display(
        self.original_image,
        max_width=600,
        max_height=450
    )

        self.modified_display, _ = self.processor.resize_for_display(
        self.modified_image,
        max_width=600,
        max_height=450
    )

        self.original_tk = self.processor.convert_to_tk_image(self.original_display)
        self.modified_tk = self.processor.convert_to_tk_image(self.modified_display)

        self.original_label.config(
        image=self.original_tk,
        anchor="center"
    )

        self.modified_label.config(
        image=self.modified_tk,
        anchor="center"
    )

    def update_status(self):
        self.status_label.config(
            text=f"Remaining: {self.game.remaining_count()} | "
                 f"Mistakes: {self.game.mistakes}/3 | "
                 f"Found: {self.game.found_count()}"
        )
    #Handles user clicks on the modified image, checks for differences, updates score and game state.
    def handle_click(self, event):
        if self.original_image is None or self.modified_image is None:
            messagebox.showinfo("No Image", "Please load an image first.")
            return

        if self.game.locked:

            if self.game.remaining_count()==0:
                    messagebox.showinfo("Game Completed", 
                                    f" You already found all 5 differences! \n\n"
                                    f"Final score: {self.score}")
            elif self.game.mistakes >= self.game.MAX_MISTAKES:   
               self.timer_running = False                   
               found=self.game.found_count()
               messagebox.showinfo("Round Locked", 
                                f"You have reached the maximum number of mistakes. \n\n"
                                f"You have found: {found}/5\n" 
                                f"Final score: {self.score}\n\n"
                                f"Click 'Load Image' to restart the game.")
            else:
                messagebox.showinfo(
                    "Round Locked",
                    "Please load a new image to try again."
                )
            return

        original_x = int(event.x / self.display_scale)
        original_y = int(event.y / self.display_scale)

        found_region = self.game.check_click(original_x, original_y)

        if found_region:
            try:
              import winsound
              winsound.Beep(700, 80)
            except ImportError:
                 pass
            self.show_feedback("✓", "#2ecc71", event.x, event.y, True)

            self.score += 10
            region = found_region.get_region()

            self.processor.draw_circle(self.original_image, region, (0, 0, 255))
            self.processor.draw_circle(self.modified_image, region, (0, 0, 255))

            self.info_label.config(text="Correct! Difference found.")
            self.update_display()

            if self.game.remaining_count() == 0:
                self.timer_running = False
                self.game.locked = True
                self.update_status()
                self.update_display()
                import time
                self.timer_label.config(text=f"Time: {int(time.time() - self.start_time)}s | Score: {self.score}")

                final_score = self.score
                import time
                elapsed_time = int(time.time() - self.start_time)
                messagebox.showinfo("Completed",f"🎉 You found all 5 differences!\nScore: {final_score}/50\n" 
                                    f"Time: {elapsed_time}seconds")
                

        else:
            try:
                 import winsound
                 winsound.Beep(400, 120)
            except ImportError:
                 pass

            self.show_feedback("✕", "#e74c3c", event.x, event.y, False)
            self.score -= 5
            if self.score < 0:
                self.score = 0
            self.info_label.config(text="Incorrect guess. Try again.")
            

        self.update_status()

#Reveals all differences by marking them on both images and locking the game.
    def reveal_differences(self):
        if self.original_image is None or self.modified_image is None:
            messagebox.showinfo("No Image", "Please load an image first.")
            return
        if self.game.remaining_count() == 0:
                messagebox.showinfo("Game Completed", 
                                    "You have already found all 5 differences!")
                return

        self.timer_running = False

        for region in self.game.regions:
            if not region.is_found():             
                self.processor.draw_circle(self.original_image, region.get_region(), (255, 0, 0))
                self.processor.draw_circle(self.modified_image, region.get_region(), (255, 0, 0))

        self.game.locked = True
        self.update_display()
        self.update_status()

        messagebox.showinfo("Revealed", "All differences revealed.")


#Main Program

if __name__ == "__main__":
    root = tk.Tk()
    app = SpotDifferenceApp(root)
    root.mainloop()