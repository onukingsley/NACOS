from flask import  render_template, redirect, flash, get_flashed_messages, request, url_for
from Nacos import app ,db
from Nacos.forms import StudentRegistration,Signin,PaymentForm,Search,StaffRegistration,Changepassword
from Nacos.models import Student,Staff,Payment,User
from flask_login import login_user,current_user,logout_user,login_required
from passlib.hash import crypt16 as cr



@app.route('/')
def homepage():
    return render_template('new template/home page.html')

@login_required
@app.route('/addstudent',methods=['GET','POST'])
def addstudent():
    if not current_user.role == 'admin':
        flash('Unauthorised access as an admin')
        return redirect(url_for('signin'))
    form = StudentRegistration()
    if form.validate_on_submit():
        user = User(reg_no=form.reg_no.data,
                    email=form.email.data,
                    password = cr.hash(form.reg_no.data),
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
        return redirect(url_for('admindashboard'))



    return render_template("staff login.html",form=form)


@login_required
@app.route('/addstaff',methods=['GET','POST'])
def addstaff():
    # if not current_user.role == 'admin':
    #     flash('Unauthorised access as an admin')
    #     return redirect(url_for('signin'))
    form = StaffRegistration()
    if form.validate_on_submit():
        if form.combo.data is 1:
            msg = 'admin'
        elif form.combo.data is 2:
            msg = 'staff'
        user = User(
                    email=form.email.data,
                    password = cr.hash(form.password.data),
                    name=form.fullname.data,
                    role = msg,
                     )
        db.session.add(user)
        db.session.commit()
        stu = User.query.filter_by(email=form.email.data).first()
        staff = Staff(name=form.fullname.data,
                          email= form.email.data,
                          user_id= stu.id,
                          role = msg,
                          password= cr.hash(form.password.data))
        db.session.add(staff)
        db.session.commit()
        flash("Registration Successful",category="successful")
        return redirect(url_for('admindashboard'))



    return render_template("add staff.html",form=form)


@login_required
@app.route('/login', methods=['GET','POST'])
def signin():
    if current_user.is_authenticated:
        if current_user.role == 'student':
            return redirect(url_for("studentDashboard"))

    form = Signin()
    if form.validate_on_submit():
            user = User.query.filter((User.reg_no == form.username.data)| (User.email == form.username.data)).first()
            print (user.password)
            if user and user.role == 'student' and cr.verify(form.password.data,user.password):

                login_user(user)
                print(current_user.name+" is currently logged in as a " + user.role)
                details = Payment.query.filter_by(reg_no=current_user.reg_no).all()
                print(current_user.name)
                flash("Login Successful", 'success')
                return redirect(url_for("studentDashboard"))
                # return render_template('new template/Student dashboard.html',detail=details)



            else:
                    flash("Invalid Login Details", 'danger')
                    print('unable to login')
                    return redirect(url_for("signin"))



    return render_template('new template/login form.html',form=form)

@app.route('/admin/login', methods=['GET','POST'])
def loginadmin():
    if current_user.is_authenticated:
        if current_user.role == 'staff':
            return redirect(url_for("staffdashboard"))
        elif current_user.role == 'admin':
            return redirect(url_for('admindashboard'))
    form = Signin()
    if form.validate_on_submit():
            user = User.query.filter((User.reg_no == form.username.data)| (User.email == form.username.data)).first()
            print (user.password)
            if user and user.role == "staff" and cr.verify(form.password.data,user.password):
                login_user(user)
                flash("Login Successful", 'success')
                print(current_user.name+" is currently logged in as a " + user.role)
                return redirect(url_for('staffdashboard'))

            elif user and user.role == "admin" and cr.verify(form.password.data,user.password):
                login_user(user)
                print(current_user.name+" is currently logged in as a " + user.role)
                flash("Welcome Admin", 'success')

                return redirect(url_for("admindashboard"))


            else:
                    flash("Invalid Login Details", 'danger')
                    print('unable to login')
                    return redirect(url_for("loginadmin"))



    return render_template('new template/admin login.html',form=form)


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

@login_required
@app.route('/studentdashboard')
def studentDashboard():
    if not current_user.role == 'student':
        flash('Unauthorised access as a student')
        return redirect(url_for('signin'))
    user = current_user
    stu = Payment.query.filter_by(reg_no = user.reg_no)
    return render_template('new template/Student dashboard.html', user=user,stu=stu)

@login_required
@app.route('/staffdashboard/', methods=['GET','POST'])
def staffdashboard():
    if not current_user.role == 'staff':
        flash('Unauthorised access as a staff')
        return redirect(url_for('signin'))
    user = current_user
    form = Search()
    if form.validate_on_submit():
        ref = str(form.reg_no.data)
        r = ref.replace('/', '')
        print(r)
        return redirect(url_for('studentPaymenttable', reg_no=r))




    return render_template('new template/Staff dashboard 1.html',form=form, user=user)

@login_required
@app.route('/studenttable/<reg_no>')
def studentPaymenttable(reg_no=' '):
    r = list(reg_no)
    str(r.insert(4,'/'))
    s = ''.join(r)
    print(s)

    studentdetail = Student.query.filter_by(reg_no=s).first()
    detail = Payment.query.filter_by(reg_no=s).all()


    return render_template('new template/Staff dashboard.html',detail=detail,st=studentdetail)
@login_required
@app.route('/admindashboard',methods=['GET','POST'])
def admindashboard():
    if not current_user.role == 'admin':
        flash('Unauthorised access as an admin')
        return redirect(url_for('signin'))
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

@login_required
@app.route('/paymentform',methods=['GET','POST'])
def paymentform():
    if not current_user.role == 'admin':
        flash('Unauthorised access as an admin')
        return redirect(url_for('signin'))
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
           return redirect(url_for('paymentform'))
        if(not user):
            flash('Student Does not exist')
            return redirect(url_for('paymentform'))




    return render_template('new template/admin form.html',form=form)

@login_required
@app.route('/more/<tablename>' )
def viewmore(tablename):
    if not current_user.role == 'admin':
        flash('Unauthorised access as an admin')
        return redirect(url_for('signin'))
    if tablename == 'Student':
        table = Student.query.all()
    elif tablename == 'Payment':
        table = Payment.query.all()
    elif tablename == 'Staff':
        table = Staff.query.all()
    return render_template('new template/staff_studenttable.html',tablename=tablename,table=table)

@app.route('/print/<paymentid>')
def printdoc(paymentid):
    recipt = Payment.query.filter_by(id=paymentid).first()
    user = User.query.filter_by(id=recipt.student_id).first()
    return render_template('new template/payment receipt.html', recipt=recipt, user=user)

@app.route('/changepassword/', methods=['GET','POST'])
def changepassword():
    form= Changepassword()
    if form.validate_on_submit():
        current_user.password = cr.hash(form.new_password.data)
        print(current_user.password)
        db.session.commit()
        if current_user.role == 'staff':
            user = Staff.query.filter_by(userid=current_user.id)
            user.password =cr.hash(form.new_password.data)
            db.session.commit()
            flash("Changed sucessfully", 'danger')

            return redirect(url_for('staffdashboard'))
        if current_user.role == 'student':
            flash("Changed sucessfully", 'danger')

            return redirect(url_for('staffdashboard'))

    return render_template("new template/change password.html",form=form)