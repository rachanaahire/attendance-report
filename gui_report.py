from tkinter import *
import os
import glob
import csv
import codecs

class Table:
    def __init__(self, root,data,num):
        trows = len(data)
        tcols = len(data[0])
        for i in range(num, trows+num):
            for j in range(tcols):
                self.cell = Entry(root)
                # print(i,j)
                self.cell.grid(row=i,column=j)
                self.cell.insert(END, data[i-num][j])
        

class MyWindow:
    options = []    
    def __init__(self, master):
        self.master = master
        master.title("Student Attendance Report")
        self.tname_data = StringVar()

        Label(self.master, bg='#e3f5a2', text="Enter Subject Code:").grid(row=0, column=0,padx=10, pady=(20,0))
        Entry(root, textvariable=StringVar(), width=40, font=('calibre', 10, 'normal')).grid(row=0,column=1,columnspan=2, pady=(20,0))
        Label(self.master, bg='#e3f5a2', text="Enter name of Teacher:").grid(row=1,column=0,padx=10, pady=(10,0))
        Entry(root, textvariable=self.tname_data, width=40, font=('calibre', 10, 'normal')).grid(row=1,column=1, columnspan=2, pady=(10,0))
        Button(root, text="Generate Attendance", command=self.generate_attendance, bg="#1dc44f", fg="white").grid(row=1,column=3, padx=10, pady=(10,0))

    def after_generate(self):
        Button(self.master, text="Get Students below\n 75% Attendance", bg="#1dc44f", command=self.below_attendance, fg="white").grid(row=2,column=0,padx=10, pady=(40,0))
        Button(self.master, text="Get Specific Student\n Attendance Details", command=self.get_attendance, bg="#1dc44f", fg="white").grid(row=3,column=0,padx=10, pady=(6,40))

    def generate_attendance(self):
        if (os.path.exists('Report.csv')):
            Label(self.master, text = "Report already created!!\nCheck the below path:\n"+os.getcwd()+"\Report.csv", fg='red').grid(row=1,column=4, padx=10)
            self.after_generate()
        else:
            pathname = os.getcwd()
            csv_files = glob.glob(os.path.join(pathname, "*.csv"))

            # Count csv files in current folder to get Total Working days
            total_attendance = len(csv_files)

            teacher = self.tname_data.get().upper()
            data = []  # Contains non-repeated all attendance data
            dict_student = {}  # To store student data
            for file in csv_files:
                csv_reader = csv.reader(codecs.open(file, 'r', 'UTF-16le'))
                next(csv_reader)
                stud_present = [] # Attendance of that day
                for line in csv_reader:
                    row = line[0].split("\t")
                    if row[0] not in stud_present:
                        stud_present.append(row[0])
                        row.append(line[1])
                        data.append(row)

                        # to get total students dict
                        if row[0] not in dict_student.keys() and 'Guest' not in row[0] and row[0].upper() != teacher:
                            dict_student[row[0]] = [0]
            
            # calculate present attendace
            for row in data:
                if row[0] in dict_student.keys():
                    dict_student[row[0]][0] += 1

            print("No. of Students: ", len(dict_student))

            # to calculate rest data
            for attendance in dict_student.values():
                # calculate absent days
                present = attendance[0]
                absent = total_attendance-present
                attendance.append(absent)

                # calculate percentage
                percent = round((present/total_attendance)*100, 2)
                attendance.append(percent)

            # Creating rows/lines to write in csv
            rows = [[name] + datalist for name, datalist in dict_student.items()]
            with open('Report.csv', 'w', newline='') as new_file:
                csv_writer = csv.writer(new_file)
                csv_writer.writerow(["Name", "Present", "Absent", "Percentage"])
                for row in rows:
                    csv_writer.writerow(row)
                Label(self.master, text = "Attendace Report Successfully Created\nOn the below path:\n"+os.getcwd()+"\Report.csv", fg='green').grid(row=1,column=4, padx=10)
                self.after_generate()
    
    def below_attendance(self):
        data = [["Name", "Present","Absent", "Percent"]]
        csv_reader = csv.reader(open('Report.csv', 'r'))
        next(csv_reader)
        for line in csv_reader:
            if int(float(line[3])) < 75:
                data.append(line)

        Label(root,font= 'Arial 10 bold', text="Students below 75 percent attendance: ").grid(row=7,column=0,columnspan=2, pady=(40,5))
        myTable = Table(root, data, 8)

    def get_attendance(self):
        options = []
        csv_reader = csv.reader(open('Report.csv', 'r'))
        next(csv_reader)
        for line in csv_reader:
            options.append(line[0])
        
        self.clicked = StringVar()
        self.clicked.set("Click on this Dropdown\t")
        Label(self.master, bg='#e3f5a2', font= 'Arial 10 bold', text="Select the \nStudent Name:").grid(row=4, column=0, padx=(10,0))
        OptionMenu( self.master , self.clicked , *options ).grid(row=4, column=1)
        Button( self.master , text = "Get Details", command=self.show, bg="#1dc44f", fg="white").grid(row=4, column=2)

    def show(self):
        details = [["Name", "Present","Absent", "Percent"]]
        csv_reader = csv.reader(open('Report.csv', 'r'))
        next(csv_reader)
        for line in csv_reader:
            if (line[0]==self.clicked.get()):
                details.append(line)

        table = Table(self.master, details, 5)


root = Tk()
root.geometry("900x600")
root.configure(background='#a0d9c6')
my_gui = MyWindow(root)

root.mainloop()
