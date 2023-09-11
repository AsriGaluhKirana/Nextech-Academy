from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import or_


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
cors = CORS(app)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:1@localhost:5432/courseonline'
db = SQLAlchemy(app)


#table user
class Pengguna(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)
    contact = db.Column(db.String)
    student = db.relationship('Coursedata', backref='student', lazy='dynamic')


#tabel course
class Course(db.Model):
    id = db.Column(db.String, primary_key=True)
    nama = db.Column(db.String, nullable=False)
    deskripsi = db.Column(db.String, nullable=False)
    # kategori = db.Column(db.String, nullable=False)
    student = db.relationship('Coursedata', backref='course', lazy='dynamic')


# tabel course data
class Coursedata(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String, db.ForeignKey("pengguna.id"))
    course_id = db.Column(db.String, db.ForeignKey("course.id"))
    status = db.Column(db.String, nullable=False)


# tabel pre-requsite
class Prequisite(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.String, db.ForeignKey("course.id"))
    prequisite_id = db.Column(db.String, db.ForeignKey("course.id"))

class Viewtopcourse(db.Model):
    __tablename__ = "viewtopcourse"
    jumlah = db.Column(db.Integer)
    nama = db.Column(db.String, primary_key=True)
    
class Viewtopstudent(db.Model):
    __tablename__ = "viewtopstudent"
    jumlah = db.Column(db.Integer)
    nama = db.Column(db.String, primary_key=True)

with app.app_context(): 
    db.create_all()
    db.session.commit()

@app.post('/login')
def login():
    username = request.authorization.get("username")
    password = request.authorization.get("password")
    
    try:
        global user
        user = Pengguna.query.filter_by(username=username).first_or_404()
    except:
        return {
            'error message' : 'Hayo salah.'
        }
    if user.password == password:
        if user.role == 'Admin':
            return {"id": user.id, "nama": user.nama, "role": user.role}, 200 
        elif user.role == 'Student':
            return {"id": user.id, "username": user.username, "role": user.role}, 200 
    else:
        return 'Password salah!'
    

#endpoint REGISTRASI & UPDATE PENGGUNA (penambahan auth) hanya bisa update diri sendiri
@app.route('/user/regis', methods=['POST'])
def create_newuser():
    last_user = Pengguna.query.order_by(Pengguna.id.desc()).first()
    last_num = int(last_user.id[3:].lstrip("0"))
    new_num = str(last_num+1)
    new_id = "S23"+ new_num.zfill(3)
    data=request.get_json()
    new_user = Pengguna(
        id = new_id,
        username = data.get('username'),
        nama = data.get('nama'),
        password = data.get('password'),
        role = data.get('role'),
        contact = data.get('contact')
    )
    
    conditions = db.or_(
        Pengguna.id == new_user.id,
        Pengguna.nama == new_user.nama
    )
    
    existing_user = db.session.query(Pengguna).filter(conditions).first()
    
    if existing_user:
        return {
            "status": "error",
            "detail": "id atau nama sudah ada!!"
        }
    
    db.session.add(new_user)
    db.session.commit()
    return {"message": "Hore! Anda berhasil mendaftar."}

@app.route('/user/<id>', methods=['GET'])
def getuser(id):
    user = Pengguna.query.filter_by(id=id).first_or_404()
    response =  {
        "nama" : user.nama,
        "username" : user.username,
        "contact" : user.contact,
        "password" : user.password
    }    
    return {'response' : response}

@app.route('/user/update/<id>', methods=['PUT'])
def create_updateuser(id):
    user = Pengguna.query.filter_by(id=id).first_or_404()
    data=request.get_json()
    user.nama = data.get('nama'),
    user.contact = data.get('contact'),
    
    db.session.add(user)
    db.session.commit()
    return {"message": "Hore! Anda berhasil mengupdate data."}


