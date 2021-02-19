import xml.etree.ElementTree as ET
from coordinates.Coordinates import TCoordinate
from traces.Trace import TTrace
from trace_groups.TraceGroups import TTraceGroup
from pathlib import Path
import os
import gc

class ParsingInkml:
    def __init__(self, inkml_dir, img_dir, thickness=10):
        # inkml_dir: direction to folder containing the inkml files
        # img_dir: direction to folder containing the saved images
        # thickness: thickness of line while drawing letter
        
        inkml_dir = Path(inkml_dir)
        self.inkml_files = list(inkml_dir.glob("*.inkml"))

        self.img_dir = img_dir
        self.thickness = thickness
    
    def parsing(self, inkml_file, img_name):
        tree = ET.parse(inkml_file)
        root = tree.getroot()

        traceGroups = []
        # gathering traceGroup elements
        for traceGroup in root.findall("traceGroup"):
            traceGroups.append(traceGroup)
        
        for traceGroup in traceGroups:
            traces = []
            for trace in traceGroup.findall("trace"):
                coordinates = TCoordinate(trace.text)
                trace = TTrace(trace.get("id"), coordinates)
                traces.append(trace)
            truth = traceGroup.find("annotationXML").find("Tg_Truth").text
            TraceGroup = TTraceGroup(traceGroup.get("id"), truth, traces, thickness=self.thickness)
            # saving the image
            TraceGroup.save_image(img_name)
        
        # release the memory
        del traceGroups
        gc.collect()

    def __call__(self):
        numbering = 0
        for inkml_file in self.inkml_files:
            numbering += 1
            img_file = os.path.join(self.img_dir, "{}.png".format(numbering))
            self.parsing(inkml_file, img_file)
        # return total number of parsed images
        return numbering