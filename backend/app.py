from flask import Flask
from resume_analyzer.routes import analyzer_blueprint
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = 'uploads'

app.register_blueprint(analyzer_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
