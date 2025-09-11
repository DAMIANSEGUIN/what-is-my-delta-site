from fastapi import FastAPI, Body, HTTPException, File, UploadFile, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional
import os
from pathlib import Path

# Import your project logic from api/core/mosaic.py
from .core.mosaic import run_wimd, run_jobsearch, run_wimd_with_file, run_wimd_with_multiple_files
from .core.opportunity_bridge import run_opportunity_bridge, run_wimd_to_opportunities

app = FastAPI(title="Mosaic API (WIMD + JSM)", version="1.0.0")

# Serve static files if directory exists
static_path = Path("static")
if static_path.exists():
    app.mount("/static", StaticFiles(directory="static"), name="static")

class WIMDRequest(BaseModel):
    prompt: str = Field(..., description="User prompt or profile text")

class JobSearchRequest(BaseModel):
    query: str = Field(..., description="Search keywords")
    location: Optional[str] = Field(default="Toronto, ON", description="City/region filter")
    max_results: int = Field(default=25, ge=1, le=200)

class OpportunityBridgeRequest(BaseModel):
    wimd_profile: dict = Field(..., description="WIMD profile data")
    search_parameters: Optional[dict] = Field(default=None, description="Custom search parameters")

class WIMDToOpportunitiesRequest(BaseModel):
    wimd_result: dict = Field(..., description="Fresh WIMD session result")
    search_preferences: Optional[dict] = Field(default=None, description="Search preferences")

@app.get("/")
def root():
    return {
        "message": "Mosaic API Server",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "wimd": "POST /wimd",
            "wimd_upload": "POST /wimd/upload",
            "wimd_multiple": "POST /wimd/multiple",
            "jobsearch": "POST /jobsearch",
            "opportunity_bridge": "POST /opportunities",
            "wimd_to_opportunities": "POST /wimd/opportunities",
            "personas_test": "GET/POST /personas/test",
            "test_interface": "GET /test",
            "docs": "/docs"
        }
    }

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/wimd")
def wimd(req: WIMDRequest):
    try:
        result = run_wimd(req.prompt)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/wimd/upload")
async def wimd_upload(
    file: UploadFile = File(...),
    prompt: str = Form(default="")
):
    """WIMD with voice/document input support"""
    try:
        # Read file content
        file_content = await file.read()
        
        # Process with WIMD
        result = run_wimd_with_file(
            prompt=prompt,
            file_content=file_content,
            filename=file.filename,
            content_type=file.content_type
        )
        
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/wimd/multiple")
async def wimd_multiple_upload(
    files: list[UploadFile] = File(...),
    prompt: str = Form(default="")
):
    """WIMD with multiple document input support"""
    try:
        # Process all files
        files_data = []
        for file in files:
            file_content = await file.read()
            files_data.append((file_content, file.filename, file.content_type))
        
        # Process with WIMD
        result = run_wimd_with_multiple_files(
            prompt=prompt,
            files_data=files_data
        )
        
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/jobsearch")
def jobsearch(req: JobSearchRequest):
    try:
        result = run_jobsearch(query=req.query, location=req.location, max_results=req.max_results)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/opportunities")
def opportunity_bridge(req: OpportunityBridgeRequest):
    """OpportunityBridge - Values-aligned career matching"""
    try:
        result = run_opportunity_bridge(req.wimd_profile, req.search_parameters)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/wimd/opportunities")
def wimd_to_opportunities(req: WIMDToOpportunitiesRequest):
    """Seamless WIMD → OpportunityBridge integration"""
    try:
        result = run_wimd_to_opportunities(req.wimd_result, req.search_preferences)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/personas/test")
def get_personas_test_status():
    """Get personas testing status and results"""
    try:
        import os
        import json
        from pathlib import Path
        
        test_dir = Path("test_results")
        results_files = list(test_dir.glob("*.json")) if test_dir.exists() else []
        
        return {
            "status": "ready",
            "test_results_available": len(results_files),
            "latest_results": max(results_files, key=os.path.getctime).name if results_files else None,
            "personas_testing_endpoint": "/personas/test",
            "instructions": "POST to this endpoint with persona data to run tests"
        }
    except Exception as e:
        return {"status": "error", "detail": str(e)}

