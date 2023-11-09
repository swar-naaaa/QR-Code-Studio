import tkinter as tk
from tkinter import ttk, filedialog, colorchooser
import qrcode
from ttkthemes import ThemedStyle
from PIL import Image, ImageTk  # Make sure to have Pillow installed: pip install Pillow

class QRCodeGeneratorApp:
    def __init__(self, master):
        self.master = master
        master.title("QR Code Generator")

        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        window_width = 800
        window_height = 600

        # Calculate the x and y coordinates for the window to be centered
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        master.geometry(f"{window_width}x{window_height}+{x}+{y}")  # Set the window size and position
        master.resizable(True, True)  # Disable window resizing

        self.background_image = tk.PhotoImage(file="Screenshot 2023-11-10 at 12.02.57 AM.png")
        self.background_label = tk.Label(master, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        self.label = tk.Label(master, text="Enter your URL:", font=("Helvetica", 18),bg="black")
        self.label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        self.entry = tk.Entry(master, font=("Helvetica", 16))
        self.entry.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        self.img_label = None  # Initialize without assigning a value
        self.qr_color = "black"

        style = ThemedStyle(master)
        style.set_theme("clam")  # Use the "clam" theme for cooler button styles

        # Configure button style for black background and white text
        style.configure("TButton", font=("Helvetica", 16), padding=10, background="black", foreground="white", borderwidth=0)
        style.map("TButton",
                  background=[("active", "white")],  # Change the button color when hovered
                  foreground=[("active", "black")])

        button_width = 150
        button_height = 40
        button_spacing = 20

        self.generate_button = ttk.Button(master, text="Generate QR Code", command=self.generate_qrcode, style="TButton", cursor="hand2")
        self.generate_button.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        self.color_button = ttk.Button(master, text="Customize QR Color", command=self.choose_color, style="TButton", cursor="hand2")
        self.color_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.save_button = ttk.Button(master, text="Save QR Code", command=self.save_qrcode, style="TButton", cursor="hand2")
        self.save_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        self.reset_button = ttk.Button(master, text="Reset", command=self.reset, style="TButton", cursor="hand2")
        self.reset_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

        self.link_label = tk.Label(master, text="", font=("Helvetica", 16), bg="black")
        self.link_label.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

    def generate_qrcode(self):
        text = self.entry.get()
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image(fill_color=self.qr_color, back_color="white")

        # Update the img_label in the main window
        if self.img_label:
            self.img_label.destroy()

        img_tk = ImageTk.PhotoImage(img)
        self.img_label = tk.Label(self.master, image=img_tk)
        self.img_label.image = img_tk  # Keep a reference to the image
        self.img_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        # Store the generated QR code image
        self.generated_qr_image = img

    def choose_color(self):
        color = colorchooser.askcolor(title="Choose QR Code Color")[1]
        if color:
            self.qr_color = color
            print(f"QR Code color set to {color}")

    def save_qrcode(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path and hasattr(self, 'generated_qr_image'):
            self.generated_qr_image.save(file_path)
            print(f"QR Code saved to {file_path}")

            # Display the tick mark animation
            self.show_tick_animation()

    def reset(self):
        self.entry.delete(0, tk.END)  # Clear the entry
        if self.img_label:
            self.img_label.destroy()
        self.generated_qr_image = None
        self.qr_color = "black"

    def show_tick_animation(self):
        # Create a canvas for the animation
        canvas = tk.Canvas(self.master, width=50, height=50, bg="#F0F0F0", highlightthickness=0)
        canvas.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

        # Draw the tick mark
        tick1 = canvas.create_line(10, 25, 20, 35, width=5, fill="green")
        tick2 = canvas.create_line(20, 35, 40, 15, width=5, fill="green")

        # After a delay, delete the canvas to remove the tick mark
        canvas.after(2000, canvas.destroy)

if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeGeneratorApp(root)
    root.mainloop()
