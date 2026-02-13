from flask import Flask, jsonify
from app import views

app = Flask(__name__)  # webserver gateway interface (WSGI)

def health():
    """Basic health check endpoint for load balancers/monitoring."""
    return jsonify(status="ok", service="face-recognition-app"), 200

app.add_url_rule(rule='/', endpoint='home', view_func=views.index)
app.add_url_rule(rule='/app/', endpoint='app', view_func=views.app)
app.add_url_rule(
    rule='/app/gender/',
    endpoint='gender',
    view_func=views.genderapp,
    methods=['GET', 'POST']
)

app.add_url_rule(
    rule='/api/predict',
    endpoint='api_predict',
    view_func=views.api_predict,
    methods=['POST']
)

app.add_url_rule(
    rule='/health/',
    endpoint='health',
    view_func=health,
    methods=['GET']
)

if __name__ == "__main__":
    app.run(debug=True)
