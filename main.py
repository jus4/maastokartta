import pyproj
import re
import requests
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("frontpage.html", title="Maastokartta Google maps")

@app.route('/link-generator', methods=['POST'])
def generate():
    maastokarttaLink = ''
    useGoogleShortUrl = request.form.get('use-google-short-url', None)
    googleMapsShortUlr = request.form['google-link']
    formLatitude = request.form["latitude"]
    formLongitude = request.form["longitude"]
    title = request.form["title"]
    description = request.form["description"]

    if (googleMapsShortUlr and useGoogleShortUrl):
        gShortUrl = getGoogleShortMapLink(googleMapsShortUlr)
        if (gShortUrl):
            generatedMaastokarttaLink = generateMaastokarttaLink(gShortUrl['northing'], gShortUrl['easting'], title, description)
            maastokarttaLink = generatedMaastokarttaLink
    
    if ( formLatitude and formLongitude ):
        try:
            latitude = validateFloat(formLatitude)
            longitude = validateFloat(formLongitude)
            if ( latitude and longitude ): 
                convertedLatLong = convertLatLong(latitude, longitude)
                generatedMaastokarttaLink = generateMaastokarttaLink(convertedLatLong['northing'], convertedLatLong['easting'], title, description)
                maastokarttaLink = generatedMaastokarttaLink
        except ValueError:
            maastokarttaLink = ''

    return f'<input id="result-input" type="text" class="w-full overflow-hidden border-t border-b border-l block truncate bg-gray-50 p-2 rounded-l-md" value="{maastokarttaLink}" />'
        
def validateFloat(input: str):
    try:
        float_value = float(input)
        return float_value
    except ValueError:
        return False


# Google maps does not like spamming from same IP address but we still get the cordinates
def getGoogleShortMapLink(shortUrl):
    res = requests.get(shortUrl, allow_redirects=True)

    # Resolve google places 
    googlePlaceLongitudePattern = r'!3d-?\d+\.\d+'
    googlePlaceLatitudePattern = r'!4d-?\d+\.\d+'
    googleLong = re.findall(googlePlaceLongitudePattern , res.url)
    googleLat = re.findall(googlePlaceLatitudePattern , res.url)
    if (googleLat and googleLong):
        convertedLatLong = convertLatLong(googleLong[0][3:], googleLat[0][3:])
        return convertedLatLong 

    # Resolve direct links
    gSearchLongPattern = r'\/search\/-?\d+\.\d+'
    gSearchLatPattern = r',%2B-?\d+\.\d+'
    gSearchLong = re.findall(gSearchLongPattern, res.url)
    gSearchLat = re.findall(gSearchLatPattern, res.url)

    if ( gSearchLong and gSearchLat):
        convertedLatLong = convertLatLong(gSearchLong[0][8:], gSearchLat[0][4:])
        return convertedLatLong 

    return False


def convertLatLong(lat, lon):
    wgs84 = pyproj.CRS("EPSG:4326")  # WGS84: Latitude/Longitude EPSG:3857
    etrs_tm35fin = pyproj.CRS("EPSG:3067")  # ETRS-TM35FIN: Easting/Northing
    
    # Create a transformer object to transform between WGS84 and ETRS-TM35FIN
    transformer = pyproj.Transformer.from_crs(wgs84, etrs_tm35fin, always_xy=True)
    
    # Transform the coordinates from WGS84 (lat, lon) to ETRS-TM35FIN (easting, northing)
    easting, northing = transformer.transform(lon, lat)
    return {'easting': "{:.3f}".format(easting), 'northing': "{:.3f}".format(northing)}

def generateMaastokarttaLink(northing: str, easting: str, title = '',description = ''):
    maastokarttaLink = f"https://asiointi.maanmittauslaitos.fi/karttapaikka/?lang=fi&share=customMarker&n={northing}&e={easting}&title={title}&desc={description}&zoom=10&layers=W3siaWQiOjIsIm9wYWNpdHkiOjEwMH1d-z"
    return maastokarttaLink



