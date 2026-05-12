"""
Template Engine Module

Handles prompt template rendering and validation.
"""

from typing import Dict, Any, List

from .settings_schema import VariableSet, PromptTemplate
from .variable_resolver import VariableResolver


class TemplateEngine:
    """Engine for rendering prompt templates with variables."""

    def __init__(self):
        self.variable_resolver = VariableResolver()

    def render_prompt(
        self,
        template: str,
        variables: VariableSet
    ) -> Dict[str, str]:
        """
        Renders a prompt template with the given variables.

        INPUT:
            template: str - prompt template with {{variable}} placeholders
            variables: VariableSet - runtime variables for substitution

        OUTPUT:
            {
                "prompt": str - fully rendered prompt
            }
        """
        # Convert VariableSet to dict
        vars_dict = {
            "duration": variables.duration,
            "episode_count": variables.episode_count,
            "orientation": variables.orientation,
            "genre": variables.genre,
            "style": variables.style,
            "mood": variables.mood,
            "channel_name": variables.channel_name
        }

        result = self.variable_resolver.resolve(template, vars_dict)
        return {"prompt": result["resolved_text"]}

    def validate_variables(
        self,
        template: str,
        variables: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validates that all required variables are present in the input.

        INPUT:
            template: str - prompt template
            variables: dict - variables to validate

        OUTPUT:
            {
                "valid": bool,
                "missing_fields": list[str]
            }
        """
        return self.variable_resolver.validate_variables(template, variables)

    def extract_variables(self, template: str) -> List[str]:
        """
        Extracts all variable names from a template.

        INPUT:
            template: str - prompt template with {{variable}} placeholders

        OUTPUT:
            list[str] - list of variable names
        """
        import re
        pattern = r'\{\{(\w+)\}\}'
        return list(set(re.findall(pattern, template)))
