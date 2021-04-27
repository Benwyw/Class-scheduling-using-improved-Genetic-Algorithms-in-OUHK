import sqlite3

"""
    School : 
         ASS => School of Arts and Social Sciences
         BA =>	Lee Shau Kee School of Business and Administration
         EL => School of Education and Languages
         NUR => School of Nursing and Health Studies
         ST => School of Science and Technology
         OUHK => 共用 （Lecture房）
    Item:
        COMP => Computer
    Type:
        Normal => Normal course
        FYP => FYP course
"""

def put_course():
    db = sqlite3.connect('ou.db')
    db.execute("DROP TABLE IF EXISTS course")
    db.execute("CREATE TABLE course (courseid TEXT PRIMARY KEY, coursename TEXT NOT NULL, coursemax INTEGER NOT NULL, courseitem TEXT NOT NULL,school TEXT NOT NULL, type TEXT NOT NULL)")
    #BCOMPHITJ Year 1
    db.execute("INSERT INTO course (courseid, coursename, coursemax, courseitem, school, type) VALUES ('IT S102F', 'Computing Fundamentals', 90, 'COMP', 'ST', 'Normal')")
    # db.execute("INSERT INTO course (courseid, coursename, coursemax, courseitem, school, type) VALUES ('IT S103F', 'Introduction to Internet Application Development', 90, 'COMP', 'ST', 'Normal')")
    db.execute("INSERT INTO course (courseid, coursename, coursemax, courseitem, school, type) VALUES ('COMP S208F', 'Introduction to Computer Programming', 90, 'COMP', 'ST', 'Normal')")
    # db.execute("INSERT INTO course (courseid, coursename, coursemax, courseitem, school, type) VALUES ('COMP S209F', 'Data Structures, Algorithms, and Problem Solving', 90, '', 'ST', 'Normal')")

    #BCOMPHITJ Year 2
    db.execute("INSERT INTO course (courseid, coursename, coursemax, courseitem, school, type) VALUES ('COMP S202F', 'Java Programming Fundamentals', 90, 'COMP', 'ST', 'Normal')")
    # db.execute("INSERT INTO course (courseid, coursename, coursemax, courseitem, school, type) VALUES ('COMP S203F', 'Intermediate Java Programming and User Interface Design', 90, 'COMP', 'ST', 'Normal')")
    db.execute("INSERT INTO course (courseid, coursename, coursemax, courseitem, school, type) VALUES ('COMP S264F', 'Discrete Mathematics', 90, '', 'ST', 'Normal')")
    # db.execute("INSERT INTO course (courseid, coursename, coursemax, courseitem, school, type) VALUES ('COMP S265F', 'Design and Analysis of Algorithms', 90, '', 'ST', 'Normal')")

    #BCOMPHITJ Year 3
    db.execute("INSERT INTO course (courseid, coursename, coursemax, courseitem, school, type) VALUES ('COMP S266F', 'Computer Architecture', 90, '', 'ST', 'Normal')")
    # db.execute("INSERT INTO course (courseid, coursename, coursemax, courseitem, school, type) VALUES ('COMP S267F', 'Operating Systems', 90, '', 'ST', 'Normal')")
    db.execute("INSERT INTO course (courseid, coursename, coursemax, courseitem, school, type) VALUES ('COMP S312F', 'Java Application Development', 90, 'COMP', 'ST', 'Normal')")
    # db.execute("INSERT INTO course (courseid, coursename, coursemax, courseitem, school, type) VALUES ('COMP S313F', 'Mobile Computing', 90, 'COMP', 'ST', 'Normal')")
    db.execute("INSERT INTO course (courseid, coursename, coursemax, courseitem, school, type) VALUES ('COMP S320F', 'Database Management', 90, 'COMP', 'ST', 'Normal')")
    # db.execute("INSERT INTO course (courseid, coursename, coursemax, courseitem, school, type) VALUES ('COMP S321F', 'Advanced Database and Data Warehousing', 90, 'COMP', 'ST', 'Normal')")
    db.execute("INSERT INTO course (courseid, coursename, coursemax, courseitem, school, type) VALUES ('COMP S350F', 'Software Engineering', 90, 'COMP', 'ST', 'Normal')")
    # db.execute("INSERT INTO course (courseid, coursename, coursemax, courseitem, school, type) VALUES ('COMP S351F', 'Software Project Management', 90, 'COMP', 'ST', 'Normal')")

    #BCOMPHITJ Year 4
    db.execute("INSERT INTO course (courseid, coursename, coursemax, courseitem, school, type) VALUES ('COMP S451F', 'Computing Project', 90, 'COMP', 'ST', 'FYP')")
    db.execute("INSERT INTO course (courseid, coursename, coursemax, courseitem, school, type) VALUES ('COMP S456F', 'Software System Development Project', 90, 'COMP', 'ST', 'FYP')")

    #BSCHCSJS Year 1 (s102f s208f already)
    db.execute("INSERT INTO course (courseid, coursename, coursemax, courseitem, school, type) VALUES ('MATH S141F', 'Algebra and Calculus', 90, '', 'ST', 'Normal')")
    
    #BSCHCSJS Year 2 (202F 204F 266F already)

    #BSCHCSJS Year 3
    db.execute("INSERT INTO course (courseid, coursename, coursemax, courseitem, school, type) VALUES ('COMP S381F', 'Server-side Technologies and Cloud Computing', 90, 'COMP', 'ST', 'Normal')")
    
    #BSCHCSJS Year 4 (456f)

    db.commit()

