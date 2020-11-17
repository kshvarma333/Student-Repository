from HW09_SriHarshaVarmaKonda import University
import unittest

class TestHomeWork9Functions(unittest.TestCase):
    def test_student(self) -> None:
        u = University("/Users/harru/PYTHON(SSW 810 )")
        self.assertNotEqual(u.student(), ValueError)
        self.assertNotEqual(u.student(), FileNotFoundError)

    def test_instructor(self)-> None:
        u = University("/Users/harru/PYTHON(SSW 810 )")
        self.assertNotEqual(u.student(), ValueError)
        self.assertNotEqual(u.student(), FileNotFoundError)




def main():
    unittest.main(exit=False, verbosity=2)


if __name__ == '__main__':
    main()