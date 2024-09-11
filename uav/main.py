import io

from client import DroneClientType, drone_factory
from flask import Flask, abort, send_file


app = Flask(__name__)
app.config["IMAGE"] = "image"


@app.get("/snapshot")
def get_snapshot():
    drone = drone_factory.get_action(DroneClientType.virtual)
    drone.connect()
    payload = drone.get_image()

    mem = io.BytesIO()
    mem.write(payload["img"])
    mem.seek(0)

    try:
        return send_file(
            mem, as_attachment=True, mimetype="image/jpeg", download_name="snapshot.jpg"
        )
    except FileNotFoundError:
        abort(404)


if __name__ == "__main__":
    host = "localhost"
    port = 5088
    app.run(host=host, port=port, debug=True)
