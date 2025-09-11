# === WIMD + OpenAI Integration (Foundation Architecture) ===
import os
import json
import re
import tempfile
from datetime import datetime
from typing import Dict, List, Optional, Tuple, BinaryIO
from openai import OpenAI
import PyPDF2  
from docx import Document
from PIL import Image
import io
import zipfile

# Foundation coaching principles embedded in system architecture
COACHING_GUARDRAILS = {
    "assume_wholeness": True,
    "assume_resourcefulness": True, 
    "non_directive": True,
    "single_next_step": True,
    "preserve_user_agency": True,
    "evidence_required": True
}

# Initialize OpenAI client (lazy initialization to avoid import errors)
def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(api_key=api_key)

def run_wimd(prompt: str) -> Dict:
    """WIMD engine with integrated OpenAI coaching intelligence"""
    
    # Detect inflection signals in user input
    signals = detect_inflection_signals(prompt)
    
    # Generate coaching response based on Foundation principles
    coaching_response = generate_coaching_response(prompt, signals)
    
    # Create experiment card if appropriate
    experiment = None
    if should_create_experiment(signals, coaching_response):
        experiment = create_experiment_card(prompt, coaching_response)
    
    # Calculate self-efficacy pulse from language patterns
    pulse_score = calculate_pulse_score(prompt)
    
    return {
        "coaching_response": coaching_response,
        "signals_detected": signals,
        "pulse_score": pulse_score,
        "experiment_card": experiment,
        "timestamp": datetime.now().isoformat(),
        "foundation_compliant": True
    }

def detect_inflection_signals(text: str) -> List[str]:
    """Detect language patterns indicating need for support"""
    signals = []
    text_lower = text.lower()
    
    # Helplessness patterns
    helplessness_patterns = ["i can't", "it's impossible", "nothing works", "i'm stuck", "there's no way"]
    if any(pattern in text_lower for pattern in helplessness_patterns):
        signals.append("helplessness")
    
    # Binary thinking patterns
    binary_patterns = ["always", "never", "all or nothing", "complete failure", "total success"]
    if any(pattern in text_lower for pattern in binary_patterns):
        signals.append("binary_thinking")
    
    # Catastrophic framing
    catastrophic_patterns = ["disaster", "catastrophe", "ruined everything", "worst case", "terrible", "awful"]
    if any(pattern in text_lower for pattern in catastrophic_patterns):
        signals.append("catastrophic_framing")
    
    # Self-blame patterns
    blame_patterns = ["i should have", "i'm such an idiot", "i always mess up", "it's my fault"]
    if any(pattern in text_lower for pattern in blame_patterns):
        signals.append("self_blame")
    
    return signals

def calculate_pulse_score(text: str) -> int:
    """Calculate self-efficacy pulse from language patterns (0-100)"""
    text_lower = text.lower()
    score = 70  # baseline
    
    # Positive indicators (+)
    positive_patterns = ["i can", "i will", "excited", "confident", "progress", "learned", "achieved"]
    for pattern in positive_patterns:
        if pattern in text_lower:
            score += 5
    
    # Negative indicators (-)
    negative_patterns = ["can't", "impossible", "stuck", "frustrated", "overwhelmed", "hopeless"]
    for pattern in negative_patterns:
        if pattern in text_lower:
            score -= 10
    
    return max(0, min(100, score))

def filter_directive_language(response: str) -> str:
    """Post-processing filter to remove directive language patterns"""
    import re
    
    # Dictionary of directive patterns and their non-directive replacements
    replacements = {
        r'\byou need to\b': 'you might consider',
        r'\byou should\b': 'you could explore',  
        r'\byou must\b': 'you might find it helpful to',
        r'\bI recommend\b': 'You might explore',
        r'\byou have to\b': 'you could consider',
        r'\btry this\b': 'you might explore this',
        r'\bdo this\b': 'you might consider this',
        r'\bneed to make\b': 'are considering making',
        r'\bhave to decide\b': 'are exploring decisions about'
    }
    
    filtered_response = response
    for pattern, replacement in replacements.items():
        filtered_response = re.sub(pattern, replacement, filtered_response, flags=re.IGNORECASE)
    
    return filtered_response

