from flask import Flask, render_template, request, redirect, url_for
import boto3
from botocore.exceptions import NoCredentialsError

app = Flask(__name__)

# AWS credentials
AWS_ACCESS_KEY = 'AKIA6HSCUECSBFHZYOUZ'
AWS_SECRET_KEY = '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'
AWS_BUCKET_NAME = 'surya_app'

# Function to upload data to S3
def upload_to_s3(data, filename):
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
    try:
        s3.upload_fileobj(data, AWS_BUCKET_NAME, filename)
        return True
    except NoCredentialsError:
        return False

# Route to handle form submission
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']
        
        # Save to S3
        if user_input:
            filename = 'user_input.txt'
            data = user_input.encode('utf-8')
            if upload_to_s3(data, filename):
                return redirect(url_for('success'))
            else:
                return "Failed to save data to S3. Check your AWS credentials."

    return render_template('index.html')

# Route to show success message
@app.route('/success')
def success():
    return "Data saved to S3 successfully!"

if __name__ == '__main__':
    app.run(debug=True)
