#!/usr/bin/env python

import os
import re
import time
import shutil
from Tkinter import *
from tkFileDialog import askopenfilename
from PIL import Image
import urllib

def collectdata(futronic_file, shiptype, aistype, aissn):
    name=""
    MMSI=""
    IMO=""
    csign=""
    lat=""
    latd=""
    lon=""
    lond=""
    heading=""
    cog=""
    sog=""
    rot=""
    pf=""
    pr=""
    vswr=""
    ais1freq=""
    ais2freq=""
    gpsa = ""
    gpsb = ""
    gpsc = ""
    gpsd = ""
    fut1msg = ""
    fut2msg = ""
    with open(futronic_file) as f:
        for line in f:
            m = re.search("Name:\s*([^@]*)", line) #Name
            if(m):
                if(m.group(1)):
                    name=m.group(1)
            m = re.search("MMSI:\s*(\d{9})", line) #MMSI
            if(m):
                if(m.group(1)):
                    MMSI=m.group(1)
            m = re.search("IMO:\s*(\d{7})", line) #IMO
            if(m):
                if(m.group(1)):
                    IMO=m.group(1)
            m = re.search("C\.SIGN:\s*(.*)\s*IMO", line) #Call Sign
            if(m):
                if(m.group(1)):
                    csign=m.group(1)
                    csign=csign.replace('@','')
            m = re.search("Position:\s*(\S*)\s*(\w)\s*(\S*)\s*(\w)", line) #Position
            if(m):
                if(m.group(1) and m.group(2) and m.group(3) and m.group(4)):
                    lat=m.group(1)
                    latd=m.group(2)
                    ddlat = float(lat.split('d')[0]) + (float(lat.split('d')[1])/60)
                    if latd == 'S':
                        ddlat = -ddlat
                    lon=m.group(3)
                    lond=m.group(4)
                    ddlon = float(lon.split('d')[0]) + (float(lon.split('d')[1])/60)
                    if lond == 'W':
                        ddlon = -ddlon
            m = re.search("True Heading:\s*(\d*)", line) #Heading
            if(m):
                if(m.group(1)):
                    heading=m.group(1)
            m = re.search("COG:\s*(\d*)", line) #COG
            if(m):
                if(m.group(1)):
                    cog=m.group(1)
            m = re.search("SOG:\s*(\d\S*)", line) #SOG
            if(m):
                if(m.group(1)):
                    sog=m.group(1)

            m = re.search("ROT:\s*(\d*)", line) #ROT
            if(m):
                if(m.group(1)):
                    rot=m.group(1)
            m = re.search("Fwd\.:\s*(\S*)", line) #Watt Forward
            if(m):
                if(m.group(1)):
                    pf=m.group(1)
            m = re.search("Rev\.:\s*(\S*)", line) #Watt Reflected
            if(m):
                if(m.group(1)):
                    pr=m.group(1)
            m = re.search("VSWR:\s*(\S*)", line) #VSWR
            if(m):
                if(m.group(1)):
                    vswr=m.group(1)
            m = re.search("AIS1 Freq\.:\s*(\S*)", line) #AIS channel 1 freq
            if(m):
                if(m.group(1)):
                    ais1freq=m.group(1)
                    ais1freq=ais1freq.replace(",","")
                    ais1freq=ais1freq.replace(".",",")
            m = re.search("AIS2 Freq\.:\s*(\S*)", line) #AIS channel 2 freq
            if(m):
                if(m.group(1)):
                    ais2freq=m.group(1)
                    ais2freq=ais2freq.replace(",","")
                    ais2freq=ais2freq.replace(".",",")
            m = re.search("ship:\s*A:\s*(\d*)m\s*B:\s*(\d*)m\s*C:\s*(\d*)m\s*D:\s*(\d*)m", line) #GPS antenna position
            if(m):
                if(m.group(1)):
                    gpsa=m.group(1)
                    gpsb=m.group(2)
                    gpsc=m.group(3)
                    gpsd=m.group(4)
            m = re.search("(Measurement made by Futronic.*)", line) #Futronic message #1 
            if(m):
                if(m.group(1)):
                    fut1msg=m.group(1)
            m = re.search("(Control measurement on.*)", line) #Futronic message #2 
            if(m):
                if(m.group(1)):
                    fut2msg=m.group(1)
    f.close()
    
    filnavn = time.strftime("%Y%m%d_")+name.replace(' ','_')+".tex"
    if(name != "N/A"):
        shutil.copyfile("futronic_ais", filnavn)

    gpsa = float(gpsa)
    gpsb = float(gpsb)
    gpsc = float(gpsc)
    gpsd = float(gpsd)

    if gpsc>0 or gpsd>0:
        gpsx = gpsc/(gpsc+gpsd)*2
    else:
        gpsx = 0
    if gpsa>0 or gpsb>0:
        gpsy = gpsb/(gpsb+gpsa)*4
    else:
        gpsy = 0

    gpsxc = float(gpsx) + 0.1
    gpsyc = float(gpsy) - 0.1

    gpsay = float(gpsy) + 1 
    gpsby = float(gpsy) - 1 
    gpscx = float(gpsx) - 1
    gpsdx = float(gpsx) + 1

    lat = lat.replace("d", "$^{\circ}$")
    lon = lon.replace("d", "$^{\circ}$")

    img = open(filnavn[:-3]+"jpg", "wb")
    img.write(urllib.urlopen('http://maps.googleapis.com/maps/api/staticmap?center='+str(ddlat)+','+str(ddlon)+'&zoom=14&size=400x300&sensor=false').read())
    img.close()
    Image.open(filnavn[:-3]+"jpg").save(filnavn[:-3]+"png")
    imgbg = Image.open(filnavn[:-3]+"png")
    imgbg = imgbg.convert('RGBA')
    imgfg = Image.open("baatsymbol.png")
    if heading == "N/A":
        imgbg.paste(imgfg, (193, 160), mask=imgfg)
    else:
        imgfg = imgfg.rotate(360 - int(heading))
        imgbg.paste(imgfg, (193, 160), mask=imgfg)
    imgbg.save(filnavn[:-3]+"png")

    newlines = []

    t = open("futronic_ais", "r")
    for line in t:
        line=line.replace("VnameV", name)
        line=line.replace("VmmsiV", MMSI)
        line=line.replace("VimoV", IMO)
        line=line.replace("VcsignV", csign)
        line=line.replace("VshiptypeV", shiptype)
        line=line.replace("VaistypeV", aistype)
        line=line.replace("VaissnV", aissn)
        line=line.replace("VlatV", lat)
        line=line.replace("VlonV", lon)
        line=line.replace("VlatdV", latd)
        line=line.replace("VlondV", lond)
        line=line.replace("VheadingV", heading)
        line=line.replace("VcogV", cog)
        line=line.replace("VsogV", sog)
        line=line.replace("VrotV", rot)
        line=line.replace("VpfV", pf)
        line=line.replace("VprV", pr)
        line=line.replace("VvswrV", vswr)
        line=line.replace("Vais1freqV", ais1freq)
        line=line.replace("Vais2freqV", ais2freq)
        line=line.replace("VgpsxV", str(gpsx))
        line=line.replace("VgpsyV", str(gpsy))
        line=line.replace("VgpsxcV", str(gpsxc))
        line=line.replace("VgpsycV", str(gpsyc))
        line=line.replace("VgpsayV", str(gpsay))
        line=line.replace("VgpsbyV", str(gpsby))
        line=line.replace("VgpscxV", str(gpscx))
        line=line.replace("VgpsdxV", str(gpsdx))
        line=line.replace("VgpsaV", str(gpsa))
        line=line.replace("VgpsbV", str(gpsb))
        line=line.replace("VgpscV", str(gpsc))
        line=line.replace("VgpsdV", str(gpsd))
        line=line.replace("Vfut1msgV", fut1msg)
        line=line.replace("Vfut2msgV", fut2msg)
        line=line.replace("VmapV", filnavn[:-3]+"png")
        newlines.append(line)
    t.close()
    o = open(filnavn, "w")
    o.writelines(newlines)
    o.close()
    os.system("pdflatex " + filnavn)
    os.system("evince " + filnavn[:-3] + "pdf")
    os.rename(filnavn, os.path.join('tex', filnavn))
    os.rename(filnavn[:-3]+"pdf", os.path.join('pdf',filnavn[:-3]+"pdf"))
    os.rename(filnavn[:-3]+"png", os.path.join('img',filnavn[:-3]+"png"))
    if os.path.exists(filnavn[:-3] + "log"):
        os.remove(filnavn[:-3] + "log")
    if os.path.exists(filnavn[:-3] + "aux"):
        os.remove(filnavn[:-3] + "aux")
    if os.path.exists(filnavn[:-3] + "jpg"):
        os.remove(filnavn[:-3] + "jpg")

