import random
import csv
import time

class Skill():
    def __init__(self, name, atributeStr, atributeVal,  difficulty=0, points=1):
        """
            Default to 0 (easy) and 1 point spent
        """

        # Error checking
        assert(type(atributeStr) == type(str()))
        assert(type(atributeVal) == type(int()))
        assert(type(difficulty) == type(int()))
        assert(type(points) == type(int()))
        assert(points>0)

        self.Name=name
        self.AtributeString = atributeStr
        self.AtributeValue = atributeVal
        self.Difficulty = difficulty
        self.Points = points
        self.CalcSkillMod()


    def CalcSkillMod(self):
        assert(self.Points > 0)
        if(self.Points < 4):
            self.SkillMod = int(self.Points / 2) 
        else:
            self.SkillMod = int(self.Points/4) + 1
        if( self.Difficulty == 0 ):
             pass
        elif( self.Difficulty == 1 ):
             self.SkillMod -= 1
        elif( self.Difficulty == 2 ):
             self.SkillMod -= 2
        elif( self.Difficulty == 3 ):
             self.SkillMod -= 3
        else:
            print "INVALID DIFFiCULTY!"
            assert(False)

    def SetAtrib(self, atributeStr, atributeVal):
        self.AtributeString = atributeStr
        self.AtributeValue = atributeVal

    def ModPoints(self, deltaPoints):
        self.Points += deltaPoints
        self.CalcSkillMod()
    
    def SetPoints(self, newPoints):
        self.Points = newPoints
        self.CalcSkillMod()

    def Check(self, mods=0):
        dieRoll = list()
        for i in range(3):
            dieRoll.append(random.randint(1,6))
        return  (self.SkillMod + self.AtributeValue) - sum(dieRoll)

    def Print(self):
        print "%s-%d (%+d)" %(self.Name, self.SkillMod + self.AtributeValue, self.SkillMod)


class CharSheet():
    
    def __init__(self,default=10):
        self.name   = "DEFAULT"
        self.ST     = default
        self.DX     = default
        self.IQ     = default
        self.HT     = default
        self.HP     = self.ST
        self.WILL   = self.IQ
        self.PER    = self.IQ
        self.FP     = self.HT
        self.Skills = dict()

        self.Height=0
        self.Weight=0
        self.Points=0+(default-10)*(10+20+20+10)
    
    def Roll(self,points=0):
        self.Height = random.gauss(1.778,0.15)

        self.GenerateName()

        statsSelection = ["ST","ST","DX","DX","IQ","IQ","HT","HT","HP","WILL","PER","FP"]

        while(self.Points < points):
            # Spend points on stuff!
            selection = random.choice(statsSelection)

            if(selection == "ST"):
                self.ST+=1
                self.HP+=1
                self.Points+=10

            elif(selection == "DX"):
                self.DX+=1
                self.Points+=20

            elif(selection == "IQ"):
                self.IQ+=1
                self.WILL+=1
                self.PER+=1
                self.Points+=20

            elif(selection == "HT"):
                self.HT+=1
                self.FP+=1
                self.Points+=10

            elif(selection == "HP" and self.HP+1 <= self.ST*1.3):
                # Limited to +/- 30% of ST
                self.HP+=1
                self.Points+=2

            elif(selection == "WILL" and self.WILL <=20):
                self.WILL+=1
                self.Points+=5

            elif(selection == "PER" and self.PER <= 20):
                self.PER+=1
                self.Points+=5

            elif(selection == "FP" and self.FP+1 <= self.HT*1.3):
                self.FP+=1
                self.Points+=3

    def __str__(self):
        return self.name

    def PrintStats(self):
        print "Name:",self.name
        print " ST:",self.ST
        print " DX:",self.DX
        print " IQ:",self.IQ
        print " HT:",self.HT
        print " HP:",self.HP
        print " WILL:",self.WILL
        print " PER:",self.PER
        print " FP:",self.FP
        print " Points:",self.Points

    def GenerateName(self,gender="male"):
        self.name = self.ParseNameFile('firstnames.csv',gender) + " " + self.ParseNameFile('lastnames.csv')

    def ParseNameFile(self,namesFile,gender="male"):
        with open(namesFile,'r') as namesFile:
            nameReader = csv.reader(namesFile)
            firstNamesMale = list()
            firstNamesFemale = list()

            # Skip the header
            nameReader.next()
            for i in nameReader:
                firstNamesMale.append(i[1:3])
                if(gender=="female"):
                    firstNamesFemale.append(i[3:5])

        # Convert counts to ints    
        if(gender=="male"):
            for i in firstNamesMale:
                i[1]=int(i[1])
        elif(gender=="female"): 
            for i in firstNamesFemale:
                i[1]=int(i[1])

        # Prep ints for random selection
        if(gender=="male"):
            runningTotalMale=0
            for i in firstNamesMale:
                i[1]=i[1]+runningTotalMale
                runningTotalMale=i[1]
        if(gender=="female"):
            runningTotalFemale=0
            for i in firstNamesFemale:
                i[1]=i[1]+runningTotalFemale
                runningTotalFemale=i[1]

        if(gender=="male"):
            selecton = random.randint(0,runningTotalMale)
            for i in firstNamesMale:
                if selecton <= i[1]:
                    return i[0].title()

        elif(gender=="female"):
            selecton = random.randint(0,runningTotalFemale)
            for i in firstNamesFemale:
                if selecton <= i[1]:
                    return i[0].title()


            





