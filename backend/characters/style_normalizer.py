"""
Style Normalizer Module
Normalizes and extracts consistent visual style parameters from story metadata.
"""
from typing import Dict, Any, Optional
from .character_schema import StyleProfile


class StyleNormalizer:
    """
    Normalizes style inputs into a consistent StyleProfile.
    Ensures that visual style, mood, lighting, and color palette 
    follow standardized formats for downstream generation.
    """

    DEFAULT_LIGHTING_MAP = {
        "dark": "low-key, high contrast",
        "bright": "high-key, soft lighting",
        "neutral": "balanced, natural lighting",
        "dramatic": "chiaroscuro, strong shadows",
        "cinematic": "three-point lighting, depth"
    }

    DEFAULT_MOOD_MAP = {
        "tense": "tense, oppressive",
        "happy": "upbeat, energetic",
        "sad": "melancholic, somber",
        "mysterious": "enigmatic, suspenseful",
        "epic": "grand, awe-inspiring"
    }

    def normalize_style(self, story_tone: str, genre: str, 
                        custom_style: Optional[Dict[str, str]] = None) -> StyleProfile:
        """
        Create a normalized StyleProfile from story attributes.
        
        Args:
            story_tone: The emotional tone of the story
            genre: The genre of the story
            custom_style: Optional custom style overrides
            
        Returns:
            StyleProfile with normalized values
        """
        # Extract base style from genre
        visual_style = self._get_genre_style(genre)
        
        # Normalize mood
        mood = self._normalize_mood(story_tone)
        
        # Normalize lighting
        lighting = self._normalize_lighting(story_tone)
        
        # Determine color palette
        color_palette = self._get_color_palette(genre, story_tone)
        
        # Apply custom overrides if provided
        if custom_style:
            visual_style = custom_style.get("visual_style", visual_style)
            mood = custom_style.get("mood", mood)
            lighting = custom_style.get("lighting", lighting)
            color_palette = custom_style.get("color_palette", color_palette)
        
        # Generate cinematic rules
        cinematic_rules = self._generate_cinematic_rules(visual_style, lighting)
        
        return StyleProfile(
            story_id="",  # Will be set by caller
            visual_style=visual_style,
            mood=mood,
            lighting=lighting,
            color_palette=color_palette,
            cinematic_rules=cinematic_rules
        )

    def _get_genre_style(self, genre: str) -> str:
        """Map genre to visual style description."""
        genre_map = {
            "sci-fi": "futuristic, sleek, high-tech aesthetics",
            "fantasy": "magical, ethereal, medieval or mystical elements",
            "horror": "dark, gritty, unsettling atmosphere",
            "romance": "soft, warm, intimate framing",
            "action": "dynamic, high-contrast, motion-oriented",
            "drama": "realistic, character-focused, naturalistic",
            "comedy": "bright, colorful, playful composition",
            "thriller": "tense, shadowy, claustrophobic"
        }
        return genre_map.get(genre.lower(), "cinematic realism")

    def _normalize_mood(self, tone: str) -> str:
        """Normalize mood string to standard format."""
        tone_lower = tone.lower()
        for key, value in self.DEFAULT_MOOD_MAP.items():
            if key in tone_lower:
                return value
        return f"{tone}, atmospheric"

    def _normalize_lighting(self, tone: str) -> str:
        """Normalize lighting based on tone."""
        tone_lower = tone.lower()
        for key, value in self.DEFAULT_LIGHTING_MAP.items():
            if key in tone_lower:
                return value
        return "balanced, cinematic lighting"

    def _get_color_palette(self, genre: str, tone: str) -> str:
        """Determine appropriate color palette."""
        genre_lower = genre.lower()
        tone_lower = tone.lower()
        
        if "horror" in genre_lower or "dark" in tone_lower:
            return "desaturated blues, greys, and deep blacks"
        elif "romance" in genre_lower or "happy" in tone_lower:
            return "warm pastels, soft pinks and golds"
        elif "sci-fi" in genre_lower:
            return "cool blues, metallic silvers, neon accents"
        elif "fantasy" in genre_lower:
            return "rich purples, emerald greens, magical glows"
        else:
            return "natural, balanced color grading"

    def _generate_cinematic_rules(self, visual_style: str, lighting: str) -> str:
        """Generate specific cinematic rules for consistency."""
        rules = [
            "Maintain consistent character proportions across all shots",
            "Keep lighting direction consistent within scenes",
            f"Apply {visual_style} aesthetic to all visual elements",
            f"Use {lighting} throughout the sequence"
        ]
        return "; ".join(rules)
