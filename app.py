from flask import Flask, render_template

app = Flask(__name__)

# Route for rendering the upload form
@app.route('/')
def upload_form():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=4000)
