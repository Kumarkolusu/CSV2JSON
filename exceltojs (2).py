class Personnel:
    def __init__(self,id,fullName,gender,dob,age,aadhar_number,city,contact_number):
        self.id=id
        self.fullName=fullName
        self.gender=gender
        self.dob=dob
        self.age=age
        self.aadhar=aadhar_number
        self.city=city
        self.contactNumber=contact_number
class Student(Personnel):
    def __init__(self,id,fullName,gender,dob,age,aadhar_number,city,contact_number,roll_no,classs,total_marks,grade,sec_percent,hs_stream):
        super().__init__(id,fullName,gender,dob,age,aadhar_number,city,contact_number)
        self.rollNumber =roll_no
        self.classs =classs
        self.totalMarks =total_marks
        self.grade =grade
        self.secPercent =sec_percent
        self.hsStream =hs_stream
class Teacher(Personnel):
    def __init__(self,id,fullName,gender,dob,age,aadhar_number,city,contact_number,emp_no,class_teacher_of,doj,servicePeriod,previous_school,post,salary,subject_teaches):
        super().__init__(id, fullName, gender, dob, age, aadhar_number, city, contact_number)
        self.empNo = emp_no
        self.classTeacher = class_teacher_of
        self.doj = doj
        self.servicePeriod = servicePeriod
        self.previous_school = previous_school
        self.post = post
        self.salary = salary
        self.subjectTeaches = subject_teaches


import json
import os
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

path_json = input("Please enter the path to save the json files:")
try:
    os.makedirs(path_json)
    print("Directory '% s' created" % path_json)
except FileExistsError:
    print("Directory '% s' already exists" % path_json)

df= pd.read_csv("master-data2.csv")
df['json'] = df.apply(lambda x: x.to_json(), axis=1)
student={"studentRecordCount" : 0,"data" : []}
teacher = {"teacherRecordCount" : 0,"data" : []}
for each in df['json']:
    each = json.loads(each)
    each = {("classs" if k=="class" else k):v for k,v in each.items() if v!=None}
    date_time_str = each['dob'].replace("-","/")
    try:
        date_time_obj = datetime.strptime(date_time_str, '%d/%m/%Y')
    except:
        date_time_obj = datetime.strptime(date_time_str, '%m/%d/%Y')
    time_difference = relativedelta(datetime.now(), date_time_obj)
    each['age'] = f"{time_difference.years} Yrs {time_difference.months} months"
    each['fullName'] = each['firstname'] + ' ' + each['lastname']
    each.pop('firstname')
    each.pop('lastname')
    if each["category"]=="student":
        if each['total_marks']>899:
            each['grade'] = "A"
        elif each['total_marks']>799:
            each['grade'] = "B"
        else:
            each['grade'] = "C"
        each.pop("category")
        each.pop("blood_group")
        studentobj = Student(**each)
        student['data'].append(studentobj.__dict__)
    else:
        date_time_str = each['doj'].replace("-", "/")
        try:
            date_time_obj = datetime.strptime(date_time_str, '%d/%m/%Y')
        except:
            date_time_obj = datetime.strptime(date_time_str, '%m/%d/%Y')
        time_difference = relativedelta(datetime.now(), date_time_obj)
        each['servicePeriod']=f"{time_difference.years} Yrs {time_difference.months} months"
        # teacher['data'].append(each)
        each.pop("category")
        each.pop("blood_group")
        teacherobj = Teacher(**each)
        teacher['data'].append(teacherobj.__dict__)
    student['studentRecordCount']=len(student['data'])
    teacher['teacherRecordCount'] = len(teacher['data'])

x = str(datetime.now())[0:10].replace("-","")
path_json=path_json.replace("\\", "//")
with open(f"{path_json}//student_record_{x}.json",mode='w') as sp ,open(f"{path_json}//teacher_record_{x}.json",mode='w') as tp:
    json.dump(student, sp)
    json.dump(teacher, tp)