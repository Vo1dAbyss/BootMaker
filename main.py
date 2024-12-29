import colorama
from colorama import Fore, Style
from tkinter import filedialog
import os
import shutil
import subprocess
import zipfile
import time
import cv2
from lib.fprint import fprint

def check_wh(info, video_path):
    capture = cv2.VideoCapture(video_path)
    video_width = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    video_height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

    if video_width == info["width"] and video_height == info["height"]:
        return True
    else:
        return False

def add_part():
    while True:
        part = {}

        fprint("I", " - p - The part will play unless the boot ends")
        fprint("I", " - c - The part will play until it finishes")

        while True:
            p_type = fprint("Q", "What's the part type?", ask=True)
            if p_type == "p" or p_type == "c":
                part["type"] = p_type
                break
            else:
                fprint("E", "Invalid type")
        
        while True:
            p_count = fprint("Q", "How many times will the part repeat?", ask=True)
            if p_count.isdigit():
                part["count"] = int(p_count)
                break
            else:
                fprint("E", "Invalid amount")
            
        while True:
            p_pause = fprint("Q", "How many frames will play after the part ends?", ask=True)
            if p_pause.isdigit():
                part["pause"] = int(p_pause)
                break
            else:
                fprint("E", "Invalid amount")
        
        fprint("I", "Select the video that will play in this part")
        part["path"] = filedialog.askopenfilename(title="Select a video file")

        if check_wh(info, part["path"]) == False:
            fprint("E", "The selected video has different dimensions than the animation")
        else:
            break

    return part

def zip_animation(source_dir):
    zipfile_name = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=[("Zip File", "*.zip")])
    fprint("I", f"Making zip at {zipfile_name}...")

    with zipfile.ZipFile(zipfile_name, mode="w", compression=zipfile.ZIP_DEFLATED) as zip_file:
        for root, _, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, source_dir)
                
                zip_file.write(filename=file_path, arcname=relative_path)
                fprint("S", f"Added {relative_path}", end="")
                print("\r", end="")
    
    print("")

def process_animation(info, parts):
    tmp_dir = os.path.join(os.getcwd(), "tmp")

    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)

    os.mkdir(tmp_dir)
    fprint("S", "Made tmp dir")

    for i, part in enumerate(parts):
        part_dir = os.path.join(tmp_dir, f"part{i}")
        os.mkdir(part_dir)
        fprint("S", f"Made part{i} dir")

        fprint("I", f"Decoding {part['path']} to frames...")

        cmd = f"ffmpeg -i {part['path']} {os.path.join(part_dir, "%04d.png")}"
        status, _ = subprocess.getstatusoutput(cmd)
        
        if status == 0:
            fprint("S", f"Decoded {part['path']} to frames")
        else:
            fprint("E", f"An error occurred decoding {part['path']} to frames with code {status}")
            break

    fprint("I", f"Making desc.txt...")
    with open(os.path.join(tmp_dir, "desc.txt"), "w") as f:
        lines = []
        lines.append(f"{info['width']} {info['height']} {info['fps']}\n")

        print("")
        fprint("S", f"Added animation info:")
        print(f" - WIDTH: {info['width']}")
        print(f" - HEIGHT: {info['height']}")
        print(f" - FPS: {info['fps']}")

        for i, part in enumerate(parts):
            lines.append(f"{part['type']} {part['count']} {part['pause']} part{i}\n")

            print("")
            fprint("S", f"Added part{i} info:")
            print(f" - TYPE: {part['type']}")
            print(f" - COUNT: {part['count']}")
            print(f" - PAUSE: {part['pause']}")
            print(f" - PATH: {os.path.relpath(f"part{i}", os.getcwd())}")
        
        f.writelines(lines)
        print("")
        fprint("S", "Wrote to desc.txt")
        
    print("")
    fprint("I", "Select the path to save the compressed zip file")
    zip_animation(tmp_dir)

    shutil.rmtree(tmp_dir)

info = {}
anim_parts = []

def main():
    fprint("S", "Welcome to BootMaker!")
    fprint("W", "App made by @vo1d_s")
    print("")

    fprint("I", "The dimensions should be formatted as WIDTHxHEIGHT")
    while True:
        dimensions = fprint("Q", "What's the animation dimensions?", ask=True)
        try:
            info["width"] = int(dimensions.split("x")[0])
            info["height"] = int(dimensions.split("x")[1])

            break
        except:
            fprint("E", "Invalid dimensions")

    while True:
        fps = fprint("Q", "How many FPS does the animation have?", ask=True)
        if fps.isdigit():
            info["fps"] = int(fps)
            break
        else:
            fprint("E", "Invalid FPS")

    while True:
        print("")
        anim_parts.append(add_part())
        print("")
        if not fprint("Q", "Do you want to add another part? [y/other]", ask=True).lower() == "y":
            break
    
    print("")
    process_animation(info, anim_parts)

    print("")
    fprint("S", "Done! The program will exit in 5s")
    time.sleep(5)
    exit(0)

if __name__ == "__main__":
    main()