# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 06:47:29 2021

@author: User
"""
import sqlite3
import random
import itertools
import copy

# all fyp course can check here
def findFYPRoom(courseName,list_items):
    roomid = None
    for i in list_items:
        # if the list can find COMP S451F L01 mean fyp already assign a room 
        if (i[0] == "COMP S451F L01" or i[0] == "COMP S456F L01")\
        and (courseName == "COMP S451F L01" or courseName == "COMP S456F L01"):
            roomid = i[7]
    return roomid

def findFYPTime(courseName,list_items):
    timeslot = None
    for i in list_items:
        # if the list can find COMP S451F L01 mean fyp already assign a room 
        if (i[0] == "COMP S451F L01" or i[0] == "COMP S456F L01")\
        and (courseName == "COMP S451F L01" or courseName == "COMP S456F L01"):
            timeslot = i[8]
    return timeslot

def findProgrammeYear(courseName):
    db = sqlite3.connect('ou.db')
    c = db.cursor()
    c.execute("SELECT programmeid, courseid, year FROM programmeCourse WHERE courseid = ?",(courseName,))
    programmeCourse = c.fetchall()
    c.close()
    temp = []
    for pc in programmeCourse:
        temp.append([pc[0],pc[2]])
    return(temp)

def findSameYear(courseName,avoidList):
    temp = []
    for avoidItem in avoidList:
        db = sqlite3.connect('ou.db')
        c = db.cursor()
        c.execute("SELECT courseid FROM programmeCourse WHERE (programmeid = ? and year = ?)",(avoidItem[0],avoidItem[1]))
        programmeCourse = c.fetchall()
        c.close()
        for pc in programmeCourse:
            if not(pc[0] in temp):
                temp.append(pc[0])
    return temp

def findRoom2Elevator(roomid):
    db = sqlite3.connect('ou.db')
    c = db.cursor()
    c.execute("SELECT roomid,floor,campus,time FROM room WHERE roomid = ?",(roomid,))
    roomInfo = c.fetchall()
    c.close()
    return roomInfo[0]

def earlyLateClassScore(weekdayList):
    slots = ["09 - 11","11 - 13","14 - 16","16 - 18"]
    tempList = []
    indexList = []
    total = 0
    earlyLateClassScore = 5
    for course in weekdayList:
        tempList.append(course[8].split(' ',1)[1])

    for time in tempList:
        for count2, slot in enumerate(slots):
            if time == slot:
                indexList.append(count2)
                break

    indexList.sort()
    #print("indexs:",indexList)
    actualTime = []
    for index in indexList:
        actualTime.append(slots[index])
    
    # count waiting time to sum the score
    if len(actualTime) > 1:
        for index in range(len(actualTime)-1):
            startTime = actualTime[index].split(' - ')[1]
            endTime = actualTime[index+1].split(' - ')[0]
            if int(endTime) - int(startTime) > 0:
                earlyLateClassScore -= int(endTime) - int(startTime)
        #print("total",total)
    #print("In earlyLateClassScore :",earlyLateClassScore)
    total += earlyLateClassScore

    return total

def distanceScore(weekdayList):
    slots = ["09 - 11","11 - 13","14 - 16","16 - 18"]
    roomList = []
    totalTime = 0.0
    score = 5
    maxTranTime = 600
    for course in weekdayList:
        roomList.append((course[7],course[8].split(' ',1)[1]))
    roomList.sort(key=lambda x: x[1])
        #距離
    if len(roomList) > 1:
        #0->1
        #1->2
        #2->3

        for count, room in enumerate(roomList):
            for count2, slot in enumerate(slots):
                if room[1] == slot:
                    #print(room[1],'==',slot)
                    roomList[count] = (room[0], count2)
                    break

        #print("距離RoomList:",roomList)

        #距離RoomList: [('C0411', 0), ('C0618', 2)]
        # [('C0411', 0), ('C0618', 2)] => (0)(1)
        temp = -1
        gogo = True 
        for index,x in enumerate(roomList):
            if temp == x[1]: #duplicate -- 唔合理
                #print("重fok",roomList[index-1],roomList[index])
                gogo = False  
                score = 0
            temp = x[1]
            

        '''
            距離:
            Room --> elevator
            Elevator 5 seconds / floor
            Campus elevator --> another campus elevator:
                MC  <==> JCC: 3 mins | 180s
                MC  <==> IOH: 5 mins | 300s
                JCC <==> IOH: 7 mins | 420s
        '''
        
        if gogo == True:
            for count in range(len(roomList)):
                if count+1 < len(roomList):
                    if roomList[count+1][1] - roomList[count][1] == 1:
                        #print(roomList[count+1][1],'-',roomList[count][1],'= 1!!!!!!!!!')
                        #to do calculate distance
                        fromRoom = findRoom2Elevator(roomList[count][0])
                        fromRoomId = fromRoom[0]
                        fromRoomFloor = fromRoom[1]
                        fromRoomCampus = fromRoom[2]
                        fromRoomElevator = fromRoom[3]

                        toRoom = findRoom2Elevator(roomList[count+1][0])
                        toRoomId = toRoom[0]
                        toRoomFloor = toRoom[1]
                        toRoomCampus = toRoom[2]
                        toRoomElevator = toRoom[3]
                        campusTime = 0.0
                        #in seconds
                        if fromRoomCampus != toRoomCampus:
                            if fromRoomCampus == 'MC' and toRoomCampus == 'JCC' or fromRoomCampus == 'JCC' and toRoomCampus == 'MC':
                                campusTime = 180.0
                            elif fromRoomCampus == 'MC' and toRoomCampus == 'IOH' or fromRoomCampus == 'IOH' and toRoomCampus == 'MC':
                                campusTime = 300.0
                            elif fromRoomCampus == 'JCC' and toRoomCampus == 'IOH' or fromRoomCampus == 'IOH' and toRoomCampus == 'JCC':
                                campusTime = 420.0
                            
                        totalTime = fromRoomElevator+fromRoomFloor*5.0+toRoomFloor*5.0+toRoomElevator + campusTime
                        if totalTime >= maxTranTime:
                            score = 0
                        else:
                            score = 5.0 - ((totalTime / maxTranTime)*5.0)
                        #print("totalTime =",totalTime)
                        #print("New Score",score)
                        
    return score
        

def checkConsistency(popu):
    newPopu = copy.deepcopy(popu)
    lessonList = []
    for programmeIndex in range(int(len(newPopu))):
        for yearIndex in range(1,5):
            for courseIndex in range(int(len(newPopu[programmeIndex][yearIndex][1]))):
                    #print(len(newPopu[programmeIndex][yearIndex]))
                    #print(newPopu[programmeIndex][yearIndex])
                    
                    for classIndex,lesson in enumerate(newPopu[programmeIndex][yearIndex][1][courseIndex]):
                        add = True
                        temp = []
                        for existLesson in lessonList:
                            if lesson[0] in existLesson[0]:
                                #print(lesson[0],existLesson[0])
                                #print(lessonList)
                                add = False
                                temp = existLesson
                            if "FYP" in lesson[6]:
                                if (("COMP S456F" in lesson[0]) or ("COMP S451F" in lesson[0])) and (("COMP S456F" in existLesson[0]) or ("COMP S451F" in existLesson[0])):
                                    add = False
                                    temp = existLesson
                            
                        if add:
                            lessonList.append(lesson)
                            """print("added")
                            print(lesson)
                            print()"""
                        else:
                            #replace the lesson by temp
                            """print("exist in list")
                            print("change")
                            print(newPopu[programmeIndex][yearIndex][1][courseIndex][classIndex])
                            print("to")
                            print(temp)"""
                            
                            """print("old")
                            print(newPopu[programmeIndex][yearIndex][1][courseIndex][classIndex])
                            print("temp")
                            print(temp)"""
                            
                            """print(programmeIndex,yearIndex,yearCourseIndex,courseIndex,classIndex)
                            print(0)
                            print(newPopu[programmeIndex][yearIndex][0])
                            print(1)
                            print(newPopu[programmeIndex][yearIndex][1])"""
                            #newPopu[programmeIndex][yearIndex][1][courseIndex][classIndex] = list(newPopu[programmeIndex][yearIndex][1][courseIndex][classIndex])
                            newPopu[programmeIndex][yearIndex][1][courseIndex][classIndex] = tuple(copy.deepcopy(temp))
                            #popuCopy[programmeIndex][yearIndex][1][courseIndex][randomClassIndex]
                            
    
    return newPopu

def checkLPConflict(course):
    db = sqlite3.connect('ou.db')
    c = db.cursor()
    c.execute("SELECT * FROM programmeCourse")
    programmeCourse = c.fetchall()
    c.close()

    relatedPY = []
    relatedCourseCode = []

    for pc in programmeCourse:
        if course[0].split(" ")[1] in pc[2]:
            relatedPG = pc[1]
            relatedYear = pc[3]
            tempPY = (relatedPG, relatedYear)
            if tempPY not in relatedPY:
                relatedPY.append(tempPY)
                #print("Related PY appended", tempPY)
                #print("Related PY list", relatedPY)

    for pc in programmeCourse:
        for rPY in relatedPY:
            if pc[1] == rPY[0] and pc[3] == rPY[1]:
                if pc[2] not in relatedCourseCode:
                    relatedCourseCode.append(pc[2])

    return relatedCourseCode

def checkLPConflictTimeslot(lesson,relatedCourseCode,popu):
    result = []
    lList = []
    pList = []
    pCourses = []
    newPopu = copy.deepcopy(popu)
    for programmeIndex in range(int(len(newPopu))):
        for yearIndex in range(1,5):
            for courseIndex in range(int(len(newPopu[programmeIndex][yearIndex][1]))):
                    for classIndex,popuLesson in enumerate(newPopu[programmeIndex][yearIndex][1][courseIndex]):
                        for relatedCourseName in relatedCourseCode:
                            if popuLesson[0].split(" ")[1] in relatedCourseName and (popuLesson[8] not in result):
                                result.append(popuLesson[8])
                                """lessonName = popuLesson[0].split(" ")[0]+" "+popuLesson[0].split(" ")[1]
                                if "L0" in popuLesson[0]: 
                                    lList.append(popuLesson[8])
                                pCount = 0
                                if "P0" in popuLesson[0]:
                                    if lessonName not in pCourses:
                                        pCourses.append(lessonName)
                                    for pCourse in pCourses:
                                        if lessonName in pCourse:
                                            pCount +=1
                                        if pCount < 2:
                                            pList.append(lesson[8])"""
    #result = lList+pList
    result = set(result)
    result = list(result)

    return result

def initial_population():
    #db first get course,room 
    db = sqlite3.connect('ou.db')
    c = db.cursor()
    c.execute("SELECT * FROM course")
    course_data = c.fetchall()
    c.execute("SELECT * FROM programme")
    programme_data = c.fetchall()
    c.execute("SELECT * FROM programmeCourse")
    programmeCourse_data = c.fetchall()
    c.execute("SELECT * FROM room")
    room_data = c.fetchall()
    c.close()
    
    # split course
    courseList = []
    for course in course_data:
        sessionCode = course[0]+" L01"
        sessionName = course[1]
        sessionType = "Lecture"
        sessionMax = course[2]
        sessionItem = ""
        sessionSchool = course[4]
        sessionCourseType = course[5]

        newSession = (sessionCode,sessionName,sessionType,sessionMax,sessionItem,sessionSchool,sessionCourseType)
        courseList.append(newSession)
        if course[5] != "FYP":
            for i in range(int(course[2]/30.0)):
                formatStr = " P0{}".format(str(i+1))
                sessionCode = course[0]+formatStr
                sessionName = course[1]
                sessionType = "Lab"
                sessionMax = 30
                sessionItem = course[3]
                sessionSchool = course[4]
                sessionCourseType = course[5]
                newSession = (sessionCode,sessionName,sessionType,sessionMax,sessionItem,sessionSchool,sessionCourseType)
                courseList.append(newSession)

    #room over used

    #'COMP S313F P02', 'Mobile Computing', 'Lab', 30, 'COMP', 'ST','D0625' <?
    # item = (course[0] , course[1] , ....., room[0])

    courseroomList = []
    lectureroomList = []
    labroomList = []

    for room in room_data:
        if room[4] == "Lab":
            labroomList.append(room)
        else:
            lectureroomList.append(room)

    for course in courseList:
        item = []
        if course[2] == "Lab":
            if course[4]== "": # if no need item
                combinedList = lectureroomList + labroomList
                seed = random.randint(0,len(combinedList)-1)
                while combinedList[seed][1] < course[3]:
                    seed = random.randint(0,len(combinedList)-1)
                item = list(course)
                item.append(combinedList[seed][0])
                item = tuple(item)
            else:
                seed = random.randint(0,len(labroomList)-1)
                # while course item not equal room item and course require item and room cap < course cap
                while course[4] != labroomList[seed][7] and course[4]!= "" and labroomList[seed][1] < course[3]: 
                    seed = random.randint(0,len(labroomList)-1)
                item = list(course)
                item.append(labroomList[seed][0])
                item = tuple(item)
            courseroomList.append(item)

        else:
            if findFYPRoom(course[0],courseroomList) != None:
                course = list(course)
                course.append(findFYPRoom(course[0],courseroomList))
                course = tuple(course)
            else:
                seed = random.randint(0,len(lectureroomList)-1)
                while lectureroomList[seed][1] <= course[3]:
                    seed = random.randint(0,len(lectureroomList)-1)
                course = list(course)
                course.append(lectureroomList[seed][0])
                course = tuple(course)
            courseroomList.append(course)
    """for i in courseroomList:
        print(i)"""
    
    #============================================================================
    timeslotList = []
    for weekday in ["Mon","Tue","Wed","Thu","Fri"]:
            #mean 9 AM start
            i = 9
            while i < 18:# mean end at 18:00 -> 6PM
                if i == 13:
                    i = 14
                start = i
                end = i+2
                if start < 10:
                    start = "0"+str(start)
                end = str(end)
                timeslot = weekday +" " + str(start)+ " - " + str(end)
                timeslotList.append(timeslot)
                i += 2
      
    #====================Try to split Timeslot====================================
    courseroomtimeList = [] 
    while len(courseroomList) > 0:
        if len(courseroomList) > 0:

            #Randomly pop a course from the courseroomList
            courseseed = random.randint(0,len(courseroomList)-1)
            timeseed = random.randint(0,len(timeslotList)-1)
            
            #Pop courseroom
            course = courseroomList.pop(courseseed)
            timeslot = timeslotList[timeseed]
            """courseName = course[0].split(" ")[0]+" "+course[0].split(" ")[1]
            avoidList = []
            avoidTimeslotList = []
            avoidList = findProgrammeYear(courseName)
            avoidList = findSameYear(courseName,avoidList)
            #print("avoid List :")
            #print(avoidList)
            #print(avoidList)
            if "L0" in course[0]:
                # to find which timeslot we need to avoid
                for avoidCourse in avoidList:
                    for courseroomtime in courseroomtimeList:
                        if (avoidCourse in courseroomtime[0]) and not(courseroomtime[8] in avoidTimeslotList):
                            avoidTimeslotList.append(courseroomtime[8])
                # print(avoidTimeslotList)
            elif "P0" in course[0]:
                # to find which timeslot we need to avoid
                for avoidCourse in avoidList:
                    count = 0 # to avoid all "P" in one time slot
                    for courseroomtime in courseroomtimeList:
                        if (avoidCourse in courseroomtime[0]) and not(courseroomtime[8] in avoidTimeslotList):
                            #print("course")
                            #print(course)
                            #print("courseroomtime")
                            #print(courseroomtime)
                            if "L0" in courseroomtime[0]:
                                avoidTimeslotList.append(courseroomtime[8])
                            elif ("P0" in courseroomtime[0]) and (avoidCourse == courseName):
                                if count > 0:
                                    break
                                else:
                                    count +=1
                                    avoidTimeslotList.append(courseroomtime[8])
                            elif ("P0" in courseroomtime[0]) and (courseroomtime[7] == course[7]):
                                avoidTimeslotList.append(courseroomtime[8])

                    
            #check existing lecture either crash timeslot
            for courseroomtime in courseroomtimeList:
                if 'L0' in course[0]:
                    while True:
                        if course[0].split(' ')[1] in courseroomtime[0] and 'P0' in courseroomtime[0] and timeslot == courseroomtime[8]:
                            #timeslot crash
                            # print('CRASH!:',course,courseroomtime)
                            timeseed = random.randint(0,len(timeslotList)-1)
                            timeslot = timeslotList[timeseed]
                        elif len(avoidList) > 0:
                            check = True
                            while check:
                                count = 0
                                for avoidTimeslot in avoidTimeslotList:
                                    if timeslot == avoidTimeslot:
                                        msg = "CRASH!" + course[0]
                                        # print(msg)
                                        count += 1
                                        timeseed = random.randint(0,len(timeslotList)-1)
                                        timeslot = timeslotList[timeseed]
                                if count == 0:
                                    check = False
                            break
                                
                        else:
                            break

                if 'P0' in course[0]:
                    
                    while True:
                        if course[0].split(' ')[1] in courseroomtime[0] and 'L0' in courseroomtime[0] and timeslot == courseroomtime[8]:
                            #timeslot crash
                            # print('CRASH!:',course,courseroomtime)
                            timeseed = random.randint(0,len(timeslotList)-1)
                            timeslot = timeslotList[timeseed]
                        elif len(avoidList) > 0:
                            check = True
                            while check:
                                count = 0
                                for avoidTimeslot in avoidTimeslotList:
                                    if timeslot == avoidTimeslot:
                                        msg = "CRASH!" + course[0]
                                        # print(msg)
                                        count += 1
                                        timeseed = random.randint(0,len(timeslotList)-1)
                                        timeslot = timeslotList[timeseed]
                                if count == 0:
                                    check = False
                            break
                        else:
                            break"""

            #Insert timeslot to poped courseroom
            course = list(course)
            if findFYPTime(course[0],courseroomtimeList) != None:
                course.append(findFYPTime(course[0],courseroomtimeList))    
            else:
                course.append(timeslot)
            course = tuple(course)
            courseroomtimeList.append(course)

            #How many course left to be assigned a timeslot
            #print(len(courseroomList),'to be assigned...')
        else:
            break
                
    #for i in courseroomtimeList:
        #print(i)

      #====================Timeslot matching Programme & Year====================================
    #Each programme in Programme table of DB
    programList = []
    for programme in programme_data:
        item = [programme[0]]
        #Year 1~4
        for counter in range(1,5):
            yearTemp = [counter,[]]
            #Your programmeCourse table DB
            for programmeCourse in programmeCourse_data:        
                #ProgrammeCourse's programme ID == Programe's programme ID AND Year 1/2/3/4 == counter
                #e.g 'BCOMPHITJS' = 'BCOMPHITJS' AND Year 1 = Counter 1
                
                if programmeCourse[1] == programme[0] and programmeCourse[3] == str(counter):
                    #print(programmeCourse[1],'Year',programmeCourse[3])
                    tempList = []
                    for courseroomtime in courseroomtimeList:
                        #If your programmeCourse's Course ID == assigned timeslot Course ID
                        #e.g 'IT S102F' in 'IT S102F P02'
                        if programmeCourse[2] in courseroomtime[0] and programmeCourse[3] == str(counter):
                            tempList.append(courseroomtime)
                    yearTemp[1].append(tempList)  
            item.append(yearTemp)
        programList.append(item)
    
    """for programme in programList:
        # programmeName => programme[0] e.g BSCHCSJS
        # print(programme[0]) 
        #programme[1] => [yr,[class of A course],[class of B course]]
        #programme[1] => to loop the list of course
        for programmeCourseList in programme[1:]:
            # programmeCourseList[0] => year e.g 1 2 3 4
            # print(programme[0],programmeCourseList[0]) => print programme name and year
            print(programme[0],programmeCourseList[0])
            for yearCourseList in programmeCourseList[1:]:
                for course in yearCourseList: # course => e.g S202F
                    for lesson in course: # lesson => e.g P01 L01
                        print(lesson)"""
    for programme in programList:
        # programmeName => programme[0] e.g BSCHCSJS
        # print(programme[0]) 
        #programme[1] => [yr,[class of A course],[class of B course]]
        #programme[1] => to loop the list of course
        for programmeCourseList in programme[1:]:
            # programmeCourseList[0] => year e.g 1 2 3 4
            # print(programme[0],programmeCourseList[0]) => print programme name and year
            #print(programme[0],programmeCourseList[0])
            
            
            for yearCourseList in programmeCourseList[1:]:
                yearList =[programme[0],programmeCourseList[0]]
                monList = []
                tueList = []
                wedList = []
                thuList = []
                friList = []
                for course in yearCourseList: # course => e.g S202F
                    for lesson in course: # lesson => e.g P01 L01
                        for weekday in ["Mon","Tue","Wed","Thu","Fri"]:
                            if weekday in lesson[8] and weekday == "Mon":
                                monList.append(lesson)
                            elif weekday in lesson[8] and weekday == "Tue":
                                tueList.append(lesson)
                            elif weekday in lesson[8] and weekday == "Wed":
                                wedList.append(lesson)
                            elif weekday in lesson[8] and weekday == "Thu":
                                thuList.append(lesson)
                            elif weekday in lesson[8] and weekday == "Fri":
                                friList.append(lesson)
                yearList.append(monList)
                yearList.append(tueList)
                yearList.append(wedList)
                yearList.append(thuList)
                yearList.append(friList)
                #print(yearList)

    
    return programList


def fitness(programList):
# 依家分左year 分左programme
# e.G
# ['BCOMPHITJS', 4, [], [], [], [('COMP S456F L01', 'Software System Development Project', 'Lecture', 90, '', 'ST', 'FYP', 'C0518', 'Thu 9 - 11'), ('COMP S451F L01', 'Computing Project', 'Lecture', 90, '', 'ST', 'FYP', 
#'C0518', 'Thu 9 - 11')], []]
# [0] 係programme 名 
# [1] 係 year
# Mon[2] Tue[3] Wed[4] Thu[5] Fri[6]
    # allList[0] => programme name
    # allList[1] => Year
    # allList[2] => pathList 折每個path 去計
    # allList[2][N] => 第N個path
    allList = []
    for programme in programList:
        # programmeName => programme[0] e.g BSCHCSJS
        # print(programme[0]) 
        #programme[1] => [yr,[class of A course],[class of B course]]
        #programme[1] => to loop the list of course
        for programmeCourseList in programme[1:]:
            # programmeCourseList[0] => year e.g 1 2 3 4
            # print(programme[0],programmeCourseList[0]) => print programme name and year
            #print(programme[0],programmeCourseList[0])
            programmeList = [programme[0],programmeCourseList[0]]
            for yearCourseList in programmeCourseList[1:]:
                #print(yearCourseList)
                yearPClass = []
                yearLClass = []
                temp = [[] for i in range(len(yearCourseList))]
                
                for index,course in enumerate(yearCourseList): # course => e.g S202F
                    pClass = []
                    lClass = []
                    for lesson in course: # lesson => e.g P01 L01
                        if "L0" in lesson[0]:
                            lClass.append(lesson)
                        else:
                            #courseName = lesson[0].split(" ")[0] + " " + lesson[0].split(" ")[1]
                            #print(courseName)
                            #if courseName in yearLesson[0]:
                            pClass.append(lesson)
                    yearLClass.append(lClass[0])
                    if pClass != []:
                        yearPClass.append(pClass)
                        temp[index] = pClass
                #print(temp)
                newList = list(itertools.product(*temp))
                pathList = []
                #print(yearLClass)
                for i in newList:
                    pathList.append(yearLClass+list(i))
                if pathList == []:
                    pathList.append(yearLClass)
                programmeList.append(pathList)
            allList.append(programmeList)
    fitnessScore = 0.0
    
    counter = 0        
    HC4 = True
    HC5 = True
    HC6 = True
    softConstraintScore = 0.0
    for i in allList:


        #Possibilities
        for group in i[2]:
            counter += 1
            groupScore = 0
            #print(group)
            #print()

            #Temp List 星期一至五List for individual groups
            monList = []
            tueList = []
            wedList = []
            thuList = []
            friList = []

            #individual => mon tue wed thu fri
            for individual in group:
                if 'Mon' in individual[8]:
                    monList.append(individual)
                if 'Tue' in individual[8]:
                    tueList.append(individual)
                if 'Wed' in individual[8]:
                    wedList.append(individual)
                if 'Thu' in individual[8]:
                    thuList.append(individual)
                if 'Fri' in individual[8]:
                    friList.append(individual)

            #Scoring the individual groups

            #=========Hard Constraint (Location & Time not crashing at the same slot)=========
            
            #Check duplicates within same list
            #if len(set([x for x in monList if monList.count(x) > 1])) != 0:
                #print("CRASH!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

            #course[0] duplicates not allowed => exact same course twice a day not ok
            #useless
            '''if len(set([course for course in monList if monList.count(course[0]) > 1])) == 0:
                groupScore += 50
            else:
                print("CRASH!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!![0]")
            if len(set([course for course in tueList if tueList.count(course[0]) > 1])) == 0:
                groupScore += 50
            else:
                print("CRASH!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!![0]")
            if len(set([course for course in wedList if wedList.count(course[0]) > 1])) == 0:
                groupScore += 50
            else:
                print("CRASH!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!![0]")
            if len(set([course for course in thuList if thuList.count(course[0]) > 1])) == 0:
                groupScore += 50
            else:
                print("CRASH!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!![0]")
            if len(set([course for course in friList if friList.count(course[0]) > 1])) == 0:
                groupScore += 50
            else:
                print("CRASH!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!![0]")'''

            montofriList = [monList, tueList, wedList, thuList, friList]

            for count, dayList in enumerate(montofriList):

                if count == 0:
                    debug_day = "Mon"
                elif count == 1:
                    debug_day = "Tue"
                elif count == 2:
                    debug_day = "Wed"
                elif count == 3:
                    debug_day = "Thu"
                elif count == 4:
                    debug_day = "Fri"

                #print(count)
                #print("{}List".format(debug_day))

                
                '''seen = {}
                dupes = []
                lec_timeslot = []
                lec_count = 0
                for course in dayList:
                    if 'L01' in course[0]:
                        if course[6] == 'FYP':
                            break
                        lec_count += 1

                        #obtain lecture's timeslot
                        lec_timeslot.append(course[8])

                for course in dayList:
                    if 'L01' not in course[0]:
                        timeslot = course[8]
                        if timeslot in lec_timeslot:
                            dupes.append(timeslot)

                if lec_count > 1:
                    print("Hard constraint 4 violations - L0 with other course",dayList)
                elif len(dupes) > 0:
                    print("Hard constraint 4 violations - L0 with other course",dayList)
                else:
                    print("Passed HC4")
                    groupScore += 50'''

                
                #4. L0 Class cannot have other class at the same timeslot
                if HC4 == True:
                    used_L = []
                    used_P = []
                    for course in dayList:
                        if course[6] == 'FYP':
                            break
                        time = course[8]
                        #print(room_time)
                        if "L0" in course[0]:
                            if time not in used_L:
                                used_L.append(time)
                            elif time in used_P:
                                HC4 = False
                            else:
                                HC4 = False
                        if "P0" in course[0]:
                            if time not in used_P:
                                used_P.append(time)
                            if time in used_L:
                                HC4 = False
                        
                    """seen = {}
                    dupes = []
                    time = ()
                    HC4_violate = False
                    for course in dayList:
                        time = (course[8])

                        if course[6] == 'FYP':
                            break

                        if time not in seen:
                            seen[time] = 1
                        else:
                            if seen[time] == 1:
                                dupes.append(time)
                            seen[time] += 1

                    if len(dupes) == 0:
                        #print("Passed HC4")
                        #groupScore += 50
                        HC4 = True
                    elif len(dupes) > 0:
                        for course in dayList:
                            time = (course[8])
                            for timeslot in dupes:
                                if time == timeslot:
                                    if 'L01' in course[0]:
                                        HC4_violate = True
                        if HC4_violate == True:
                            HC4 = False
                            #pass
                            #print("HC4 violations", dayList)
                        else:
                            #print("Passed HC4")
                            #groupScore += 50
                            HC4 = True
                    else:
                        #print("Passed HC4")
                        #groupScore += 50
                        HC4 = True"""

                #5. All P0 of the same course in same timeslot not allowed
                if HC5 == True:
                    seen = {}
                    dupes = []
                    course_code = ""
                    h5_violate = False
                    for course in dayList:
                        course_code = course[0].split(" ")[0] +" "+ course[0].split(" ")[1]

                        if "P0" in course[0]:
                            if course_code not in seen:
                                course_code +" P0" #e.g COMP S123F P0
                                if sum(course.count(course_code) for course in dayList) > 3:
                                    #print("Hard constraint 5 violations - P01 P02 P03 violation:",course)
                                    h5_violate = True
                                else:
                                    h5_violate = False

                                seen[course_code] = 1
                        
                    if h5_violate == False:
                        #print("Passed HC5")
                        #groupScore += 50
                        HC5 = True
                    else:
                        HC5 = False

                #6. course[7] and course[8] duplicates not allowed => two courses same location same timeslot not ok
                if HC6 == True:
                    used = []
                    for course in dayList:
                        if course[6] == 'FYP':
                            break
                        room_time = [course[7],course[8]]
                        #print(room_time)
                        if room_time not in used:
                            used.append(room_time)
                        else:
                            HC6 = False
                            
                    """
                    seen = {}
                    dupes = []
                    room_time = ()
                    for course in dayList:
                        room_time = (course[7],course[8])
                        #print("evaluate:",room_time)

                        if course[6] == 'FYP':
                            seen[room_time] = 1
                            break


                        if room_time not in seen:
                            seen[room_time] = 1
                        else:
                            if seen[room_time] == 1:
                                dupes.append(room_time)
                            seen[room_time] += 1

                    if len(dupes) == 0:
                        HC6 = True
                        #groupScore += 50
                        #print("Passed HC6")
                    else:
                        HC6 = False
                        #pass
                        #print("Duplicate {}: {}".format(debug_day,dupes))"""

                #print("")

            '''
            seen = {}
            dupes = []
            room_time = ()

            for course in tueList:
                room_time = (course[7],course[8])
                if room_time not in seen:
                    seen[room_time] = 1
                else:
                    if seen[room_time] == 1:
                        dupes.append(room_time)
                    seen[room_time] += 1
            if len(dupes) == 0:
                groupScore += 50
            else:
                print("Len of Tue:",len(tueList))
                print("course of Tue:",[course for course in tueList])
                print("Duplicate Tue:",dupes)

            seen = {}
            dupes = []
            room_time = ()

            for course in wedList:
                room_time = (course[7],course[8])
                if room_time not in seen:
                    seen[room_time] = 1
                else:
                    if seen[room_time] == 1:
                        dupes.append(room_time)
                    seen[room_time] += 1
            if len(dupes) == 0:
                groupScore += 50
            else:
                print("Len of Wed:",len(wedList))
                print("course of Wed:",[course for course in wedList])
                print("Duplicate Wed:",dupes)

            seen = {}
            dupes = []
            room_time = ()

            for course in thuList:
                room_time = (course[7],course[8])
                if room_time not in seen:
                    seen[room_time] = 1
                else:
                    if seen[room_time] == 1:
                        dupes.append(room_time)
                    seen[room_time] += 1
            if len(dupes) == 0:
                groupScore += 50
            else:
                print("Len of Thu:",len(thuList))
                print("course of Thu:",[course for course in thuList])
                print("Duplicate Thu:",dupes)

            seen = {}
            dupes = []
            room_time = ()

            for course in friList:
                room_time = (course[7],course[8])
                if room_time not in seen:
                    seen[room_time] = 1
                else:
                    if seen[room_time] == 1:
                        dupes.append(room_time)
                    seen[room_time] += 1
            if len(dupes) == 0:
                groupScore += 50
            else:
                print("Len of Fri:",len(friList))
                print("course of Fri:",[course for course in friList])
                print("Duplicate Fri:",dupes)
            print("")'''

            '''for course in monList:
                    print("Mon")
                    print(course[7])
            print("")
            for course in tueList:
                    print("Tue")
                    print(course[7])
            print("")
            for course in wedList:
                    print("Wed")
                    print(course[7])
            print("")
            for course in thuList:
                    print("Thu")
                    print(course[7])
            print("")
            for course in friList:
                    print("Fri")
                    print(course[7])
            print("")
            '''

            '''if len(set([course for course in monList if monList.count(course[7]) > 1])) != 0 and len(set([course for course in monList if monList.count(course[8]) > 1])) != 0:
                print("CRASH!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!![7][8]")
            else:
                groupScore += 50
            if len(set([course for course in tueList if tueList.count(course[7]) > 1])) != 0 and len(set([course for course in tueList if tueList.count(course[8]) > 1])) != 0:
                print("CRASH!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!![7][8]")
            else:
                groupScore += 50
            if len(set([course for course in wedList if wedList.count(course[7]) > 1])) != 0 and len(set([course for course in wedList if wedList.count(course[8]) > 1])) != 0:
                print("CRASH!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!![7][8]")
            else:
                groupScore += 50
            if len(set([course for course in thuList if thuList.count(course[7]) > 1])) != 0 and len(set([course for course in thuList if thuList.count(course[8]) > 1])) != 0:
                print("CRASH!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!![7][8]")
            else:
                groupScore += 50
            if len(set([course for course in friList if friList.count(course[7]) > 1])) != 0 and len(set([course for course in friList if friList.count(course[8]) > 1])) != 0:
                print("CRASH!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!![7][8]")
            else:
                groupScore += 50'''


            #=======================2 hard constraint left to-do=======================
            
            #scourse[0] 'P0' duplicates not allowed => same course same or different tutorial group
            '''seen = {}
            dupes = []

            for course in monList:
                if 'P0' in course[0]:
                    courseTutorial = course[0].split(' ')[0]+' '+course[0].split(' ')[1]+' '+'P0'

                    if course not in seen:
                        seen[course] = 1
                    else:
                        if seen[course] == 1:
                            dupes.append(course)
                        seen[course] += 1
            else:
                if len(dupes) != 0:
                    print("CRASH!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!![0]P0")
                else:
                    groupScore += 50'''
            
            #course[3] : course[7] => course max ppl less than or equals room capacity
            #差呢個hard constraint未check  


            #course[7] have the room item course[5] needed (item in room : item course needed)
            '''
            db = sqlite3.connect('ou.db')
            c = db.cursor()

            for course in monList:
                print("course:",course)

                course_item = course[4]
                room_id = course[7]

                print("course_item:",course_item)
                print("room_id:",course_item)

                c.execute("SELECT item FROM room WHERE roomid = ?",(room_id,))
                room_item = c.fetchall()
                print("room_item:",room_item)

                
                print("\n")
                #if  course[4] != labroomList[seed][7] and course[4]!= "" and labroomList[seed][1] < course[3]
            c.close()
            '''

            #============================Soft constraint============================

            '''
            天地堂:
            9 - 11 => 16 - 18
            '''

            monScore = earlyLateClassScore(monList)
            tueScore = earlyLateClassScore(tueList)
            wedScore = earlyLateClassScore(wedList)
            thuScore = earlyLateClassScore(thuList)
            friScore = earlyLateClassScore(friList)

            groupScore += (monScore+tueScore+wedScore+thuScore+friScore)
            #print("earlyLateClassScore: {}".format(groupScore))

            #print('monScore',monScore)
            #print('tueScore',tueScore)
            #print('wedScore',wedScore)
            #print('thuScore',thuScore)
            #print('friScore',friScore)


            totalDistanceScore = (distanceScore(monList) + distanceScore(tueList) + distanceScore(wedList) + distanceScore(thuList) + distanceScore(monList))
            #print("totalDistanceScore: {}".format(totalDistanceScore))
            groupScore += totalDistanceScore
            #print("groupScore: {}".format(groupScore))
            softConstraintScore += groupScore

            #print('monList',monList)
            #print('tueList',tueList)
            #print('wedList',wedList)
            #print('thuList',thuList)
            #print('friList',friList)
            #print('groupScore:',groupScore)
            #print()
    fitnessScore += 50*3 #by default, HC1~3 granted
    if HC4:
        fitnessScore += 50
        #print("HC4 OK")
    if HC5:
        fitnessScore += 50
        #print("HC5 OK")
    if HC6:
        fitnessScore += 50
        #print("HC6 OK")

    fitnessScore += softConstraintScore/counter

    return fitnessScore