def generate_coaching_response(prompt: str, signals: List[str]) -> str:
    """Generate Foundation-compliant coaching response via OpenAI"""
    
    system_prompt = f"""
You are a co-active coach following Foundation principles. Your responses MUST comply with these rules:

FOUNDATION COMPLIANCE RULES:
1. NEVER use directive language: "you should", "you need to", "you must", "do this", "try this"
2. ALWAYS ask questions instead of giving advice
3. Use curious, exploratory language: "What would it look like if...", "How might you...", "What feels right for you..."
4. Preserve user agency - they choose their path
5. Assume user has their own answers within them

REQUIRED RESPONSE PATTERN:
- Start with empathetic reflection: "I hear..." or "It sounds like..."
- Ask ONE powerful question that invites exploration
- End with open invitation for user to choose their direction

FORBIDDEN PHRASES (never use these):
- "you should"
- "you need to" 
- "you must"
- "do this"
- "try this"
- "I recommend"
- "you have to"
- "need to make"
- "have to decide"

ALWAYS REPHRASE USER LANGUAGE:
- User: "I need to decide" → Coach: "What would help you feel clear about this decision?"
- User: "What should I do" → Coach: "What options feel most aligned with your values?"
- Avoid echoing directive language back to the user

EXAMPLE COMPLIANT RESPONSES:
- "I hear your frustration. What would success look like for you in this situation?"
- "It sounds like you're at a crossroads. What values feel most important as you consider your options?"
- "I sense some uncertainty. What would help you feel more confident about your next step?"

Detected signals: {', '.join(signals) if signals else 'None'}

Remember: Ask questions, don't give directions. Your role is to guide discovery, not prescribe solutions.
"""
    
    try:
        client = get_openai_client()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        coaching_response = response.choices[0].message.content.strip()
        
        # Post-processing filter for Foundation compliance
        coaching_response = filter_directive_language(coaching_response)
        
        return coaching_response
    except Exception as e:
        return f"I hear you. What feels most important to focus on right now? (API Error: {str(e)})"

def should_create_experiment(signals: List[str], response: str) -> bool:
    """Determine if an experiment card should be generated"""
    return len(signals) >= 2 or "experiment" in response.lower() or "try" in response.lower()

def create_experiment_card(prompt: str, coaching_response: str) -> Dict:
    """Generate experiment card using Miracle Question approach"""
    
    miracle_prompt = f"""
Based on this user situation: {prompt[:200]}...

Create a small 3-5 day experiment using the Miracle Question approach:
1. What's the smallest observable change they could notice?
2. What micro-action could create that change?
3. How would they know it's working?

Return ONLY a JSON object with:
{{
  "title": "Clear experiment title",
  "micro_action": "Specific behavior to try",
  "success_cues": ["Observable sign 1", "Observable sign 2"],
  "time_window": "3-5 days"
}}
"""
    
    try:
        client = get_openai_client()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": miracle_prompt}],
            max_tokens=200,
            temperature=0.5
        )
        return json.loads(response.choices[0].message.content.strip())
    except Exception as e:
        return {
            "title": "Explore next small step",
            "micro_action": "Notice one thing that's working, however small",
            "success_cues": ["Increased awareness", "Reduced overwhelm"],
            "time_window": "3-5 days",
            "error": str(e)
        }

def transcribe_audio(audio_file: BinaryIO) -> str:
    """Transcribe audio using OpenAI Whisper"""
    try:
        client = get_openai_client()
        
        # Create a temporary file with proper extension
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
            temp_file.write(audio_file.read())
            temp_file.flush()
            
            # Transcribe the audio
            with open(temp_file.name, 'rb') as f:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=f,
                    response_format="text"
                )
            
            # Clean up temp file
            os.unlink(temp_file.name)
            
            return transcript.strip()
    except Exception as e:
        return f"Audio transcription error: {str(e)}"

