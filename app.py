from flask import Flask, request, render_template_string, render_template, jsonify
import os
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/render', methods=['POST'])
def render_template_vulnerable():
    """
    VULNERABLE FUNCTION
    This function contains a Server-Side Template Injection vulnerability.
    It directly renders user input as part of a template.
    """
    user_template = request.form.get('template', '')
    
    # WARNING: The following line is intentionally vulnerable to SSTI
    # In a real application, NEVER render user input as a template
    rendered_template = render_template_string(user_template)
    
    return render_template('result.html', 
                          rendered_template=rendered_template,
                          template_source=user_template)

@app.route('/secure', methods=['POST'])
def render_template_secure():
    """
    SECURE FUNCTION
    This function demonstrates the secure way to handle user input.
    """
    user_input = request.form.get('template', '')
    
    # Here the user input is passed as a variable to the template, not rendered as a template itself
    return render_template('result.html', 
                          rendered_template=user_input,
                          template_source=user_input,
                          secure=True)

@app.route('/get_popen_index', methods=['GET'])
def get_popen_index():
    """
    Helper endpoint to find the index of subprocess.Popen in __subclasses__()
    This helps demonstrate the SSTI vulnerability more effectively.
    """
    try:
        for i, cls in enumerate(object.__subclasses__()):
            if cls.__name__ == 'Popen' and cls.__module__.startswith('subprocess'):
                return jsonify({'index': i, 'name': cls.__name__, 'module': cls.__module__})
        return jsonify({'error': 'subprocess.Popen not found in subclasses'})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
