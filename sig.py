import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import os
import cv2
from skimage.metrics import structural_similarity as ssim
import sys

# Match Threshold
THRESHOLD = 85

def browsefunc(ent):
    filename = askopenfilename(filetypes=[
        ("image", ".jpeg"),
        ("image", ".png"),
        ("image", ".jpg"),
    ])
    ent.delete(0, tk.END)
    ent.insert(tk.END, filename)

def capture_image_from_cam_into_temp(sign=1):
    cam = cv2.VideoCapture(0)

    cv2.namedWindow("test")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to grab frame")
            break
        cv2.imshow("test", frame)

        k = cv2.waitKey(1)
        if k % 256 == 27:
            print("Escape hit, closing...")
            break
        elif k % 256 == 32:
            if not os.path.isdir('temp'):
                os.mkdir('temp', mode=0o777)
            if sign == 1:
                img_name = os.path.join("temp", "test_img1.png")
            else:
                img_name = os.path.join("temp", "test_img2.png")
            cv2.imwrite(img_name, frame)
            print(f"{img_name} written!")
            break

    cam.release()
    cv2.destroyAllWindows()
    return True

def captureImage(ent, sign=1):
    res = messagebox.askquestion(
        'Click Picture', 'Press Space Bar to click picture and ESC to exit')
    if res == 'yes':
        capture_image_from_cam_into_temp(sign=sign)
        if sign == 1:
            filename = os.path.join(os.getcwd(), 'temp', 'test_img1.png')
        else:
            filename = os.path.join(os.getcwd(), 'temp', 'test_img2.png')
        ent.delete(0, tk.END)
        ent.insert(tk.END, filename)
    return True

def checkSimilarity(window, path1, path2):
    result = match(path1=path1, path2=path2)
    if result <= THRESHOLD:
        messagebox.showerror("Failure: Signatures Do Not Match",
                             f"Signatures are {result} % similar!!")
    else:
        messagebox.showinfo("Success: Signatures Match",
                            f"Signatures are {result} % similar!!")
    return True

def match(path1, path2):
    img1 = cv2.imread(path1, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(path2, cv2.IMREAD_GRAYSCALE)
    img1 = cv2.resize(img1, (300, 300))
    img2 = cv2.resize(img2, (300, 300))
    similarity_value = "{:.2f}".format(ssim(img1, img2) * 100)
    return float(similarity_value)

def create_gui():
    root = tk.Tk()
    root.title("Signature Matching")
    root.geometry("500x500")

    img1_message = tk.Label(root, text="Signature 1")
    img1_message.grid(row=0, column=0)

    image1_path_entry = tk.Entry(root)
    image1_path_entry.grid(row=0, column=1)

    img1_capture_button = tk.Button(root, text="Capture",
                                    command=lambda: captureImage(ent=image1_path_entry, sign=1))
    img1_capture_button.grid(row=0, column=2)

    img1_browse_button = tk.Button(root, text="Browse",
                                   command=lambda: browsefunc(ent=image1_path_entry))
    img1_browse_button.grid(row=0, column=3)

    img2_message = tk.Label(root, text="Signature 2")
    img2_message.grid(row=1, column=0)

    image2_path_entry = tk.Entry(root)
    image2_path_entry.grid(row=1, column=1)

    img2_capture_button = tk.Button(root, text="Capture",
                                    command=lambda: captureImage(ent=image2_path_entry, sign=2))
    img2_capture_button.grid(row=1, column=2)

    img2_browse_button = tk.Button(root, text="Browse",
                                   command=lambda: browsefunc(ent=image2_path_entry))
    img2_browse_button.grid(row=1, column=3)

    compare_button = tk.Button(root, text="Compare",
                               command=lambda: checkSimilarity(window=root,
                                                               path1=image1_path_entry.get(),
                                                               path2=image2_path_entry.get()))
    compare_button.grid(row=2, column=1)

    root.mainloop()

if __name__ == "__main__":
    if 'nogui' in sys.argv:
        # Test mode without GUI
        path1 = os.path.join(os.getcwd(), 'temp', 'test_img1.png')
        path2 = os.path.join(os.getcwd(), 'temp', 'test_img2.png')
        if os.path.exists(path1) and os.path.exists(path2):
            result = match(path1, path2)
            print(f"Signatures are {result} % similar!!")
        else:
            print("Test images not found. Make sure to capture the images first.")
    else:
        create_gui()