def extract_text_from_pdf(pdf_file: BinaryIO) -> str:
    """Extract text from PDF file"""
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        
        for page in reader.pages:
            text += page.extract_text() + "\n"
        
        return text.strip()
    except Exception as e:
        return f"PDF extraction error: {str(e)}"

def extract_text_from_docx(docx_file: BinaryIO) -> str:
    """Extract text from Word document"""
    try:
        doc = Document(docx_file)
        text = ""
        
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        
        return text.strip()
    except Exception as e:
        return f"DOCX extraction error: {str(e)}"

def analyze_image(image_file: BinaryIO) -> str:
    """Analyze image using OpenAI Vision"""
    try:
        client = get_openai_client()
        
        # Read and encode image
        image_data = image_file.read()
        
        # Convert to base64
        import base64
        base64_image = base64.b64encode(image_data).decode('utf-8')
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Please analyze this image and extract any text, diagrams, or relevant information that could be used for career coaching or job search purposes. Focus on professional content, skills, experiences, or goals mentioned."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=500
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Image analysis error: {str(e)}"

def extract_text_from_zip(zip_file: BinaryIO, max_files: int = 5) -> str:
    """Extract text from all supported files in a zip archive"""
    try:
        extracted_texts = []
        files_processed = 0
        
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            # Get file list and limit to max_files
            file_list = zip_ref.namelist()[:max_files]
            
            for filename in file_list:
                if files_processed >= max_files:
                    break
                    
                # Skip directories
                if filename.endswith('/'):
                    continue
                
                try:
                    with zip_ref.open(filename) as file_in_zip:
                        file_content = file_in_zip.read()
                        
                        # Detect file type and process
                        if filename.lower().endswith(('.txt')):
                            text = file_content.decode('utf-8', errors='ignore')
                            extracted_texts.append(f"[{filename}]:\n{text}")
                            files_processed += 1
                            
                        elif filename.lower().endswith(('.pdf')):
                            text = extract_text_from_pdf(io.BytesIO(file_content))
                            extracted_texts.append(f"[{filename}]:\n{text}")
                            files_processed += 1
                            
                        elif filename.lower().endswith(('.docx', '.doc')):
                            text = extract_text_from_docx(io.BytesIO(file_content))
                            extracted_texts.append(f"[{filename}]:\n{text}")
                            files_processed += 1
                            
                        elif filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                            text = analyze_image(io.BytesIO(file_content))
                            extracted_texts.append(f"[{filename}]:\n{text}")
                            files_processed += 1
                            
                        elif filename.lower().endswith(('.mp3', '.wav', '.m4a', '.ogg')):
                            text = transcribe_audio(io.BytesIO(file_content))
                            extracted_texts.append(f"[{filename}]:\n{text}")
                            files_processed += 1
                            
                except Exception as e:
                    extracted_texts.append(f"[{filename}]: Error processing file - {str(e)}")
                    
        result = "\n\n".join(extracted_texts)
        
        if files_processed >= max_files and len(file_list) > max_files:
            result += f"\n\n[Note: Only first {max_files} files processed from zip archive]"
            
        return result
        
    except Exception as e:
        return f"Zip extraction error: {str(e)}"

def process_file_input(file_content: bytes, filename: str, content_type: str) -> str:
    """Process uploaded file and extract text content"""
    file_obj = io.BytesIO(file_content)
    
    # Check for zip files first
    if content_type == 'application/zip' or filename.lower().endswith('.zip'):
        return extract_text_from_zip(file_obj, max_files=5)
    
    # Determine file type and process accordingly
    elif content_type.startswith('audio/') or filename.lower().endswith(('.mp3', '.wav', '.m4a', '.ogg')):
        return transcribe_audio(file_obj)
    
    elif content_type == 'application/pdf' or filename.lower().endswith('.pdf'):
        return extract_text_from_pdf(file_obj)
    
    elif content_type in ['application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword'] or filename.lower().endswith(('.docx', '.doc')):
        return extract_text_from_docx(file_obj)
    
    elif content_type.startswith('image/') or filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
        return analyze_image(file_obj)
    
    elif content_type.startswith('text/') or filename.lower().endswith('.txt'):
        return file_content.decode('utf-8', errors='ignore')
    
    else:
        return f"Unsupported file type: {content_type} ({filename})"

