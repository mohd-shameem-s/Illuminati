import requests
import http.server
import socketserver

PORT = 8080  # Change if needed

class TrackIPHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        ip = self.client_address[0]
        location_data = get_location(ip)

        print(f"🌍 Target IP: {ip}")
        print(f"📍 Location: {location_data}")

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Location tracked successfully!")

def get_location(ip):
    """Fetch location from IP"""
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        return {
            "City": data.get("city", "Unknown"),
            "Region": data.get("regionName", "Unknown"),
            "Country": data.get("country", "Unknown"),
            "Latitude": data.get("lat", "Unknown"),
            "Longitude": data.get("lon", "Unknown"),
            "ISP": data.get("isp", "Unknown")
        }
    except:
        return {"Error": "Failed to get location"}

with socketserver.TCPServer(("", PORT), TrackIPHandler) as httpd:
    print(f"🌐 Tracking Server Running on Port {PORT}")
    httpd.serve_forever()
