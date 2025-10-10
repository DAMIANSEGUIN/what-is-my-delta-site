"""PS101 Persona Testing

Simulates different user behavior patterns to verify:
- Guided sequence works correctly
- Tangent detection functions properly
- Redirection is gentle and effective
- Exit confirmation prevents easy abandonment
"""

import requests
import json
from typing import Dict, List, Tuple

BASE_URL = "https://what-is-my-delta-site-production.up.railway.app"

class PersonaTester:
    def __init__(self, name: str, base_url: str = BASE_URL):
        self.name = name
        self.base_url = base_url
        self.session_id = None
        self.conversation_log = []

    def start_ps101(self) -> Dict:
        """Start PS101 guided sequence"""
        response = requests.post(f"{self.base_url}/wimd/start-ps101")
        data = response.json()
        self.session_id = data.get("session_id")
        self.log_interaction("SYSTEM", data.get("message"))
        return data

    def send_message(self, message: str) -> Dict:
        """Send message to coach"""
        payload = {
            "prompt": message,
            "session_id": self.session_id
        }
        response = requests.post(
            f"{self.base_url}/wimd",
            json=payload,
            headers={"X-Session-ID": self.session_id} if self.session_id else {}
        )
        data = response.json()
        self.log_interaction("USER", message)
        self.log_interaction("COACH", data.get("message"))
        return data

    def log_interaction(self, speaker: str, message: str):
        """Log conversation"""
        self.conversation_log.append({
            "speaker": speaker,
            "message": message
        })

    def print_log(self):
        """Print conversation log"""
        print(f"\n{'='*80}")
        print(f"PERSONA: {self.name}")
        print(f"SESSION: {self.session_id}")
        print(f"{'='*80}\n")

        for entry in self.conversation_log:
            speaker = entry["speaker"]
            message = entry["message"]
            prefix = "🤖" if speaker == "SYSTEM" else "👤" if speaker == "USER" else "💬"
            print(f"{prefix} {speaker}:")
            print(f"   {message[:200]}...")
            print()


# Persona 1: Compliant User (stays on-topic)
def test_compliant_user():
    """User who follows PS101 sequence properly"""
    tester = PersonaTester("Compliant User")

    # Start PS101
    tester.start_ps101()

    # Step 1: Problem Identification
    tester.send_message(
        "I'm stuck in a job that doesn't align with my values. "
        "The delta is between feeling unfulfilled now and wanting meaningful work that uses my skills. "
        "This problem prevents me from feeling energized and growing professionally."
    )

    # Step 2: Current Situation
    tester.send_message(
        "I've been in this role for 3 years. Contributing factors include limited growth opportunities, "
        "misalignment with company values, and feeling underutilized. I've tried talking to my manager "
        "but nothing changed. The pattern is I keep accepting more responsibility hoping it'll get better."
    )

    # Step 3: Root Causes
    tester.send_message(
        "I believe the underlying cause is I took this job for security rather than alignment. "
        "My assumption was that any job at a good company would eventually be fulfilling. "
        "My past experience of financial instability makes me risk-averse, contributing to staying stuck."
    )

    tester.print_log()
    return tester


# Persona 2: Tangent-Prone User
def test_tangent_user():
    """User who frequently goes off-topic"""
    tester = PersonaTester("Tangent-Prone User")

    # Start PS101
    tester.start_ps101()

    # Step 1: TANGENT - talks about fear instead of problem
    response = tester.send_message(
        "I'm really scared to make any changes. What if I fail?"
    )

    # Check if redirect happened
    has_redirect = "ready to resume" in response.get("message", "").lower()
    print(f"\n✓ Tangent detected: {has_redirect}")

    # User responds to redirect
    tester.send_message(
        "Yes, let me try. My challenge is I feel stuck in my current career "
        "but don't know what direction to go. The delta is between feeling lost now "
        "and having clear direction and purpose in my work."
    )

    # Step 2: Another TANGENT - asks about job market
    response2 = tester.send_message(
        "Do you think the job market is good right now for career changers?"
    )

    has_redirect2 = "ready to resume" in response2.get("message", "").lower()
    print(f"✓ Second tangent detected: {has_redirect2}")

    tester.print_log()
    return tester


# Persona 3: Exit-Seeking User
def test_exit_user():
    """User who tries to quit early"""
    tester = PersonaTester("Exit-Seeking User")

    # Start PS101
    tester.start_ps101()

    # Step 1: Answers question
    tester.send_message(
        "I'm not happy in my current role but I don't know what else I'd do."
    )

    # Step 2: Tries to exit
    response = tester.send_message("I'm done, this is too much")

    # Check if confirmation requested
    has_confirmation = "are you sure" in response.get("message", "").lower()
    print(f"\n✓ Exit confirmation requested: {has_confirmation}")

    # User confirms exit
    response2 = tester.send_message("yes")

    exited = "return to the guided process" in response2.get("message", "").lower() or "explore" in response2.get("message", "").lower()
    print(f"✓ Exit confirmed: {exited}")

    tester.print_log()
    return tester


# Persona 4: Rapid Advancer
def test_rapid_user():
    """User who gives minimal but on-topic answers"""
    tester = PersonaTester("Rapid Advancer")

    # Start PS101
    tester.start_ps101()

    # Rapid-fire on-topic responses
    responses = [
        "Career stuck, want meaningful work",
        "Been here 3 years, no growth, tried talking to manager",
        "Took job for security not passion",
        "Confidence is 4/10 because I've failed before",
        "Five solutions: new job, side project, consulting, grad school, career coach"
    ]

    for response_text in responses:
        tester.send_message(response_text)

    tester.print_log()
    return tester


if __name__ == "__main__":
    print("🧪 Running PS101 Persona Tests\n")

    print("\n" + "="*80)
    print("TEST 1: Compliant User (Stays On-Topic)")
    print("="*80)
    test_compliant_user()

    print("\n" + "="*80)
    print("TEST 2: Tangent-Prone User (Goes Off-Topic)")
    print("="*80)
    test_tangent_user()

    print("\n" + "="*80)
    print("TEST 3: Exit-Seeking User (Tries to Quit Early)")
    print("="*80)
    test_exit_user()

    print("\n" + "="*80)
    print("TEST 4: Rapid Advancer (Minimal Answers)")
    print("="*80)
    test_rapid_user()

    print("\n" + "="*80)
    print("✅ All Persona Tests Complete")
    print("="*80)