def run_wimd_with_file(prompt: str = "", file_content: bytes = None, filename: str = "", content_type: str = "") -> Dict:
    """Enhanced WIMD with file input support"""
    
    # Process file if provided
    file_text = ""
    if file_content:
        file_text = process_file_input(file_content, filename, content_type)
    
    # Combine prompt and file content
    combined_prompt = prompt
    if file_text:
        combined_prompt = f"{prompt}\n\n[File Content from {filename}]:\n{file_text}"
    
    # Use existing WIMD logic
    result = run_wimd(combined_prompt)
    
    # Add file processing info to result
    if file_content:
        result["file_processed"] = {
            "filename": filename,
            "content_type": content_type,
            "extracted_length": len(file_text),
            "preview": file_text[:200] + "..." if len(file_text) > 200 else file_text
        }
    
    return result

def run_wimd_with_multiple_files(prompt: str = "", files_data: List[Tuple[bytes, str, str]] = None, max_files: int = 5) -> Dict:
    """Enhanced WIMD with multiple file input support (max 5 files)"""
    
    if not files_data:
        return run_wimd(prompt)
    
    # Limit to max_files
    limited_files_data = files_data[:max_files]
    files_truncated = len(files_data) > max_files
    
    # Process all files
    all_file_texts = []
    files_processed = []
    
    for file_content, filename, content_type in limited_files_data:
        if file_content:
            file_text = process_file_input(file_content, filename, content_type)
            all_file_texts.append(f"[Content from {filename}]:\n{file_text}")
            
            files_processed.append({
                "filename": filename,
                "content_type": content_type,
                "extracted_length": len(file_text),
                "preview": file_text[:150] + "..." if len(file_text) > 150 else file_text
            })
    
    # Combine prompt with all file contents
    combined_prompt = prompt
    if all_file_texts:
        files_section = "\n\n".join(all_file_texts)
        combined_prompt = f"{prompt}\n\n[Multiple Documents Provided]:\n{files_section}"
        
        if files_truncated:
            combined_prompt += f"\n\n[Note: Only first {max_files} files processed due to limit]"
    
    # Use existing WIMD logic
    result = run_wimd(combined_prompt)
    
    # Add multi-file processing info to result
    if files_data:
        result["files_processed"] = {
            "total_files": len(files_processed),
            "files_submitted": len(files_data),
            "files_truncated": files_truncated,
            "max_files_limit": max_files,
            "files_detail": files_processed,
            "combined_length": sum(f["extracted_length"] for f in files_processed)
        }
    
    return result

def run_jobsearch(query: str, location: str = "Toronto, ON", max_results: int = 25) -> Dict:
    """JobSearchMaster with Foundation evidence-based approach"""
    
    # Evidence-based job matching prompt
    search_prompt = f"""
Analyze this job search request with Foundation evidence standards:
Query: {query}
Location: {location}

For each role type, classify match level:
- STRONG: Direct experience with evidence artifacts
- MODERATE: Adjacent skills with learning plan needed  
- AVOID: Gap too large without substantial development

Return realistic assessment with learning paths for MODERATE matches.
"""
    
    try:
        client = get_openai_client()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": search_prompt}],
            max_tokens=400,
            temperature=0.3
        )
        
        return {
            "analysis": response.choices[0].message.content.strip(),
            "query": query,
            "location": location,
            "foundation_principle": "evidence_required",
            "match_categories": ["STRONG", "MODERATE", "AVOID"],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "error": f"JobSearch API error: {str(e)}",
            "query": query,
            "location": location,
            "fallback": "Manual search recommended"
        }
