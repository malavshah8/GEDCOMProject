from unittest import TestCase
import os
from .parser import GEDCOMParser

from .userStoriesValidation import birth_before_marriage, birth_before_death
from .classModels import individualPerson, familyClass

cur_path = os.path.dirname(__file__)

FAIL_DIR = "gedcom_files/fail/"
PASS_DIR = "gedcom_files/pass/"

fail_file = os.path.relpath("..\\" + FAIL_DIR + acceptfile, cur_path)
pass_file = os.path.relpath("..\\" + PASS_DIR + acceptfile, cur_path)

acceptfile = "/Users/malavshah/GEDCOMProject/gedcom_files/pass/Family.ged"
fail_file1 = "/Users/malavshah/GEDCOMProject/gedcom_files/fail/Family.ged"

class test_birth_before_marriage(TestCase):

    def test_birth_before_marriage_1(self):
        individuals, families = GEDCOMParser(pass_file)
        self.assertTrue(birth_before_marriage(individuals, families))

    def test_birth_before_marriage_2(self):
        individuals, families = GEDCOMParser(pass_file)
        for family in families:
            if family.marriage:
                husband = None
                wife = None
                for indiv in individuals:
                    if indiv.uid == family.husband:
                        husband = indiv
                    if indiv.uid == family.wife:
                        wife = indiv
                self.assertNotEquals(husband.birthday, wife.birthday)


    def test_birth_before_marriage_3(self):
        individuals, families = GEDCOMParser(fail_file)
        self.assertFalse(birth_before_marriage(individuals, families))

    def test_birth_before_marriage_4(self):
        individuals, families = GEDCOMParser(pass_file)
        self.assertIsNot(individuals, familyClass)

    def test_birth_before_marriage_5(self):
        individuals, families = GEDCOMParser(pass_file)
        self.assertNotIsInstance(families,individualPerson)

class test_birth_before_death(TestCase):
    def test_birth_before_death1(self):
        individuals, _ = GEDCOMParser(acceptfile)
        self.assertTrue(birth_before_death(individuals))

    def test_birth_before_death2(self):
        individuals, _ = GEDCOMParser(acceptfile)
        self.assertEqual(birth_before_death(individuals),True)

    def test_birth_before_death3(self):
        individuals, _ = GEDCOMParser(acceptfile)
        self.assertIsNot(birth_before_death(individuals),False)

    def test_birth_before_death4(self):
        individuals, _ = GEDCOMParser(fail_file1)
        self.assertIsNotNone(birth_before_death(individuals))

    def test_birth_before_death5(self):
        individuals, _ = GEDCOMParser(acceptfile)
        self.assertIs(birth_before_death(individuals),True)