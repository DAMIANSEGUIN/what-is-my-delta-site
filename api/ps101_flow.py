"""PS101 Guided Problem-Solving Sequence

10-step guided flow for career problem-solving, based on PS101_Intro_and_Prompts.docx
Includes tangent detection and gentle redirection to keep users engaged.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime

# PS101 10-Step Guided Sequence
PS101_STEPS = [
    {
        "step": 1,
        "title": "Problem Identification and Delta Analysis",
        "prompts": [
            "What specific challenge are you currently facing in your personal or professional life?",
            "Why is it a problem?",
            "Reduce this to a simple problem statement",
            "If you were to wake up tomorrow and this problem was solved, what would be different? (Miracle Question)",
            "What is the 'delta' or gap between your current situation and your desired state?",
            "How would solving this problem align with your long-term goals or values?"
        ],
        "keywords": ["challenge", "problem", "facing", "delta", "gap", "goals", "values", "miracle"]
    },
    {
        "step": 2,
        "title": "Current Situation Analysis",
        "prompts": [
            "Describe your current situation in detail. What factors are contributing to the problem?",
            "What attempts have you made so far to address this issue? What were the outcomes?",
            "Are there any patterns or recurring themes you've noticed related to this problem?",
            "How is this problem affecting different areas of your life (e.g., career, relationships, personal growth)?"
        ],
        "keywords": ["situation", "factors", "contributing", "attempts", "outcomes", "patterns", "themes", "affecting"]
    },
    {
        "step": 3,
        "title": "Root Cause Exploration",
        "prompts": [
            "What do you believe are the underlying causes of this problem?",
            "Are there any assumptions you're making about the problem or its causes?",
            "How might your own beliefs, habits, or past experiences be contributing to the situation?",
            "If you were to view this problem from an outsider's perspective, what insights might you gain?"
        ],
        "keywords": ["causes", "underlying", "assumptions", "beliefs", "habits", "experiences", "perspective", "insights"]
    },
    {
        "step": 4,
        "title": "Self-Efficacy Assessment",
        "prompts": [
            "On a scale of 1-10, how confident do you feel in your ability to solve this problem? Why?",
            "What past experiences or skills can you draw upon to address this challenge?",
            "How might your perception of your own capabilities be influencing your approach to this problem?",
            "What small wins or successes have you had in the past that you can build upon?"
        ],
        "keywords": ["confident", "scale", "1-10", "ability", "skills", "experiences", "capabilities", "wins", "successes"]
    },
    {
        "step": 5,
        "title": "Solution Brainstorming",
        "prompts": [
            "List at least five potential solutions to your problem, no matter how unconventional they may seem.",
            "For each solution, what are the potential benefits and drawbacks?",
            "Which solution feels most aligned with your values and long-term goals?",
            "How might you combine elements from different solutions to create a more comprehensive approach?"
        ],
        "keywords": ["solutions", "potential", "five", "benefits", "drawbacks", "aligned", "combine", "approach"]
    },
    {
        "step": 6,
        "title": "Experimental Design",
        "prompts": [
            "Based on your chosen solution(s), what small, low-risk experiment could you conduct to test its effectiveness?",
            "What specific, measurable outcome would indicate that your experiment was successful?",
            "What resources or support might you need to carry out this experiment?",
            "How long will you run this experiment before evaluating its results?"
        ],
        "keywords": ["experiment", "test", "low-risk", "measurable", "outcome", "resources", "support", "evaluate"]
    },
    {
        "step": 7,
        "title": "Obstacle Identification",
        "prompts": [
            "What external factors (e.g., time, resources, other people) might hinder your progress?",
            "What internal obstacles (e.g., self-doubt, fear, lack of knowledge) do you anticipate facing?",
            "For each obstacle identified, brainstorm at least one strategy to overcome or mitigate it.",
            "How can you reframe these obstacles as opportunities for growth or learning?"
        ],
        "keywords": ["obstacles", "factors", "hinder", "self-doubt", "fear", "strategy", "overcome", "opportunities"]
    },
    {
        "step": 8,
        "title": "Action Planning",
        "prompts": [
            "What specific steps will you take to implement your chosen experiment?",
            "How will you measure and track your progress throughout the experiment?",
            "What milestones can you set to celebrate small wins along the way?",
            "Who can you enlist to provide support or accountability during this process?"
        ],
        "keywords": ["steps", "implement", "measure", "track", "milestones", "celebrate", "accountability", "support"]
    },
    {
        "step": 9,
        "title": "Reflection and Iteration",
        "prompts": [
            "After conducting your experiment, what were the results? What did you learn?",
            "How has this experience affected your confidence in problem-solving?",
            "Based on what you've learned, what adjustments would you make to your approach?",
            "What new experiments or actions will you take based on these insights?"
        ],
        "keywords": ["results", "learned", "experience", "confidence", "adjustments", "approach", "insights", "actions"]
    },
    {
        "step": 10,
        "title": "Building Mastery and Self-Efficacy",
        "prompts": [
            "Reflecting on this problem-solving process, what new skills or knowledge have you gained?",
            "How can you apply what you've learned to future challenges or goals?",
            "What strategies will you use to maintain momentum and continue building your problem-solving abilities?",
            "How has this experience changed your perception of your own capabilities?"
        ],
        "keywords": ["skills", "knowledge", "gained", "apply", "future", "strategies", "momentum", "perception", "capabilities"]
    }
]


def get_ps101_step(step_number: int) -> Optional[Dict[str, Any]]:
    """Get a specific PS101 step by number (1-10)"""
    if 1 <= step_number <= 10:
        return PS101_STEPS[step_number - 1]
    return None


def is_tangent(user_response: str, current_step: int) -> bool:
    """Detect if user's response is a tangent (not addressing current step)

    Lenient approach: Only flag as tangent if response is very short (yes/no)
    OR clearly off-topic. Most substantive responses are accepted.
    """
    step_data = get_ps101_step(current_step)
    if not step_data:
        return False

    response_lower = user_response.lower()
    keywords = step_data.get("keywords", [])

    # Check if response contains at least one keyword from the step
    keyword_match = any(keyword in response_lower for keyword in keywords)

    # Also check for explicit exit signals - if exiting, not a tangent
    exit_signals = ["stop", "quit", "exit", "i'm done", "im done", "no more", "enough"]
    is_exit = any(signal in response_lower for signal in exit_signals)

    # Check if response seems substantive (more than just yes/no/ok)
    word_count = len(response_lower.split())
    is_very_brief = word_count <= 2

    # Short confirmations like "yes" or "ok" when resuming
    is_simple_confirmation = response_lower.strip() in ["yes", "no", "ok", "sure", "yeah", "nope"]

    # Only tangent if: no keyword match AND not an exit AND (very brief OR simple confirmation)
    # This means anything 3+ words is accepted as on-topic
    return not keyword_match and not is_exit and (is_very_brief or is_simple_confirmation)


def get_redirect_message(step_number: int) -> str:
    """Get gentle redirect message to bring user back to current step"""
    step_data = get_ps101_step(step_number)
    if not step_data:
        return "Are you ready to resume with the clarifying questions?"

    first_prompt = step_data["prompts"][0]
    return f"Are you ready to resume with the clarifying questions?\n\nLet's return to: {first_prompt}"


def format_step_for_user(step: Dict[str, Any], prompt_index: int = 0) -> str:
    """Format a step into a user-friendly message - shows ONE prompt at a time

    Args:
        step: PS101 step dictionary
        prompt_index: Which prompt within the step (0-based index)

    Cache bust: 2025-10-14
    """
    prompts = step.get("prompts", [])
    if prompt_index >= len(prompts):
        prompt_index = 0  # Fallback to first

    current_prompt = prompts[prompt_index]
    return f"""**Step {step['step']}: {step['title']}**

