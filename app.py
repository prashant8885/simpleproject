from flask import Flask,render_template,abort,request,redirect,url_for
from db_connect import get_connection
app=Flask(__name__)
name=[('Prashant','2001-01-02'),('Dipesh','2005-02-05'),('Hero','2005-02-05')]
@app.route("/",methods=['GET','POST'])
def index():
    connection=get_connection()
    if request.method=='POST':
        student_name=request.form.get('student_name')
        student_dob=request.form.get('student_dob')
        student_email=request.form.get('student_email')
        values=(student_name,student_dob,student_email)
        with connection.cursor() as cur:
            sql_smth="insert into student(student_name,date_of_birth,student_email) values(?,?,?)"
            cur.execute(sql_smth,values)
            connection.commit()


    with get_connection().cursor() as cur:
        cur.execute("SELECT * FROM student")
        res=cur.fetchall()
    name=res
    return render_template('index.html',nm=name)
@app.route("/student/<int:id>")
def get_student(id):
    with get_connection().cursor() as cur:
        cur.execute(f"SELECT * FROM student where id={id}")
        res=cur.fetchall()
    if res:
        return render_template('student_detail.html',student=res)
    else:
        abort(404)

@app.route("/delete/<int:id>")
def delete_student(id):
    connection=get_connection()
    with connection.cursor() as cur:
        sql_smth="DELETE FROM student where id=?"
        cur.execute(sql_smth,(id,))
        connection.commit()
    return redirect(url_for('index'))

@app.route("/edit/<int:id>",methods=['GET','POST'])
def edit_student(id):
    connection=get_connection()
    if request.method=='POST':
        student_name=request.form.get('student_name')
        student_dob=request.form.get('student_dob')
        student_email=request.form.get('student_email')
        with connection.cursor() as cur:
            cur.execute("""
            UPDATE student
            SET student_name=?, date_of_birth=?,student_email=?
            WHERE id=?
                """,(student_name,student_dob,student_email,id))
            connection.commit()
            connection.close()
            return redirect(url_for('index'))
    with connection.cursor() as cur:
        sql_smth="SELECT * FROM student where id=?"
        cur.execute(sql_smth,(id,))
        res=cur.fetchone()
    if res:
        return render_template('update_student.html',student=res)
    else:
        abort(404)

if __name__=='__main__':
    app.run(debug=True)