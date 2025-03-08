Start-Process -NoNewWindow -FilePath "powershell" -ArgumentList "-NoExit", "-Command", "cd C:\Users\Jason\polish-passion-project\server; .\venv\Scripts\Activate; python app.py"
Start-Process -NoNewWindow -FilePath "powershell" -ArgumentList "-NoExit", "-Command", "cd C:\Users\Jason\polish-passion-project\client; npm run dev"