def crossover(popu1,popu2):
    
    popu1Copy = []
    #print("All lesson : ",popu[0][1][1][0])
    #print(popu1[0])
    #print(popu1[0][1])
    #print(popu1[0][2])
    '''print(popu1[0])
    print()
    print(popu1[1])
    print("====================================")'''

    ranNum = 0
    
    for programmeIndex in range(int(len(popu1))):
        for yearIndex in range(1,5):
            """if ranNum == 0:
                ranNum = random.randint(1,(int(len(popu1[programmeIndex][yearIndex][1]))))
                #print(ranNum)"""
            if len(popu1[programmeIndex][yearIndex][1]) <= 1:
                for courseIndex in range(int(len(popu1[programmeIndex][yearIndex][1]))):
                    popu1Copy.append(popu1[programmeIndex][yearIndex][1][courseIndex])
            else:
                #for courseIndex in range(int(len(popu1[programmeIndex][yearIndex][1])/ ranNum)):
                for courseIndex in range(int(len(popu1[programmeIndex][yearIndex][1])/ 2)):
                    popu1Copy.append(popu1[programmeIndex][yearIndex][1][courseIndex])

    #print(popu1Copy)
    
    
    """for index, item in enumerate(popu1Copy):
            print(index)
            print(item)"""
    
    #print("=============================End of Popu1==========================================")
    #print()

    #popu2
    popu2Copy = []
    for programmeIndex in range(int(len(popu2))):
        for yearIndex in range(1,5):
            if len(popu2[programmeIndex][yearIndex][1]) <= 1:
                for courseIndex in range(int(len(popu2[programmeIndex][yearIndex][1]))):
                    popu2Copy.append(popu2[programmeIndex][yearIndex][1][courseIndex])
            else:
                #for courseIndex in range(int(len(popu2[programmeIndex][yearIndex][1])/ ranNum)):
                for courseIndex in range(int(len(popu2[programmeIndex][yearIndex][1])/ 2)):
                    popu2Copy.append(popu2[programmeIndex][yearIndex][1][courseIndex])

    #print(popu2Copy)
    
    """for index, item in enumerate(popu2Copy):
        print(index)
        print(item)"""
    
    """for programmeIndex, programme in enumerate(popu2Copy):
        for yearIndex, year in enumerate(programme):
            print(yearIndex)
            print(year)"""

    #print("=============================End of Popu2==========================================")
    #print()

    #print("=============================Crossover Popu1==========================================")
    #print()

    for programmeIndex in range(int(len(popu1))):
        for yearIndex in range(1,5):
            if len(popu1[programmeIndex][yearIndex][1]) <= 1:
                for courseIndex in range(int(len(popu1[programmeIndex][yearIndex][1]))):
                    popu1[programmeIndex][yearIndex][1][courseIndex] = popu2Copy.pop(0)
            else:
                #for courseIndex in range(int(len(popu1[programmeIndex][yearIndex][1])/ ranNum)):
                for courseIndex in range(int(len(popu1[programmeIndex][yearIndex][1])/ 2)):
                    popu1[programmeIndex][yearIndex][1][courseIndex] = popu2Copy.pop(0)

    #print(popu1)
    """for index, item in enumerate(popu2):
            print(index)
            print(item)"""

    #print(popu2)
    """for programme in popu1:
        # programmeName => programme[0] e.g BSCHCSJS
        # print(programme[0]) 
        #programme[1] => [yr,[class of A course],[class of B course]]
        #programme[1] => to loop the list of course
        for programmeCourseList in programme[1:]:
            # programmeCourseList[0] => year e.g 1 2 3 4
            # print(programme[0],programmeCourseList[0]) => print programme name and year
            print(programme[0],programmeCourseList[0])
            for yearCourseList in programmeCourseList[1:]:
                for course in yearCourseList: # course => e.g S202F
                    for lesson in course: # lesson => e.g P01 L01
                        print(lesson)"""

    #print("=============================Crossover Popu2==========================================")
    #print()

    for programmeIndex in range(int(len(popu2))):
        for yearIndex in range(1,5):
            if len(popu2[programmeIndex][yearIndex][1]) <= 1:
                for courseIndex in range(int(len(popu2[programmeIndex][yearIndex][1]))):
                    popu2[programmeIndex][yearIndex][1][courseIndex] = popu1Copy.pop(0)
            else:
                #for courseIndex in range(int(len(popu2[programmeIndex][yearIndex][1])/ ranNum)):
                for courseIndex in range(int(len(popu2[programmeIndex][yearIndex][1])/ 2)):
                    popu2[programmeIndex][yearIndex][1][courseIndex] = popu1Copy.pop(0)

    #print(popu1)
    """for index, item in enumerate(popu2):
            print(index)
            print(item)"""

    #print(popu2)
    """for programme in popu2:
        # programmeName => programme[0] e.g BSCHCSJS
        # print(programme[0]) 
        #programme[1] => [yr,[class of A course],[class of B course]]
        #programme[1] => to loop the list of course
        for programmeCourseList in programme[1:]:
            # programmeCourseList[0] => year e.g 1 2 3 4
            # print(programme[0],programmeCourseList[0]) => print programme name and year
            print(programme[0],programmeCourseList[0])
            for yearCourseList in programmeCourseList[1:]:
                for course in yearCourseList: # course => e.g S202F
                    for lesson in course: # lesson => e.g P01 L01
                        print(lesson)"""

    popu1 = checkConsistency(copy.deepcopy(popu1))
    popu2 = checkConsistency(copy.deepcopy(popu2))

    return (popu1,popu2)
   
