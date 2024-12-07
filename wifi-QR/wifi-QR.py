import qrcode

# Wi-Fi details (replace [SSID] with the network name and [PASSWORD] with the network password.
# Must also ensure the encryption type is correct. If not WPA/WPA2, change that as well.
wifi_details = "WIFI:T:WPA;S:[SSID];P:[PASSWORD];;"

# Generate QR Code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(wifi_details)
qr.make(fit=True)

# Save the QR Code as an image
img = qr.make_image(fill_color="black", back_color="white")
img.save("wifi_qr.png")
