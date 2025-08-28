import tkinter as tk
from PIL import Image, ImageTk
import numpy as np

def show_static_window(width=1280, height=720, refresh_ms=10, random_path='/dev/random', colorful=True):
	root = tk.Tk()
	root.title('TV Static')
	root.resizable(False, False)
	canvas = tk.Canvas(root, width=width, height=height)
	canvas.pack()

	img_label = tk.Label(root)
	img_label.pack()

	def update_image():
		try:
			if colorful:
				# Pro barevnou statiku načti 3x více dat (RGB)
				with open(random_path, 'rb') as f:
					data = f.read(width * height * 3)
				arr = np.frombuffer(data, dtype=np.uint8)
				if arr.size < width * height * 3:
					arr = np.pad(arr, (0, width * height * 3 - arr.size), 'constant', constant_values=0)
				arr = arr.reshape((height, width, 3))
				img = Image.fromarray(arr, mode='RGB')
			else:
				with open(random_path, 'rb') as f:
					data = f.read(width * height)
				arr = np.frombuffer(data, dtype=np.uint8)
				if arr.size < width * height:
					arr = np.pad(arr, (0, width * height - arr.size), 'constant', constant_values=0)
				arr = arr.reshape((height, width))
				img = Image.fromarray(arr, mode='L')
			tk_img = ImageTk.PhotoImage(img)
			canvas.create_image(0, 0, anchor='nw', image=tk_img)
			canvas.image = tk_img
		except Exception as e:
			canvas.create_text(width//2, height//2, text=str(e), fill='red')
		root.after(refresh_ms, update_image)

	update_image()
	root.mainloop()

show_static_window()