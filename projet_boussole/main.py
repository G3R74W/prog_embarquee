from sense_hat import SenseHat
import tkinter as tk
from tkinter import ttk
import threading
import time
import math
from multiprocessing import Value
from PIL import Image,ImageTk

def button_about_click():

  """
  This function is called when the button "about" is clicked.
  Shows a pop up window with information about the program.
  @param: None
  return: None
  """
  #creation d'un pop up
  print("clicked")
  # Create a new window (pop-up)
  popup_window = tk.Toplevel(root, borderwidth=2, relief="ridge")
  popup_window.title("About")
  popup_window.geometry("300x100")

  # Add labels to the pop-up window
  popup_label_author = tk.Label(
      popup_window, text="Author : Florent BROTTEL-PATIENCE\n Tobias WENDL")
  popup_label_affiliation = tk.Label(popup_window,
                                     text="Affiliation : Polytech Dijon")
  popup_label_date = tk.Label(popup_window, text="Date : 14-02-2024")
  popup_label_version = tk.Label(popup_window, text="Version : 1.0.2")

  popup_label_author.pack()
  popup_label_affiliation.pack()
  popup_label_date.pack()
  popup_label_version.pack()

# Fonction pour dessiner la boussole
def draw_compass(canvas, angle):
    # Effacer le contenu précédent
    canvas.delete("all")
    # Dessiner le cercle extérieur de la boussole
    canvas.create_oval(50, 50, 250, 250, outline="black", width=2)
    
    # Dessiner les directions
    directions = ["E", "N", "W", "S"]
    for i in range(4):
        x = 150 + 90 * math.cos(math.radians(90*i))
        y = 150 - 90 * math.sin(math.radians(90*i))
        canvas.create_text(x, y, text=directions[i], font=("Helvetica", 16, "bold"))

    adjusted_angle = (angle - 90)%360
    
    # Dessiner l'aiguille de la boussole
    x2 = 150 + 90 * math.cos(math.radians(angle))
    y2 = 150 - 90 * math.sin(math.radians(angle))
    canvas.create_line(150, 150, x2, y2, fill="red", width=3)

# Fonction pour mettre à jour l'angle de la boussole
def update_compass_angle(canvas, angle, root):
    
    draw_compass(canvas, angle)
    #root.after(100, update_compass_angle(canvas, angle, root))  # Appelle la fonction toutes les 100 millisecondes


def interface(shared_value_heading):
    # Create the main application window
    root = tk.Tk()

    # Set the title of the window
    root.title("COMPASS")

    # Set the size of the window
    root.geometry("600x600")

    # Create a button widget
    button = tk.Button(root, text="About", command=button_about_click)
    button.place(x=500, y=10)

    #degres actuels
    label = tk.Label(root, text="{:.2f}".format(shared_value_heading.value))
    label.pack(pady=10)

    # Créer un canevas pour dessiner la boussole
    canvas = tk.Canvas(root, width=300, height=300, bg="white")
    canvas.pack()

    # Initialiser l'angle de la boussole
    angle = 0

    # Dessiner la boussole initiale
    draw_compass(canvas, angle)

    while True:
        with shared_value_heading.get_lock():
            label.config(text="{:.2f}".format(shared_value_heading.value))
            

            # Mettre à jour l'angle de la boussole périodiquement
            update_compass_angle(canvas, int(shared_value_heading.value), root)
            root.update()
            #time.sleep(0.1)


    # Run the Tkinter event loop
    root.mainloop()


def compass(shared_value_heading):

    #variables colors
    letter_color = (25,38,59)

    sense = SenseHat()
    
    while True:
        heading = sense.get_compass()
        with shared_value_heading.get_lock():
            shared_value_heading.value = heading
        if heading < 45 or heading > 315:
            sense.show_letter('N', letter_color)
        elif heading < 135:
            sense.show_letter('E', letter_color)
        elif heading < 225:
            sense.show_letter('S', letter_color)    
        else:
            sense.show_letter('W', letter_color)  
             


shared_value_heading = Value('d', 12.3) #valeur partagee entre les threads 

thread_interface = threading.Thread(target=interface, args=(shared_value_heading,))
thread_compass = threading.Thread(target=compass, args=(shared_value_heading,))

thread_interface.start()
thread_compass.start()

