from flask import render_template, send_from_directory
import flask, os, json

app = flask.Flask(__name__)

# Serve locally for debugging
@app.route('/')
def home():
    with open(os.path.join('temp', 'dashInfo.json'), 'r') as file:
        dashInfo = json.load(file)

    return render_template('index.html', dashInfo=dashInfo)

@app.route('/temp/<path:filename>')
def serveTemp(filename):
    return send_from_directory('temp', filename)

if __name__ == "__main__":
    app.debug = True
    app.run(port=8080)

    # with app.app_context():
    #     rendered = render_template('blog.html', \
    #         title = "My Generated Page", \
    #         people = [{"name": "Mark"}, {"name": "Michael"}])
    #     print(rendered)
