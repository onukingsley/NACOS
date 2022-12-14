from flask import  render_template, redirect, flash, get_flashed_messages, request, url_for
from Nacos import app ,db
from Nacos.forms import StudentRegistration,Signin,PaymentForm,Search,StaffRegistration
from Nacos.models import Student,Staff,Payment,User
from flask_login import login_user,current_user,logout_user,login_required




@app.route('/addstudent',methods=['GET','POST'])
def addstudent():
    form = StudentRegistration()
    if form.validate_on_submit():
        user = User(reg_no=form.reg_no.data,
                    email=form.email.data,
                    password = form.reg_no.data,
                    name=form.fullname.data,
                    role = 'student',
                     )
        db.session.add(user)
        db.session.commit()
        stu = User.query.filter_by(reg_no=form.reg_no.data).first()
        student = Student(name=form.fullname.data,
                          reg_no= form.reg_no.data,
                          user_id= stu.id,
                          current_level= form.current_level.data)
        db.session.add(student)
        db.session.commit()
        flash("Registration Successful",category="successful")
        return redirect(url_for('signin'))



    return render_template("staff login.html",form=form)


@app.route('/addstaff',methods=['GET','POST'])
def addstaff():
    form = StaffRegistration()
    if form.validate_on_submit():
        if form.combo.data is 1:
            msg = 'admin'
        elif form.combo.data is 2:
            msg = 'staff'
        user = User(
                    email=form.email.data,
                    password = form.password.data,
                    name=form.fullname.data,
                    role = msg,
                     )
        db.session.add(user)
        db.session.commit()
        stu = User.query.filter_by(email=form.email.data).first()
        staff = Staff(name=form.fullname.data,
                          email= form.email.data,
                          user_id= stu.id,
                          role = form.msg.data,
                          password= form.reg_no.data)
        db.session.add(staff)
        db.session.commit()
        flash("Registration Successful",category="successful")
        return redirect(url_for('signin'))



    return render_template("add staff.html",form=form)


@app.route('/', methods=['GET','POST'])
def signin():
    form = Signin()
    if form.validate_on_submit():
            user = User.query.filter((User.reg_no == form.username.data)| (User.email == form.username.data)).first()

            if user and user.role == 'student' and user.password == form.password.data:

                login_user(user)
                print(current_user.name+" is currently logged in as a " + user.role)
                details = Payment.query.filter_by(reg_no=current_user.reg_no).all()
                print(current_user.name)
                return redirect(url_for("studentDashboard"))
                # return render_template('new template/Student dashboard.html',detail=details)
            elif user and user.role == "staff" and user.password == form.password.data:
                login_user(user)
                print(current_user.name+" is currently logged in as a " + user.role)
                return redirect(url_for('staffdashboard'))

            elif user and user.role == "admin" and user.password == form.password.data:
                login_user(user)
                print(current_user.name+" is currently logged in as a " + user.role)
                return redirect(url_for("admindashboard"))
                flash("Welcome Admin", 'success')

            else:
                    flash("Invalid Login Details", 'danger')
                    print('unable to login')
                    return redirect(url_for("signin"))



    return render_template('new template/login form.html',form=form)


# @app.route('/', methods=['GET','POST'])
# def signin():
#     form = Signin()
#     if form.validate_on_submit():
#         if form.combo.data is 1:
#             student = Student.query.filter_by(reg_no = form.username.data ).first()
#             if student and form.password.data==form.username.data:
#                 login_user(student)
#                 print(current_user.name+" is currently logged in as a student")
#                 details = Payment.query.filter_by(reg_no=current_user.reg_no).all()
#                 print(current_user.name)
#                 return redirect(url_for("studentDashboard"))
#                 # return render_template('new template/Student dashboard.html',detail=details)
#             else:
#                 print("no student user found")
#                 flash("Invalid Login Details",'danger')
#         elif form.combo.data is 2:
#             staff = Staff.query.filter_by(email=form.username.data).first()
#             if staff and form.password.data == staff.password:
#                 print("staff is seen")
#                 print(staff.role)
#
#                 if staff.role == "staff":
#                     print("staff is staff")
#                     login_user(staff)
#
#                     return redirect(url_for('staffdashboard'))
#                     flash("Welcome Staff", 'success')
#                 elif staff.role == "admin":
#                     print("staff is now an admin")
#                     login_user(staff)
#                     return redirect(url_for("admindashboard"))
#                     flash("Welcome Admin", 'success')
#                 else:
#                     flash("Invalid Login Details", 'danger')
#                     print('unable to login')
#                     return redirect(url_for("signin"))
#
#
#
#     return render_template('Student login.html',form=form)

@app.route('/studentdashboard')
def studentDashboard():
    user = current_user
    stu = Payment.query.filter_by(reg_no = user.reg_no)
    return render_template('new template/Student dashboard.html', user=user,stu=stu)

@app.route('/staffdashboard/', methods=['GET','POST'])
def staffdashboard():
    user = current_user
    form = Search()
    if form.validate_on_submit():
        ref = str(form.reg_no.data)
        r = ref.replace('/', '')
        print(r)
        return redirect(url_for('studentPaymenttable', reg_no=r))




    return render_template('new template/Staff dashboard 1.html',form=form, user=user)


@app.route('/studenttable/<reg_no>')
def studentPaymenttable(reg_no=' '):
    r = list(reg_no)
    str(r.insert(4,'/'))
    s = ''.join(r)
    print(s)

    studentdetail = Student.query.filter_by(reg_no=s).first()
    detail = Payment.query.filter_by(reg_no=s).all()


    return render_template('new template/Staff dashboard.html',detail=detail,st=studentdetail)

@app.route('/admindashboard',methods=['GET','POST'])
def admindashboard():
    students = Student.query.all()
    payment = Payment.query.all()
    staff = Staff.query.all()
    total_student = len(students)
    total_staff = len(staff)
    total_payment = len(payment)


    form = Search()
    if form.validate_on_submit():
        ref =str(form.reg_no.data)
        r = ref.replace('/','')
        print(r)
        return redirect(url_for('studentPaymenttable',reg_no=r))

    print(students)


    return render_template('new template/Admin.html',form=form,students=students,payment=payment,total_payment=total_payment,staff=staff,total_student=total_student,total_staff=total_staff)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("signin"))

@app.route('/paymentform',methods=['GET','POST'])
def paymentform():
    form = PaymentForm()
    if form.validate_on_submit():
        user = Student.query.filter_by(reg_no=form.reg_no.data).first()
        if form.combo.data == 1:
            status = True
        else: status = False


        if(user):
           payment = Payment(student_id=user.id,status=status,level=form.current_level.data,reg_no=form.reg_no.data)
           db.session.add(payment)
           db.session.commit()
           flash('Payment Recorded')



    return render_template('new template/admin form.html',form=form)


@app.route('/more/<tablename>' )
def viewmore(tablename):
    if tablename == 'Student':
        table = Student.query.all()
    elif tablename == 'Payment':
        table = Payment.query.all()
    elif tablename == 'Staff':
        table = Staff.query.all()
    return render_template('new template/staff_studenttable.html',tablename=tablename,table=table)