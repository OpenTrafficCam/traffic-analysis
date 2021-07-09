from gui_dict import *
import json
from tkinter import Listbox, filedialog


def load_tracks(object_dict, ListboxTracks):
    """loads detectors from a .Track-File and converts into displayable format
    """

    filepath = filedialog.askopenfile(filetypes=[("Detectors", '*.ottrk')])   
    files = open(filepath.name, "r")
    files = files.read()

    loaded_dict = json.loads(files)

    detections = {}

    detections.update(loaded_dict["data"])



    for frame in detections:
        for detection in detections[frame]:
            if 'object_'+str(detection) in object_dict.keys():
                object_dict['object_%s' % detection]["Coord"].append([detections[frame][detection]["x"], detections[frame][detection]["y"]])
            else:
                object_dict['object_%s' % detection] = {}
                object_dict['object_%s' % detection]["Coord"] = []
                object_dict['object_%s' % detection]["Class"] = detections[frame][detection]["class"]
                object_dict['object_%s' % detection]["Coord"].append([detections[frame][detection]["x"], detections[frame][detection]["y"]])
    

    for object in list(object_dict.keys()):

        ListboxTracks.insert(0,object)