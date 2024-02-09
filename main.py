#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk


class ImageApp:
    def __init__(self, root):
        self.root = root
        root.title('Image Coordinate Finder')

        self.canvas = tk.Canvas(root, cursor='cross')
        self.canvas.bind('<Button-1>', self.click_event)

        # Set scrollbars
        vbar = tk.Scrollbar(root, orient='vertical', command=self.canvas.yview)
        hbar = tk.Scrollbar(root, orient='horizontal', command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=vbar.set, xscrollcommand=hbar.set)

        vbar.pack(side='right', fill='y')
        hbar.pack(side='bottom', fill='x')
        self.canvas.pack(side='left', fill='both', expand=True)

        # Place buttons
        button_frame = tk.Frame(root)
        button_frame.pack(side='top', fill='x', expand=False)

        open_button = tk.Button(button_frame, text='Open Image', command=self.open_image)
        open_button.pack(side='left', padx=10, pady=5)

        scale_button = tk.Button(button_frame, text='Scale Image', command=self.scale_image)
        scale_button.pack(side='right', padx=10, pady=5)

        self.org_resolution_label_text = 'Original Resolution (WxH): '
        self.info_label = tk.Label(root, text=self.org_resolution_label_text)
        self.info_label.pack(side='bottom')

        self.coords_label_text = 'Coordinates at original resolution: '
        self.coords_label = tk.Label(root, text=self.coords_label_text)
        self.coords_label.pack(side='bottom')

        self.original_image = None
        self.displayed_image = None
        self.scale = 1.0
        self.current_cross = []

    def open_image(self):
        filepath = filedialog.askopenfilename()
        if not filepath:
            return
        self.original_image = Image.open(filepath)
        self.display_image(self.original_image)
        self.info_label.config(
            text=f'{self.org_resolution_label_text}{self.original_image.width}x{self.original_image.height}')

    def display_image(self, image):
        self.displayed_image = ImageTk.PhotoImage(image)
        self.canvas.config(scrollregion=(0, 0, image.width, image.height))
        self.canvas.create_image(0, 0, image=self.displayed_image, anchor='nw')
        self.canvas.image = self.displayed_image
        self.clear_cross()

    def scale_image(self):
        if self.original_image is None:
            return
        scale_factor = simpledialog.askfloat('Scale Factor', 'Enter scale factor\n(0.1 ~ 10.0)',
                                             minvalue=0.1, maxvalue=10.0)
        if scale_factor:
            self.scale = scale_factor
            new_size = (int(self.original_image.width * scale_factor), int(self.original_image.height * scale_factor))
            resized_image = self.original_image.resize(new_size, Image.Resampling.LANCZOS)
            self.display_image(resized_image)

    def click_event(self, event):
        if self.original_image is None:
            return
        original_x, original_y = int(event.x / self.scale), int(event.y / self.scale)
        self.coords_label.config(text=f'{self.coords_label_text}{original_x}, {original_y}')
        self.clear_cross()

        # Draw cross when clicked
        cross_size = 10
        horizontal = self.canvas.create_line(event.x - cross_size, event.y, event.x + cross_size, event.y, fill='red')
        vertical = self.canvas.create_line(event.x, event.y - cross_size, event.x, event.y + cross_size, fill='red')
        self.current_cross.extend([horizontal, vertical])

    def clear_cross(self):
        for line in self.current_cross:
            self.canvas.delete(line)
        self.current_cross.clear()


def main():
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
