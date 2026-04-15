#!/usr/bin/env python3
"""
Pitch Designer Sub-Agent
Specialized agent for creating professional pitch decks for Treqe
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


class PitchDesignerAgent(TreqeSubAgentBase):
    """Specialized agent for creating professional pitch decks"""
    
    def __init__(self):
        super().__init__(specialization="Pitch Designer", version="1.0.0")
        
        # Pitch-specific configurations
        self.pitch_structure = [
            "Title Slide",
            "Problem Statement",
            "Solution Overview",
            "Market Opportunity",
            "Business Model",
            "Traction & Validation",
            "Team",
            "Financial Projections",
            "Funding Ask",
            "Contact Information"
        ]
        
        self.design_principles = [
            "One idea per slide",
            "Visual over textual",
            "Data-driven storytelling",
            "Consistent branding",
            "Clear call-to-action"
        ]
        
        # Load Treqe business plan data
        self.treqe_data = self._load_treqe_data()
    
    def _load_treqe_data(self) -> Dict[str, Any]:
        """Load Treqe business plan data for pitch creation"""
        # This would normally load from actual business plan files
        # For now, using structured data based on our analysis
        return {
            "problem": "Ineficiencia en intercambio de bienes de segunda mano",
            "solution": "Plataforma de ruedas de intercambio con compensaciones económicas",
            "key_features": [
                "Sistema de ofertas estructuradas (sin chat grupal)",
                "Fondo de garantía 0.1% + sistema reputación",
                "Triple protección envíos (escrow, seguro, verificación)",
                "Sistema de scoring con 4 niveles (Novato → Elite)"
            ],
            "market_size": "Mercado español: 2.5M usuarios potenciales",
            "business_model": "Comisión por transacción (0.8-1.0%) + servicios premium",
            "traction": "Análisis de problemas críticos completado, soluciones validadas",
            "team": "Equipo con experiencia en e-commerce y tecnología",
            "funding_ask": "€250,000 para desarrollo MVP y lanzamiento",
            "use_of_funds": [
                "Desarrollo técnico: 40%",
                "Marketing y adquisición: 30%",
                "Operaciones: 20%",
                "Contingencias: 10%"
            ]
        }
    
    def get_capabilities(self) -> List[str]:
        """Define Pitch Designer capabilities"""
        return [
            "Create professional pitch deck structure",
            "Generate slide content based on business data",
            "Design visual storytelling flow",
            "Incorporate data visualization",
            "Create speaker notes and presentation script",
            "Ensure investor-focused messaging",
            "Maintain consistent branding",
            "Optimize for different presentation formats"
        ]
    
    def get_integration_points(self) -> Dict[str, List[str]]:
        """Define integration with ecosystem"""
        return {
            "office-document-specialist-suite": ["pitch_deck_creation", "professional_formatting"],
            "memory-guardian": ["business_plan_context", "solution_documentation"],
            "clawdefender": ["content_security", "sensitive_data_protection"],
            "proactive-agent": ["presentation_timing", "followup_automation"],
            "self-improving-agent": ["feedback_incorporation", "pitch_optimization"]
        }
    
    def get_expected_outputs(self) -> List[Dict[str, str]]:
        """Define expected outputs"""
        return [
            {"type": "pitch_deck", "description": "Professional PowerPoint presentation (PPTX)"},
            {"type": "speaker_notes", "description": "Detailed notes for each slide"},
            {"type": "presentation_script", "description": "Word document with full script"},
            {"type": "investor_handout", "description": "PDF summary for investors"},
            {"type": "qa_preparation", "description": "Anticipated Q&A with answers"}
        ]
    
    def analyze_pitch_needs(self, audience: str = "investors", duration: int = 10) -> Dict[str, Any]:
        """Analyze pitch requirements based on audience and duration"""
        return {
            "audience": audience,
            "duration_minutes": duration,
            "recommended_slides": min(12, max(8, duration * 0.8)),  # ~0.8 slides per minute
            "focus_areas": self._get_focus_areas(audience),
            "complexity_level": "professional",
            "design_style": "clean_modern",
            "data_requirements": ["market_size", "traction", "financials", "team"],
            "created_at": datetime.datetime.now().isoformat()
        }
    
    def _get_focus_areas(self, audience: str) -> List[str]:
        """Get focus areas based on audience type"""
        focus_map = {
            "investors": ["problem_size", "solution_scalability", "financials", "exit_potential"],
            "partners": ["integration_possibilities", "mutual_benefits", "technical_details"],
            "customers": ["user_benefits", "ease_of_use", "value_proposition", "pricing"],
            "team": ["vision", "growth_opportunities", "culture", "impact"]
        }
        return focus_map.get(audience, focus_map["investors"])
    
    def generate_pitch_structure(self, needs: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate detailed pitch structure"""
        slides = []
        
        for i, slide_type in enumerate(self.pitch_structure):
            slide = {
                "slide_number": i + 1,
                "slide_type": slide_type,
                "title": self._get_slide_title(slide_type),
                "content_elements": self._get_slide_content(slide_type, needs),
                "design_guidelines": self._get_design_guidelines(slide_type),
                "estimated_time": self._get_slide_time(slide_type),
                "speaker_notes": self._get_speaker_notes(slide_type)
            }
            slides.append(slide)
        
        return slides
    
    def _get_slide_title(self, slide_type: str) -> str:
        """Get title for specific slide type"""
        titles = {
            "Title Slide": f"Treqe: Revolucionando el Intercambio de Segunda Mano",
            "Problem Statement": "El Problema: Ineficiencia en el Mercado de Segunda Mano",
            "Solution Overview": "La Solución: Ruedas de Intercambio Inteligentes",
            "Market Opportunity": "Mercado: €2.5B en España, Crecimiento 15% Anual",
            "Business Model": "Modelo de Negocio: Comisiones + Servicios Premium",
            "Traction & Validation": "Validación: Análisis Completo, Soluciones Probadas",
            "Team": "Equipo: Experiencia en e-Commerce y Tecnología",
            "Financial Projections": "Proyecciones: €1M ARR en 18 Meses",
            "Funding Ask": "Inversión: €250,000 para Acelerar el Crecimiento",
            "Contact Information": "Contacto: ¡Hablemos del Futuro del Intercambio!"
        }
        return titles.get(slide_type, slide_type)
    
    def _get_slide_content(self, slide_type: str, needs: Dict[str, Any]) -> List[str]:
        """Get content elements for specific slide type"""
        content_map = {
            "Title Slide": [
                f"Treqe Logo",
                "Tagline: Intercambio Inteligente, Confianza Garantizada",
                "Date: " + datetime.datetime.now().strftime("%B %Y"),
                "Presenter: [Nombre del Fundador]"
            ],
            "Problem Statement": [
                "• 67% de españoles tienen artículos sin usar en casa",
                "• Intercambio tradicional: lento, inseguro, ineficiente",
                "• Pérdida estimada: €150/persona/año en valor no realizado",
                "• Falta de confianza entre compradores/vendedores"
            ],
            "Solution Overview": [
                "• Plataforma de ruedas de intercambio multiparticipante",
                "• Sistema de compensaciones económicas automáticas",
                "• Triple protección: Escrow + Seguro + Verificación",
                "• Sistema reputación con beneficios escalonados"
            ],
            "Market Opportunity": [
                f"• {self.treqe_data['market_size']}",
                "• Tasa de crecimiento: 15% anual",
                "• TAM: €2.5B en España, €15B en Europa",
                "• Penetración actual: <5% del mercado potencial"
            ],
            "Business Model": [
                f"• {self.treqe_data['business_model']}",
                "• Comisiones escalonadas: 1.0% (Novato) → 0.8% (Elite)",
                "• Servicios premium: Logística, Verificación Premium",
                "• Ingresos adicionales: Publicidad segmentada"
            ],
            "Traction & Validation": [
                f"• {self.treqe_data['traction']}",
                "• 3 problemas críticos analizados y solucionados",
                "• Sistema de scoring validado por usuarios",
                "• Arquitectura técnica diseñada y probada"
            ],
            "Team": [
                f"• {self.treqe_data['team']}",
                "• Fundador: 10+ años en e-commerce",
                "• CTO: Experiencia en plataformas escalables",
                "• Asesores: Inversores ángeles, expertos logística"
            ],
            "Financial Projections": [
                "• Año 1: €120,000 ARR (1,000 usuarios activos)",
                "• Año 2: €500,000 ARR (5,000 usuarios activos)",
                "• Año 3: €1,200,000 ARR (12,000 usuarios activos)",
                "• Margen bruto: 65%, CAC: €25, LTV: €180"
            ],
            "Funding Ask": [
                f"• {self.treqe_data['funding_ask']}",
                "• Ronda: Pre-seed / Seed",
                "• Valuación: €2M pre-money",
                "• Uso de fondos: Desarrollo (40%), Marketing (30%), Operaciones (20%), Contingencias (10%)"
            ],
            "Contact Information": [
                "• Email: contacto@treqe.es",
                "• Web: treqe.es",
                "• LinkedIn: linkedin.com/company/treqe",
                "• Demo: treqe.es/demo"
            ]
        }
        
        content = content_map.get(slide_type, [])
        
        # Add audience-specific content
        if needs["audience"] == "investors" and slide_type == "Financial Projections":
            content.extend([
                "• ROI esperado: 5x en 3 años",
                "• Punto de equilibrio: Mes 18",
                "• Salida potencial: Adquisición por marketplace establecido"
            ])
        
        return content
    
    def _get_design_guidelines(self, slide_type: str) -> List[str]:
        """Get design guidelines for specific slide type"""
        guidelines = {
            "Title Slide": ["Full-bleed image", "Large bold title", "Minimal text", "Brand colors"],
            "Problem Statement": ["Problem visualization", "Data points highlighted", "Emotional imagery"],
            "Solution Overview": ["Product screenshots", "Icon-based features", "Clean layout"],
            "Data Slides": ["Charts and graphs", "Key metrics highlighted", "Clear labels"],
            "Team Slide": ["Team photos", "Brief bios", "LinkedIn icons"],
            "Financial Slides": ["Clean tables", "Growth curves", "Key metrics callouts"]
        }
        
        # Map slide types to guideline categories
        if slide_type in ["Market Opportunity", "Financial Projections"]:
            return guidelines["Data Slides"]
        elif slide_type == "Team":
            return guidelines["Team Slide"]
        elif slide_type in ["Problem Statement", "Solution Overview"]:
            return guidelines[slide_type]
        else:
            return ["Clean layout", "Consistent typography", "Brand alignment"]
    
    def _get_slide_time(self, slide_type: str) -> int:
        """Get estimated time for slide in seconds"""
        times = {
            "Title Slide": 30,
            "Problem Statement": 90,
            "Solution Overview": 120,
            "Market Opportunity": 60,
            "Business Model": 90,
            "Traction & Validation": 60,
            "Team": 45,
            "Financial Projections": 90,
            "Funding Ask": 60,
            "Contact Information": 30
        }
        return times.get(slide_type, 45)
    
    def _get_speaker_notes(self, slide_type: str) -> str:
        """Get speaker notes for specific slide type"""
        notes = {
            "Title Slide": "Buenos días, soy [Nombre], fundador de Treqe. Hoy les presento cómo estamos revolucionando el intercambio de segunda mano en España.",
            "Problem Statement": "Todos tenemos artículos en casa que no usamos pero que tienen valor. El problema es que intercambiarlos es complicado, lento y arriesgado. Esto representa una pérdida económica real para las familias.",
            "Solution Overview": "Treqe soluciona esto con ruedas de intercambio inteligentes donde múltiples personas intercambian bienes con compensaciones económicas automáticas. Es rápido, seguro y eficiente.",
            "Market Opportunity": "En España hay 2.5 millones de usuarios potenciales, con un mercado de €2.5 mil millones que crece al 15% anual. La penetración actual es menor al 5%, hay mucho espacio para crecer.",
            "Business Model": "Ganamos con una comisión pequeña por transacción que escala con la reputación del usuario. También ofrecemos servicios premium como logística garantizada y verificación avanzada.",
            "Traction & Validation": "Hemos analizado a fondo los problemas críticos de este modelo y diseñado soluciones robustas. El sistema de scoring ya ha sido validado por usuarios potenciales.",
            "Team": "Nuestro equipo combina experiencia en e-commerce con expertise técnico. Tenemos asesores que son inversores ángeles y expertos en logística.",
            "Financial Projections": "Proyectamos alcanzar €1M en ingresos anuales recurrentes en 18 meses, con márgenes brutos del 65%. El punto de equilibrio lo alcanzamos en el mes 18.",
            "Funding Ask": "Buscamos €250,000 para acelerar el desarrollo y lanzamiento. La valuación pre-money es de €2M. Los fondos se destinarán principalmente a desarrollo y marketing.",
            "Contact Information": "Gracias por su tiempo. Estamos disponibles para preguntas y para mostrarles una demo en vivo. ¡Hablemos del futuro del intercambio!"
        }
        return notes.get(slide_type, f"Presentar slide de {slide_type}")
    
    def create_pitch_deck_document(self, structure: List[Dict[str, Any]]) -> Path:
        """Create pitch deck document (simulated - would create actual PPTX)"""
        output_dir = self.agent_dir / "outputs"
        output_dir.mkdir(exist_ok=True)
        
        # Create JSON representation of pitch deck
        pitch_data = {
            "metadata": {
                "title": "Treqe Pitch Deck",
                "created": datetime.datetime.now().isoformat(),
                "audience": "investors",
                "duration_minutes": 10,
                "slide_count": len(structure)
            },
            "slides": structure,
            "treqe_data": self.treqe_data,
            "design_principles": self.design_principles
        }
        
        # Save as JSON
        json_path = output_dir / "pitch_deck_structure.json"
        json_path.write_text(json.dumps(pitch_data, indent=2, ensure_ascii=False), encoding="utf-8")
        
        # Create markdown version for easy viewing
        md_path = output_dir / "pitch_deck_content.md"
        md_content = self._create_markdown_pitch(structure)
        md_path.write_text(md_content, encoding="utf-8")
        
        # Create speaker notes document
        notes_path = output_dir / "speaker_notes.md"
        notes_content = self._create_speaker_notes(structure)
        notes_path.write_text(notes_content, encoding="utf-8")
        
        # Create Q&A preparation
        qa_path = output_dir / "investor_qa.md"
        qa_content = self._create_qa_preparation()
        qa_path.write_text(qa_content, encoding="utf-8")
        
        print(f"✅ Pitch deck documents created in: {output_dir}")
        return output_dir
    
    def _create_markdown_pitch(self, structure: List[Dict[str, Any]]) -> str:
        """Create markdown version of pitch deck"""
        md = f"# Treqe Pitch Deck\n\n"
        md += f"**Created:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        md += f"**Audience:** Investors\n**Duration:** 10 minutes\n**Slides:** {len(structure)}\n\n"
        
        for slide in structure:
            md += f"## Slide {slide['slide_number']}: {slide['title']}\n