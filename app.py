
from flask import Flask, request, jsonify
from model import log_measurement, run_thinning_model

app = Flask(__name__)

@app.route("/log", methods=["POST"])
def log():
    data = request.json
    required = {"cultivar", "tree", "cluster", "fruitlet", "size_mm"}
    if not required.issubset(data.keys()):
        return jsonify({"error": "Missing fields"}), 400
    response = log_measurement(
        data["cultivar"], data["tree"], data["cluster"],
        data["fruitlet"], data["size_mm"], data.get("date")
    )
    return jsonify({"message": response})

@app.route("/thinning", methods=["GET"])
def thinning():
    cultivar = request.args.get("cultivar")
    tree = request.args.get("tree", type=int)
    cluster = request.args.get("cluster", type=int)
    if not cultivar or tree is None or cluster is None:
        return jsonify({"error": "Missing parameters"}), 400
    response = run_thinning_model(cultivar, tree, cluster)
    return jsonify({"result": response})

if __name__ == "__main__":
    app.run(debug=True)
