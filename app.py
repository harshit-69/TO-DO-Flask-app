from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db=SQLAlchemy(app)

class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    decr=db.Column(db.String(500),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno}-{self.title}"

@app.route("/",methods=['GET','POST'])
def hello_world():
    if request.method=="POST":
        title=request.form.get("title")
        decr=request.form.get("decr")
        todo=Todo(title=title,decr=decr or "")
        db.session.add(todo)
        db.session.commit()
        if not title:
            return "title is req"

    all_todo=Todo.query.all()
    return render_template("index.html",all_todo=all_todo)
   

@app.route("/Show")
def Products():
    all_todo=Todo.query.all()
    print(all_todo)
    
    return "Products page"

@app.route("/update/<int:sno>",methods=['GET','POST'])
def Update(sno):
    if request.method=="POST":
        title=request.form.get("title")
        decr=request.form.get("decr")
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.decr=decr
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    todo=Todo.query.filter_by(sno=sno).first()
    return render_template("update.html",todo=todo)

@app.route("/delete/<int:sno>")
def Delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")
    
   

if __name__=="__main__":
    app.run(debug=True)