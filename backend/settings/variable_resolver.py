"""
Variable Resolver Module

Handles variable substitution in prompt templates.
"""

import re
from typing import Dict, Any


class VariableResolver:
    """Resolves variables in template strings."""

    def resolve(self, template: str, variables: Dict[str, Any]) -> Dict[str, str]:
        """
        Resolves all variables in the template string.

        INPUT:
            template: str - template with {{variable_name}} placeholders
            variables: dict - key-value pairs for substitution

        OUTPUT:
            {
                "resolved_text": str - template with all variables substituted
            }

        RAISES:
            KeyError if a required variable is missing
        """
        resolved = template

        # Find all {{variable}} patterns
        pattern = r'\{\{(\w+)\}\}'
        matches = re.findall(pattern, template)

        missing_fields = []
        for var_name in matches:
            if var_name not in variables:
                missing_fields.append(var_name)
            else:
                # Replace {{var_name}} with actual value
                resolved = resolved.replace(f'{{{{{var_name}}}}}', str(variables[var_name]))

        if missing_fields:
            raise KeyError(f"Missing variables: {missing_fields}")

        return {"resolved_text": resolved}

    def validate_variables(
        self,
        template: str,
        variables: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validates that all required variables are present.

        INPUT:
            template: str - template with {{variable_name}} placeholders
            variables: dict - key-value pairs to check

        OUTPUT:
            {
                "valid": bool,
                "missing_fields": list[str]
            }
        """
        pattern = r'\{\{(\w+)\}\}'
        required_vars = set(re.findall(pattern, template))
        provided_vars = set(variables.keys())

        missing_fields = list(required_vars - provided_vars)

        return {
            "valid": len(missing_fields) == 0,
            "missing_fields": missing_fields
        }
