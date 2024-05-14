import pytest

def test_instance():
    assert isinstance('this is str',str)
    assert not isinstance('10',int)

def test_boolean():
    validated = True
    assert(validated is True)


class Student:
    def  __init__(self,first_name:str,last_name: str,major:str,years:int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years

@pytest.fixture
def default_employee():
    return Student('john','Doe','computer science',4)

def test_student_initialization(default_employee):
    assert default_employee.first_name == 'john','First name should be john'
    assert default_employee.last_name == 'Doe','Last name should be Doe'
    assert default_employee.major == 'computer science'
    assert default_employee.years == 4