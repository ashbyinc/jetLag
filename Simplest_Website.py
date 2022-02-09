from flask import Flask, redirect, render_template, request, url_for
import datetime as datetime
import math as mth
global flag
global sRange
flag = 0

def valueexchange(column):
    iter = 0
    arrayop = []
    with open("data/airport.csv", "r", encoding="utf8") as airData:
        for line in airData:
            if iter != 0: 
                workingline = line.split(",")
                arrayop.append(workingline[column].replace('"', ""))
            else:
                pass
            iter += 1
    return(arrayop)

code = (valueexchange(4))
timeZone = (valueexchange(9))
places = (valueexchange(3))

app = Flask(__name__)

# @app.route("/")
# def home():
#     return render_template("main.html")

@app.route("/",  methods=["POST", "GET"])
def form():
    if request.method == "POST":

        global depT, depAir, arvAir, flyLen
        depT = request.form["departing"]
        depAir = (request.form["depAir"]).upper()
        arvAir = (request.form["arvAir"]).upper()
        flyLen = request.form["flyLen"]


        napCal(depT, depAir, arvAir, flyLen)

        if flag == 0:
            fValStar = whydidiwriteacustomfunctionforthis(0)
            fValEnd = whydidiwriteacustomfunctionforthis(1)
            return redirect(url_for("final1", fValStar=fValStar, fValEnd=fValEnd))
        else:
            return redirect(url_for)("final2")

        
        
    else:
        return render_template("form.html")

"""---------------------------------------------------------------"""
#function to convert into utc
def utcConv(local, code):
    return (local+code)

#constants
totalday = [0,4800]

#########################################

#givens
# depT = 1900 #departure time = 7:00 pm
# depAir = "LGA" #departing airport = LaGuardia
# arvAir = "CDG" #arrivial airport = Charles DeGual
# flyLen = 1500 #flight length


#########################################
def napCal(depT, depAir, arvAir, flyLen):

    try:
        depT = int((datetime.datetime.strptime(depT, "%I %p")).strftime("%H"))*100
    except:
        depT = int((datetime.datetime.strptime(depT, "%I%p")).strftime("%H"))*100
    
    depAir = str(depAir)
    arvAir = str(arvAir)
    flyLen = int(flyLen)*100
    #calculated
    depUTCcode = (int(timeZone[code.index(depAir)]))*100
    arvUTCcode = (int(timeZone[code.index(arvAir)]))*100 #these functions search for the airport code, then use its index value to find its respective timezone


     #block of code to calcuate everything

    ##define flight path (fP)
    fP = [0,0]
    #start of fP = dep time in utc
    fP[0] = utcConv(depT, depUTCcode)
    #end of fP = start plus flight time
    fP[1] = fP[0]+flyLen

    ##define night time in destination (sBlue)
    ## roughly 9pm to 7am, can adjust as needed
    night = 2100
    day = 700 + 2400 #2400 to adjust for math on a 48 hr system
    ##conv night and day to utc using destination
    sBlue = [0,0]
    sBlue[0] = utcConv(night, arvUTCcode)
    sBlue[1] = utcConv(day, arvUTCcode)

    ##define don't sleep by adjusting flight path
    fP[1] = fP[1]-20

    ##define what Martin's Gap is: (mG)
    mG = [0,0]
    mG[0] = sBlue[0]
    mG[1] = fP[1]

    ##check if mG is too small e.g under an hour
    if mth.sqrt(mG[0]**2+mG[1]**2) < 100:
        flag = 1
        print("too short")
    elif (mG[0]-mG[1]) > 0:
        flag = 1
        print("too short")
    else: pass
        
    #d
    ##sleep check: must be: within fP, sBlue, and mG
    ## if so, 
    ## works by colapsing the ranges
    
    sRange = [0,0] # sleep range
    ## compare mG and sBlue
    sRange[0] = max(mG[0], sBlue[0]) #unneeded but helps me remember how it works so, >:)
    sRange[1] = min(mG[1], sBlue[1])
    ##compare new range from now on, comparing to fP
    sRange[0] = max(fP[0], sRange[0])
    sRange[1] = min(fP[1], sRange[1])
    ##
    print("srange", sRange)
    return(sRange)


def whydidiwriteacustomfunctionforthis(x):
    dia = ""
    firsthalf = str(napCal(depT, depAir, arvAir, flyLen)[x])

    if len(firsthalf) < 4:
        stSleep = "0" + firsthalf
    else:
        stSleep = int(firsthalf)

    stSleep = (int(firsthalf[0:2]))


    if stSleep > 24:
        stSleep = (stSleep-24)
        dia = "AM"
        if stSleep > 12:
            stSleep = (stSleep-12)
            dia = "PM"
            print("im a lil dirty boy")
    elif stSleep > 12:
        stSleep = (stSleep-12)
        dia = "PM"
    else:
        stSleep = (stSleep)
        dia = "AM"

    min = (int(firsthalf[2:]))
    extrahour = 0
    while (min) >= 60:
        extrahour = extrahour + 1
        min = min - 60

    min = str(min)
    stSleep = str(stSleep + extrahour)
    secondhalf = (str(int(firsthalf[2:])%60))
    if len(secondhalf) == 1:
        min = "0" + str(secondhalf)

    stSleep = stSleep + ":" + min + " " + dia
    return(stSleep)


"""------------------------------------------------------"""



@app.route("/<fValStar>,<fValEnd>")
def final1(fValStar, fValEnd):
    return render_template("final1.html", content=fValStar, content2=fValEnd)

@app.route("/final2")
def final2():
    return render_template("final2.html")



############################
if __name__ == "__main__":
    app.run(debug="True")
############################