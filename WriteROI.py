from FunWriteROI import *
#input filepath, roiname, type, parameters

def putShort(offset, v):
    offset = int(offset)
    data[offset:offset+2] = struct.pack('>h',v)

def putFloat(offset, v):
    offset = int(offset)
    data[offset:offset+4] = struct.pack('>f',v)

def putInt(offset, v):
    offset = int(offset)
    data[offset:offset+4] = struct.pack('>i',v)

def putHeader2(hdr2Offset):
    putInt(HEADER2_OFFSET, hdr2Offset)
    putInt(HEADER2_OFFSET+C_POSITION_OFFSET, c_position)
    putInt(HEADER2_OFFSET+Z_POISTION_OFFSET, z_position)
    putInt(HEADER2_OFFSET+T_POSITION_OFFSET, t_position)
    #if overlay label color.....
    #if font.........
    putName(hdr2Offset)
    #if.. put stroke width
    #if... put Roi property size
    #if... put countersize
    #if... put group

def putName(hdr2Offset):
    offset = hdr2Offset + HEADER2_SIZE
    NameLength = len(roiName)
    putInt(hdr2Offset+NAME_OFFSET,offset) # I think offset is equal to hdr2offset+name_offset
    putInt(hdr2Offset+NAME_LENGTH_OFFSET,NameLength)
    for i in range(NameLength):
        print(offset+i*2)
        putShort(offset+i*2,ord(roiName[i]))

filepath= 'C:\\Users\\LTS\\Desktop\\'
roiName = 'one rect-default'
ExpType = 'rect'
para = [69,108,273,335] #top, left, bottom, right

c_position = 0 #channel
z_position = 0 #depth
t_position = 0 #frame


#----------------------------------------------------------------------
HEADER_SIZE = int(64)
HEADER2_SIZE = int(64) #what is it?
VERSION = int(228)

types ={"polygon":0, "rect":1, "oval":2, "line":3, "freeline":4, "polyline":5, "noRoi":6, "freehand":7, "traced":8,
        "angle":9, "point":10}

type = types[ExpType]
options = 0
roiNameSize = len(roiName)*2
#roiProps =
#Get roiPropsSize.....
roiPropsSize = 0
#if roi is composite write another way. See RoiEncoder.java
n=0
floatSize =0
#if roi is PolygonRoi .....it would change floatSize. skip for now
countersSize = 0
#if roi is Point modify the countersSize...

dataSize = HEADER_SIZE + HEADER2_SIZE + n*4 + floatSize + roiNameSize + roiPropsSize + countersSize
data = bytearray(dataSize)
data[0]=73; data[1]=111; data[2]=117; data[3]=116; #"Iout"
putShort(VERSION_OFFSET,VERSION)
data[TYPE_OFFSET] = type
putShort(TOP_OFFSET,para[0])
putShort(LEFT_OFFSET,para[1])
putShort(BOTTOM_OFFSET,para[2])
putShort(RIGHT_OFFSET,para[3])
#if subPixelReslution and type is rect or oval...... put XD, YD,WIDTHD,HEIGHTD,Optionss
#if n>65535 and type is not point..........
#if type is point and n>65535 put SIZE, N_Coordinates
#put Position. I haven't knew the position means in the roi yet.
#if tpye is Rectangle check the Arc size and put arcSize
#if roi is type of line put x1,y1,x2,y2. And if roi is arrow put subtype arrow, options, arrow style and arrow head size.
#if roi is type of Point roi, put point type and stroke width
#if roi is type of Rotate Rectangle or Ellipse, put Subtype, x1,y1,x2,y2, float_param
#if version> 218.......
#if n equal to zero and roi is type of textRoi..........
#if n equal to zero and roi is type of ImageROI.........
hdr2Offset= HEADER_SIZE+n*4+floatSize    #for those are not textROI and ImageROI
putHeader2(hdr2Offset)
#if n lager than 0,........
#Save overlay options

fout = open(filepath+'test.roi','wb')
fout.write(data)
fout.close()


print(dataSize)







