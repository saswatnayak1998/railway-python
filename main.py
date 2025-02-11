from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess

app = FastAPI()

class CodeExecutionRequest(BaseModel):
    code: str

@app.post("/run")
def run_code(request: CodeExecutionRequest):
    try:
        # Run the Python code inside the container
        result = subprocess.run(
            ["python3", "-c", request.code],
            text=True,
            capture_output=True,
            timeout=5
        )

        return {
            "output": result.stdout if result.stdout else result.stderr
        }

    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=400, detail="Execution timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
