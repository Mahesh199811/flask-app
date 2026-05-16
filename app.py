from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from CI/CD Pipeline! Learning to build CI/CD Pipeline for my flask app  ✅"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
