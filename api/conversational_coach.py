"""Conversational Coaching Layer - Human-Responsive Chat

Implements intent detection, acknowledgment, and contextual routing
to make PS101 flow feel human and adaptive instead of robotic.

Pattern based on prompts.csv coaching responses:
1. Acknowledge what user said (reflection)
2. Validate/normalize the feeling or situation
3. Offer insight or reframe
4. Suggest tiny next action
5. Point toward possibility
"""

from typing import Dict, Any, List, Optional, Tuple
from enum import Enum
import re


class UserIntent(Enum):
    """Classification of user's message intent"""
    ANSWER = "answer"  # Answering the current question
    META_QUESTION = "meta_question"  # Asking about the process itself
    FRUSTRATION = "frustration"  # Expressing frustration or confusion
    CIRCULAR_THINKING = "circular_thinking"  # Negative self-talk loop
    POSSIBILITY_THINKING = "possibility_thinking"  # Positive shift
    REQUEST_HELP = "request_help"  # Asking for help/clarification
    TANGENT = "tangent"  # Off-topic but substantive
    SIMPLE_CONFIRMATION = "simple_confirmation"  # "yes", "ok", "sure"


class EmotionalTone(Enum):
    """User's emotional state"""
    HOPEFUL = "hopeful"
    DISCOURAGED = "discouraged"
    CONFUSED = "confused"
    FRUSTRATED = "frustrated"
    NEUTRAL = "neutral"
    ENGAGED = "engaged"


def detect_intent(
    user_message: str,
    current_question: str,
    conversation_history: List[Dict]
) -> Tuple[UserIntent, EmotionalTone]:
    """Detect user's intent and emotional tone

    Uses pattern matching + heuristics (no LLM call for speed)
    """
    msg_lower = user_message.lower().strip()

    # Simple confirmations
    if msg_lower in ["yes", "no", "ok", "sure", "yeah", "nope", "maybe"]:
        return (UserIntent.SIMPLE_CONFIRMATION, EmotionalTone.NEUTRAL)

    # Meta-questions (asking about the process)
    meta_patterns = [
        r"why (are you|did you)",
        r"what made you",
        r"why (aren't|isnt|arent) you",
        r"(answer|respond to) (my|the) question",
        r"what (is|does) this",
        r"how (does|will) this (work|help)",
        r"can (you|we|i) (skip|stop|pause)",
    ]
    if any(re.search(pattern, msg_lower) for pattern in meta_patterns):
        # Check if frustrated
        if any(word in msg_lower for word in ["not answering", "ignoring", "why are you"]):
            return (UserIntent.META_QUESTION, EmotionalTone.FRUSTRATED)
        return (UserIntent.META_QUESTION, EmotionalTone.CONFUSED)

    # Frustration signals
    frustration_patterns = [
        r"you (are not|arent|didnt|did not|wont|will not)",
        r"(this|that) (is not|isnt|does not|doesnt) (work|help|make sense)",
        r"i (already|just) (said|told|answered)",
        r"(stop|quit|enough|jesus|christ|fuck|shit|damn)",
    ]
    if any(re.search(pattern, msg_lower) for pattern in frustration_patterns):
        return (UserIntent.FRUSTRATION, EmotionalTone.FRUSTRATED)

    # Circular/negative thinking patterns
    circular_patterns = [
        r"i (cant|cannot|can't|am not|will never|always)",
        r"(nothing|no one|nobody) (works|helps|cares|wants)",
        r"(everything|everyone) (is|seems) (against|hard|impossible)",
        r"(too|not) (old|young|late|stupid|qualified)",
        r"(no|zero) (responses|replies|interest|hope|point)",
        r"(never|not) (good|smart|skilled|talented) enough",
    ]
    if any(re.search(pattern, msg_lower) for pattern in circular_patterns):
        # Check for hope mixed in
        if any(word in msg_lower for word in ["but", "maybe", "if", "could", "hope", "want"]):
            return (UserIntent.CIRCULAR_THINKING, EmotionalTone.DISCOURAGED)
        return (UserIntent.CIRCULAR_THINKING, EmotionalTone.DISCOURAGED)

    # Possibility thinking (positive shift)
    possibility_patterns = [
        r"i (could|can|might|want to|would like)",
        r"maybe i (should|can|will)",
        r"what if i",
        r"(hope|wish|dream|imagine)",
    ]
    if any(re.search(pattern, msg_lower) for pattern in possibility_patterns):
        return (UserIntent.POSSIBILITY_THINKING, EmotionalTone.HOPEFUL)

    # Request for help
    help_patterns = [
        r"(help|show|tell|explain|how do|what do|where do)",
        r"i (don't|dont|do not) (know|understand)",
        r"(what|how|where|when|why) (should|can|do) i",
    ]
    if any(re.search(pattern, msg_lower) for pattern in help_patterns):
        return (UserIntent.REQUEST_HELP, EmotionalTone.CONFUSED)

    # Default to answer if substantive (>10 words)
    word_count = len(msg_lower.split())
    if word_count > 10:
        # Check tone
        if any(word in msg_lower for word in ["hopeless", "anxious", "stressed", "worried", "scared"]):
            return (UserIntent.ANSWER, EmotionalTone.DISCOURAGED)
        elif any(word in msg_lower for word in ["excited", "hopeful", "ready", "want", "can"]):
            return (UserIntent.ANSWER, EmotionalTone.ENGAGED)
        return (UserIntent.ANSWER, EmotionalTone.NEUTRAL)

    # Short substantive answer
    if word_count >= 3:
        return (UserIntent.ANSWER, EmotionalTone.NEUTRAL)

    # Fallback
    return (UserIntent.TANGENT, EmotionalTone.NEUTRAL)


