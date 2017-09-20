import pytest
import unittest.mock
import canvas2nbgrader as c2nb
import io

grades_csv = '''\
Student,ID,SIS User ID,SIS Login ID,Section,Computer lab: Basic Python (23769),Computer lab: basic Unix (23892),Computer lab:git (24233),Uppgifter Current Points,Uppgifter Final Points,Uppgifter Current Score,Uppgifter Unposted Current Score,Uppgifter Final Score,Uppgifter Unposted Final Score,Assignments Current Points,Assignments Final Points,Assignments Current Score,Assignments Unposted Current Score,Assignments Final Score,Assignments Unposted Final Score,Current Points,Final Points,Current Score,Unposted Current Score,Final Score,Unposted Final Score
    Points Possible,,,,,"0,0","0,0","0,0",(läs endast),(läs endast),(läs endast),(läs endast),(läs endast),(läs endast),(läs endast),(läs endast),(läs endast),(läs endast),(läs endast),(läs endast),(läs endast),(läs endast),(läs endast),(läs endast),(läs endast),(läs endast)
"Sinclair, Lord Brett",12345,brettid,sinclair@gmail.com,Section for the course Programming in Python,,,,0,0,,,,,0,0,,,,,0.0,0.0,,,,
"Craig, Danny",67890,dannyid,craig@gmail.com,Section for the course Programming in Python,,,,0,0,,,,,0,0,,,,,0.0,0.0,,,,
'''

@pytest.fixture
def csv_stream():
    return iter(grades_csv.split('\n'))


def test_get_cid(csv_stream):
    records = c2nb.get_records(csv_stream)
    assert records[1]["ID"] == '12345'
    assert records[2]["ID"] == '67890'

def test_get_uid(csv_stream):
    records = c2nb.get_records(csv_stream)
    assert records[1]["SIS User ID"] == 'brettid'
    assert records[2]["SIS User ID"] == 'dannyid'

def test_get_account(csv_stream):
    records = c2nb.get_records(csv_stream)
    assert records[1]["SIS Login ID"] == 'sinclair@gmail.com'
    assert records[2]["SIS Login ID"] == 'craig@gmail.com'

def test_get_names(csv_stream):
    records = c2nb.get_records(csv_stream)
    assert records[1]["Student"] == 'Sinclair, Lord Brett'
    assert records[2]["Student"] == 'Craig, Danny'

def test_split_names(csv_stream):
    initial_recs = [{"ID": 1, "Student": "Doe, John"}]
    assert c2nb.split_names(initial_recs) == [
        {"ID": 1, "Student": "Doe, John", "first_name": "John", "last_name": "Doe"}
        ]

def test_outdict():
    initial = [
        {
            "ID": 1,
            "Student": "Doe, John",
            "SIS Login ID": "john.doe@gmail.com",
            "first_name": "John",
            "last_name": "Doe"
        }
    ]
    with unittest.mock.patch('builtins.open') as mock_open:
        c2nb.out_dict(initial)
    
    mock_open.assert_called_once_with('students.csv', 'w')
