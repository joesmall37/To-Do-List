
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id
# our index form
# adding post and get to our routes so we can add data to our dattabase
@app.route('/', methods=['POST', 'GET'])
def index():
    # if the request that's sent to this route is post
    if request.method == 'POST':
        # variable for our task
        # task content is equal to the input in the form
        task_content = request.form['content']
        # the todo object will have its contents equal to the contents of input
        new_task = Todo(content=task_content)
        # now push the contents of this input to our database
        try:
            db.session.add(new_task)
            # commmit to our database
            db.session.commit()
            # switch back to our index.html
            return redirect('/')
            # if our task failed to add to db
        except:
            return 'There was an issue adding your task'
    # if the request is not post
    else:
        # create a task variable
        # this will look at the db contents in the order they were created and return all of them
        tasks = Todo.query.order_by(Todo.date_created).all()
        #  render our page
        return render_template('index.html', tasks=tasks)

# delete route
@app.route('/delete/<int:id>')
# get the id of task
# id -primary key is unique so good way to identify it
def delete(id):
    # create a variable for our task to delete
    # this will get our task by id and if it doesn't exist, we'll gget a 404
    task_to_delete = Todo.query.get_or_404(id)

    try:
        # push to database
        db.session.delete(task_to_delete)
        db.session.commit()
        # redirect back to homepage
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

# post route to update
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)
