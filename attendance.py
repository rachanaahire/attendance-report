import os
import glob
import csv
import codecs

if (os.path.exists('Report.csv')):
    print("Report already created!!\nPlease check: "+os.getcwd()+"\Report.csv")
else:
    path = os.getcwd()
    csv_files = glob.glob(os.path.join(path, "*.csv"))

    # Count csv files in current folder to get Total Working days
    print("Total working days: ", len(csv_files))
    total_attendance = len(csv_files)

    # To exclude teacher from attendance calculation
    teacher = input("Enter the Teacher Name: ")
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
                if row[0] not in dict_student.keys() and 'Guest' not in row[0] and row[0] != teacher:
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
        print("Attendace report created Successfully!!\nPlease check: "+os.getcwd()+"\Report.csv")
