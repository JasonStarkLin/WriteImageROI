import struct
with open("one rect-default.roi","rb") as fin:
    data = fin.read()
size = len(data)
# between 18-33 bytes, it's the parameter to describe the roi. I set it as para (parameter).
keys_1 = ['version','type','top','left','bottom','right','NCoordinates']
keys_2 = ['stroke_width','shape_roi_size','stroke_color','fill_color','subtype','options']
keys_3 = ['arrow_head_size','rounded_rect_arc_size','position','header2_offset']

Roi_check = struct.unpack("4s",data[0:4])

results_1 = struct.unpack(">hBx4hH",data[4:18]) #skip one byte (x) because it did not used.
results_2 = struct.unpack(">h3i2h",data[34:52]) #">" for the alignment
results_3 = struct.unpack(">Bh2i",data[53:64])

#generate header dictionary
head1 = dict(zip(keys_1,results_1))
head2 = dict(zip(keys_2,results_2))
head3 = dict(zip(keys_3,results_3))
header = {}
for i in [head1,head2,head3]:
    header.update(i)


#Options
options = {"SPLINE_FIT":1, "DOUBLE_HEADED":2, "OUTLINE":4, "OVERLAY_LABELS":8, "OVERLAY_NAMES":16,
           "OVERLAY_BACKGROUPNDS":32, "OVERLAY_BOLD":64, "SUB_PIXEL_RESOLUTION":128, "DRAW_OFFSET":256,
           "ZERO_TRANSPARENT":512, "SHOW_LABELS":1024,"SCALE_LABELS":2048, "PROMPT_BEFORE_DELETING":4098,
           "SCALE_STROKE_WIDTH":8192}
#types
types ={"polygon":0, "rect":1, "oval":2, "line":3, "freeline":4, "polyline":5, "noRoi":6, "freehand":7, "traced":8,
        "angle":9, "point":10}

channel = int(0); slice=int(0); frame=int(0)
overlayLabelColor=int(0); overlayFontSize=int(0)
group = int(0)
imageOpacity=int(0); imageSize=int(0)
subPixelResolution =((header["options"] & options["SUB_PIXEL_RESOLUTION"]) !=0) and (header["version"]>=228) #those !=0 seems to be ignorable.
drawOffset = subPixelResolution and ((header["options"]&options["DRAW_OFFSET"])!=0)
scaleStrokeWidth = True
if(header["version"]>=228):
    scaleStrokeWidth = (header["options"] & options["SCALE_STROKE_WIDTH"]) !=0 #those !=0 seems to be ignorable.
subPixelRect = header["version"]>=223 and subPixelResolution and (header["type"]==types["rect"] or header["type"]==types["oval"])
xd = float(0); yd=float(0); width=float(0); heightd=float(0)
keys_4 = ["xD","yD","widthD","heightD"]
if(subPixelRect):
    results_4 = struct.unpack(">4f",data[18:34])
    head4 = dict(zip(keys_4, results_4))
    header.update(head4)
keys_5 = ["channel","slice","frame","nameOffset","nameLength","overlayLabelColor","overlayFontSize","group","imageOpacity",
          "imageSize","strokeWidthD","roiPropsOffset","roiPropsLength","counters"]
if(header["header2_offset"]>0 and header["header2_offset"]+32+4<=size): #32 is the IMAGE_SIZE offsets
    results_5 = struct.unpack(">6ih2Bif3i",data[header["header2_offset"]+4:header["header2_offset"]+52])
    head5 = dict(zip(keys_5, results_5))
    header.update(head5)

nameL = header["nameLength"]
nameoffset = header["nameOffset"]
test = struct.unpack(">"+str(nameL)+"h",data[nameoffset:nameoffset+nameL*2])
name=""
for i in range(nameL):
    name +=  chr(test[i])
print("ROI Name: ",name)


print("Program finished")