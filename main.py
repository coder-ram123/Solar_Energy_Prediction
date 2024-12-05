from flask import Flask, render_template, request
from aqi_api import fetch_aqi, estimate_solar_generation

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_aqi", methods=["POST"])
def get_aqi():
    city = request.form.get("city")
    aqi_data = fetch_aqi(city)
    
    if "stations" in aqi_data and aqi_data.get("message") == "success":
        station = aqi_data["stations"][0]  
        aqi_context = {
            "city": station.get("city"),
            "state": station.get("state"),
            "CO": station.get("CO", 0),
            "NO2": station.get("NO2", 0),
            "OZONE": station.get("OZONE", 0),
            "PM10": station.get("PM10", 0),
            "PM25": station.get("PM25", 0),
            "SO2": station.get("SO2", 0),
            "AQI": station.get("AQI"),
            "category": station.get("aqiInfo", {}).get("category"),
            "updated_at": station.get("updatedAt")
        }
        
        solar_generation, contributions = estimate_solar_generation(aqi_context)
        aqi_context["solar_generation"] = solar_generation
        aqi_context["contributions"] = contributions
    else:
        aqi_context = {
            "error": "Unable to fetch AQI data for the specified city."
        }

    return render_template("result.html", context=aqi_context)

if __name__ == "__main__":
    app.run(debug=True)
