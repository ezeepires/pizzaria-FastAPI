import requests

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3IiwiZXhwIjoxNzc3NjkwMTQ4fQ.dxX5BiWmYOMzLDvLWfobT68sS3CHGkX9CT9EOvycLtw"
}

requisicao = requests.get("http://127.0.0.1:8000/auth/refresh", headers=headers)
print(requisicao.json())