#ENDPOINT COURSE Add & Update (penambahan auth) hanya bisa update diri sendiri
@app.route('/course/add', methods=['POST'])
def create_course():
    last_course = Course.query.order_by(Course.id.desc()).first()
    last_num = int(last_course.id[2:].lstrip("0"))
    new_num = str(last_num+1)
    new_id = "CO"+ new_num.zfill(3)
    data=request.get_json()
    new_course = Course(
        id = new_id,
        nama = data.get('nama'),
        deskripsi = data.get('deskripsi')
    )
    
    conditions = db.or_(
        Course.id == new_course.id,
        Course.nama == new_course.nama
    )
    
    existing_course = db.session.query(Course).filter(conditions).first()
    
    if existing_course:
        return {
            "status": "error",
            "detail": "id atau nama course sudah ada!!"
        }
    
    db.session.add(new_course)
    db.session.commit()
    return {"message": "Hore! Anda berhasil menambahkan course."}


@app.route('/course/update/<id>', methods=['PUT'])
def update_course(id):
    course = Course.query.filter_by(id=id).first_or_404()
    data=request.get_json()
    course.nama = data.get('nama')
    course.deskripsi = data.get('deskripsi')
    
    db.session.add(course)
    db.session.commit()
    return {"message": "Hore! Anda berhasil mengupdate data."}

#GET ALL COURSES
@app.route('/course', methods=['GET'])
def get_course():
    all_courses = Course.query.order_by(Course.id).all()
    
    result = []
    for course in all_courses:
        result.append({'id': course.id, 'nama': course.nama, 'deskripsi': course.deskripsi})
    
    return jsonify(result)

#Endpoint Enroll course (tidak boleh ambil course yg sama 2x)
@app.route('/course/enroll/<id>', methods=['POST'])
def enroll_course(id):
    #    user = login()
    # if user.role == 'Student':

        data = request.get_json()
        user = db.session.query(Pengguna).filter(Pengguna.username == data["nama"]).first()
        enrollment_count = db.session.query(Coursedata).filter(Coursedata.user_id == user.id).filter(Coursedata.status.in_(['in progress', 'dropout'])).count()

        if enrollment_count >= 5:
            return {"message": "Enrollment gagal. Course yang boleh diambil adalah maksimal 5",}

        get_course = db.session.query(Course).filter(Course.id == id).first()
        if get_course is None :
            return {"message": "course not available!"}
        else:
            if db.session.query(Prequisite).filter(Prequisite.course_id == id).first() != None:
                preqid = db.session.query(Prequisite).filter(Prequisite.course_id == id).first().prequisite_id
                preqcomp = db.session.query(Coursedata).filter(Coursedata.user_id == user.id).filter(Coursedata.course_id == preqid).first()
                if preqcomp != None:
                    if preqcomp.status == 'completed':
                        add_enroll = Coursedata(user_id=user.id, course_id=id, status='in progress')
                        db.session.add(add_enroll)
                        db.session.commit()
                        return {"message": "success enroll", "code":"success"}
                    else :
                        return {"message": "fail enroll because not completed yet","code":"pre not completed"}
                else:
                    return {"message": "Maaf gagal, kamu belum enroll sama sekali si prequisitenya!!","code":"pre not enrolled"}
            else :
                    add_enroll = Coursedata(user_id=user.id, course_id=id, status='in progress')
                    db.session.add(add_enroll)
                    db.session.commit()
                    return {"message": "success enroll"}
       
    # else:
    #     return {"message": "Hanya boleh dilakukan oleh student."}


#Endpoint enroll status complete or dropout
@app.route('/course/status/<id>', methods=['PUT'])
def complete_course(id):
    # user = login()
    # return user.id
    data = request.get_json()
    course = Coursedata.query.filter_by(user_id=user.id).filter_by(course_id=id).first_or_404()
    if user.role == 'Student':
        course.status = data.get("status")
        
        db.session.add(course)
        db.session.commit()
        return {"message": "Hore! Anda selesai."}


