from tkinter import *
import requests

def theThing():
    updatetime = 10000

    def getBuses(requestLink): #expects a URL linking to the schedule to display, taken from friend.
        #get bus stop arrival prediction
        request = requests.get(requestLink).json()

        #organise bus destinations
        destinations = {}

        #organise bus arrival info
        stop = {}

        #gets all arriving buses and appends them to a dictionary with expectedArrival as key
        for bus in range(len(request)):
            try:
                if request[bus]["lineName"] not in destinations:
                    destinations[request[bus]["lineName"]] = request[bus]["destinationName"]
            except:
                pass

            try:
                if request[bus]["lineName"] not in stop:
                    stop[request[bus]["lineName"]] = [round(request[bus]["timeToStation"]/60)]
                else:
                    stop[request[bus]["lineName"]].append(round(request[bus]["timeToStation"]/60))
            except:
                pass

        ordered = []
        for key in stop:
            for item in stop[key]:
                ordered.append({'bus': key, 'time': item})
        ordered = sorted(ordered, key=lambda x: x['time'])

        stop = {}
        for item in ordered:
            if item['bus'] not in stop:
                stop[item['bus']] = [item['time']]
            else:
                stop[item['bus']].append(item['time'])

        return stop, destinations

    def wrapthething(): #This forms the structure of the created window
        listy, listy2 = getBuses('https://api.tfl.gov.uk/StopPoint/490009117T/Arrivals')
        listy3, listy4 = getBuses('https://api.tfl.gov.uk/StopPoint/490009117V/Arrivals')
        listofbusses = list(listy.keys())
        listofbusses2= list(listy3.keys())

        TEXTSIZE = 35
        COLUMNSTART = 0
        ROWSTART = 0

        labelheadhead = Label(root,text = "Catford Road/Lewisham Town Hall (T)",font=("Courier", TEXTSIZE))
        labelheadhead.grid(row = ROWSTART,columnspan = 3,column = COLUMNSTART)

        labelheadhead2 = Label(root,text = "\nCatford Road/Lewisham Town Hall (V)",font=("Courier", TEXTSIZE))
        labelheadhead2.grid(row = ROWSTART+10,columnspan = 3,column = COLUMNSTART)

        labelhead = Label(root,text = "Route",anchor = "w", width = 6,font=("Courier", TEXTSIZE))
        labelhead.grid(row= ROWSTART+1, column = COLUMNSTART)

        labelhead2 = Label(root,text = "Destination",anchor = "w", width = 25,font=("Courier", TEXTSIZE))
        labelhead2.grid(row= ROWSTART+1, column = COLUMNSTART+1)

        labelhead3 = Label(root,text = "Time",anchor = "w", width = 5,font=("Courier", TEXTSIZE))
        labelhead3.grid(row= ROWSTART+1, column = COLUMNSTART+2)

        for i in range(len(listy)):
            try:
                busnumber = listofbusses[i]
                duetime = listy[busnumber][0]
                destin = listy2[busnumber]

                if duetime == 0:
                    duetime = "Due"

                if len(destin) > 20: #string to long
                    destin = destin[:20] + "..."

                lbl = Label(root,text = busnumber,anchor = "w", width = 6,font=("Courier", TEXTSIZE))
                lbl.grid(row = i+2+ROWSTART,column = COLUMNSTART)

                lbl2 = Label(root,text = destin,anchor = "w", width = 25,font=("Courier", TEXTSIZE))
                lbl2.grid(row = i+2+ROWSTART,column = COLUMNSTART+1)

                lbl3 = Label(root,text = duetime,anchor = "w", width = 5,font=("Courier", TEXTSIZE))
                lbl3.grid(row = i+2+ROWSTART,column = COLUMNSTART+2)
            except:
                pass

        labelhead21 = Label(root,text = "Route",anchor = "w", width = 6,font=("Courier", TEXTSIZE))
        labelhead21.grid(row= ROWSTART+100, column = COLUMNSTART)

        labelhead22 = Label(root,text = "Destination",anchor = "w", width = 25,font=("Courier", TEXTSIZE))
        labelhead22.grid(row= ROWSTART+100, column = COLUMNSTART+1)

        labelhead23 = Label(root,text = "Time",anchor = "w", width = 5,font=("Courier", TEXTSIZE))
        labelhead23.grid(row= ROWSTART+100, column = COLUMNSTART+2)


        for i in range(len(listy3)):
            busnumber = listofbusses2[i]
            duetime = listy3[busnumber][0]
            destin = listy4[busnumber]

            if duetime == 0:
                duetime = "Due"

            if len(destin) > 20: #string too long
                destin = destin[:20] + "..."

            lbl21 = Label(root,text = busnumber,anchor = "w", width = 6,font=("Courier", TEXTSIZE))
            lbl21.grid(row = i+2+100,column = COLUMNSTART)

            lbl22 = Label(root,text = destin,anchor = "w", width = 25,font=("Courier", TEXTSIZE))
            lbl22.grid(row = i+2+100,column = COLUMNSTART+1)

            lbl32 = Label(root,text = duetime,anchor = "w", width = 5,font=("Courier", TEXTSIZE))
            lbl32.grid(row = i+2+100,column = COLUMNSTART+2)


    #end of function

    root = Tk()



    #makes screen fullscreen, toggles with escape
    #Copied from outside


    class FullScreenApp(object):
        def __init__(self, master, **kwargs):
            self.master=master
            pad=3
            self._geom='1700x900+0+0'
            master.geometry("{0}x{1}+0+0".format(
                master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
            master.bind('<Escape>',self.toggle_geom)
        def toggle_geom(self,event):
            geom=self.master.winfo_geometry()
            print(geom,self._geom)
            self.master.geometry(self._geom)
            self._geom=geom


    app=FullScreenApp(root)
    ###

    def update():
        wrapthething()
        root.after(updatetime,update)

    wrapthething()

    root.after(updatetime,update)
    root.mainloop()


theThing()





