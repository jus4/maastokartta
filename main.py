import pyproj
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
    googleLink = request.form["google-link"]
    if ( googleLink ) :
        getGoogleShortMapLink(googleLink)
    latitude = request.form["latitude"]
    longitude = request.form["longitude"]
    title = request.form["title"]
    description = request.form["description"]
    
    if ( latitude and longitude ):
        easting, northing = convertLatLong("{:.8}".format(latitude), "{:.8}".format(longitude))
        maastokarttaLink = f"https://asiointi.maanmittauslaitos.fi/karttapaikka/?lang=fi&share=customMarker&n={northing}&e={easting}&title={title}&desc={description}&zoom=10&layers=W3siaWQiOjIsIm9wYWNpdHkiOjEwMH1d-z"
        return f'<input id="result-input" type="text" class="w-full overflow-hidden border-t border-b border-l block truncate bg-gray-50 p-2 rounded-l-md" value="{maastokarttaLink}" />'

    return ''
        

def getGoogleShortMapLink(shortUrl):
    res = requests.get(shortUrl, allow_redirects=True)
    print(res.url)

    # coords_pattern = r"@(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)"
    # match = re.search(coords_pattern, res.url)
    # if match:
    #     latitude, longitude = match.groups()
    #     print(f"Latitude: {latitude}, Longitude: {longitude}")


    # data = res.text
    # pattern = r"window\.ES5DGURL\s*=\s*'([^']+)';"
    # # Search for the pattern in the HTML content
    # match = re.search(pattern, res.text)
    # 
    # if match:
    #     es5dgurl = match.group(1)
    #     print("Extracted ES5DGURL:", es5dgurl)
    # else:
    #     print("ES5DGURL not found in the HTML content")
    #     print(res.url)
    #
def convertLatLong(lat, lon):
    wgs84 = pyproj.CRS("EPSG:4326")  # WGS84: Latitude/Longitude EPSG:3857
    etrs_tm35fin = pyproj.CRS("EPSG:3067")  # ETRS-TM35FIN: Easting/Northing
    
    # Create a transformer object to transform between WGS84 and ETRS-TM35FIN
    transformer = pyproj.Transformer.from_crs(wgs84, etrs_tm35fin, always_xy=True)
    
    # Transform the coordinates from WGS84 (lat, lon) to ETRS-TM35FIN (easting, northing)
    northing, easting = transformer.transform(lon, lat)
    return {"{:.3f}".format(easting), "{:.3f}".format(northing)}

def generateMaastokarttaLink(northing, easting, title = '',description = ''):
    if (northing or easting):
        maastokarttaLink = f"https://asiointi.maanmittauslaitos.fi/karttapaikka/?lang=fi&share=customMarker&n={northing}&e={easting}&title={title}&desc={description}&zoom=10&layers=W3siaWQiOjIsIm9wYWNpdHkiOjEwMH1d-z"
        return maastokarttaLink
    return False



