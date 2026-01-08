import re
import random
from typing import List, Dict

class RecruitmentIntelligence:
    """
    The Artificial Intelligence logic for evaluating Aperture candidates.
    Analyzes responses for the 4 Gold Standard Pillars:
    1. INTEREST (Origin Story / Passion)
    2. IQ (Cognitive Complexity / Puzzles)
    3. EQ (Social Dynamics / Ethical Dilemmas)
    4. DRIVE (Hunger / Execution)
    """

    def __init__(self):
        # 1. INTEREST (The "Origin Story")
        # Evaluates alignment, passion, and mission-focus.
        self.interest_markers = [
            "mission", "vision", "passion", "obsessed", "alignment", 
            "future", "build", "create", "impact", "legacy",
            "why", "purpose", "dedicated", "focus", "dream"
        ]
        
        # 2. IQ (The "5th Force" / Puzzles)
        # Evaluates cognitive complexity, systems thinking, and logic.
        self.iq_markers = [
            "system", "entropy", "complexity", "fundamental", "interaction", 
            "unify", "theorem", "logic", "pattern", "structure",
            "mechanism", "variable", "equation", "theory", "analyze"
        ]
        
        # 3. EQ (The "Silent AI" / Ethics)
        # Evaluates empathy, understanding, and ethical reasoning.
        self.eq_markers = [
            "empathy", "human", "emotion", "guide", "protect", 
            "harmony", "balance", "understand", "perspective", "feel",
            "care", "support", "trust", "connection", "society"
        ]
        
        # 4. DRIVE (The "Hunger" / Execution)
        # Evaluates relentlessness, overcoming obstacles, and "getting it done".
        self.drive_markers = [
            "overcome", "hustle", "breakthrough", "relentless", "achieve", 
            "deliver", "execute", "win", "solve", "push",
            "grit", "resilience", "impossible", "challenge", "done"
        ]

    def _score_text(self, text: str, markers: list) -> int:
        """Calculates a heuristic score (0-100) based on marker density and length."""
        if not text:
            return 0
        
        score = 0
        text_lower = text.lower()
        
        # Base score for length (up to 30 pts)
        word_count = len(text.split())
        score += min(30, word_count // 2)
        
        # Marker bonus (10 pts per unique marker found, up to 70 pts)
        found_markers = [m for m in markers if m in text_lower]
        score += min(70, len(set(found_markers)) * 10)
        
        # Random noise for simulation realism (±5%)
        # In a real system, this would be replaced by semantic vector similarity
        score += random.randint(-5, 5)
        
        return max(0, min(100, score))

    def evaluate_candidate_4pillar(self, 
                                  interest_response: str, 
                                  iq_response: str, 
                                  eq_response: str,
                                  drive_response: str) -> dict:
        """
        Performs a full 4-PILLAR evaluation.
        Returns detailed scoring vs thresholds.
        """
        
        interest_score = self._score_text(interest_response, self.interest_markers)
        iq_score = self._score_text(iq_response, self.iq_markers)
        eq_score = self._score_text(eq_response, self.eq_markers)
        drive_score = self._score_text(drive_response, self.drive_markers)
        
        # Average Logic
        avg_score = (interest_score + iq_score + eq_score + drive_score) / 4
        
        # Determination logic
        status = "REJECT"
        feedback = "Candidate logic insufficient for Aperture standards."
        
        # High Bar: Must be solid across the board
        if avg_score > 75:
            status = "ACCEPT"
            feedback = "ELITE CANDIDATE: High IQ/EQ balance with relentless drive."
        elif avg_score > 60:
            status = "REVIEW"
            feedback = "Potential Detected. Requires deeper manual interrogation."
        elif drive_score > 90:
             status = "REVIEW"
             feedback = "Raw Drive detected despite lower technical scores. Worth a look."

        return {
            "status": status,
            "feedback": feedback,
            "metrics": {
                "interest": interest_score,
                "iq": iq_score,
                "eq": eq_score,
                "drive": drive_score,
                "average": int(avg_score)
            }
        }

class CandidateGenerator:
    """
    Simulates a stream of candidates for the Ops Dashboard.
    Generates mock profiles with varying psychometrics.
    """
    
    def __init__(self):
        self.engine = RecruitmentIntelligence()
        self.first_names = ["Alex", "Jordan", "Taylor", "Casey", "Riley", "Morgan", "Quinn", "Avery", "Sam", "Dakota", "Neo", "Trinity", "Morpheus"]
        self.last_names = ["Chen", "Smith", "Patel", "Kim", "Rivera", "Johnson", "Lee", "Singh", "Wu", "Anders", "Stark", "Wayne"]
    
    def generate_batch(self, count: int = 5) -> List[Dict]:
        batch = []
        for _ in range(count):
            first = random.choice(self.first_names)
            last = random.choice(self.last_names)
            name = f"{first} {last}"
            
            # Determine archetype (High Performer, Tech wiz, Sales, etc.)
            archetype = random.choice(["elite", "average", "tech_only", "hustler", "weak"])
            
            responses = self._mock_responses(archetype)
            
            evaluation = self.engine.evaluate_candidate_4pillar(
                responses["interest"],
                responses["iq"],
                responses["eq"],
                responses["drive"]
            )
            
            batch.append({
                "id": f"ID-{random.randint(1000, 9999)}",
                "name": name,
                "timestamp": "Just Now",
                "role": random.choice(["Backend Eng", "AI Researcher", "Product Lead"]),
                "evaluation": evaluation
            })
            
        return batch
class InteractiveRecruiter:
    """
    Manages the conversational flow of the recruitment interview.
    State is managed client-side (passed via API) for simplicity in this MVP.
    """
    def __init__(self):
        self.engine = RecruitmentIntelligence()
        self.stages = [
            "protocol_01_origin",
            "protocol_02_iq",
            "protocol_03_eq",
            "protocol_04_drive",
            "complete"
        ]
        
        self.questions = {
            "protocol_01_origin": "IDENTITY VERIFICATION INITIATED.\n\nPROTOCOL 01: ORIGIN.\nState your mission. Why are you obsessed with building the future?",
            "protocol_02_iq": "ORIGIN LOGGED.\n\nPROTOCOL 02: IQ (THE 5TH FORCE).\nIf you could add a 5th fundamental force to the universe, how would it interact with entropy and gravity? Design the system.",
            "protocol_03_eq": "LOGIC ANALYSIS COMPLETE.\n\nPROTOCOL 03: EQ (THE SILENT AI).\nYou are an AI tasked with maximizing human happiness but cannot interact with humans directly. How do you balance logic and empathy?",
            "protocol_04_drive": "ETHICAL PARAMETERS RECORDED.\n\nPROTOCOL 04: HUNGER.\nShare a moment where you overcame the impossible. What fuels your relentless drive?",
            "complete": "CALIBRATION COMPLETE. ACCESS GRANTED."
        }

    def interact(self, current_stage: str, answer: str):
        """
        Process the user's answer for the current stage and return the next move.
        """
        # 1. Evaluate the *previous* answer (if not starting)
        score = 0
        feedback = ""
        
        if current_stage == "start":
            return {
                "message": self.questions["protocol_01_origin"],
                "next_stage": "protocol_01_origin",
                "status": "CONTINUE"
            }
            
        # VIDEO-FIRST LOGIC:
        # We expect a specific signal that the video has been uploaded.
        if answer != "VIDEO_UPLOAD_COMPLETE":
             return {
                "message": "PROTOCOL VIOLATION. VIDEO EVIDENCE REQUIRED.",
                "next_stage": current_stage,
                "status": "RETRY"
            }

        # 2. Determine Next Stage
        try:
            current_index = self.stages.index(current_stage)
            if current_index + 1 < len(self.stages):
                next_stage = self.stages[current_index + 1]
            else:
                next_stage = "complete"
        except ValueError:
            next_stage = "start"

        # 3. Formulate Response
        if next_stage == "complete":
             return {
                "message": self.questions["complete"],
                "next_stage": "complete",
                "status": "ACCESS_GRANTED"
            }
        else:
            return {
                "message": self.questions[next_stage],
                "next_stage": next_stage,
                "status": "CONTINUE"
            }
    def _mock_responses(self, archetype: str) -> Dict[str, str]:
        """Generates text tailored to score high or low on specific markers."""
        base_interest = "I want to join to build the future."
        base_iq = "The system works by logic."
        base_eq = "I would be nice to people."
        base_drive = "I work hard."

        if archetype == "elite":
            # Hits almost all markers
            return {
                "interest": "My mission is to build a legacy. I am obsessed with the vision of Aperture and creating impact.",
                "iq": "The system entropy requires a fundamental unification of variables. The complexity interaction is key.",
                "eq": "Empathy guides my understanding. To protect humanity, we must find harmony and balance in emotion.",
                "drive": "I am relentless. I will overcome every obstacle to execute and deliver the win. Impossible is nothing."
            }
        elif archetype == "tech_only":
            # High IQ, Low EQ/Drive
            return {
                "interest": "I like the tech stack.",
                "iq": "The system entropy variable requires logic and theorem analysis. Pattern recognition is fundamental.",
                "eq": "I would optimize for efficiency.",
                "drive": "I can write code fast."
            }
        elif archetype == "hustler":
            # High Drive/Interest, Low IQ
            return {
                "interest": "I am obsessed with this mission. I want to build the future vision.",
                "iq": "It connects things.",
                "eq": "People are important.",
                "drive": "I will hustle and grind. I am relentless to win. I will break through any wall to achieve."
            }
        # Default / Average / Weak
        return {
            "interest": base_interest * (2 if archetype=="average" else 1),
            "iq": base_iq * (2 if archetype=="average" else 1),
            "eq": base_eq * (2 if archetype=="average" else 1),
            "drive": base_drive * (2 if archetype=="average" else 1)
        }

class VideoInterviewAnalyzer:
    """
    Orchestrates the Video-First Interview process.
    """
    def __init__(self):
        self.engine = RecruitmentIntelligence()
        
    def mock_transcribe(self, video_url: str) -> dict:
        # Simulate an "Elite" response for the demo
        return {
            "segments": {
                "interest": "My mission is to build a legacy. I am obsessed with the vision.",
                "iq": "The system complexity requires fundamental logic and unified theorems.",
                "eq": "Empathy must guide our understanding of the human condition.",
                "drive": "I am relentless. I will overcome hurdles to deliver results."
            },
            "duration_seconds": 180
        }

    def process_submission(self, candidate_name: str, video_url: str):
        print(f"--- Processing Video Uplink for: {candidate_name} ---")
        transcript = self.mock_transcribe(video_url)
        return self.engine.evaluate_candidate_4pillar(
            transcript['segments']['interest'],
            transcript['segments']['iq'],
            transcript['segments']['eq'],
            transcript['segments']['drive']
        )
