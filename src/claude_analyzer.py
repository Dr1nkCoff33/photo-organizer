#!/usr/bin/env python3
"""
Claude AI Integration for Photo Content Analysis
Provides additional context and validation for photo categorization
"""

import os
import json
import base64
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging
import requests
from PIL import Image
import io

logger = logging.getLogger(__name__)

class ClaudePhotoAnalyzer:
    """Claude AI integration for photo content analysis"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-sonnet-20240229"):
        self.api_key = api_key or os.getenv('CLAUDE_API_KEY')
        self.model = model
        self.base_url = "https://api.anthropic.com/v1/messages"
        
        if not self.api_key:
            logger.warning("Claude API key not found. Content analysis will be disabled.")
            self.enabled = False
        else:
            self.enabled = True
    
    def encode_image(self, image_path: Path) -> Optional[str]:
        """Encode image to base64 for Claude API"""
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            logger.error(f"Error encoding image {image_path}: {e}")
            return None
    
    def analyze_photo_content(self, image_path: Path, exif_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Analyze photo content using Claude AI"""
        if not self.enabled:
            return None
        
        try:
            # Encode image
            base64_image = self.encode_image(image_path)
            if not base64_image:
                return None
            
            # Prepare prompt with EXIF context
            exif_summary = self._create_exif_summary(exif_data)
            
            prompt = f"""
You are an expert photography analyst. Analyze this photo and provide insights about its content and category.

EXIF Data Context:
{exif_summary}

Please analyze the photo content and provide:
1. Primary subject(s) in the photo
2. Suggested photography category based on content (Portrait, Landscape, Street, Wildlife, Sports, Macro, Architecture, Night, Event)
3. Confidence level (1-10) for your category suggestion
4. Brief description of what you see
5. Any notable compositional elements

Respond in JSON format:
{{
    "primary_subject": "description",
    "suggested_category": "category_name",
    "confidence": 8,
    "description": "brief description",
    "compositional_elements": ["element1", "element2"]
}}
"""
            
            # Prepare request
            headers = {
                "Content-Type": "application/json",
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01"
            }
            
            data = {
                "model": self.model,
                "max_tokens": 1000,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/jpeg",
                                    "data": base64_image
                                }
                            }
                        ]
                    }
                ]
            }
            
            # Make request
            response = requests.post(self.base_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            # Parse response
            result = response.json()
            content = result['content'][0]['text']
            
            # Extract JSON from response
            try:
                # Find JSON in the response
                start_idx = content.find('{')
                end_idx = content.rfind('}') + 1
                if start_idx != -1 and end_idx != 0:
                    json_str = content[start_idx:end_idx]
                    analysis = json.loads(json_str)
                    return analysis
                else:
                    logger.warning(f"Could not extract JSON from Claude response for {image_path}")
                    return None
                    
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse Claude response as JSON for {image_path}: {e}")
                return None
                
        except Exception as e:
            logger.error(f"Error analyzing photo content for {image_path}: {e}")
            return None
    
    def _create_exif_summary(self, exif_data: Dict[str, Any]) -> str:
        """Create a readable summary of EXIF data for Claude"""
        summary_parts = []
        
        # Camera info
        camera = f"{exif_data.get('Make', '')} {exif_data.get('Model', '')}".strip()
        if camera:
            summary_parts.append(f"Camera: {camera}")
        
        # Lens info
        lens = exif_data.get('LensModel') or exif_data.get('LensSpec', '')
        if lens:
            summary_parts.append(f"Lens: {lens}")
        
        # Technical settings
        focal_length = exif_data.get('FocalLength', '')
        f_number = exif_data.get('FNumber', '')
        iso = exif_data.get('ISO', '')
        shutter_speed = exif_data.get('ShutterSpeed', '')
        
        if focal_length:
            summary_parts.append(f"Focal Length: {focal_length}")
        if f_number:
            summary_parts.append(f"Aperture: f/{f_number}")
        if iso:
            summary_parts.append(f"ISO: {iso}")
        if shutter_speed:
            summary_parts.append(f"Shutter Speed: {shutter_speed}")
        
        # Focus and metering
        focus_mode = exif_data.get('FocusMode', '')
        metering_mode = exif_data.get('MeteringMode', '')
        scene_mode = exif_data.get('SceneMode', '')
        
        if focus_mode:
            summary_parts.append(f"Focus Mode: {focus_mode}")
        if metering_mode:
            summary_parts.append(f"Metering: {metering_mode}")
        if scene_mode:
            summary_parts.append(f"Scene Mode: {scene_mode}")
        
        return "\n".join(summary_parts)
    
    def validate_category(self, exif_category: str, claude_category: str, confidence: int) -> Dict[str, Any]:
        """Validate and potentially override EXIF-based category with Claude analysis"""
        validation = {
            "exif_category": exif_category,
            "claude_category": claude_category,
            "confidence": confidence,
            "final_category": exif_category,
            "overridden": False,
            "reason": "No override"
        }
        
        # Only override if Claude is very confident (8+) and categories don't match
        if confidence >= 8 and exif_category != claude_category:
            # Special cases where Claude might be more accurate
            if claude_category in ['Portrait', 'Macro', 'Wildlife']:
                validation["final_category"] = claude_category
                validation["overridden"] = True
                validation["reason"] = f"Claude confident ({confidence}/10) about {claude_category}"
            elif exif_category == 'Uncategorized' and confidence >= 9:
                validation["final_category"] = claude_category
                validation["overridden"] = True
                validation["reason"] = f"Claude very confident ({confidence}/10) about {claude_category}"
        
        return validation

def integrate_claude_analysis(photos: List[Dict[str, Any]], 
                            claude_analyzer: ClaudePhotoAnalyzer,
                            sample_size: int = 20) -> List[Dict[str, Any]]:
    """Integrate Claude analysis for a sample of photos"""
    
    if not claude_analyzer.enabled:
        logger.info("Claude analysis disabled - skipping content analysis")
        return photos
    
    logger.info(f"Running Claude content analysis on {sample_size} sample photos...")
    
    # Select sample photos (prioritize uncategorized and low-confidence ones)
    sample_photos = []
    for photo in photos:
        if photo.get('analyzed_category') == 'Uncategorized':
            sample_photos.append(photo)
        if len(sample_photos) >= sample_size // 2:
            break
    
    # Add random photos to reach sample size
    remaining_photos = [p for p in photos if p not in sample_photos]
    sample_photos.extend(remaining_photos[:sample_size - len(sample_photos)])
    
    # Analyze sample photos
    for photo in sample_photos:
        try:
            image_path = Path(photo['filepath'])
            if not image_path.exists():
                continue
            
            # Run Claude analysis
            claude_result = claude_analyzer.analyze_photo_content(
                image_path, 
                photo.get('exif_data', {})
            )
            
            if claude_result:
                # Validate and potentially override category
                validation = claude_analyzer.validate_category(
                    photo['analyzed_category'],
                    claude_result.get('suggested_category', 'Uncategorized'),
                    claude_result.get('confidence', 0)
                )
                
                # Update photo with Claude analysis
                photo['claude_analysis'] = claude_result
                photo['category_validation'] = validation
                photo['analyzed_category'] = validation['final_category']
                
                if validation['overridden']:
                    logger.info(f"Category overridden for {photo['filename']}: "
                              f"{validation['exif_category']} → {validation['final_category']}")
            
        except Exception as e:
            logger.error(f"Error in Claude analysis for {photo.get('filename', 'unknown')}: {e}")
    
    return photos 