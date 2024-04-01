from .database import db
import csv
from .models.student import Student

def upload_student_data():
    if db.record_count(Student) <= 0:
        with open('data/raw/studentdataset.csv', newline='') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(csvreader, None)
            for row in csvreader:
                student = Student()
                student.read_CSV_Row(row)
                db.add_new_record(student)
            db.commit()