top = Tk()
top.minsize(width=300, height=110)
top.title("Futronic")

filelabel = Label(top, text="Ingen fil")
filelabel.grid(row=4, column=1, sticky="w")

def opendatafile():
    global datafilename
    datafilename = askopenfilename()
    filelabel["text"] = os.path.basename(datafilename)
    reportbutton.config(state='normal')

datafilebutton = Button(top, text="Velg loggfil", command=opendatafile)
datafilebutton.grid(row=4, column=0)

shiptypes= [
    "20 Wing in ground",
    #"21 Wing in ground (WIG), Hazardous catagory A",
    #"22 Wing in ground (WIG), Hazardous catagory B",
    #"23 Wing in ground (WIG), Hazardous catagory C",
    #"24 Wing in ground (WIG), Hazardous catagory D",
    #"25 Wing in ground (WIG), Reserved for future use",
    #"26 Wing in ground (WIG), Reserved for future use",
    #"27 Wing in ground (WIG), Reserved for future use",
    #"28 Wing in ground (WIG), Reserved for future use",
    #"29 Wing in ground (WIG), No additional information",
    "30 Fishing",
    "31 Towing",
    #"32 towing length exceeds 200m or breadth exceeds 25m",
    "33 Dredging",
    "34 Diving ops",
    "35 Military ops",
    "36 Sailing",
    "37 Pleasure craft",
    #"38 reserved",
    #"39 reserved",
    "40 High speed craft",
    #"41 High speed craft (HSC), Hazardous catagory A",
    #"42 High speed craft (HSC), Hazardous catagory B",
    #"43 High speed craft (HSC), Hazardous catagory C",
    #"44 High speed craft (HSC), Hazardous catagory D",
    #"45 High speed craft (HSC), Reserved for future use",
    #"46 High speed craft (HSC), Reserved for future use",
    #"47 High speed craft (HSC), Reserved for future use",
    #"48 High speed craft (HSC), Reserved for future use",
    #"49 High speed craft (HSC), No additional information",
    "50 Pilot vessel",
    "51 Search and rescue",
    "52 Tug",
    "53 Port tender",
    "54 Anti-polution equipment",
    "55 Law enforcement",
    "56 Spare - local vessel",
    "57 Spare - local vessel",
    "58 Medical transport",
    "59 Ship according to RR Resolution No. 18",
    "60 Passenger",
    #"61 passenger, Hazardous catagory A",
    #"62 passenger, Hazardous catagory B",
    #"63 passenger, Hazardous catagory C",
    #"64 passenger, Hazardous catagory D",
    #"65 passenger, Reserved for future use",
    #"66 passenger, Reserved for future use",
    #"67 passenger, Reserved for future use",
    #"68 passenger, Reserved for future use",
    #"69 passenger, No additional information",
    "70 Cargo",
    #"71 cargo, Hazardous catagory A",
    #"72 cargo, Hazardous catagory B",
    #"73 cargo, Hazardous catagory C",
    #"74 cargo, Hazardous catagory D",
    #"75 cargo, Reserved for future use",
    #"76 cargo, Reserved for future use",
    #"77 cargo, Reserved for future use",
    #"78 cargo, Reserved for future use",
    #"79 cargo, No additional information",
    "80 Tanker",
    #"81 tanker, Hazardous catagory A",
    #"82 tanker, Hazardous catagory B",
    #"83 tanker, Hazardous catagory C",
    #"84 tanker, Hazardous catagory D",
    #"85 tanker, Reserved for future use",
    #"86 tanker, Reserved for future use",
    #"87 tanker, Reserved for future use",
    #"88 tanker, Reserved for future use",
    #"89 tanker, No additional information",
    "90 Other type",
    #"91 other type, Hazardous catagory A",
    #"92 other type, Hazardous catagory B",
    #"93 other type, Hazardous catagory C",
    #"94 other type, Hazardous catagory D",
    #"95 other type, Reserved for future use",
    #"96 other type, Reserved for future use",
    #"97 other type, Reserved for future use",
    #"98 other type, Reserved for future use",
    #"99 other type, No additional information",
]
shiptypelabel = Label(top, text="Shiptype")
shiptypelabel.grid(row=1, column=0)
choosenshiptype = StringVar()
choosenshiptype.set(shiptypes[0])
shiptype = OptionMenu(top, choosenshiptype, *shiptypes)
shiptype.grid(row=1, column=1, sticky="w")

aistypelabel = Label(top, text="Ais-type")
aistypelabel.grid(row=2, column=0)
aistype = Entry(top)
aistype.grid(row=2, column=1, sticky="w")

aissnlabel = Label(top, text="Serienummer")
aissnlabel.grid(row=3, column=0)
aissn = Entry(top)
aissn.grid(row=3, column=1, sticky="w")

def createreport():
    global datafilename 
    collectdata(datafilename, str(choosenshiptype.get()), str(aistype.get()), str(aissn.get()))
reportbutton = Button(top, text="Lag rapport", command=createreport)
reportbutton.config(state='disabled')
reportbutton.grid(row=5, column=1, sticky="w")

top.mainloop()


