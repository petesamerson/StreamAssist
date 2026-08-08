import math
import sys
import tkinter as tk

import sounddevice as sd
import numpy as np

SAMPLE_RATE = 44100
BLOCK_SIZE = 1024

stream = sd.InputStream(
    channels = 1,
    samplerate = SAMPLE_RATE,
    blocksize = BLOCK_SIZE
)

stream.start()

root = tk.Tk()

transparent_color = "magenta"
root.configure(bg=transparent_color)
root.wm_attributes("-transparentcolor", transparent_color)

# root.overrideredirect(True) # Remove window border
root.geometry("500x500")

canvas = tk.Canvas(
    root,
    width = 500,
    height = 500,
    bg=transparent_color,
    highlightthickness=0
)
canvas.pack()

def get_mic_volume():
    data, overflowed = stream.read(1024)

    rms = np.sqrt(np.mean(data.astype(np.float64)**2))

    return rms * 1000

def rgb(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}"
x = 200
y = 200

ball = canvas.create_oval(
    x - 200, y - 200,
    x + 200, y + 200,
    fill="black",
    outline="",
    width=0
)

dots = []
for i in range(50):
    alpha = 1
    color = rgb(255 - i*5, 255,  255)
    dots.append(
        canvas.create_oval(
            x - 8, y - 8,
            x + 8, y + 8,
            fill = color
        )
    )


smoothed_volume = 0
rotation_modifier = 0.00

def animate():
    global smoothed_volume
    global rotation_modifier

    volume = get_mic_volume()
    rotation_modifier = rotation_modifier + 0.1
    if(rotation_modifier > 2*math.pi):
        rotation_modifier = 0

    # Smooth the volume so the ball doesn't jitter
    smoothed_volume = smoothed_volume * 0.8 + volume * 0.2

    radius = 25 + smoothed_volume

    # canvas.coords(
    #     ball,
    #     x - radius,
    #     y - radius,
    #     x + radius,
    #     y + radius
    # )

    if(radius > 200):
        radius = 180
    for i in range(len(dots)):
        rotateX = x + (radius/len(dots))*(i) * math.cos(i + rotation_modifier)
        rotateY = y + (radius/len(dots))*(i) * math.sin(i + rotation_modifier)
        canvas.coords(
            dots[i],
            rotateX - 20,
            rotateY - 20,
            rotateX + 20,
            rotateY + 20,
        )

    root.after(16, animate)  # ~60 FPS

animate()
root.mainloop()

#
# def start_timer():
#     global window
#     timer.timeout.connect(lambda: window.update_rotation_pos())
#     timer.start(8)
#
# def start_animation_ui():
#     global app
#     window.show()
#     start_timer()
#     sys.exit(app.exec())
#
#
# if __name__ == "__main__":
#     start_animation_ui()
