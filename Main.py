from FunWriteROI import *

filepath= '.\\'

roi_1 = RectRoi(223,223,64,64,name='samll')
roi_2 = RectRoi(191,191,128,128,name='medium')
roi_3 = RectRoi(127,127,256,256,name='large')
RoiList = [roi_1,roi_2,roi_3]
WriteRois(RoiList,filepath,'TestROIs')