def put_programme():
    db = sqlite3.connect('ou.db')
    db.execute("DROP TABLE IF EXISTS programme")
    db.execute("CREATE TABLE programme (programmeid TEXT PRIMARY KEY, programmename TEXT NOT NULL, school TEXT NOT NULL)")

    #Computing Programmes
    db.execute("INSERT INTO programme (programmeid, programmename, school) VALUES ('BCOMPHITJS', 'Bachelor of Computing with Honours in Internet Technology', 'ST')")
    db.execute("INSERT INTO programme (programmeid, programmename, school) VALUES ('BSCHCSJS', 'Bachelor of Science with Honours in Computer Science', 'ST')")
    #db.execute("INSERT INTO programme (programmeid, programmename, school) VALUES ('BSCHDSAIF', 'Bachelor of Science with Honours in Data Science & Artificial Intelligence', 'ST')")
    #db.execute("INSERT INTO programme (programmeid, programmename, school) VALUES ('BAHCIEFS', 'Bachelor of Arts with Honours in Computing and Interactive Entertainment', 'ST')")

    db.commit()

# select programmeid, courseid from programmeCourse,course WHERE programmeCourse.courseid = course.courseid AND course.type = 'FYP' GROUP BY programmeCourse.programmeid
def put_programmeCourse():
    db = sqlite3.connect('ou.db')
    db.execute("DROP TABLE IF EXISTS programmeCourse")
    db.execute("CREATE TABLE programmeCourse(id INTEGER PRIMARY KEY AUTOINCREMENT, programmeid TEXT NOT NULL, courseid TEXT NOT NULL,year TEXT NOT NULL,FOREIGN KEY(programmeid) REFERENCES programme(programmeid),FOREIGN KEY(courseid) REFERENCES course(courseid))")
    # BCOMPHITJS 
    db.execute("INSERT INTO programmeCourse (programmeid, courseid, year) VALUES ('BCOMPHITJS', 'IT S102F','1')") # mean BCOMPHITJS yr1 take IT S102F
    db.execute("INSERT INTO programmeCourse (programmeid, courseid, year) VALUES ('BCOMPHITJS', 'COMP S208F','1')")
    db.execute("INSERT INTO programmeCourse (programmeid, courseid, year) VALUES ('BCOMPHITJS', 'COMP S202F','2')")
    db.execute("INSERT INTO programmeCourse (programmeid, courseid, year) VALUES ('BCOMPHITJS', 'COMP S264F','2')")
    db.execute("INSERT INTO programmeCourse (programmeid, courseid, year) VALUES ('BCOMPHITJS', 'COMP S266F','3')")
    db.execute("INSERT INTO programmeCourse (programmeid, courseid, year) VALUES ('BCOMPHITJS', 'COMP S312F','3')")
    db.execute("INSERT INTO programmeCourse (programmeid, courseid, year) VALUES ('BCOMPHITJS', 'COMP S320F','3')")
    db.execute("INSERT INTO programmeCourse (programmeid, courseid, year) VALUES ('BCOMPHITJS', 'COMP S350F','3')")
    db.execute("INSERT INTO programmeCourse (programmeid, courseid, year) VALUES ('BCOMPHITJS', 'COMP S456F','4')") # same as S451F 
    db.execute("INSERT INTO programmeCourse (programmeid, courseid, year) VALUES ('BCOMPHITJS', 'COMP S451F','4')") # same as S456F 

    #BSCHCSJS
    db.execute("INSERT INTO programmeCourse (programmeid, courseid, year) VALUES ('BSCHCSJS', 'MATH S141F','1')")
    db.execute("INSERT INTO programmeCourse (programmeid, courseid, year) VALUES ('BSCHCSJS', 'IT S102F','1')")
    db.execute("INSERT INTO programmeCourse (programmeid, courseid, year) VALUES ('BSCHCSJS', 'COMP S208F','1')")
    db.execute("INSERT INTO programmeCourse (programmeid, courseid, year) VALUES ('BSCHCSJS', 'COMP S202F','2')")
    db.execute("INSERT INTO programmeCourse (programmeid, courseid, year) VALUES ('BSCHCSJS', 'COMP S264F','2')")
    db.execute("INSERT INTO programmeCourse (programmeid, courseid, year) VALUES ('BSCHCSJS', 'COMP S266F','2')")
    db.execute("INSERT INTO programmeCourse (programmeid, courseid, year) VALUES ('BSCHCSJS', 'COMP S312F','3')")
    db.execute("INSERT INTO programmeCourse (programmeid, courseid, year) VALUES ('BSCHCSJS', 'COMP S320F','3')")
    db.execute("INSERT INTO programmeCourse (programmeid, courseid, year) VALUES ('BSCHCSJS', 'COMP S350F','3')")
    db.execute("INSERT INTO programmeCourse (programmeid, courseid, year) VALUES ('BSCHCSJS', 'COMP S381F','3')")
    db.execute("INSERT INTO programmeCourse (programmeid, courseid, year) VALUES ('BSCHCSJS', 'COMP S456F','4')")

    db.commit()

