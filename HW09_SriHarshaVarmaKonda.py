import os
import csv
from typing import List, DefaultDict, Any
from collections import defaultdict
from prettytable import PrettyTable


class University:
    def __init__(self, path: str) -> None:
        self.path: str = path
        self.directory = os.listdir(self.path)
        self.instructor_summary_dict: [str, DefaultDict[str, Any]] = defaultdict(dict)
        self.student_dict: [str, DefaultDict[str, Any]] = defaultdict(dict)
        self.instructor_dict: [str, DefaultDict[str, Any]] = defaultdict(dict)
        self.student_course: [str, List[str]] = defaultdict(list)
        self.instructor_course:[str, List[str]] = defaultdict(list)
        self.course_list: List = []
        self.pt_student: PrettyTable = PrettyTable(
            field_names=['CWID', 'NAME', 'COMPLETED COURSE'])
        self.pt_instructor: PrettyTable = PrettyTable(
            field_names=['CWID', 'NAME', 'DEPT', 'COURSE','STUDENTS'])
        
        for file in self.directory:
            """ This for loop is to get the CWID and Course of students to course_list """
            if file.endswith("grades.txt"):
                file_name = file
                print(file_name)
                try:
                    fp = open(file_name, "r")
                except FileNotFoundError:
                    print(f"{self.path}/{file_name} not found")
                else:
                    reader = csv.reader(fp, dialect="excel-tab")
                    for index, line in enumerate(reader):
                        if len(line) != 4:
                            raise ValueError(
                            f"{self.path}/{file_name} has {len(line)} fields on line {index} but expected 3")
                        else:
                            self.course_list.append(line)

    def student(self) -> PrettyTable:
        """ Getting student details and printing a pretty table"""

        for file in self.directory:
            """ This for loop is to get student CWID and NAME into self.student_dict """
            if file.endswith("students.txt"):
                file_name = file
                try:
                    fp = open(file_name, "r")
                except FileNotFoundError:
                    print(f"{self.path}/{file_name} not found")
                else:
                    reader = csv.reader(fp, dialect="excel-tab")
                    for index, line in enumerate(reader):
                        if len(line) != 3:
                            raise ValueError(
                                f"{self.path}/{file_name} has {len(line)} fields on line {index} but expected 3")
                        else:
                            self.student_dict[line[0]]["name"] = line[1]

        for i in self.course_list:
            """ This for loop is to convert course_list of type list to student_course of type dictionary """
            self.student_course[i[0]].append(i[1])

        for i in self.student_course:
            """ Sorting the list of courses in student_course """
            self.student_course[i].sort()   

        for i in self.student_dict:
            """ Adding the list of courses from student_course to student_dict """
            for j in self.student_course:
                if i == j:
                    self.student_dict[i]["course"] = self.student_course[j]

        for key in self.student_dict:
            """ Printing the pretty table """
            self.pt_student.add_row([key, self.student_dict[key]['name'], self.student_dict[key]
                                     ['course']])
        return self.pt_student

    def instructor(self) -> PrettyTable:
        for file in self.directory:
            """ This for loop is to get information of instructors from file to instructor_dict """
            if file.endswith("instructors.txt"):
                file_name = file
                try:
                    fp = open(file_name, "r")
                except FileNotFoundError:
                    print(f"{self.path}/{file_name} not found")
                else:
                    reader = csv.reader(fp, dialect="excel-tab")
                    for index, line in enumerate(reader):
                        if len(line) != 3:
                            raise ValueError(
                                f"{self.path}/{file_name} has {len(line)} fields on line {index} but expected 3")
                        else:
                            self.instructor_dict[line[0]]["name"] = line[1]
                            self.instructor_dict[line[0]]["dept"] = line[2]
            
        for i in self.course_list:
            """ Getting courses and instructors """
            self.instructor_course[i[1]].append(i[3])
        
        for i in self.instructor_course:
            """ Getting all the recors for instructor_summary into instructor_summary_dict """
            for j in self.instructor_dict:
                if self.instructor_course[i][0] == j:
                    self.instructor_summary_dict[i]["cwid"] = j
                    self.instructor_summary_dict[i]["name"] = self.instructor_dict[j]["name"]
                    self.instructor_summary_dict[i]["dept"] = self.instructor_dict[j]["dept"]
                    self.instructor_summary_dict[i]["students"] = len(self.instructor_course[i])

        for key in self.instructor_summary_dict:
            """ Printing the pretty table """
            self.pt_instructor.add_row([self.instructor_summary_dict[key]['cwid'], self.instructor_summary_dict[key]['name'], self.instructor_summary_dict[key]['dept'], key, self.instructor_summary_dict[key]
                                     ['students']])

        return self.pt_instructor    


uni = University("C:/PYTHON/Student-Repository")
print(uni.student())
print(uni.instructor())
