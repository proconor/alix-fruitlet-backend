
# Alix Fruitlet Backend

This Flask app receives spoken-style fruitlet measurements and returns real-time growth tracking and thinning model predictions.

## Endpoints

### POST /log
Logs a fruitlet measurement.
```json
{
  "cultivar": "Fuji",
  "tree": 3,
  "cluster": 6,
  "fruitlet": 2,
  "size_mm": 9.5
}
```

### GET /thinning
Runs Greene-style thinning model.
Query params: `?cultivar=Fuji&tree=3&cluster=6`

## Deploy (example on DigitalOcean)
```bash
sudo apt update && sudo apt install -y python3-pip git
git clone <your-repo>
cd alix_fruitlet_backend
pip3 install -r requirements.txt
python3 app.py
```

For production, use Gunicorn and Nginx.
