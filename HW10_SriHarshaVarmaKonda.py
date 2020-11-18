import os
import csv
from typing import List, DefaultDict, Any
from collections import defaultdict
from prettytable import PrettyTable


class University:
    def __init__(self, path: str) -> None:
        """ Initializing all the required elements """
        self.path: str = path
        self.directory = os.listdir(self.path)
        self.instructor_summary_dict: [
            str, DefaultDict[str, Any]] = defaultdict(dict)
        self.student_dict: [str, DefaultDict[str, Any]] = defaultdict(dict)
        self.instructor_dict: [str, DefaultDict[str, Any]] = defaultdict(dict)
        self.student_course: [str, List[str]] = defaultdict(list)
        self.student_grade_list: [str, List[str]] = defaultdict(list)
        self.student_remaining_required: [str, List[str]] = defaultdict(list)
        self.student_remaining_elective: [str, List[str]] = defaultdict(list)
        self.instructor_course: [str, List[str]] = defaultdict(list)
        self.major_required_dict: [str, List[str]] = defaultdict(list)
        self.major_elective_dict: [str, List[str]] = defaultdict(list)
        self.major_dict: [str, DefaultDict[str, Any]] = defaultdict(dict)
        self.course_list: List = []
        self.pt_student: PrettyTable = PrettyTable(
            field_names=['CWID', 'NAME', 'MAJOR', 'COMPLETED COURSE', 'REMAINING REQUIRED', 'REMAINING ELECTIVE', 'GPA'])
        self.pt_instructor: PrettyTable = PrettyTable(
            field_names=['CWID', 'NAME', 'DEPT', 'COURSE', 'STUDENTS'])
        self.pt_major: PrettyTable = PrettyTable(
            field_names=['MAJOR', 'REQUIRED', 'ELECTIVE'])

        for file in self.directory:
            """ This for loop is to get the CWID and Course of students to course_list """
            if file.endswith("grades.txt"):
                file_name = file
                try:
                    fp = open(file_name, "r")
                except FileNotFoundError:
                    print(f"{self.path}/{file_name} not found")
                else:
                    reader = csv.reader(fp, delimiter="|")
                    for index, line in enumerate(reader):
                        if index != 0:
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
                    reader = csv.reader(fp, delimiter=";")
                    for index, line in enumerate(reader):
                        if index != 0:
                            if len(line) != 3:
                                raise ValueError(
                                    f"{self.path}/{file_name} has {len(line)} fields on line {index} but expected 3")
                            else:
                                self.student_dict[line[0]]["name"] = line[1]
                                self.student_dict[line[0]]["major"] = line[2]

        for i in self.student_dict:
            """ Initializing student_grade_list """
            self.student_grade_list[i] = []

        minimum_grade_requirement: List[str] = [
            'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']
        for i in self.course_list:
            """ This for loop is to convert course_list of type list to student_course of type dictionary """
            if i[2] not in minimum_grade_requirement:
                continue
            else:
                self.student_course[i[0]].append(i[1])
                self.student_grade_list[i[0]].append(i[2])

        for i in self.student_course:
            """ Sorting the list of courses in student_course """
            self.student_course[i].sort()

        for i in self.student_dict:
            """ Initializing completed courses, remaining_required & remaining_elective in student_dict """
            self.student_dict[i]["course"] = []
            self.student_dict[i]["remaining_required"] = []
            self.student_dict[i]["remaining_elective"] = []

        for i in self.student_dict:
            """ Adding the list of courses from student_course to student_dict """
            for j in self.student_course:
                if i == j:
                    self.student_dict[i]["course"] = self.student_course[j]

        uni = University("/Users/harru/PYTHON(SSW 810 )")
        uni.major()

        for i in self.student_dict:
            for j in uni.major_dict:
                if self.student_dict[i]['major'] == j:
                    for k in uni.major_dict[j]['required']:
                        if k not in self.student_dict[i]['course']:
                            self.student_remaining_required[i].append(k)

        for i in self.student_dict:
            """ Adding remaining_required courses to student dict """
            for j in self.student_remaining_required:
                if i == j:
                    self.student_dict[i]["remaining_required"] = self.student_remaining_required[j]

        for i in self.student_dict:
            for j in uni.major_dict:
                if self.student_dict[i]['major'] == j:
                    for k in uni.major_dict[j]['elective']:
                        if k not in self.student_dict[i]['course']:
                            self.student_remaining_elective[i].append(k)

        for i in self.student_dict:
            """ Adding remaining_elective courses to student dict """
            for j in self.student_remaining_elective:
                if i == j:
                    self.student_dict[i]["remaining_elective"] = self.student_remaining_elective[j]

        grade_value_dict: [str, int] = {"A": 4.0,
                                        "A-": 3.75,
                                        "B+": 3.25,
                                        "B": 3.0,
                                        "B-": 2.75,
                                        "C+": 2.25,
                                        "C": 2.0}

        for i in self.student_grade_list:
            numer = 0
            den = 0
            for j in self.student_grade_list[i]:
                numer += grade_value_dict[j]
            den = len(self.student_grade_list[i])
            if den == 0:
                self.student_dict[i]['gpa'] = 0
            else:
                self.student_dict[i]['gpa'] = numer/den

        for key in self.student_dict:
            """ Printing the pretty table """
            self.pt_student.add_row([key, self.student_dict[key]['name'], self.student_dict[key]['major'], self.student_dict[key]
                                     ['course'], self.student_dict[key]["remaining_required"], self.student_dict[key]["remaining_elective"],  self.student_dict[key]['gpa']])
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
                    reader = csv.reader(fp, delimiter="|")
                    for index, line in enumerate(reader):
                        if index != 0:
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
                    self.instructor_summary_dict[i]["students"] = len(
                        self.instructor_course[i])

        for key in self.instructor_summary_dict:
            """ Printing the pretty table """
            self.pt_instructor.add_row([self.instructor_summary_dict[key]['cwid'], self.instructor_summary_dict[key]['name'], self.instructor_summary_dict[key]['dept'], key, self.instructor_summary_dict[key]
                                        ['students']])

        return self.pt_instructor

    def major(self) -> None:
        for file in self.directory:
            if file.endswith("majors.txt"):
                file_name = file
                try:
                    fp = open(file_name, "r")
                except FileNotFoundError:
                    print(f"{self.path}/{file_name} not found")
                else:
                    reader = csv.reader(fp, dialect="excel-tab")
                    for index, line in enumerate(reader):
                        if index != 0:
                            if len(line) != 3:
                                raise ValueError(
                                    f"{self.path}/{file_name} has {len(line)} fields on line {index} but expected 3")
                            else:
                                if line[1] == 'R':
                                    self.major_required_dict[line[0]].append(
                                        line[2])
                                elif line[1] == 'E':
                                    self.major_elective_dict[line[0]].append(
                                        line[2])

        for i in self.major_required_dict:
            """ Getting COURSE NAME - REQUIRED & ELECTIVE COURSES into one dictionary => self.major_dict"""
            for j in self.major_elective_dict:
                if i == j:
                    self.major_dict[i]['required'] = self.major_required_dict[i]
                    self.major_dict[i]['elective'] = self.major_elective_dict[j]

        for key in self.major_dict:
            """ Printing the pretty table """
            self.pt_major.add_row([key, self.major_dict[key]['required'], self.major_dict[key]
                                   ['elective']])
        return self.pt_major


# uni = University("/Users/harru/PYTHON(SSW 810 )")
# print(uni.student())
# print(uni.instructor())
# print(uni.major())