def generate_acknowledgment(
    user_message: str,
    intent: UserIntent,
    tone: EmotionalTone
) -> str:
    """Generate natural acknowledgment of what user said

    Pattern: "I hear that..." / "That makes sense..." / "I understand..."
    """
    msg_snippet = user_message[:60] + "..." if len(user_message) > 60 else user_message

    if intent == UserIntent.META_QUESTION:
        if tone == EmotionalTone.FRUSTRATED:
            return "You're absolutely right to call that out"
        return "That's a fair question"

    elif intent == UserIntent.FRUSTRATION:
        return "I hear your frustration"

    elif intent == UserIntent.CIRCULAR_THINKING:
        if "can't" in user_message.lower() or "cant" in user_message.lower():
            return "I hear that feeling of being stuck"
        if "never" in user_message.lower() or "nothing" in user_message.lower():
            return "That sense of hopelessness is real"
        return "I hear the weight in that"

    elif intent == UserIntent.POSSIBILITY_THINKING:
        return "I hear that spark of possibility"

    elif intent == UserIntent.REQUEST_HELP:
        return "That's a great question"

    elif intent == UserIntent.ANSWER:
        if tone == EmotionalTone.DISCOURAGED:
            return "I hear the struggle in that"
        elif tone == EmotionalTone.ENGAGED:
            return "I appreciate that thoughtful response"
        return "Thank you for sharing that"

    return "I hear you"


def generate_validation(
    user_message: str,
    intent: UserIntent,
    tone: EmotionalTone,
    ps101_context: Dict
) -> str:
    """Validate/normalize the user's experience

    Pattern: "That makes sense because..." / "This often means..." / "Many people feel..."
    """
    if intent == UserIntent.META_QUESTION:
        return "Let me explain what happened"

    elif intent == UserIntent.CIRCULAR_THINKING:
        if "not trying hard enough" in user_message.lower():
            return "That's interesting, because earlier you mentioned applying to many positions with no responses. It sounds like there might be a gap between the effort you're actually putting in and how you're judging yourself"
        if "anxious" in user_message.lower() or "hopeless" in user_message.lower():
            return "Six months of searching with no responses is genuinely difficult. That anxiety is a signal, not a flaw"
        if "ageism" in user_message.lower():
            return "Age bias is real in hiring. Naming it shows clarity, not defeat"
        return "This kind of self-critical thinking often comes when we've been trying hard with little feedback. The lack of response doesn't mean lack of value"

    elif intent == UserIntent.POSSIBILITY_THINKING:
        return "That shift in perspective is exactly what opens new paths"

    elif intent == UserIntent.FRUSTRATION:
        return "You're engaged in this process, and I should have recognized that"

    return ""


def generate_reframe_or_insight(
    user_message: str,
    intent: UserIntent,
    tone: EmotionalTone,
    ps101_context: Dict
) -> str:
    """Offer gentle reframe or insight

    Pattern: "What if..." / "Try this..." / "One way to see this..."
    """
    if intent == UserIntent.CIRCULAR_THINKING:
        if "not trying hard enough" in user_message.lower():
            return "If an outsider saw your 6-month search, they might think 'this person is persistent,' not 'they're not trying.' Sometimes we're the harshest judge."
        if "tight market" in user_message.lower():
            return "Market tightness is real, but strategy matters more than volume. One tailored application can outperform 100 generic ones."
        if "discouraged" in user_message.lower() or "hopeless" in user_message.lower():
            return "Hopelessness often signals you're doing the same thing repeatedly expecting different results. What if the problem isn't you, but the approach?"
        return "What if this isn't about working harder, but working differently?"

    elif intent == UserIntent.POSSIBILITY_THINKING:
        return "Let's explore that possibility"

    return ""


