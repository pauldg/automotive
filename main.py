from flask import Flask, request, redirect, jsonify, render_template
import os
import pickle
from werkzeug.utils import secure_filename
from parse import parse_predictors


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["TEMPLATES_AUTO_RELOAD"] = True

model = pickle.load(open('model.pickle','rb'))

@app.route("/")
def index():
    return redirect("/static/index.html")

@app.route("/sendfile", methods=["POST"])
def send_file():
    try:
        os.remove("uploads/" + os.listdir("uploads")[0])
    except IndexError:
	    pass
    fileob = request.files["file2upload"]
    filename = secure_filename(fileob.filename)
    save_path = "{}/{}".format(app.config["UPLOAD_FOLDER"], filename)
    fileob.save(save_path)

    # open and close to update the access time.
    with open(save_path, "r") as f:
        pass

    return "successful_upload"

@app.route("/filenames", methods=["GET"])
def get_filenames():
    filenames = os.listdir("uploads/")

    def modify_time_sort(file_name):
        file_path = "uploads/{}".format(file_name)
        file_stats = os.stat(file_path)
        last_access_time = file_stats.st_atime
        return last_access_time

    filenames = sorted(filenames, key=modify_time_sort)
    return_dict = dict(filenames=filenames)
    return jsonify(return_dict)
	
@app.route("/result", methods=['POST'])
def score():
	input_file_path = "uploads/" + os.listdir("uploads")[0]
	predictors = parse_predictors(input_file_path)
	prediction = model.predict_proba(predictors)
	output = round(prediction[0][0][0], 4)
	return render_template('result.html', result = output)

@app.route("/return_home", methods=['POST'])
def return_home():
	return render_template('index.html')


if __name__ == '__main__':
    app.run(port=5000, debug=True)