#Endpoint to get status enrollment
@app.route('/course/status/<id>', methods=['GET'])
def course_status(id):
    user_id = request.headers.get("id")
    course = Coursedata.query.filter_by(user_id=user_id).filter_by(course_id=id).first()
    
    if course:
        response = {
                "id" : course.id,
                "user_id" : course.user_id,
                "course_id" : course.course_id,
                "status" : course.status
        }
        
        return {
            "message": "OK",
            "data": response,
        }, 201
    
    else:
        return {
            "message": "Not Found"
        }, 404


#Endpoint Get list users enrolled to course
@app.route('/course/list/<id>', methods=['GET'])
def list_enrolled_users(id):
    course = Coursedata.query.filter_by(course_id=id).all()

    response = [
        {
            "id" : c.id,
            "user_id" : c.user_id,
            "course_id" : c.course_id,
            "status" : c.status
        } for c in course
    ] #penambahan nama user/student
    return {"message": "success.", "data" : response}


#Endpoint delete from course
@app.route('/course/enroll/<id>', methods=['DELETE'])
def delete_enroll(id):
    user_id = request.headers.get("user_id")
    course = Coursedata.query.filter_by(user_id=user_id, course_id=id).first()
    # if user.role == 'Admin':
    db.session.delete(course)
    db.session.commit()
    return {"message": "Hore! Data selesai dihapus."}


#Endpoint search course by name
# @app.route('/search/course/<name>', methods=['GET'])
# def search_course(name):
#     courses = Course.query.filter(Course.nama.ilike(f'%{name}%')).all()
    
#     if not courses:
#         return jsonify({'message': 'No courses found'})
    
#     result = []
#     for course in courses:
#         result.append({'id': course.id, 'nama': course.nama, 'deskripsi': course.deskripsi})
    
#     return jsonify(result)


#Endpoint search course by deskripsi
# @app.route('/search/course/deskripsi/<description>', methods=['GET'])
# def search_course_description(description):
#     courses = Course.query.filter(Course.deskripsi.ilike(f'%{description}%')).all()
    
#     if not courses:
#         return jsonify({'message': 'No courses found'})
    
#     result = []
#     for course in courses:
#         result.append({'id': course.id, 'nama': course.nama, 'deskripsi': course.deskripsi})

#     return jsonify(result)


#Endpoint search by course & description
@app.route('/search', methods=['GET'])
def search_course_desc():
    keyword = request.args["keyword"]
    search_list = (
        Course.query.filter(
            or_(Course.nama.ilike(f"%{keyword}%"), Course.deskripsi.ilike(f"%{keyword}%"))
        )
        .all()
    )
    if not search_list:
        return jsonify({'message': 'No courses found'})
    
    result = []
    for course in search_list:
        result.append({'id': course.id, 'nama': course.nama, 'deskripsi': course.deskripsi})

    return jsonify(result)

#endpoint reporting Get top 5 course (most enrolled)
@app.route('/top5course')
def view_report_course():
    course = Viewtopcourse.query.all()
    
    result = []
    rank = 0
    for i in course:
        rank +=1
        result.append({'rank': rank, 'nama' : i.nama, 'jumlah_siswa' : i.jumlah})
    return jsonify(result)


#endpoint reporting Get top 5 student (most enrolled)
@app.route('/top5student')
def view_report_student():
    student = Viewtopstudent.query.all()
    
    result = []
    rank = 0
    for i in student:
        rank +=1
        result.append({'rank': rank, 'nama' : i.nama, 'jumlah_completed' : i.jumlah})
    return jsonify(result)


@app.route('/listenroll')
def get_student_enroll():
    coursedata = Coursedata.query.all()
    
    response = [
        {
            "id" : c.student.id,
            "user_name": c.student.nama,
            "course_name": c.course.nama,
            "status" : c.status,
        } for c in coursedata
    ] #penambahan nama user/student
    return {"message": "success.", "data" : response}

#detail-course
@app.route('/course/detail-course/<id>', methods=['GET'])
def detail_course(id):
    course = Course.query.filter_by(id=id).first()

    response = {
            "nama" : course.nama,
            "deskripsi" : course.deskripsi,
        } 
    return response

if __name__ == '__main__':
    app.run(debug=True)
    