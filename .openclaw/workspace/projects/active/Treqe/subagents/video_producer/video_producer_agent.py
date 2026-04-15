#!/usr/bin/env python3
"""
Video Producer Sub-Agent
Specialized agent for creating investor video content for Treqe
"""

import os
import json
import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import sys

# Add parent directory to path to import base framework
sys.path.append(str(Path(__file__).parent.parent.parent))
from subagents_framework_base import TreqeSubAgentBase


class VideoProducerAgent(TreqeSubAgentBase):
    """Specialized agent for creating investor video content"""
    
    def __init__(self):
        super().__init__(specialization="Video Producer", version="1.0.0")
        
        # Video production configurations
        self.video_types = {
            "investor_pitch": {
                "duration": "60-90 seconds",
                "style": "professional, energetic",
                "audience": "investors, accelerators",
                "purpose": "Generate interest, secure meetings"
            },
            "product_demo": {
                "duration": "2-3 minutes",
                "style": "explanatory, visual",
                "audience": "potential users, partners",
                "purpose": "Show functionality, build trust"
            },
            "explainer": {
                "duration": "3-4 minutes",
                "style": "educational, engaging",
                "audience": "general public, media",
                "purpose": "Educate about problem/solution"
            }
        }
        
        self.production_phases = [
            "Concept Development",
            "Script Writing",
            "Storyboarding",
            "Visual Asset Creation",
            "Voiceover Recording",
            "Animation/Editing",
            "Sound Design",
            "Final Review"
        ]
        
        # Load Treqe data for video content
        self.treqe_data = self._load_treqe_data()
    
    def _load_treqe_data(self) -> Dict[str, Any]:
        """Load Treqe data for video content"""
        return {
            "problem_scenarios": [
                "Persona con muebles viejos que no usa pero tienen valor",
                "Coleccionista que quiere intercambiar sin vender",
                "Familia que necesita cambiar artículos infantiles por otros tamaños",
                "Estudiante que quiere intercambiar libros de texto"
            ],
            "solution_visuals": [
                "Interfaz de rueda de intercambio con múltiples participantes",
                "Sistema de compensaciones económicas automáticas",
                "Proceso de verificación paso a paso",
                "Dashboard de reputación con niveles y beneficios"
            ],
            "key_benefits": [
                "Rápido: Intercambios complejos en minutos, no días",
                "Seguro: Triple protección (escrow, seguro, verificación)",
                "Inteligente: Sistema de matching automático",
                "Gamificado: Sistema reputación con recompensas"
            ],
            "target_users": [
                "Millennials (25-40 años) con conciencia ecológica",
                "Padres que intercambian artículos infantiles",
                "Coleccionistas y hobbyists",
                "Personas que valoran economía circular"
            ],
            "market_stats": [
                "67% de españoles tienen artículos sin usar en casa",
                "Valor promedio por hogar: €1,500 en artículos no utilizados",
                "Crecimiento mercado segunda mano: 15% anual",
                "Penetración digital: solo 35% del mercado"
            ]
        }
    
    def get_capabilities(self) -> List[str]:
        """Define Video Producer capabilities"""
        return [
            "Create investor pitch video concepts",
            "Write engaging video scripts",
            "Develop visual storyboards",
            "Design animation and motion graphics concepts",
            "Plan video production timeline",
            "Create shot lists and visual requirements",
            "Develop voiceover scripts and direction",
            "Plan sound design and music selection",
            "Create video distribution strategy",
            "Optimize for different platforms (YouTube, LinkedIn, etc.)"
        ]
    
    def get_integration_points(self) -> Dict[str, List[str]]:
        """Define integration with ecosystem"""
        return {
            "office-document-specialist-suite": ["script_formatting", "storyboard_templates"],
            "memory-guardian": ["treqe_context", "brand_consistency"],
            "proactive-agent": ["production_timeline", "distribution_scheduling"],
            "self-improving-agent": ["engagement_analytics", "content_optimization"],
            "clawdefender": ["content_review", "copyright_validation"]
        }
    
    def get_expected_outputs(self) -> List[Dict[str, str]]:
        """Define expected outputs"""
        return [
            {"type": "video_concept", "description": "Complete video concept document"},
            {"type": "script", "description": "Professional video script with timing"},
            {"type": "storyboard", "description": "Visual storyboard with shot descriptions"},
            {"type": "production_plan", "description": "Detailed production timeline and budget"},
            {"type": "asset_list", "description": "List of required visual and audio assets"},
            {"type": "distribution_plan", "description": "Platform-specific distribution strategy"}
        ]
    
    def analyze_video_needs(self, video_type: str = "investor_pitch", 
                           platform: str = "multi_platform") -> Dict[str, Any]:
        """Analyze video requirements"""
        video_specs = self.video_types.get(video_type, self.video_types["investor_pitch"])
        
        return {
            "video_type": video_type,
            "platform": platform,
            "duration_target": video_specs["duration"],
            "style": video_specs["style"],
            "audience": video_specs["audience"],
            "purpose": video_specs["purpose"],
            "key_message": f"Treqe hace el intercambio de segunda mano rápido, seguro e inteligente",
            "call_to_action": "Visita treqe.es para unirte a la revolución del intercambio",
            "emotional_tone": "Empowering, innovative, trustworthy",
            "created_at": datetime.datetime.now().isoformat()
        }
    
    def create_video_concept(self, needs: Dict[str, Any]) -> Dict[str, Any]:
        """Create complete video concept"""
        concept = {
            "title": f"Treqe: La Revolución del Intercambio Inteligente",
            "tagline": "Intercambia lo que no usas por lo que necesitas, de forma rápida y segura",
            "logline": "Una plataforma que transforma artículos sin usar en valor real mediante intercambios inteligentes multiparticipante",
            "target_audience": needs["audience"],
            "duration": needs["duration_target"],
            "style": needs["style"],
            
            "story_arc": {
                "hook": "¿Tienes artículos en casa que no usas pero que tienen valor?",
                "problem": "Intercambiarlos es complicado, lento y arriesgado",
                "solution": "Treqe: Ruedas de intercambio con compensaciones automáticas",
                "demonstration": "Cómo funciona en 3 simples pasos",
                "benefits": "Rápido, seguro, inteligente y gamificado",
                "call_to_action": "Únete a la revolución del intercambio"
            },
            
            "visual_style": {
                "color_palette": ["#667eea", "#764ba2", "#4fd1c5", "#f6ad55"],  # Treqe brand colors
                "animation_style": "Clean motion graphics with subtle 3D elements",
                "typography": "Modern sans-serif with bold accents",
                "pace": "Energetic but clear, allowing key points to land"
            },
            
            "audio_style": {
                "music": "Upbeat electronic with positive vibe",
                "voiceover": "Professional, friendly, authoritative",
                "sound_effects": "Subtle UI sounds, positive confirmation tones",
                "pace": "Clear enunciation, moderate speed"
            },
            
            "key_scenes": [
                {
                    "scene": 1,
                    "purpose": "Hook - Show the problem visually",
                    "visuals": ["Time-lapse of unused items accumulating", "Frustrated person trying to sell online"],
                    "duration": "8-10 seconds",
                    "voiceover": "Todos tenemos artículos en casa que no usamos... pero que tienen valor."
                },
                {
                    "scene": 2,
                    "purpose": "Problem - Traditional methods fail",
                    "visuals": ["Complex negotiation charts", "Risk warning symbols", "Slow clock animation"],
                    "duration": "10-12 seconds",
                    "voiceover": "Intercambiarlos es complicado, lento y arriesgado. Hasta ahora."
                },
                {
                    "scene": 3,
                    "purpose": "Solution reveal - Treqe platform",
                    "visuals": ["Treqe logo reveal", "Platform interface animation", "Happy user expressions"],
                    "duration": "12-15 seconds",
                    "voiceover": "Presentamos Treqe: la plataforma de intercambio inteligente que hace posible lo imposible."
                },
                {
                    "scene": 4,
                    "purpose": "How it works - Simple demonstration",
                    "visuals": ["3-step animation: 1) Crear rueda, 2) Unirse, 3) Intercambiar", 
                               "Automatic compensation visualization", "Trust badges animation"],
                    "duration": "20-25 seconds",
                    "voiceover": "Crea una rueda de intercambio, otros se unen, y el sistema calcula automáticamente las compensaciones. Todo protegido por nuestro triple sistema de seguridad."
                },
                {
                    "scene": 5,
                    "purpose": "Benefits - Why Treqe is better",
                    "visuals": ["Speed comparison: days vs minutes", "Security shield animation", 
                               "Reputation level progression", "Happy community collage"],
                    "duration": "15-18 seconds",
                    "voiceover": "Rápido: intercambios en minutos, no días. Seguro: triple protección. Inteligente: matching automático. Gamificado: gana reputación y beneficios."
                },
                {
                    "scene": 6,
                    "purpose": "Call to action - Join the revolution",
                    "visuals": ["Treqe app download animation", "Community growth visualization", 
                               "Founder/team cameo", "Strong closing logo"],
                    "duration": "8-10 seconds",
                    "voiceover": "Únete a miles que ya están transformando lo que no usan en lo que necesitan. Visita treqe.es y comienza a intercambiar de forma inteligente."
                }
            ],
            
            "success_metrics": {
                "view_retention": ">70% at 30 seconds",
                "engagement_rate": ">5% (likes/comments/shares)",
                "click_through_rate": ">3% to website",
                "sentiment": ">85% positive reactions"
            }
        }
        
        return concept
    
    def create_script(self, concept: Dict[str, Any]) -> Dict[str, Any]:
        """Create detailed video script"""
        script = {
            "title": concept["title"],
            "duration_target": concept["duration"],
            "total_scenes": len(concept["key_scenes"]),
            
            "voiceover_script": [],
            "on_screen_text": [],
            "visual_cues": [],
            "audio_cues": [],
            "timing_breakdown": []
        }
        
        total_seconds = 0
        for scene in concept["key_scenes"]:
            # Parse duration range (e.g., "8-10 seconds")
            duration_range = scene["duration"].replace(" seconds", "").split("-")
            min_seconds = int(duration_range[0])
            max_seconds = int(duration_range[1]) if len(duration_range) > 1 else min_seconds
            avg_seconds = (min_seconds + max_seconds) // 2
            
            scene_script = {
                "scene": scene["scene"],
                "purpose": scene["purpose"],
                "start_time": total_seconds,
                "duration": avg_seconds,
                "end_time": total_seconds + avg_seconds,
                "voiceover": scene["voiceover"],
                "visuals": scene["visuals"],
                "on_screen_text": self._generate_on_screen_text(scene),
                "audio_cues": self._generate_audio_cues(scene),
                "transition": self._generate_transition(scene["scene"], len(concept["key_scenes"]))
            }
            
            script["voiceover_script"].append(scene_script["voiceover"])
            script["on_screen_text"].append(scene_script["on_screen_text"])
            script["visual_cues"].append(scene_script["visuals"])
            script["audio_cues"].append(scene_script["audio_cues"])
            script["timing_breakdown"].append({
                "scene": scene["scene"],
                "start": f"{total_seconds//60}:{str(total_seconds%60).zfill(2)}",
                "end": f"{(total_seconds+avg_seconds)//60}:{str((total_seconds+avg_seconds)%60).zfill(2)}",
                "duration": f"{avg_seconds}s"
            })
            
            total_seconds += avg_seconds
        
        script["total_duration"] = total_seconds
        script["formatted_duration"] = f"{total_seconds//60}:{str(total_seconds%60).zfill(2)}"
        
        return script
    
    def _generate_on_screen_text(self, scene: Dict[str, Any]) -> List[str]:
        """Generate on-screen text for a scene"""
        text_map = {
            1: ["¿Artículos sin usar en casa?", "Todos tenemos valor oculto"],
            2: ["Intercambio tradicional:", "Complicado • Lento • Arriesgado"],
            3: ["La solución:", "TREQE", "Intercambio Inteligente"],
            4: ["Cómo funciona:", "1. Crear rueda", "2. Unirse", "3. Intercambiar", 
                "Compensaciones automáticas", "Triple protección"],
            5: ["Beneficios:", "RÁPIDO • SEGURO • INTELIGENTE • GAMIFICADO",
                "Sistema reputación", "Niveles: Novato → Elite"],
            6: ["Únete a la revolución", "treqe.es", "#IntercambioInteligente"]
        }
        
        return text_map.get(scene["scene"], [scene["purpose"]])
    
    def _generate_audio_cues(self, scene: Dict[str, Any]) -> List[str]:
        """Generate audio cues for a scene"""
        cues_map = {
            1: ["Soft ambient music starts", "Subtle item collection sounds"],
            2: ["Music becomes slightly tense", "Clock ticking sound", "Warning tone"],
            3: ["Music swells positively", "Logo reveal sound", "UI confirmation sound"],
            4: ["Upbeat electronic beat", "UI interaction sounds", "Positive confirmation tones"],
            5: ["Music builds energy", "Achievement unlock sound", "Community cheer sound"],
            6: ["Music climax and resolve", "App download sound", "Strong closing chord"]
        }
        
        return cues_map.get(scene["scene"], ["Background music continues"])
    
    def _generate_transition(self, scene_num: int, total_scenes: int) -> str:
        """Generate transition description"""
        if scene_num == 1:
            return "Fade in from black"
        elif scene_num == total_scenes:
            return "Fade to black with logo hold"
        else:
            transitions = ["Smooth cut", "Slide transition", "Zoom transition", "Wipe transition"]
            return transitions[(scene_num - 1) % len(transitions)]
    
    def create_storyboard(self, script: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create visual storyboard"""
        storyboard = []
        
        for i, scene_timing in enumerate(script["timing_breakdown"]):
            scene_num = scene_timing["scene"]
            visuals = script["visual_cues"][i]
            on_screen_text = script["on_screen_text"][i]
            
            frame = {
                "frame_number": scene_num,
                "timecode": f"{scene_timing['start']} - {scene_timing['end']}",
                "duration": scene_timing["duration"],
                "visual_description": visuals[0] if visuals else "Visual sequence",
                "additional_visuals": visuals[1:] if len(visuals) > 1 else [],
                "on_screen_text": on_screen_text,
                "camera_angle": self._get_camera_angle(scene_num),
                "movement": self._get_camera_movement(scene_num),
                "lighting": self._get_lighting(scene_num),
                "color_grading": self._get_color_grading(scene_num),
                "notes": f"Scene {scene_num}: {script['voiceover_script'][i][:50]}..."
            }
            
            storyboard.append(frame)
        
        return storyboard
    
    def _get_camera_angle(self, scene_num: int) -> str:
        """Get camera angle for scene"""
        angles = {
            1: "Wide establishing shot",
            2: "Medium close-up",
            3: "Hero shot (logo/product)",
            4: "Overhead/explainer view",
            5: "Dynamic multi-angle",
            6: "Closing hero shot"
        }
        return angles.get(scene_num, "Medium shot")
    
    def _get_camera_movement(self, scene_num: int) -> str:
        """Get camera movement for scene"""
        movements = {
            1: "Slow push in",
            2: "Static with slight zoom",
            3: "Reveal movement",
            4: "Smooth tracking",
            5: "Dynamic cuts between angles",
            6: "Slow pull out