from HW11_SriHarshaVarmaKonda import University
import unittest

class TestHomeWork10Functions(unittest.TestCase):

    def test_student(self) -> None:
        """ Testing student """
        uni = University("/Users/harru/PYTHON(SSW 810 )")
        uni.student()
        lis = []
        for key in uni.student_dict:
            lis.append(uni.student_dict[key])
        result: list = [{'name': 'Jobs, S', 'major': 'SFEN', 'course': ['CS 501', 'SSW 810'], 'remaining_required': ['SSW 540', 'SSW 555'], 'remaining_elective': ['CS 546'], 'gpa': 3.375}]
        self.assertEqual(lis[0], result[0])

    def test_instructor(self) -> None:
        uni = University("/Users/harru/PYTHON(SSW 810 )")
        uni.instructor()
        lis = []
        for key in uni.instructor_summary_dict:
            lis.append(uni.instructor_summary_dict[key])
        result: list = [{'cwid': '98763', 'name': 'Rowland, J', 'dept': 'SFEN', 'students': 4}]
        self.assertEqual(lis[0], result[0])

    def test_major(self) -> None:
        uni = University("/Users/harru/PYTHON(SSW 810 )")
        uni.major()
        lis = []
        for key in uni.major_dict:
            lis.append(uni.major_dict[key])
        result: list = [{'required': ['SSW 540', 'SSW 810', 'SSW 555'], 'elective': ['CS 501', 'CS 546']}]
        self.assertEqual(lis[0], result[0])

    def test_student_grades_table_db(self) -> None:
        uni = University("/Users/harru/PYTHON(SSW 810 )")
        uni.student_grades_table_db("/Users/harru/PYTHON(SSW 810 )/HW11.db")
        result: list = ('Bezos, J', '10115', 'SSW 810', 'A', 'Rowland, J')
        lis = uni.student_grade_list_db[0]
        self.assertEqual(lis, result)

        




def main():
    unittest.main(exit=False, verbosity=2)


if __name__ == '__main__':
    main()

