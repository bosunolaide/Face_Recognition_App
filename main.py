from flask import Flask, jsonify
from app import views

app = Flask(__name__)

def health():
    return jsonify(
        status="ok",
        service="face-recognition-app"
    ), 200

app.add_url_rule('/', 'home', views.index)
app.add_url_rule('/app/', 'app', views.app)
app.add_url_rule(
    '/app/gender/',
    'gender',
    views.genderapp,
    methods=['GET', 'POST']
)
app.add_url_rule(
    '/api/predict',
    'api_predict',
    views.api_predict,
    methods=['POST']
)
app.add_url_rule(
    '/health/',
    'health',
    health,
    methods=['GET']
)

if __name__ == "__main__":
    app.run(debug=True)
