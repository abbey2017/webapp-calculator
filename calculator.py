from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

def perform_calculation(a, b, operation):
    try:
        a, b = float(a), float(b)
        if operation == 'add':
            return a + b
        elif operation == 'subtract':
            return a - b
        elif operation == 'multiply':
            return a * b
        elif operation == 'divide':
            if b == 0:
                raise ValueError("Division by zero is not allowed")
            return a / b
        else:
            raise ValueError("Invalid operation")
    except ValueError as e:
        return str(e)
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Add a root route to show API instructions
@app.route("/", methods=["GET", "POST"])
def index():
    """
    '''
    <h1>Calculator API</h1>
    <p>Use the calculator with GET requests:</p>
    <ul>
        <li><a href="/calculate?a=10&b=5&operation=add">Addition: /calculate?a=10&b=5&operation=add</a></li>
        <li><a href="/calculate?a=10&b=5&operation=subtract">Subtraction: /calculate?a=10&b=5&operation=subtract</a></li>
        <li><a href="/calculate?a=10&b=5&operation=multiply">Multiplication: /calculate?a=10&b=5&operation=multiply</a></li>
        <li><a href="/calculate?a=10&b=5&operation=divide">Division: /calculate?a=10&b=5&operation=divide</a></li>
    </ul>
    '''
    """
    result = ""
    if request.method == "POST":
        a = float(request.form["a"])
        b = float(request.form["b"])
        operation = request.form["operation"]

        result = perform_calculation(a, b, operation)

        return render_template("calculator.html", a=a, b=b, operation=operation, result=result)
    else:
        return render_template("calculator.html", result=result)

@app.route('/calculate', methods=['GET', 'POST'])
def calculate():
    if request.method == 'POST':
        data = request.get_json()
        
        if not all(k in data for k in ('a', 'b', 'operation')):
            return jsonify({'error': 'Missing required fields'}), 400
        
        a = data['a']
        b = data['b']
        operation = data['operation']
    else:  # GET request
        a = request.args.get('a')
        b = request.args.get('b')
        operation = request.args.get('operation')
        
        if not all([a, b, operation]):
            return jsonify({'error': 'Missing required parameters. Use ?a=number&b=number&operation=add'}), 400
    
    result = perform_calculation(a, b, operation)
    
    if isinstance(result, str):
        return jsonify({'error': result}), 400
    
    return jsonify({
        'result': result,
        'operation': operation,
        'a': a,
        'b': b
    })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

# Add error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found. Please check the URL or visit the root path (/) for instructions.'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error. Please try again later.'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)