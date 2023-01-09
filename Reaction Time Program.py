from guizero import App, Box, Text, PushButton, Window, TextBox, Combo
import matplotlib.pyplot as plt
import pickle
import time
import random

# Color scheme of the program
darkblue = [61, 90, 128]
midblue = [152, 193, 217]
lightblue = [224, 251, 252]
orange = [238, 108, 77]
black = [41, 50, 65]

ibm = 'IBMPlexSans-SemiBoldItalic.ttf'

# Attributes for the app that each of the windows will inherit
app = App(width=1000, height=700, bg=darkblue)
app.font = ibm

# Variables used in each of the windows
students = []
numStudents = len(students)
runs = 0
haschanged = False
programend=False
buttoncolorchange = time.time()

# Student object - each of the students and their data is saved this way
class Student():
    #studentNumber = 0
    age = 0
    bestTime = 0
    allTimes = []

# Takes the current 'students' list and saves it as a .pickle file
def saveClose():
    global students, ibm, fileTo
    window = Window(app, title='Save Data to File')
    window.font=ibm
    userHelp = Text(window, text='Enter name to save as: ', align='top', color='white')
    fileTo = TextBox(window, width=150, align='top')
    submit1 = Box(window, align='bottom', width='fill', height=300)
    submit1.bg = [200,200,200]
    def do_this():
        global fileTo
        global students, saveConfirm, fileTo
        # Takes the value of the text box on the button press and uses it as the file name
        store = fileTo.value+'.pickle'
        with open(store, 'wb') as outfile:
            pickle.dump(students, outfile)
        # Confirmation message
        saveConfirm = app.info(app, text=f'Data has been saved as {store}')
    submit1.when_clicked = do_this

# Takes the user's input and looks for a .pickle file of the same name
# to overwrite the current 'students' list
def openAFile():
    global students, ibm
    window = Window(app, title='Open Data from File', bg=darkblue)
    window.font=ibm
    def openTheFile():
        global students
        openFile = fileFrom.value
        try:
            with open(f'{openFile}.pickle', 'rb') as infile:
                students = pickle.load(infile)
                fileConfirm.visible=True
        except:
            # Exception handler for if the user's input does not correspond to any saved file
            notFound=Text(window, text='File not found.')
    userHelp = Text(window, text='Enter file name (case sensitive): ')
    fileFrom = TextBox(window, width=150)
    chooseFile = PushButton(window, text='Enter', command=openTheFile, width='fill', height=10)
    fileConfirm = Text(window, text='File has been retrieved successfully', visible=False)

def runTest():
    global students, ibm, react, reactiontime, runs, programend, starttime
    list_of_results = []
    window = Window(app, title='Run Test', height=700, width=1000, bg=darkblue)
    window.font = ibm
    spacer = Box(window, height=100, width=1000)
    react = Box(window, width='fill', height='fill')
    react.bg = [224, 251, 252]
    def testprocedure():
        global runs, programend, starttime, haschanged
        starttime = time.time()
        if runs == 0:
            window.info("Information", "Click as fast as you can when the color changes.")
        chosentime = round(random.uniform(2.00,5.00), 3)
        def buttonpress():
            global haschanged, runs, programend, currenttime, buttoncolorchange
            if haschanged:
                # Will only run if the button color has changed. If not, the user's click will not allow them to progress.
                finaltime=round(time.time()-buttoncolorchange, 3)*1000
                window.warn(window, text=f'Your reaction time: {finaltime} ms')
                list_of_results.append(finaltime)
                react.bg = [224,251,252]
                runs +=1
                if runs == 3:
                    # Completed all tests - print final results (lowest, average, place on leaderboard).
                    programend=True
                    react.destroy()
                    completion = Text(window, text='Tests completed!')
                    showbesttime = Text(window, text=f'Your best time: {min(list_of_results)}ms')
                    showaveragetime = Text(window, text=f'Your average time: {round(sum(list_of_results)/len(list_of_results),1)}')
                    averagetime = round((list_of_results[0]+list_of_results[1]+list_of_results[2])/3,3)
                    besttime = min(list_of_results)
                    runs=0
                    newStudent()
                else:
                    haschanged = False
                    testprocedure()
            else:
                # If the user clicks and the color has not changed, they are given a warning and they have to restart the current trial.
                window.warn('Warning','Button has not yet changed color')
                testprocedure()

        def counter():
            global haschanged, buttoncolorchange
            try:
                timer.value = int(timer.value) + 1
                # If the predetermined amount of time has passed, the color of the button will change.
                if int(timer.value) == int(chosentime):
                    react.bg=[238, 108, 77]
                    haschanged=True
                    buttoncolorchange=time.time()
                    react.when_clicked = buttonpress
            except:
                pass
        timer=Text(window, visible=False, text='0')
        timer.repeat(1000, counter)
        # Functions being used to save the student's information
        def indexStudent(results):
            # Using classes to create objects for each student
            s = Student()
            s.name = typeName.value
            s.age = ageinput.value
            s.bestTime=min(results)
            s.allTimes=results
            students.append(s)
            confirmation = Text(window, text=f'Student has been saved successfully.', color='white')

        def newStudent():
            global typeName, ageinput
            # Once the 3 trials have been completed, the student can then input their data.
            guide = Text(window, text='Input Student Name:')
            typeName = TextBox(window, width=100)
            guide2 = Text(window, text='Input Student Age:')
            ageinput = TextBox(window, width=100)
            submit = PushButton(window, text='Submit', command=indexStudent, args=[list_of_results], image='submitbutton.png')
            window.show(wait=True)

    testprocedure()


