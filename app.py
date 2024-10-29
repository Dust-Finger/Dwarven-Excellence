from flask import Flask, request, redirect, url_for, render_template, send_from_directory, abort
import os
import uuid

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'logs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the upload folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    if file:
        # Generate a unique filename and save the file
        filename = f"{uuid.uuid4()}.log"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Redirect to the unique link for the uploaded log file
        return redirect(url_for('view_log', filename=filename))

@app.route('/logs/<filename>')
def view_log(filename):
    # Check if file exists
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(file_path):
        abort(404)

    # Read the log file contents
    with open(file_path, 'r') as file:
        log_content = file.read()

    # Render the log content in an HTML template
    return render_template('view_log.html', log_content=log_content)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # Make sure the port is open
