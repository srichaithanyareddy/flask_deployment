from flask import Flask, render_template, request
import re

app = Flask(__name__)

def highlight_matches(test_string, regex_pattern):
    if not test_string or not regex_pattern:
        return ""
    
    try:
        regex = re.compile(regex_pattern)
        highlighted_text = regex.sub(
            lambda match: f'<span style="background-color: yellow;">{match.group()}</span>',
            test_string
        )
        return highlighted_text
    except re.error:
        return "Invalid regex pattern"

@app.route('/', methods=['GET', 'POST'])
def index():
    matches = []
    email = None
    is_valid = False
    if request.method == 'POST':
        if 'test_string' in request.form and 'regex_pattern' in request.form:
            test_string = request.form['test_string']
            regex_pattern = request.form['regex_pattern']
            matches = re.findall(regex_pattern, test_string)
        elif 'email' in request.form:
            email = request.form['email']
            is_valid = bool(re.fullmatch(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email))
    return render_template('index.html', matches=matches, email=email, is_valid=is_valid, highlight_matches=highlight_matches)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)