from flask import Flask,request
import json
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:manjusha@localhost/logicloop'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class task(db.Model):
    __tablename__ = 'TASK_INFO'
    id = db.Column('id', db.Integer(), primary_key = True)
    title = db.Column('title', db.String(30))
    description = db.Column('description', db.Text(30))
    done = db.Column('done', db.Boolean)

    # @staticmethod
    # def dummy_task():
    #     return task(id=0, title='', description='', done=True)

@app.route('/todo/api/v1.0/tasks/',methods = ['POST'])
def add_task():
    task_data = None
    reqdata = request.get_json()
    if reqdata:
        dbtask = task.query.filter_by(id=reqdata.get('ID')).first()
        if dbtask:
            return json.dumps({"ERROR": "DUPLICATE TASK"})
        else:
            #{"ID": 103, "TITLE": "title3", "DESCRIPTION": "title3 task added", "DONE": true}
            task_data = task(id=reqdata.get('ID'),
                           title=reqdata.get('TITLE'),
                           description=reqdata.get('DESCRIPTION'),
                           done=reqdata.get('DONE'))
            db.session.add(task_data)
            db.session.commit()
            msg = "Task Added Successfully...!"
    return json.dumps({"status": msg,
                       "task_data": {"ID": task_data.id, "TITLE": task_data.title, "DESCRIPTION": task_data.description, "DONE": task_data.done}})


@app.route('/todo/api/v1.0/tasks/<int:tid>',methods = ['DELETE'])
def delete_task(tid):
    task_data = task.query.filter_by(id=tid).first()
    if task_data:
        db.session.delete(task_data)
        db.session.commit()
        return json.dumps({"SUCCESS": f"task {tid} with given id removed..!"})
    return json.dumps({"ERROR": f"task {tid} with given id NOT PRESENT..!"})


@app.route('/todo/api/v1.0/tasks/<int:tid>',methods = ['PUT'])
def update_task(tid):
    dbtask = task.query.filter_by(id=tid).first()
    if dbtask:
        reqdata = request.get_json()
        dbtask.title = reqdata.get('TITLE')
        dbtask.description = reqdata.get('DESCRIPTION')
        dbtask.done = reqdata.get('DONE')
        db.session.commit()
        msg = "task Updated Successfully...!"
        task_data = dbtask
        return json.dumps({"status": msg,
                           "task_data": {"ID": task_data.id, "TITLE": task_data.title, "DESCRIPTION": task_data.description, "DONE": task_data.done}})

    return json.dumps({"ERROR": "TASK WITH GIVEN ID NOT PRESENT..SO CANNOT UPDATE"})

def serialize_task_model(task_data):
    if task_data:
        return {"ID": task_data.id, "TITLE": task_data.title, "DESCRIPTION": task_data.description, "DONE": task_data.done}


@app.route('/todo/api/v1.0/tasks/<int:tid>',methods = ['GET'])
def search_task(tid):
    task_data = task.query.filter_by(id=tid).first()
    if task_data:
        return json.dumps(serialize_task_model(task_data))
    return json.dumps({"ERROR": "task WITH GIVEN ID NOT PRESENT"})


@app.route('/todo/api/v1.0/tasks/',methods = ['GET'])
def fetch_all_task():
    task_data = task.query.all()
    tasks_list = []
    for tsk in task_data:
        tasks_list.append(serialize_task_model(tsk))
    return json.dumps(tasks_list)

if __name__ == '__main__':
    app.run(debug=True)