def mutation(popu):
    popuCopy = popu.copy()
    timeslotList = []
    for weekday in ["Mon","Tue","Wed","Thu","Fri"]:
            #mean 9 AM start
            i = 9
            while i < 18:# mean end at 18:00 -> 6PM
                if i == 13:
                    i = 14
                start = i
                end = i+2
                if start < 10:
                    start = "0"+str(start)
                end = str(end)
                timeslot = weekday +" " + str(start)+ " - " + str(end)
                timeslotList.append(timeslot)
                i += 2
    #randomIndex = random.randint(0,len(timeslotList)-1)
    for programmeIndex in range(int(len(popuCopy))):
        for yearIndex in range(1,5):
            for courseIndex in range(int(len(popuCopy[programmeIndex][yearIndex][1]))):
                #s380f = [(L01),(P01),(P02)]
                #for count in range(1,3):
                randomClassIndex = random.randint(0,len(popuCopy[programmeIndex][yearIndex][1][courseIndex])-1)
                #print("HAPPY NEW YEAR")
                #print("Default :　",popu[programmeIndex][yearIndex][1][courseIndex][randomClassIndex][8])
                #print(popu[programmeIndex][yearIndex][1][courseIndex])
                #print("timeslotList[randomIndex] : ",timeslotList[randomIndex])
                courseToMu = popuCopy[programmeIndex][yearIndex][1][courseIndex][randomClassIndex]
                tempRandomtimeslot = ''

                relatedCourseCode = checkLPConflict(courseToMu)

                #print("rCC",relatedCourseCode)

                tempFlow = False
                while tempFlow is False:
                    count = 0
                    randomIndex = random.randint(0,len(timeslotList)-1)
                    tempRandomtimeslot = timeslotList[randomIndex]

                    for course in popuCopy[programmeIndex][yearIndex][1][courseIndex]:
                        currentCourseCode = course[0].split(" ")[0]+" "+course[0].split(" ")[1]
                        #print(course[0])
                        if 'P0' in courseToMu[0]:
                            if 'L0' in course[0] and currentCourseCode in relatedCourseCode:
                                if tempRandomtimeslot == course[8]:
                                    '''print()
                                    print("CRASH!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                                    print("courseToMu:")
                                    print(courseToMu)
                                    print("Timeslot to be changed to:",tempRandomtimeslot)
                                    print("Found crashing:")
                                    print(course)
                                    print()'''
                                    count += 1
                                    break
                        else:
                            if currentCourseCode in relatedCourseCode:
                                if tempRandomtimeslot == course[8]:
                                    '''print()
                                    print("CRASH!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                                    print("courseToMu:")
                                    print(courseToMu)
                                    print("Timeslot to be changed to:",tempRandomtimeslot)
                                    print("Found crashing:")
                                    print(course)
                                    print()'''
                                    count += 1
                                    break
                    
                    if count == 0:
                        tempFlow = True

                #print(tempRandomtimeslot)
                courseToMu = list(courseToMu)
                courseToMu[8] = tempRandomtimeslot
                popuCopy[programmeIndex][yearIndex][1][courseIndex][randomClassIndex] = tuple(courseToMu)
                #print("Finally", popuCopy[programmeIndex][yearIndex][1][courseIndex][randomClassIndex])
                #print("Now : ",popu[programmeIndex][yearIndex][1][courseIndex][randomClassIndex][8])
                #print(popu[programmeIndex][yearIndex][1][courseIndex])
    popuCopy = checkConsistency(copy.deepcopy(popuCopy))
    return mutation_1(popuCopy)

