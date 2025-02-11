import dxcam
import tkinter as tk
import pyvirtualcam as pvc
import cv2
import numpy as np
import re

# This application is intended to capture a windowed portion of the monitor and direct into a camera source.
# Currently only intended for windows
# Requires OBS Virtual Cam plugin

# configuration
fps = 10
show_border = True

# output stream
# cap = cv2.VideoCapture(0)
# if not cap.isOpened():
#     print("Cannot open camera")
#     exit()
#print(cap.getBackendName())

# screencapture / input
camera = dxcam.create(output_idx=0)
print(dxcam.output_info())

# init transparent window
root = tk.Tk()
root.geometry('640x360')

tk_frame = tk.Frame(root)
if show_border:
    tk_frame['highlightbackground'] = 'red'
    tk_frame['highlightthickness'] = 5
tk_frame.pack(fill=tk.BOTH, expand=True)
tk_frame['bg'] = 'white'

# stay on top
root.wm_attributes("-topmost", True)
# renders white as transparent i think?
root.wm_attributes("-transparentcolor", "white")

# start capturing
#camera.start(target_fps=fps, )


def loop(cam: pvc.Camera):
    # ensure that dimension info is resolved
    root.update_idletasks()
    # 'WxH+X+Y'
    dim = [int(i) for i in re.split(r'[x+]', root.winfo_geometry())]
    dim[2:3] = (root.winfo_rootx(), root.winfo_rooty()) # adjust for actual position
    region = (dim[2], dim[3], dim[2]+dim[0], dim[3]+dim[1])
    print("{}".format(region,), end='\r')
    #print("{} {}".format(cam.height, cam.width))
    
    frame = None
    try:
        frame = camera.grab(region=region)
    except ValueError:
        # TODO: fill in with solid color instead?
        print("Image going out of bounds!")

    # when check if frame changed
    if not frame is None:
        cam.send(cv2.resize( frame, (cam.width, cam.height) ))
    
    # queue the next iteration
    root.after(int(1000/fps), loop, cam)

with pvc.Camera(width=1280,height=720,fps=20) as cam:
    root.after(int(1000/fps), loop, cam)
    root.mainloop()

camera.release()
#cap.release()