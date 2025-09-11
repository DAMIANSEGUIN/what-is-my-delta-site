from fastapi import FastAPI, Body, HTTPException, File, UploadFile, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
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

@app.get("/test")
def get_test_interface():
    """Serve the test interface HTML"""
    try:
        return FileResponse('static/test_interface.html')
    except:
        return {"message": "Test interface not available", "alternative": "Use /docs for API documentation"}