def mutation_1(popu):
    popuCopy = popu.copy()
    timeslotList = []
    for weekday in ["Mon","Tue","Wed","Thu","Fri"]:
            #mean 9 AM start
            i = 9
            while i < 18:# mean end at 18:00 -> 6PM
                if i == 13:
                    i = 14
                start = i
                end = i+2
                if start < 10:
                    start = "0"+str(start)
                end = str(end)
                timeslot = weekday +" " + str(start)+ " - " + str(end)
                timeslotList.append(timeslot)
                i += 2
    #randomIndex = random.randint(0,len(timeslotList)-1)

    for programmeIndex in range(int(len(popuCopy))):
        for yearIndex in range(1,5):
            for courseIndex in range(int(len(popuCopy[programmeIndex][yearIndex][1]))):
                #randomClassIndex = random.randint(0,len(popuCopy[programmeIndex][yearIndex][1][courseIndex])-1)

                for classIndex,lesson in enumerate(popuCopy[programmeIndex][yearIndex][1][courseIndex]):
                    tempRandomtimeslot = lesson[8]
                    #print(lesson)
                    relatedTimeslots = []
                    relatedCourseCodes = copy.deepcopy(checkLPConflict(lesson))
                    #print(lesson)
                    #print(relatedCourseCodes)
                    relatedTimeslots = copy.deepcopy(checkLPConflictTimeslot(lesson,relatedCourseCodes,copy.deepcopy(popuCopy)))
                    #print(relatedTimeslots)
                    #print()
                    #print(lesson[0])
                    #print(relatedTimeslot)
                    
                    run = True
                    while run and len(relatedTimeslots) > 0 :
                        #print("IN")
                        count = 0
                        ranCounter = 0
                        assignIndex = 0
                        #print(relatedTimeslots)
                        for relatedTimeslot in relatedTimeslots:
                            #print("IN 2")
                            #print("tempRandomtimeslot",tempRandomtimeslot)
                            #print("len",len(relatedTimeslots))
                            #print(relatedTimeslots)
                            if tempRandomtimeslot in relatedTimeslot:
                                #print("IN 3")
                                count+=1
                                ranCounter+=1
                                #print("ranCounter",ranCounter)
                                randomIndex = random.randint(0,len(timeslotList)-1)
                                tempRandomtimeslot = timeslotList[randomIndex]
                        """if ranCounter > 2:
                            tempRandomtimeslot = timeslotList[assignIndex]
                            assignIndex+=1
                        elif assignIndex > len(timeslotList):
                            print("GG")
                            run = False"""
                        if count == 0:
                            run = False
                        if len(relatedTimeslots)>=20:
                            run = False
                #print(tempRandomtimeslot)
                #popuCopy[programmeIndex][yearIndex][1][courseIndex][classIndex] = list(popuCopy[programmeIndex][yearIndex][1][courseIndex][classIndex])
                #popuCopy[programmeIndex][yearIndex][1][courseIndex][classIndex][8] = tempRandomtimeslot
                #popuCopy[programmeIndex][yearIndex][1][courseIndex][classIndex] = tuple(popuCopy[programmeIndex][yearIndex][1][courseIndex][classIndex])

                    newLesson = popuCopy[programmeIndex][yearIndex][1][courseIndex][classIndex]
                    #print(type(newLesson))
                    newLesson = list(newLesson)
                    newLesson[8] = copy.deepcopy(tempRandomtimeslot)
                    newLesson = tuple(newLesson)
                    #print(newLesson)
                    #print(popuCopy[programmeIndex][yearIndex][1][courseIndex][classIndex])
                    #print()
                    #print("READY",newLesson)
                    popuCopy[programmeIndex][yearIndex][1][courseIndex][classIndex] = copy.deepcopy(newLesson)
                    #print("DONE",newLesson)

                    #courseToMu = list(courseToMu)
                    #courseToMu[8] = tempRandomtimeslot
                    #popuCopy[programmeIndex][yearIndex][1][courseIndex][classIndex] = tuple(courseToMu)
    popuCopy = checkConsistency(copy.deepcopy(popuCopy))
    return popuCopy