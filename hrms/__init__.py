from flask import Flask


app = Flask(__name__)
app.config['SECRET_KEY'] = 'thequickbrownfox'


from hrms.main.routes import main
from hrms.employee.routes import employee
app.register_blueprint(main)
app.register_blueprint(employee)