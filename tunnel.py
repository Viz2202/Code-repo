from pyngrok import conf,ngrok
import os
config = conf.PyngrokConfig(auth_token=os.getenv("NGROK_AUTH_TOKEN"))

# Open an HTTP tunnel on port 8080
public_url = ngrok.connect(8000)
print("Public URL:", public_url)

# Keep the tunnel open (use your web framework or input to pause)
input("Press Enter to exit...\n")