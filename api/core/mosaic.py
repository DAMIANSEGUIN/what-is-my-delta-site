# === WIMD + OpenAI Integration (Foundation Architecture) ===
import os
import openai
import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple

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
    return openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
