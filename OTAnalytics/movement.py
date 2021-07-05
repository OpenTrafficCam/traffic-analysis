from tkinter import filedialog, Toplevel
import tkinter as tk
from tkinter.constants import ANCHOR, END
import json
    
def new_movement(ListboxMovement, movement_dict):
    """creates new movement and adds it to the movement listbox
    """
    new_movement_creation = Toplevel()

    new_movement_creation.title("Create new movement")
    movement_name_entry = tk.Entry(new_movement_creation, textvariable="Movement")
    movement_name_entry.grid(row=1, column=0, sticky="w",pady=10, padx=10)
    movement_name_entry.delete(0, END)
    add_movement = tk.Button(new_movement_creation,text="Add movement", command = lambda: recieve_movement_name(movement_name_entry,ListboxMovement, movement_dict, new_movement_creation ))
    add_movement.grid( row=1, column=1, sticky="w", pady=10, padx=10)   
    new_movement_creation.protocol("WM_DELETE_WINDOW")

def recieve_movement_name(movement_name_entry ,ListboxMovement, movement_dict, new_movement_creation):
    movement_name = movement_name_entry.get()
    ListboxMovement.insert(0,movement_name)
    movement_dict[movement_name] = {}

    new_movement_creation.destroy()

def save_movements(movement_dict):
    files = [('Files', '*.OTMov')]
    file = filedialog.asksaveasfile(filetypes = files, defaultextension = files)

    a_file = open(file.name, "w")


    json.dump(movement_dict, a_file)

    a_file.close()


def load_movements(movement_dict, ListboxMovement, linedetectors, ListboxDetector):
    filepath = filedialog.askopenfile(filetypes=[("Detectors", '*.OTMov')])   
    files = open(filepath.name, "r")
    files = files.read()

    loaded_movement_dict = json.loads(files)

    movement_dict.update(loaded_movement_dict)

    #insert listbox with movements
    for movement in movement_dict:

        ListboxMovement.insert(0,movement)
                        
        for detector in movement_dict[movement]:
            if movement_dict[movement][detector]["type"] == "line":
                linedetectors.update(movement_dict[movement])
                ListboxDetector.insert(0, detector)

           # else: polygondetectors.update(movement_dict[movement])

    # resets polypoints list or else creation of new polygon leads to bug
    polypoints = []

def add_to_movement(Listbox, ListboxMovement, linedetectors, polygondetectors, movement_dict, Listbox4):
    """when movement is highlighted in the listbox, it is possible
        to add detectors and sections to the selected movement
    """

    detector_selection = Listbox.curselection()
    detector_name = Listbox.get(detector_selection[0])

    movement_selection = ListboxMovement.curselection()
    movement_name = ListboxMovement.get(movement_selection[0])

    if detector_name in linedetectors:

        movement_dict[movement_name].update({detector_name : linedetectors[detector_name]})

    else:
        movement_dict[movement_name].update({detector_name : polygondetectors[detector_name]})

    #self.movement_dict[self.movement_name].append(detector_name)

    Listbox4.insert(0, detector_name)


def curselected_movement(event, Listbox4,ListboxMovement, movement_dict):
    #shows detectors and sections belonging to selected movement         

    Listbox4.delete(0,'end')

    movement_selection = ListboxMovement.curselection()
    movement_name = ListboxMovement.get(movement_selection[0])

    for detector_name in movement_dict[movement_name]:
        Listbox4.insert(0, detector_name)