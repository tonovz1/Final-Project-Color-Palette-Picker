"""
Project module for the Color Palette Picker application.
Contains the GUI class, helper methods, and the main entry point.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime
from color_utils import (
    hex_to_rgb, rgb_to_hex, is_valid_hex,
    get_harmony_rules, generate_random_palette
)


class ColorPalettePicker:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Palette Picker for Digital Art")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)

        self.current_palette = []
        self.color_buttons = []

        self.setup_styles()
        self.build_ui()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('Title.TLabel', background='#f0f0f0', font=('Arial', 16, 'bold'))
        style.configure('TButton', font=('Arial', 10))

    def build_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        title_label = ttk.Label(main_frame, text="Color Palette Picker", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=10)

        input_frame = ttk.LabelFrame(main_frame, text="Generate Palette", padding="10")
        input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

        ttk.Label(input_frame, text="Base Color (Hex):").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.base_color_entry = ttk.Entry(input_frame, width=15)
        self.base_color_entry.insert(0, "#FF5733")
        self.base_color_entry.grid(row=0, column=1, padx=5)

        self.color_preview = tk.Label(input_frame, width=5, height=1, bg="#FF5733", relief=tk.SUNKEN)
        self.color_preview.grid(row=0, column=2, padx=5)

        ttk.Label(input_frame, text="Harmony Rule:").grid(row=0, column=3, sticky=tk.W, padx=5)
        self.harmony_var = tk.StringVar(value="Complementary")
        self.harmony_dropdown = ttk.Combobox(
            input_frame,
            textvariable=self.harmony_var,
            values=list(get_harmony_rules().keys()),
            state='readonly',
            width=18
        )
        self.harmony_dropdown.grid(row=0, column=4, padx=5)

        ttk.Button(input_frame, text="Generate", command=self.generate_palette).grid(row=0, column=5, padx=5)
        ttk.Button(input_frame, text="Random", command=self.generate_random).grid(row=0, column=6, padx=5)

        display_frame = ttk.LabelFrame(main_frame, text="Generated Palette", padding="10")
        display_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)

        self.palette_frame = ttk.Frame(display_frame)
        self.palette_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        display_frame.columnconfigure(0, weight=1)
        display_frame.rowconfigure(0, weight=1)

        export_frame = ttk.LabelFrame(main_frame, text="Export Palette", padding="10")
        export_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

        ttk.Button(export_frame, text="Export to JSON", command=self.export_json).pack(side=tk.LEFT, padx=5)
        ttk.Button(export_frame, text="Export to TXT", command=self.export_txt).pack(side=tk.LEFT, padx=5)
        ttk.Button(export_frame, text="Copy All to Clipboard", command=self.copy_all_to_clipboard).pack(side=tk.LEFT, padx=5)

        self.status_label = ttk.Label(main_frame, text="Ready", relief=tk.SUNKEN)
        self.status_label.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)

        self.base_color_entry.bind('<KeyRelease>', self.update_color_preview)
        self.generate_palette()

    def update_color_preview(self, event=None):
        hex_color = self.base_color_entry.get().strip()
        if is_valid_hex(hex_color):
            self.color_preview.config(bg=hex_color)
        else:
            self.color_preview.config(bg="#CCCCCC")

    def generate_palette(self):
        hex_color = self.base_color_entry.get().strip()
        if not is_valid_hex(hex_color):
            messagebox.showerror("Invalid Color", "Please enter a valid hex color (e.g., #FF5733)")
            return

        try:
            harmony_rule = self.harmony_var.get()
            harmony_func = get_harmony_rules()[harmony_rule]
            self.current_palette = harmony_func(hex_color)
            self.display_palette()
            self.status_label.config(text=f"Generated {harmony_rule} palette with {len(self.current_palette)} colors")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate palette: {str(e)}")

    def generate_random(self):
        try:
            self.current_palette = generate_random_palette(5)
            self.display_palette()
            self.status_label.config(text="Generated random palette with 5 colors")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate random palette: {str(e)}")

    def display_palette(self):
        for widget in self.palette_frame.winfo_children():
            widget.destroy()
        self.color_buttons = []

        if not self.current_palette:
            return

        swatch_container = ttk.Frame(self.palette_frame)
        swatch_container.pack(fill=tk.BOTH, expand=True)

        for hex_color in self.current_palette:
            swatch_frame = tk.Frame(swatch_container, relief=tk.RAISED, bd=2)
            swatch_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

            swatch_button = tk.Button(
                swatch_frame,
                bg=hex_color,
                height=8,
                relief=tk.RAISED,
                command=lambda color=hex_color: self.on_swatch_click(color)
            )
            swatch_button.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)
            self.color_buttons.append((swatch_button, hex_color))

            info_frame = ttk.Frame(swatch_frame)
            info_frame.pack(fill=tk.X, padx=3, pady=2)

            hex_label = ttk.Label(info_frame, text=hex_color, font=('Courier', 9, 'bold'))
            hex_label.pack()

            try:
                r, g, b = hex_to_rgb(hex_color)
                rgb_label = ttk.Label(info_frame, text=f"RGB({r}, {g}, {b})", font=('Courier', 8))
                rgb_label.pack()
            except Exception:
                pass

            hint_label = ttk.Label(info_frame, text="Click to copy", font=('Arial', 7, 'italic'), foreground='gray')
            hint_label.pack()

    def on_swatch_click(self, hex_color):
        self.copy_to_clipboard(hex_color)

    def copy_to_clipboard(self, text):
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            self.root.update()
            self.status_label.config(text=f"Copied {text} to clipboard")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy to clipboard: {str(e)}")

    def copy_all_to_clipboard(self):
        if not self.current_palette:
            messagebox.showwarning("No Palette", "Generate a palette first")
            return

        palette_text = "\n".join(self.current_palette)
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(palette_text)
            self.root.update()
            self.status_label.config(text=f"Copied all {len(self.current_palette)} colors to clipboard")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy to clipboard: {str(e)}")

    def export_json(self):
        if not self.current_palette:
            messagebox.showwarning("No Palette", "Generate a palette first")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile=f"palette_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )

        if file_path:
            try:
                palette_data = {
                    "generated_at": datetime.now().isoformat(),
                    "harmony_rule": self.harmony_var.get(),
                    "base_color": self.base_color_entry.get().strip(),
                    "colors": self.current_palette,
                    "color_count": len(self.current_palette)
                }
                with open(file_path, 'w') as f:
                    json.dump(palette_data, f, indent=2)
                self.status_label.config(text=f"Exported to {os.path.basename(file_path)}")
                messagebox.showinfo("Success", f"Palette exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")

    def export_txt(self):
        if not self.current_palette:
            messagebox.showwarning("No Palette", "Generate a palette first")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"palette_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )

        if file_path:
            try:
                content = f"""Color Palette Export
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Harmony Rule: {self.harmony_var.get()}
Base Color: {self.base_color_entry.get().strip()}

Colors:
{'-' * 40}
"""
                for i, hex_color in enumerate(self.current_palette, 1):
                    try:
                        r, g, b = hex_to_rgb(hex_color)
                        content += f"{i}. HEX: {hex_color} | RGB: ({r}, {g}, {b})\n"
                    except Exception:
                        content += f"{i}. HEX: {hex_color}\n"
                with open(file_path, 'w') as f:
                    f.write(content)
                self.status_label.config(text=f"Exported to {os.path.basename(file_path)}")
                messagebox.showinfo("Success", f"Palette exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")


def main():
    root = tk.Tk()
    app = ColorPalettePicker(root)
    root.mainloop()