class PersonaTestRequest(BaseModel):
    persona_data: dict = Field(..., description="Persona data for testing")
    stages: int = Field(default=3, description="Number of journey stages to test")

@app.post("/personas/test")
def run_personas_test(req: PersonaTestRequest):
    """Run personas testing on live WIMD system"""
    try:
        # Simple persona test using existing WIMD
        persona = req.persona_data
        stages_to_test = req.stages
        
        test_results = []
        
        # Generate test prompts based on persona
        name = persona.get("name", "User")
        maslow_level = persona.get("maslow_level", "safety")
        constraints = persona.get("primary_barriers", [])
        
        # Test scenarios
        test_scenarios = [
            f"Hi, I'm {name}. I'm struggling with my career direction and need guidance.",
            f"I'm feeling overwhelmed by my job search. I have constraints around {', '.join(constraints[:2]) if constraints else 'time and resources'}.",
            f"I want to make progress but I'm not sure what my next step should be."
        ][:stages_to_test]
        
        for i, scenario in enumerate(test_scenarios, 1):
            result = run_wimd(scenario)
            test_results.append({
                "stage": i,
                "scenario": scenario,
                "wimd_response": result,
                "foundation_compliant": result.get("foundation_compliant", False),
                "pulse_score": result.get("pulse_score", 0)
            })
        
        # Calculate test summary
        compliance_rate = sum(1 for r in test_results if r["foundation_compliant"]) / len(test_results)
        avg_pulse = sum(r["pulse_score"] for r in test_results) / len(test_results)
        
        return {
            "persona_tested": persona.get("name", "Unknown"),
            "maslow_level": maslow_level,
            "stages_tested": len(test_results),
            "compliance_rate": round(compliance_rate * 100, 1),
            "average_pulse_score": round(avg_pulse, 1),
            "detailed_results": test_results,
            "timestamp": result.get("timestamp")
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/personas/results")
def get_personas_results():
    """Get historical personas testing results"""
    try:
        import pandas as pd
        from pathlib import Path
        
        results_dir = Path("personas_results")
        if not results_dir.exists():
            return {"error": "No personas results found"}
        
        # Load historical data
        results = {}
        
        # WIMD Output
        wimd_output_path = results_dir / "wimd_output.csv"
        if wimd_output_path.exists():
            df = pd.read_csv(wimd_output_path)
            results["wimd_sessions"] = {
                "total_sessions": len(df),
                "sample_data": df.head(3).to_dict('records'),
                "columns": list(df.columns)
            }
        
        # Tester Feedback
        feedback_path = results_dir / "tester_feedback.csv"
        if feedback_path.exists():
            df_feedback = pd.read_csv(feedback_path)
            avg_ratings = {
                "clarity": df_feedback["clarity_rating_1_5"].mean(),
                "relevance": df_feedback["relevance_rating_1_5"].mean(),
                "trust": df_feedback["trust_rating_1_5"].mean()
            }
            results["tester_feedback"] = {
                "total_tests": len(df_feedback),
                "average_ratings": {k: round(v, 2) for k, v in avg_ratings.items()},
                "sample_feedback": df_feedback.head(3).to_dict('records')
            }
        
        # Personas Definitions
        personas_path = results_dir / "personas.csv"
        if personas_path.exists():
            df_personas = pd.read_csv(personas_path)
            results["personas_tested"] = {
                "total_personas": len(df_personas),
                "personas_list": df_personas.to_dict('records')
            }
        
        return {
            "message": "Historical personas testing results",
            "timestamp": "2025-09-10T11:30:00Z",
            "results": results,
            "access_points": {
                "live_testing": "http://127.0.0.1:8000/test",
                "api_docs": "http://127.0.0.1:8000/docs",
                "new_persona_test": "POST /personas/test"
            }
        }
        
    except Exception as e:
        return {"error": f"Failed to load results: {str(e)}"}

@app.get("/test-simple")
def get_simple_test():
    """Simple test endpoint to verify deployment"""
    return HTMLResponse(content="<h1>✅ Test endpoint working!</h1><p>The deployment is successful.</p>")

@app.get("/test")
def get_test_interface():
    """Serve the test interface HTML"""
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mosaic WIMD Testing Interface</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
        .section { margin: 20px 0; padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px; }
        .section h3 { color: #34495e; margin-top: 0; }
        textarea, input, select { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; font-size: 14px; }
        textarea { height: 100px; font-family: monospace; }
        button { background: #3498db; color: white; border: none; padding: 12px 24px; border-radius: 6px; cursor: pointer; font-size: 14px; margin: 5px; }
        button:hover { background: #2980b9; }
        .result { background: #f8f9fa; border-left: 4px solid #28a745; padding: 15px; margin: 10px 0; border-radius: 4px; }
        .error { background: #f8d7da; border-left: 4px solid #dc3545; color: #721c24; }
        .endpoint { background: #e9f7ff; padding: 10px; border-radius: 4px; font-family: monospace; font-size: 12px; }
        pre { background: #f8f9fa; padding: 10px; border-radius: 4px; overflow-x: auto; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧪 Mosaic WIMD Testing Interface</h1>
        <p><strong>Base URL:</strong> <span class="endpoint" id="apiUrl">Loading...</span></p>

        <div class="section">
            <h3>💬 Basic WIMD Chat Test</h3>
            <textarea id="wimdPrompt" placeholder="Enter your coaching prompt here...">I'm feeling stuck in my career and need guidance on next steps.</textarea>
            <button onclick="testWIMD()">Test WIMD</button>
            <div id="wimdResult"></div>
        </div>

        <div class="section">
            <h3>🔍 Job Search Test</h3>
            <div style="display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 10px;">
                <input type="text" id="jobQuery" placeholder="Job search query" value="data analyst">
                <input type="text" id="jobLocation" placeholder="Location" value="Toronto, ON">
                <input type="number" id="maxResults" placeholder="Max results" value="5">
            </div>
            <button onclick="testJobSearch()">Test Job Search</button>
            <div id="jobResult"></div>
        </div>

        <div class="section">
            <h3>📊 Quick Status Check</h3>
            <button onclick="checkHealth()">Health Check</button>
            <button onclick="openDocs()">API Docs</button>
            <div id="statusResult"></div>
        </div>
    </div>

    <script>
        // Detect if running locally or on Vercel
        const API_BASE = window.location.origin;
        document.getElementById('apiUrl').textContent = API_BASE;

        async function apiCall(endpoint, method = 'GET', body = null, headers = {}) {
            try {
                const config = { method, headers };
                if (body) {
                    config.headers['Content-Type'] = 'application/json';
                    config.body = JSON.stringify(body);
                }
                const response = await fetch(`${API_BASE}${endpoint}`, config);
                return await response.json();
            } catch (error) {
                return { error: error.message };
            }
        }

        function displayResult(containerId, data) {
            const container = document.getElementById(containerId);
            if (data.error) {
                container.innerHTML = `<div class="result error"><strong>Error:</strong> ${data.error}</div>`;
            } else {
                container.innerHTML = `<div class="result"><pre>${JSON.stringify(data, null, 2)}</pre></div>`;
            }
        }

        async function testWIMD() {
            const prompt = document.getElementById('wimdPrompt').value;
            const result = await apiCall('/wimd', 'POST', { prompt });
            displayResult('wimdResult', result);
        }

        async function testJobSearch() {
            const query = document.getElementById('jobQuery').value;
            const location = document.getElementById('jobLocation').value;
            const max_results = parseInt(document.getElementById('maxResults').value);
            
            const result = await apiCall('/jobsearch', 'POST', { query, location, max_results });
            displayResult('jobResult', result);
        }

        async function checkHealth() {
            const result = await apiCall('/health');
            displayResult('statusResult', result);
        }

        function openDocs() {
            window.open(`${API_BASE}/docs`, '_blank');
        }

        // Auto-load status on page load
        window.onload = () => {
            checkHealth();
        };
    </script>
</body>
</html>"""
    return HTMLResponse(content=html_content)
