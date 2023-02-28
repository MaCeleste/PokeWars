from tkinter import *
from PIL import ImageTk,Image

root = Tk()
root.title('PokeWars')
root.iconbitmap('icon.png')
root.geometry('1200x900')

# Create frames for cards

pc_frame = LabelFrame(root, bg='white', text = 'PC cards')
pc_frame.grid(column=0, row=0)
player_frame =LabelFrame(root, bg='white', text = 'Player cards')
player_frame.grid(column=0, row=1)

# Put cards in frames

pc_label = Label(pc_frame, text='')
pc_label.pack()
player_label = Label(player_frame, text='')
player_label.pack()

root.mainloop()