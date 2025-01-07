import os
import requests
import json

# Replace these with your actual values
SERVICE_ID = os.getenv('RENDER_SERVICE_ID')
API_KEY = os.getenv('RENDER_API_KEY')

def trigger_deploy():
    url = f"https://api.render.com/v1/services/{SERVICE_ID}/deploys"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, headers=headers)
        if response.status_code == 201:
            print("Deployment triggered successfully!")
            deploy_data = response.json()
            print(f"Deploy ID: {deploy_data.get('id')}")
            print(f"Status: {deploy_data.get('status')}")
        else:
            print(f"Failed to trigger deployment. Status code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error triggering deployment: {str(e)}")

if __name__ == "__main__":
    if not SERVICE_ID or not API_KEY:
        print("Error: Please set RENDER_SERVICE_ID and RENDER_API_KEY environment variables")
        exit(1)
    
    trigger_deploy()