def generate_next_action(
    current_ps101_step: int,
    current_prompt_index: int,
    next_step: int,
    next_prompt_index: int,
    intent: UserIntent,
    should_advance: bool
) -> str:
    """Generate next question or action

    Returns: next_question_text
    """
    # Import here to avoid circular dependency
    from api.ps101_flow import get_ps101_step, format_step_for_user

    if intent == UserIntent.META_QUESTION:
        # Answer the meta question, then continue with same question
        step = get_ps101_step(current_ps101_step)
        next_q = format_step_for_user(step, current_prompt_index)
        return f"Let me continue where we were:\n\n{next_q}"

    elif intent == UserIntent.FRUSTRATION:
        # Apologize, offer escape hatch, continue
        step = get_ps101_step(current_ps101_step)
        next_q = format_step_for_user(step, current_prompt_index)
        return f"Would you like to continue with the guided questions, or would you prefer to have a more open conversation? If you want to continue:\n\n{next_q}"

    elif should_advance:
        # Return next question after advance
        step = get_ps101_step(next_step)
        if step:
            return format_step_for_user(step, next_prompt_index)
        return ""

    else:
        # Stay on current question
        step = get_ps101_step(current_ps101_step)
        if step:
            return format_step_for_user(step, current_prompt_index)
        return ""


def generate_conversational_response(
    user_message: str,
    intent: UserIntent,
    tone: EmotionalTone,
    ps101_context: Dict,
    current_question: str,
    conversation_history: List[Dict],
    session_data: Dict
) -> Tuple[str, bool]:
    """Generate full conversational response

    Returns: (response, should_advance_ps101_state)

    Structure:
    1. Acknowledgment
    2. Validation (if applicable)
    3. Reframe/insight (if applicable)
    4. Next question
    """
    parts = []
    should_advance = False

    # 1. Acknowledge
    ack = generate_acknowledgment(user_message, intent, tone)
    if ack:
        parts.append(ack)

    # 2. Validate
    val = generate_validation(user_message, intent, tone, ps101_context)
    if val:
        parts.append(val)

    # 3. Reframe
    reframe = generate_reframe_or_insight(user_message, intent, tone, ps101_context)
    if reframe:
        parts.append(reframe)

    # 4. Decide if we should advance PS101 state
    if intent == UserIntent.ANSWER and tone != EmotionalTone.CONFUSED:
        should_advance = True
    elif intent == UserIntent.POSSIBILITY_THINKING:
        should_advance = True
    elif intent == UserIntent.SIMPLE_CONFIRMATION:
        should_advance = True

    # 5. Calculate next position (for generating question text)
    current_step = ps101_context.get("ps101_step", 1)
    current_prompt_idx = ps101_context.get("ps101_prompt_index", 0)

    # Temporarily advance to get next position
    if should_advance:
        from api.ps101_flow import get_ps101_step
        step_data = get_ps101_step(current_step)
        if step_data:
            total_prompts = len(step_data.get("prompts", []))
            if current_prompt_idx + 1 < total_prompts:
                next_step = current_step
                next_prompt_idx = current_prompt_idx + 1
            else:
                next_step = min(current_step + 1, 10)
                next_prompt_idx = 0
        else:
            next_step = current_step
            next_prompt_idx = current_prompt_idx
    else:
        next_step = current_step
        next_prompt_idx = current_prompt_idx

    # 6. Get next action text
    next_action = generate_next_action(
        current_step,
        current_prompt_idx,
        next_step,
        next_prompt_idx,
        intent,
        should_advance
    )

    if next_action:
        parts.append(next_action)

    # Combine with double line breaks
    response = "\n\n".join(parts)

    return (response, should_advance)


def should_exit_ps101(user_message: str, intent: UserIntent) -> bool:
    """Determine if user wants to exit PS101 flow

    More careful than simple keyword matching
    """
    msg_lower = user_message.lower().strip()

    # Explicit exit only
    explicit_exit = [
        "i want to stop",
        "i want to quit",
        "i want to exit",
        "let me stop",
        "i'm done",
        "im done",
    ]

    if any(phrase in msg_lower for phrase in explicit_exit):
        return True

    # Single word "stop" or "quit" when frustrated
    if intent == UserIntent.FRUSTRATION:
        if msg_lower.strip() in ["stop", "quit", "exit", "enough"]:
            return True

    return False
