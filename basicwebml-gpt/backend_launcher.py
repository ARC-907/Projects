import subprocess
import sys
import os


def main() -> None:
    """Launch the FastAPI backend using uvicorn."""
    backend_dir = os.path.join(os.path.dirname(__file__), "backend")
    cmd = [sys.executable, "-m", "uvicorn", "app:app", "--host", "127.0.0.1", "--port", "8000"]
    proc = subprocess.Popen(cmd, cwd=backend_dir)
    try:
        proc.wait()
    except KeyboardInterrupt:
        proc.terminate()
        proc.wait()


if __name__ == "__main__":
    main()
