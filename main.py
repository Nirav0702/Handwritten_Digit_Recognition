import cv2
from PIL import ImageGrab, Image
import numpy as np
from PIL import ImageTk, Image, ImageDraw
import PIL
import tkinter as tk
from tkinter import ttk
from tkinter import Tk,Button,Canvas
from keras.models import load_model
import win32gui
import tensorflow as tf

classes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
model = load_model('E:/trained_model.h5')
probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])

gui = Tk()
gui.title("Digit Recognizer")
gui.geometry("600x550")

def clear_cnvs():
    cnvs1.delete("all")
    cnvs2.create_rectangle(55, 410, 85, 440, outline="white", fill="white")
    for i in range(10):
        y_text=50+(35*i)
        cnvs2.create_rectangle(90, y_text - 10, 190, y_text + 5, outline="black", fill='white')


def predict_digit(img):
    img = img.resize((28, 28))
    img.save("hey.png", 'png')
    img = cv2.imread("E:\Projects\digit-recognizer\hey.png")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.bitwise_not(img)
    img = img.reshape(1, 28, 28, 1)
    res = probability_model.predict(img)
    print(res)
    return np.argmax(res), max(res)

def initial_output():
    for i in range(10):
        y_text=50+(35*i)
        cnvs2.create_text(70, y_text, text=str(i), fill="black", font=('Helvetica 20'))
        cnvs2.create_rectangle(90, y_text-10, 190, y_text+5, outline="black")

def final_output(digit):
    for i in range(10):
        y_text=50+(35*i)
        cnvs2.create_text(70, y_text, text=str(i), fill="black", font=('Helvetica 20'))
        cnvs2.create_rectangle(90, y_text-10, 190, y_text+5, outline="black")
        if i==digit:
            cnvs2.create_rectangle(90, y_text - 10, 190, y_text + 5, outline="black",fill='blue')
    cnvs2.create_text(70, 425, text=str(digit), fill="black", font=('Helvetica 30 bold'))

def recognize():
    HWND = cnvs1.winfo_id()
    print(HWND)
    rect = win32gui.GetWindowRect(HWND)
    print(rect)
    print(rect[0])
    a, b, c, d = rect
    rect=(a+50,b+50,c,d)
    img = ImageGrab.grab(rect)
    digit, acc = predict_digit(img)
    print()
    print(digit)
    final_output(digit)

def draw_lines(event):
    x = event.x
    y = event.y
    r = 8
    cnvs1.create_oval(x - r, y - r, x + r, y + r, fill='black')

button1 = ttk.Button(gui, text="Clear",command=clear_cnvs)
button1.grid(row=1,column=0)
button2=ttk.Button(gui, text="Recognize", command=recognize)
button2.grid(row=1,column=1)

cnvs2=Canvas(gui, width=300, height=500, bg='white')
cnvs2.grid(row=0, column=1)

cnvs1 = Canvas(gui, width=300, height=400, bg='white')
#cnvs1.bind("<Button-1>", get_x_and_y)
cnvs1.bind("<B1-Motion>", draw_lines)
cnvs1.grid(row=0, column=0)


initial_output()

gui.mainloop()