{current_prompt}"""


def create_ps101_session_data() -> Dict[str, Any]:
    """Create initial PS101 session data"""
    return {
        "ps101_active": True,
        "ps101_step": 1,
        "ps101_prompt_index": 0,  # Track which prompt within current step
        "ps101_started_at": datetime.utcnow().isoformat(),
        "ps101_responses": [],
        "ps101_tangent_count": 0  # Track tangents per step
    }


def record_ps101_response(session_data: Dict[str, Any], step: int, response: str) -> Dict[str, Any]:
    """Record user's response to a PS101 step"""
    session_data["ps101_responses"].append({
        "step": step,
        "response": response,
        "timestamp": datetime.utcnow().isoformat()
    })
    return session_data


def handle_tangent(session_data: Dict[str, Any]) -> Dict[str, Any]:
    """Track tangent occurrence"""
    session_data["ps101_tangent_count"] = session_data.get("ps101_tangent_count", 0) + 1
    return session_data


def advance_ps101_prompt(session_data: Dict[str, Any]) -> Dict[str, Any]:
    """Advance to next prompt within current step, or next step if all prompts done

    Returns:
        Updated session_data with new prompt_index or step number
    """
    current_step = session_data.get("ps101_step", 1)
    prompt_index = session_data.get("ps101_prompt_index", 0)

    step_data = get_ps101_step(current_step)
    if not step_data:
        return session_data

    total_prompts = len(step_data.get("prompts", []))

    # Check if there are more prompts in current step
    if prompt_index + 1 < total_prompts:
        # Move to next prompt within same step
        session_data["ps101_prompt_index"] = prompt_index + 1
    else:
        # All prompts done - advance to next step
        session_data["ps101_step"] = min(current_step + 1, 10)
        session_data["ps101_prompt_index"] = 0  # Reset to first prompt of new step
        session_data["ps101_tangent_count"] = 0  # Reset tangent count for new step

    return session_data


def advance_ps101_step(session_data: Dict[str, Any]) -> Dict[str, Any]:
    """Advance to next step in PS101 sequence (legacy function - now calls advance_ps101_prompt)"""
    return advance_ps101_prompt(session_data)


def exit_ps101_flow(session_data: Dict[str, Any]) -> Dict[str, Any]:
    """Exit PS101 guided flow with confirmation"""
    session_data["ps101_active"] = False
    session_data["ps101_completed_at"] = datetime.utcnow().isoformat()
    return session_data


def get_exit_confirmation() -> str:
    """Get exit confirmation message"""
    return """Are you sure you want to stop the guided process?

This problem-solving framework works best when you complete all the steps. Taking the time to work through each question can lead to breakthrough insights.

Type 'yes' to exit, or continue sharing your thoughts to keep going."""


def is_complete(current_step: int) -> bool:
    """Check if user has completed all 10 steps"""
    return current_step > 10


def get_completion_message() -> str:
    """Get completion message when all steps done"""
    return """**Congratulations!** 🎉

You've completed the PS101 problem-solving framework. You now have:
- A clear understanding of your challenge and desired state
- Insights into root causes and obstacles
- A testable experiment to move forward
- An action plan with accountability

Your responses have been saved. You can now:
- Explore job opportunities that align with your goals
- Work with the coach on specific challenges
- Design new experiments based on what you've learned

What would you like to do next?"""
# Cache bust: 1760083676_ps101_fixes