def openleaderboard():
    global students
    leaderBoard = Window(app, title='Leaderboard', height=700, width=1000, bg=darkblue)
    times = students
    # Takes all the students in the system and sorts them by time.
    # Then it outputs the top 10 school-wide.
    title=Text(leaderBoard, text='Top 10 Times School-Wide:', size=50)
    def getstudentinfo(student):
        # Takes the student's bestTime attribute and returns it.
        return student.bestTime
    # I can use the function to sort the terms in the 'times' list by the bestTime attribute.
    times.sort(key=getstudentinfo)
    scores = Text(leaderBoard, text='', visible=False, size=22)
    pos = 1
    # Sets a limit so only the first 10 times in the sorted list are printed.
    for j in times:
        if pos==11:
            break
        scores.append(f'{pos}. {j.name}: {int(j.bestTime)}ms \n')
        pos+=1

    def visualiser():
        # I use matplotlib to display the correlation between age and reaction time.
        # x-axis data
        ages = []
        # y-axis data
        xtimes = []
        for i in times:
            # Splits the list of students and takes only their age and bestTime (because this is all that will be plotted)
            ages.append(int(i.age))
            xtimes.append(int(i.bestTime))
        # Scatter plot object
        plt.scatter(ages, xtimes)
        # Axis titles
        plt.title("Age vs Reaction Time")
        plt.xlabel("Age")
        plt.ylabel("Reaction Time (ms)")
        plt.show()
    displayresultsbutton = PushButton(leaderBoard, text='Visualise Data', command=visualiser)

    def agegroupstats(sv):
        # Takes the top 10 times of any age group.
        # Probably more complicated than it needed to be
        agegroups=Box(leaderBoard, visible=False, height=200, width=400)
        agegroups.bg=orange
        includedstudents=[]
        for i in students:
            if i.age==sv:
                includedstudents.append(i)
        includedstudents.sort(key=getstudentinfo)
        includedtimes=[]
        for i in includedstudents:
            for x in i.allTimes:
                includedtimes.append(x)
        # Gives the best time and average time of the year group.
        agestats=Text(agegroups, text=f'Stats for age {sv}:\nAverage time: {int(sum(includedtimes)/len(includedtimes))}ms\nBest time: {min(includedtimes)}\nWorst time: {max(includedtimes)}')
        displaystudents=Text(agegroups, text=f'Age {sv} leaderboard:\n', visible=False)
        counter=1
        # Counter so only the first 10 times are shown.
        for x in includedstudents:
            displaystudents.append(f'{counter}. {x.name} - {x.bestTime}\n')
            counter+=1
            if counter==12:
                break
        displaystudents.visible=True
        agegroups.visible=True
        def destroy():
            # When the 'close' button is pressed, the mini box with the year-group specific data is closed.
            agegroups.destroy()
            closeall.destroy()
        closeall = PushButton(leaderBoard, command=destroy, text='close')
    scores.visible = True
    multiselect=Combo(leaderBoard, options=[12, 13, 14, 15, 16, 17, 18], command=agegroupstats)

def bruh():
    # Helped for figuring out what was wrong when something broke
    for i in students:
        print(f'{i.name} is {i.age} and their best time is {i.bestTime}ms')

# Menu screen buttons for each of the functions
title = Text(app, text='Menu', size=100, color=orange)
spacer = Box(app, height=100, width=100)
testbutton = PushButton(app, text='Test Reaction Time', command=runTest, image='reactiontimetest.png')
viewleaderboard = PushButton(app, text='View Leaderboard', command=openleaderboard)
savenclosebutton = PushButton(app, text='Save Data to File', command=saveClose, image='savenclose.png')
saveopenbutton = PushButton(app, text='Open Data from File', command=openAFile, image='openfromfile.png')
# This was just to help me figure out what wasn't working when something broke
#debugbutton=PushButton(app, text='frick', command=bruh)
app.display()
