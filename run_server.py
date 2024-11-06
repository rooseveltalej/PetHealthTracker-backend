import subprocess
import sys

if __name__ == "__main__":
    # Comando para iniciar el servidor con python -m uvicorn
    command = [sys.executable, "-m", "uvicorn", "app:app", "--reload"]

    try:
        print("Starting FastAPI server...")
        subprocess.run(command)
    except KeyboardInterrupt:
        print("\nServer stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")