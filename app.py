from flask import Flask, request, jsonify
import subprocess
import tempfile

app = Flask(__name__)

@app.route("/run", methods=["POST"])
def run_code():
    code = request.json.get("code", "")
    
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as tmp_file:
        tmp_file.write(code.encode("utf-8"))
        tmp_file.flush()
        
        try:
            result = subprocess.run(
                ["python3", tmp_file.name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=5  # prevent infinite loop
            )
            return jsonify({
                "stdout": result.stdout.decode("utf-8"),
                "stderr": result.stderr.decode("utf-8")
            })
        except subprocess.TimeoutExpired:
            return jsonify({"stdout": "", "stderr": "Execution timed out."})