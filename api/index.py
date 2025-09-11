from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(title="Mosaic API (Minimal)", version="1.0.0")

class WIMDRequest(BaseModel):
    prompt: str = Field(..., description="User prompt or profile text")

class JobSearchRequest(BaseModel):
    query: str = Field(..., description="Search keywords")
    location: Optional[str] = Field(default="Toronto, ON", description="City/region filter")
    max_results: int = Field(default=25, ge=1, le=200)

@app.get("/")
def root():
    return {
        "message": "Mosaic API Server (Minimal Mode)",
        "version": "1.0.0",
        "status": "running",
        "note": "Core WIMD functionality temporarily disabled for deployment testing",
        "endpoints": {
            "health": "/health",
            "test_interface": "GET /test",
            "docs": "/docs"
        }
    }

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/test-simple")
def get_simple_test():
    """Simple test endpoint to verify deployment"""
    return HTMLResponse(content="<h1>✅ Test endpoint working!</h1><p>The deployment is successful.</p>")

@app.post("/wimd")
def wimd_placeholder(req: WIMDRequest):
    """Placeholder WIMD endpoint for testing"""
    return {
        "result": {
            "message": "WIMD functionality temporarily disabled",
            "prompt_received": req.prompt,
            "status": "placeholder_mode"
        }
    }

@app.post("/jobsearch")
def jobsearch_placeholder(req: JobSearchRequest):
    """Placeholder job search endpoint"""
    return {
        "results": [
            {"title": "Sample Job", "company": "Test Company", "location": req.location}
        ],
        "message": "Job search functionality temporarily disabled",
        "status": "placeholder_mode"
    }

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
        .warning { background: #fff3cd; border-left: 4px solid #ffc107; color: #856404; padding: 15px; margin: 10px 0; border-radius: 4px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧪 Mosaic WIMD Testing Interface</h1>
        <p><strong>Base URL:</strong> <span class="endpoint" id="apiUrl">Loading...</span></p>
        
        <div class="warning">
            <strong>⚠️ Testing Mode:</strong> Core WIMD functionality is temporarily in placeholder mode for deployment testing.
        </div>

        <div class="section">
            <h3>💬 Basic WIMD Chat Test</h3>
            <textarea id="wimdPrompt" placeholder="Enter your coaching prompt here...">I'm feeling stuck in my career and need guidance on next steps.</textarea>
            <button onclick="testWIMD()">Test WIMD (Placeholder)</button>
            <div id="wimdResult"></div>
        </div>

        <div class="section">
            <h3>🔍 Job Search Test</h3>
            <div style="display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 10px;">
                <input type="text" id="jobQuery" placeholder="Job search query" value="data analyst">
                <input type="text" id="jobLocation" placeholder="Location" value="Toronto, ON">
                <input type="number" id="maxResults" placeholder="Max results" value="5">
            </div>
            <button onclick="testJobSearch()">Test Job Search (Placeholder)</button>
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