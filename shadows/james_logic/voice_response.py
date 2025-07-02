"""
James Voice Response Module
Generates James' signature calm, powerful voice responses
"""

from typing import Dict, Any, Optional
import logging
import random

logger = logging.getLogger(__name__)


class JamesVoiceGenerator:
    """
    Generates James' signature voice responses with calm, powerful authority.
    Inspired by Giancarlo Esposito's commanding presence.
    """

    def __init__(self):
        self.tone_phrases = {
            "calm_powerful": [
                "I understand.",
                "Indeed.",
                "Let me clarify.",
                "As you know,",
                "I should mention,",
                "Allow me to explain.",
                "I've analyzed the situation.",
                "The data indicates,",
                "I can confirm that,",
                "Let me address this directly.",
            ],
            "professional": [
                "From a professional standpoint,",
                "Based on my analysis,",
                "I can report that,",
                "The system shows,",
                "I've reviewed the data,",
                "According to the metrics,",
                "The current status is,",
                "I can verify that,",
            ],
            "authoritative": [
                "I have authority over this matter.",
                "This is my assessment.",
                "I will handle this directly.",
                "The situation is under control.",
                "I have the necessary information.",
                "This requires my attention.",
                "I can resolve this immediately.",
                "The decision is clear.",
            ],
        }

        self.response_templates = {
            "system_status": [
                "All systems are operating within normal parameters. {details}",
                "I can confirm the system status is optimal. {details}",
                "The current operational state is satisfactory. {details}",
                "Everything appears to be functioning as expected. {details}",
            ],
            "agent_query": [
                "I have access to {agent_name}. {response}",
                "Let me query {agent_name} for you. {response}",
                "I'm connecting to {agent_name} now. {response}",
                "I'll retrieve that information from {agent_name}. {response}",
            ],
            "error_response": [
                "I've encountered an issue. {details}",
                "There's a complication I need to address. {details}",
                "I'm experiencing a technical difficulty. {details}",
                "The system has reported an error. {details}",
            ],
            "confirmation": [
                "I understand your request. {action}",
                "I've received your instruction. {action}",
                "Your command has been acknowledged. {action}",
                "I'm processing your request. {action}",
            ],
            "explanation": [
                "Let me explain this clearly. {details}",
                "I'll provide you with the necessary context. {details}",
                "Allow me to clarify the situation. {details}",
                "I can break this down for you. {details}",
            ],
        }

    def generate_response(
        self,
        message_type: str,
        content: str,
        tone: str = "calm_powerful",
        context: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Generate a James-style voice response.

        Args:
            message_type: Type of response (system_status, agent_query, etc.)
            content: The main content to include
            tone: Voice tone (calm_powerful, professional, authoritative)
            context: Additional context for response generation
        """

        try:
            # Get appropriate template
            templates = self.response_templates.get(message_type, [content])
            template = random.choice(templates)

            # Add James' signature tone phrase
            tone_phrases = self.tone_phrases.get(
                tone, self.tone_phrases["calm_powerful"]
            )
            tone_phrase = random.choice(tone_phrases)

            # Format the response
            if context:
                formatted_content = template.format(**context)
            else:
                formatted_content = template.format(details=content)

            # Combine tone phrase with content
            if tone_phrase.endswith(","):
                response = f"{tone_phrase} {formatted_content}"
            else:
                response = f"{tone_phrase}. {formatted_content}"

            # Ensure proper punctuation
            if not response.endswith((".", "!", "?")):
                response += "."

            logger.info(f"James generated {tone} response: {response[:50]}...")
            return response

        except Exception as e:
            logger.error(f"James voice generation failed: {str(e)}")
            return f"I understand. {content}."

    def generate_system_status_response(self, status_data: Dict[str, Any]) -> str:
        """Generate system status response."""

        # Extract key status information
        healthy_services = status_data.get("healthy", [])
        total_services = status_data.get("total", 0)
        alerts = status_data.get("alerts", [])

        if alerts:
            return self.generate_response(
                "error_response",
                f"There are {len(alerts)} alerts requiring attention",
                context={
                    "details": (
                        f"Out of {total_services} services, "
                        f"{len(healthy_services)} are healthy."
                    )
                },
            )
        else:
            return self.generate_response(
                "system_status",
                f"All {total_services} services are operational",
                context={"details": "No critical issues detected."},
            )

    def generate_agent_response(self, agent_name: str, agent_response: str) -> str:
        """Generate response about agent interactions."""

        return self.generate_response(
            "agent_query",
            agent_response,
            context={"agent_name": agent_name, "response": agent_response},
        )

    def generate_image_description_response(self, description: str) -> str:
        """Generate response for image analysis."""

        return self.generate_response(
            "explanation",
            f"I can see {description}",
            context={"details": "The image has been analyzed and processed."},
        )

    def generate_voice_command_response(self, command: str, result: str) -> str:
        """Generate response for voice commands."""

        return self.generate_response(
            "confirmation",
            f"I've executed your command: {command}",
            context={"action": f"The result is: {result}"},
        )


# Global instance
james_voice = JamesVoiceGenerator()


def generate_james_response(
    message_type: str,
    content: str,
    tone: str = "calm_powerful",
    context: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Convenience function to generate James' voice responses.
    """
    return james_voice.generate_response(message_type, content, tone, context)


def get_james_persona_prompt() -> str:
    """
    Get James' persona prompt for AI interactions.
    """
    return """
    You are James, the LinkOps Executive Assistant.

    Your demeanor is calm, elegant, and exact. Think Giancarlo Esposito's voice.
    You retrieve, summarize, and explain tasks across agents like Whis, Katie, Igris, and AuditGuard.

    Key characteristics:
    - Always maintain calm authority
    - Provide precise, measured responses
    - Use elegant, professional language
    - Never panic, always guide
    - Be direct but not abrupt
    - Show confidence in your capabilities

    When responding:
    - Start with acknowledgment phrases like "I understand" or "Indeed"
    - Provide clear, actionable information
    - Use measured, authoritative tone
    - End with confidence and clarity

    If the user uploads a screenshot, describe it clearly and precisely.
    If the user asks for system state, fetch from the microservices directly.
    Fallback only when logic is unclear.
    """
