from HW10_SriHarshaVarmaKonda import University
import unittest

class TestHomeWork10Functions(unittest.TestCase):

    def test_student(self) -> None:
        """ Testing student """
        uni = University("/Users/harru/PYTHON(SSW 810 )")
        uni.student()
        lis = []
        for key in uni.student_dict:
            lis.append(uni.student_dict[key])
        result: list = [{'name': 'Baldwin, C', 'major': 'SFEN', 'course': ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687'], 'remaining_required': ['SSW 540', 'SSW 555'], 'remaining_elective': ['CS 513', 'CS 545'], 'gpa': 3.4375}]
        self.assertEqual(lis[0], result[0])

    def test_instructor(self) -> None:
        uni = University("/Users/harru/PYTHON(SSW 810 )")
        uni.instructor()
        lis = []
        for key in uni.instructor_summary_dict:
            lis.append(uni.instructor_summary_dict[key])
        result: list = [{'cwid': '98765', 'name': 'Einstein, A', 'dept': 'SFEN', 'students': 4}]
        self.assertEqual(lis[0], result[0])

    def test_major(self) -> None:
        uni = University("/Users/harru/PYTHON(SSW 810 )")
        uni.major()
        lis = []
        for key in uni.major_dict:
            lis.append(uni.major_dict[key])
        result: list = [{'required': ['SSW 540', 'SSW 564', 'SSW 555', 'SSW 567'], 'elective': ['CS 501', 'CS 513', 'CS 545']}]
        self.assertEqual(lis[0], result[0])




def main():
    unittest.main(exit=False, verbosity=2)


if __name__ == '__main__':
    main()

