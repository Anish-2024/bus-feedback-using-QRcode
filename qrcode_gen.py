import qrcode

# Replace with your laptop's local IP (from app.py output)
base_url = "http://192.168.193.47:5000/feedback"
bus_id = "KA25B1221"

# Final URL
full_url = f"{base_url}?bus={bus_id}"

# Generate QR Code
qr = qrcode.make(full_url)
qr.save(f"{bus_id}_qrcode.png")

print(f"✅ QR Code generated for bus {bus_id} at URL: {full_url}")