def put_room():
    """
    Campus :　
        MC
        JCC
        IOH
    """
    db = sqlite3.connect('ou.db')
    db.execute("DROP TABLE IF EXISTS room")
    db.execute("CREATE TABLE room (roomid TEXT PRIMARY KEY, capacity INTEGER NOT NULL, floor INTEGER NOT NULL, campus TEXT NOT NULL, type TEXT NOT NULL, school TEXT NOT NULL, time DOUBLE NOT NULL, item TEXT NOT NULL)")
    #School: OUHK
    db.execute("INSERT INTO room (roomid,capacity,floor,campus,type,school,time,item) VALUES ('A-101',120,-1,'MC','Lecture','OUHK',35.5,'')")
    db.execute("INSERT INTO room (roomid,capacity,floor,campus,type,school,time,item) VALUES ('A0411',120,4,'MC','Lecture','OUHK',36.5,'')")
    db.execute("INSERT INTO room (roomid,capacity,floor,campus,type,school,time,item) VALUES ('B-129',120,-1,'MC','Lecture','OUHK',50.0,'')")
    db.execute("INSERT INTO room (roomid,capacity,floor,campus,type,school,time,item) VALUES ('B0614',120,6,'MC','Lecture','OUHK',40.0,'')")
    db.execute("INSERT INTO room (roomid,capacity,floor,campus,type,school,time,item) VALUES ('C0G01',120,0,'MC','Lecture','OUHK',30.5,'')")
    db.execute("INSERT INTO room (roomid,capacity,floor,campus,type,school,time,item) VALUES ('C0311',120,3,'MC','Lecture','OUHK',35.0,'')")
    db.execute("INSERT INTO room (roomid,capacity,floor,campus,type,school,time,item) VALUES ('C0518',120,5,'MC','Lecture','OUHK',36.0,'')")
    db.execute("INSERT INTO room (roomid,capacity,floor,campus,type,school,time,item) VALUES ('C0618',120,6,'MC','Lecture','OUHK',35.8,'')")
    db.execute("INSERT INTO room (roomid,capacity,floor,campus,type,school,time,item) VALUES ('C0721',120,7,'MC','Lecture','OUHK',36.2,'')")
    db.execute("INSERT INTO room (roomid,capacity,floor,campus,type,school,time,item) VALUES ('C0910',120,9,'MC','Lecture','OUHK',37.2,'')")
    db.execute("INSERT INTO room (roomid,capacity,floor,campus,type,school,time,item) VALUES ('D0309',120,3,'JCC','Lecture','OUHK',38.9,'')")

    

    #School :ST
    db.execute("INSERT INTO room (roomid,capacity,floor,campus,type,school,time,item) VALUES ('C0411',30,4,'MC','Lab','ST',12.2,'COMP')")
    db.execute("INSERT INTO room (roomid,capacity,floor,campus,type,school,time,item) VALUES ('C0412',30,4,'MC','Lab','ST',15.2,'COMP')")
    db.execute("INSERT INTO room (roomid,capacity,floor,campus,type,school,time,item) VALUES ('C0413',30,4,'MC','Lab','ST',18.6,'COMP')")
    db.execute("INSERT INTO room (roomid,capacity,floor,campus,type,school,time,item) VALUES ('C0415',30,4,'MC','Lab','ST',19.9,'COMP')")
    db.execute("INSERT INTO room (roomid,capacity,floor,campus,type,school,time,item) VALUES ('C0417',30,4,'MC','Lab','ST',22.6,'COMP')")
    db.execute("INSERT INTO room (roomid,capacity,floor,campus,type,school,time,item) VALUES ('D0627',30,6,'JCC','Lab','ST',26.5,'COMP')")
    db.execute("INSERT INTO room (roomid,capacity,floor,campus,type,school,time,item) VALUES ('D0625',30,6,'JCC','Lab','ST',23.2,'COMP')")
    db.commit()

if __name__ == '__main__':
    put_course()
    put_programme()
    put_programmeCourse()
    put_room()

    '''
    Display data
    '''
    db = sqlite3.connect('ou.db')
    c = db.cursor()
    c.execute("SELECT * FROM course")
    course_data = c.fetchall()
    c.execute("SELECT * FROM programme")
    programme_data = c.fetchall()
    c.execute("SELECT * FROM programmeCourse")
    programmeCourse_data = c.fetchall()
    c.execute("SELECT * FROM room")
    room_data = c.fetchall()
    c.close()

    print('\n==================== Course Data ====================')
    for i in course_data:
        print(i)
    print('\n==================== Programme Data ====================')
    for i in programme_data:
        print(i)
    print('\n==================== ProgrammeCourse Data ====================')
    for i in programmeCourse_data:
        print(i)
    print('\n==================== Room Data ====================')
    for i in room_data:
        print(i)