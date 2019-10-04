# Billsplit.py
# GUI version
# Added to github under velocity301
# currently working on adding a tip button and box
# next will be the checkbox state logic and math splitting it between people
from tkinter import *
personBoxes = []
personList = []
foodBoxes = []
# foodCostBoxes = []
foodColumnLabels = []
costBoxes = []
checkBoxes = []
checkButtons = []
foodItemList = []


class Person():
    def __init__(self, name, cost):
        self.name = name
        self.cost = 0
        if len(self.name) > 4:
            self.abbreviation = self.name[0:4]
        else:
            self.abbreviation = self.name
        print(str(self.name) + "\t" + str(self.cost))

    def __str__(self):
        return(str(self.name) + "\t" + str(self.cost))

    def tax():
        self.cost *= taxPercentage / 100


class FoodItem():
    def __init__(self, cost, peopleSharing):
        self.cost = cost
        self.peopleSharing = peopleSharing
        self.waysToSplit = len(peopleSharing)

    def __str__(self):
        return(str(self.cost) + "\t" + str(self.peopleSharing))


class Check():
    def __init__(self, column, row, whose, checkButtons):
        self.var = IntVar()
        c = Checkbutton(variable=self.var, command=self.state)
        checkButtons.append(c)
        c.grid(column=column, row=row)
        self.whose = whose

    def state(self):
        return self.var.get()

    def destroyBox(self):
        self.grid_forget()  # self.pack_forget()


class BoxCount:
    def __init__(self):
        self.counter = 2

    def increment(self):
        self.counter += 1

    def decrement(self):
        self.counter -= 1

    def get_value(self):
        return self.counter


def AddFoodEntryBox(foodBoxCount):
    foodBoxX = Entry()
    foodBoxes.append(foodBoxX)
    foodBoxX.grid(column=0, row=foodBoxCount.get_value())

    costBoxX = Entry()
    costBoxes.append(costBoxX)
    costBoxX.grid(column=1, row=foodBoxCount.get_value())

    foodBoxCount.increment()

    for i in range(len(personList)):
        checkBoxes.append(
            Check(i + 2, foodBoxCount.get_value() - 1, personList[i], checkButtons))
    # print(checkBoxes)


def SubtractFoodEntryBox(foodBoxCount):
    foodBoxes[-1].destroy()
    del foodBoxes[-1]
    costBoxes[-1].destroy()
    del costBoxes[-1]
    print(checkButtons)
    for i in range(len(personList)):
        checkButtons[-1].destroy()
        del checkButtons[-1]
        del checkBoxes[-1]


def AddPersonEntryBox(personBoxCount):
    personBoxX = Entry()
    personBoxes.append(personBoxX)
    personBoxX.grid(column=0, row=personBoxCount.get_value() + 1)
    personBoxCount.increment()
    # print(personBoxCount.get_value())
    # print(personBoxes)


def SubtractPersonEntryBox(personBoxCount):
    personBoxes[-1].destroy()
    del personBoxes[-1]
    personBoxCount.decrement()
    # print(personBoxCount.get_value())
    # print(personBoxes)


personBoxCount = BoxCount()
foodBoxCount = BoxCount()
foodBoxCount.decrement()


def NextButton(personList, root):
    for i in personBoxes:
        personList.append(Person(i.get(), 0))
        # print(personList)

    UI2(root)


def Finalize(personList, root, tipEntry, costBoxes, foodWindow):
    tipPercentage = eval(tipEntry) / 100
    rowLength = len(personList)
    foodCosts = []
    currentRow = []
    for i in costBoxes:
        foodCosts.append(float(i.get()))
        for j in checkBoxes[rowLength * costBoxes.index(i):rowLength * (costBoxes.index(i) + 1)]:
            if j.state() == 1:
                currentRow.append(checkBoxes.index(j) % rowLength)
        foodItemList.append(FoodItem(float(i.get()), currentRow))
        currentRow = []
    for i in foodItemList:
        for j in range(rowLength):
            if j in i.peopleSharing:
                (personList[j]).cost += i.cost / len(i.peopleSharing)
    for i in personList:
        i.cost *= (1 + tipPercentage)
        print(i)
    UI3(foodWindow, personList)


def UI():
    root = Tk()

    # Column 1: Label(People), Box1, Box2, Box3
    peopleLabel = Label(text="People")
    personBox1 = Entry()
    personBoxes.append(personBox1)
    personBox2 = Entry()
    personBoxes.append(personBox2)
    peopleLabel.grid(column=0, row=0)
    personBox1.grid(column=0, row=1)
    personBox2.grid(column=0, row=2)
    addSubLabel = Label(text="Add or Subtract People")
    minusButton = Button(
        text="   -   ", command=lambda: SubtractPersonEntryBox(personBoxCount))
    plusButton = Button(
        text="  +  ", command=lambda: AddPersonEntryBox(personBoxCount))
    nextButton1 = Button(
        text="Next", command=lambda: NextButton(personList, root))
    addSubLabel.grid(column=1, row=0, columnspan=2)
    minusButton.grid(column=1, row=1, sticky=E)
    plusButton.grid(column=2, row=1, sticky=W)
    nextButton1.grid(column=2, row=100, sticky=E)

    mainloop()

# this is the second screen with food items and costs


def UI2(root):

    root.destroy()
    foodWindow = Tk()
    AddSubLabel2 = Label(text="Add or Subtract Food Items",
                         borderwidth=2, relief="sunken")
    FoodLabel = Label(text="Food Items", borderwidth=2, relief="solid")
    FoodCostLabel = Label(text="Cost of Item ($)",
                          borderwidth=2, relief="solid")
    minusButton2 = Button(
        text="   -   ", command=lambda: SubtractFoodEntryBox(foodBoxCount))
    plusButton2 = Button(
        text="  +  ", command=lambda: AddFoodEntryBox(foodBoxCount))
    tipLabel = Label(text="Tip %")
    tipLabel.grid(column=2 + len(personList), row=2)
    tipEntry = Entry()
    tipEntry.insert(0, "15")
    tipEntry.grid(column=2 + len(personList), row=3)

    finalizeButton = Button(
        text="Complete", command=lambda: Finalize(personList, root, tipEntry.get(), costBoxes, foodWindow))
    for i in personList:
        foodColumnLabels.append(
            Label(text=i.abbreviation, borderwidth=2, relief="ridge"))
    for i in foodColumnLabels:
        i.grid(column=foodColumnLabels.index(i) + 2, row=0)

    FoodLabel.grid(column=0, row=0)
    FoodCostLabel.grid(column=1, row=0)
    minusButton2.grid(column=2 + len(personList), row=1, sticky=E)
    plusButton2.grid(column=3 + len(personList), row=1, sticky=W)
    AddSubLabel2.grid(column=2 + len(personList), row=0, columnspan=2)
    finalizeButton.grid(column=100, row=100)
    AddFoodEntryBox(foodBoxCount)


def UI3(foodWindow, personList):
    foodWindow.destroy()
    resultsWindow = Tk()
    NAME = Label(text="Name: ")
    NAME.grid(column=0, row=0)
    TOTAL = Label(text="Total: ")
    TOTAL.grid(column=2, row=0, sticky=W)
    personLabelList = []
    costLabelList = []
    for i in personList:
        personLabelList.append(Label(text=i.name))
        costLabelList.append(Label(text="$" + str(round(i.cost, 2))))
    for i in personLabelList:
        i.grid(column=0, row=1 + personLabelList.index(i))
    for i in costLabelList:
        i.grid(column=2, row=1 + costLabelList.index(i))


def main():
    UI()


main()
