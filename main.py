from flask import Flask, jsonify
from app import views

app = Flask(__name__)

def health():
    try:
        from app.face_recognition import model
        return jsonify(status="ok", model_loaded=True), 200
    except Exception as e:
        return jsonify(status="error", error=str(e)), 500

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
