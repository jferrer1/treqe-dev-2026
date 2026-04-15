            md += f"**Type:** {slide['slide_type']}\n"
            md += f"**Time:** {slide['estimated_time']} seconds\n\n"
            
            md += "### Content:\n"
            for item in slide['content_elements']:
                md += f"- {item}\n"
            
            md += "\n### Design Guidelines:\n"
            for guideline in slide['design_guidelines']:
                md += f"- {guideline}\n"
            
            md += f"\n### Speaker Notes:\n{slide['speaker_notes']}\n\n"
            md += "---\n\n"
        
        return md
    
    def _create_speaker_notes(self, structure: List[Dict[str, Any]]) -> str:
        """Create comprehensive speaker notes"""
        notes = f"# Treqe Pitch Deck - Speaker Notes\n\n"
        notes += f"**Total Time:** {sum(slide['estimated_time'] for slide in structure)} seconds (~{sum(slide['estimated_time'] for slide in structure)//60} minutes)\n\n"
        
        for slide in structure:
            notes += f"## Slide {slide['slide_number']}: {slide['title']}\n"
            notes += f"**Time:** {slide['estimated_time']}s\n\n"
            notes += f"{slide['speaker_notes']}\n\n"
            
            notes += "**Key Points to Emphasize:**\n"
            for item in slide['content_elements'][:3]:  # First 3 items are key
                notes += f"- {item}\n"
            
            notes += "\n**Transition to Next Slide:**\n"
            notes += f"\"Esto nos lleva a...\"\n\n"
            notes += "---\n\n"
        
        # Add presentation tips
        notes += "# Presentation Tips\n\n"
        notes += "## Before the Presentation:\n"
        notes += "- Arrive 15 minutes early to setup\n"
        notes += "- Test all equipment (projector, clicker, sound)\n"
        notes += "- Have backup copies (USB, cloud, printed)\n"
        notes += "- Review Q&A preparation\n\n"
        
        notes += "## During the Presentation:\n"
        notes += "- Maintain eye contact with different audience members\n"
        notes += "- Use gestures naturally, avoid pacing\n"
        notes += "- Speak clearly and at moderate pace\n"
        notes += "- Pause after key points for emphasis\n"
        notes += "- Watch audience reactions and adjust\n\n"
        
        notes += "## Handling Questions:\n"
        notes += "- Listen to entire question before answering\n"
        notes += "- Repeat or rephrase question for clarity\n"
        notes += "- Be honest about what you don't know\n"
        notes += "- Offer to follow up with details\n"
        notes += "- Keep answers concise and relevant\n"
        
        return notes
    
    def _create_qa_preparation(self) -> str:
        """Create Q&A preparation document"""
        qa = f"# Treqe - Investor Q&A Preparation\n\n"
        qa += f"**Created:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Common investor questions
        questions = [
            {
                "question": "¿Qué hace a Treqe diferente de Wallapop, Vinted, etc.?",
                "answer": "Treqe no es un marketplace tradicional. Somos una plataforma de intercambio multiparticipante con compensaciones económicas automáticas. Mientras que Wallapop/Vinted son 1:1 compra/venta, nosotros permitimos intercambios complejos entre múltiples personas en una sola transacción.",
                "category": "Differentiation",
                "confidence": "High"
            },
            {
                "question": "¿Cómo resuelven el problema de confianza entre usuarios?",
                "answer": "Triple sistema: 1) Escrow que retiene pagos hasta confirmación, 2) Seguro opcional para artículos de valor, 3) Sistema de verificación por pasos. Además, nuestro sistema de reputación con 4 niveles (Novato → Elite) incentiva comportamiento positivo.",
                "category": "Trust & Safety",
                "confidence": "High"
            },
            {
                "question": "¿Qué pasa si un usuario desiste a las 23 horas?",
                "answer": "Tenemos un fondo de garantía del 0.1% de todas las transacciones que cubre estas situaciones. El usuario que desiste pierde reputación (-30 puntos) y puede quedar excluido de futuras ruedas. La mercancía puede ser readjudicada o Treqe la retiene para subasta.",
                "category": "Operations",
                "confidence": "Medium"
            },
            {
                "question": "¿Cómo escalan técnicamente?",
                "answer": "Arquitectura microservicios diseñada para escalar horizontalmente. Comenzamos con stack simple (Python/FastAPI, PostgreSQL, Redis) que podemos escalar a Kubernetes cuando sea necesario. Hemos diseñado para 10,000 usuarios concurrentes desde el inicio.",
                "category": "Technology",
                "confidence": "High"
            },
            {
                "question": "¿Cuál es su CAC y LTV estimado?",
                "answer": "CAC estimado: €25 (canales orgánicos + SEM segmentado). LTV estimado: €180 basado en 2 transacciones/mes × €90 valor promedio × 12 meses × 8.3% comisión promedio. Ratio LTV:CAC de 7.2:1, muy saludable.",
                "category": "Financials",
                "confidence": "Medium"
            },
            {
                "question": "¿Quiénes son sus competidores directos?",
                "answer": "No hay competidores directos en intercambio multiparticipante. Competidores indirectos: Wallapop (compra/venta 1:1), grupos de Facebook (informales, sin protección), plataformas de trueque tradicional (sin compensaciones económicas). Nuestro modelo es único en el mercado.",
                "category": "Competition",
                "confidence": "High"
            },
            {
                "question": "¿Qué validación tienen del mercado?",
                "answer": "1) Análisis de 3 problemas críticos con soluciones validadas por usuarios, 2) Sistema de scoring probado y aceptado, 3) Arquitectura técnica diseñada por expertos, 4) Feedback de 50+ usuarios potenciales en grupos focales.",
                "category": "Validation",
                "confidence": "High"
            },
            {
                "question": "¿Cómo monetizan además de las comisiones?",
                "answer": "1) Comisiones escalonadas (0.8-1.0%), 2) Servicios premium (logística garantizada, verificación avanzada), 3) Publicidad segmentada para marcas relacionadas, 4) Data insights anonimizados para estudios de mercado.",
                "category": "Business Model",
                "confidence": "High"
            },
            {
                "question": "¿Cuál es su estrategia de adquisición de usuarios?",
                "answer": "Fase 1: Comunidades nicho (coleccionistas, gamers, padres). Fase 2: SEM segmentado por intereses. Fase 3: Referral program con incentivos. Fase 4: Partnerships con marcas de segunda mano. Meta: 1,000 usuarios activos en 6 meses.",
                "category": "Growth",
                "confidence": "Medium"
            },
            {
                "question": "¿Qué necesitan para alcanzar el punto de equilibrio?",
                "answer": "18 meses y €250,000 de inversión. Con 5,000 usuarios activos generando €500,000 ARR y márgenes del 65%, alcanzamos punto de equilibrio. La inversión acelera este timeline en 6-9 meses.",
                "category": "Financials",
                "confidence": "Medium"
            }
        ]
        
        # Organize by category
        categories = {}
        for qa_item in questions:
            category = qa_item["category"]
            if category not in categories:
                categories[category] = []
            categories[category].append(qa_item)
        
        # Write organized Q&A
        for category, items in categories.items():
            qa += f"## {category}\n\n"
            for i, item in enumerate(items, 1):
                qa += f"### Q{i}: {item['question']}\n"
                qa += f"**Confidence:** {item['confidence']}\n\n"
                qa += f"{item['answer']}\n\n"
        
        # Add handling difficult questions
        qa += "# Handling Difficult Questions\n\n"
        qa += "## If You Don't Know:\n"
        qa += "- \"That's an excellent question. We're currently researching that and I'd be happy to follow up with our findings.\"\n"
        qa += "- \"We haven't finalized that aspect yet, but our approach will be...\"\n"
        qa += "- \"Let me take note of that and get back to you with a detailed answer.\"\n\n"
        
        qa += "## If Question is Off-Topic:\n"
        qa += "- \"That's an interesting point, though slightly outside our current focus. What I can tell you about our core model is...\"\n"
        qa += "- \"While that's important, our immediate priority is...\"\n\n"
        
        qa += "## If Question is Critical/Negative:\n"
        qa += "- \"I appreciate you raising that concern. Here's how we're addressing it...\"\n"
        qa += "- \"That's a valid point, and here are the safeguards we've built in...\"\n"
        qa += "- \"We recognize that challenge, which is why we've designed...\"\n"
        
        return qa
    
    def generate_solution(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate pitch deck solution based on analysis"""
        # Analyze pitch needs
        needs = self.analyze_pitch_needs(
            audience=analysis.get("audience", "investors"),
            duration=analysis.get("duration_minutes", 10)
        )
        
        # Generate structure
        structure = self.generate_pitch_structure(needs)
        
        # Calculate total time
        total_time = sum(slide["estimated_time"] for slide in structure)
        
        return {
            "solution_type": "pitch_deck",
            "audience": needs["audience"],
            "duration_minutes": needs["duration_minutes"],
            "slide_count": len(structure),
            "total_presentation_time": total_time,
            "structure": structure,
            "design_principles": self.design_principles,
            "focus_areas": needs["focus_areas"],
            "files_to_create": [
                "pitch_deck_structure.json",
                "pitch_deck_content.md",
                "speaker_notes.md",
                "investor_qa.md"
            ],
            "next_steps": [
                "Convert markdown to PowerPoint template",
                "Create visual assets (charts, diagrams)",
                "Practice presentation with timer",
                "Schedule dry run with team"
            ]
        }
    
    def create_outputs(self, solution: Dict[str, Any]) -> List[Path]:
        """Create actual output files"""
        outputs = []
        
        # Create base outputs (README, metadata)
        base_outputs = super().create_outputs(solution)
        outputs.extend(base_outputs)
        
        # Create pitch-specific outputs
        if "structure" in solution:
            output_dir = self.create_pitch_deck_document(solution["structure"])
            outputs.append(output_dir)
        
        # Log this session
        session_data = {
            "action": "pitch_deck_creation",
            "audience": solution.get("audience", "unknown"),
            "slide_count": solution.get("slide_count", 0),
            "duration_minutes": solution.get("duration_minutes", 0),
            "files_created": [str(p) for p in outputs]
        }
        
        self.log_session(session_data)
        
        return outputs
    
    def run_demo(self) -> bool:
        """Run a demonstration of Pitch Designer capabilities"""
        print(f"\n{'='*60}")
        print(f"🎨 DEMO: Pitch Designer Sub-Agent")
        print(f"{'='*60}")
        
        # Show capabilities
        print(f"\n🔧 Capabilities:")
        for i, capability in enumerate(self.get_capabilities(), 1):
            print(f"  {i}. {capability}")
        
        # Show integration
        print(f"\n🔄 Ecosystem Integration:")
        for system, integrations in self.get_integration_points().items():
            print(f"  • {system}: {', '.join(integrations[:2])}...")
        
        # Analyze needs
        print(f"\n📊 Analyzing pitch needs for investors (10-minute pitch)...")
        needs = self.analyze_pitch_needs(audience="investors", duration=10)
        print(f"  • Audience: {needs['audience']}")
        print(f"  • Duration: {needs['duration_minutes']} minutes")
        print(f"  • Recommended slides: {needs['recommended_slides']}")
        print(f"  • Focus areas: {', '.join(needs['focus_areas'][:3])}...")
        
        # Generate structure
        print(f"\n🏗️ Generating pitch structure...")
        structure = self.generate_pitch_structure(needs)
        print(f"  • Slides created: {len(structure)}")
        print(f"  • Total time: {sum(slide['estimated_time'] for slide in structure)} seconds")
        
        # Show sample slides
        print(f"\n📄 Sample Slides:")
        for i, slide in enumerate(structure[:3], 1):  # Show first 3 slides
            print(f"  {i}. Slide {slide['slide_number']}: {slide['title']}")
            print(f"     Content: {slide['content_elements'][0][:50]}...")
        
        # Create outputs
        print(f"\n💾 Creating output files...")
        solution = self.generate_solution({"audience": "investors", "duration_minutes": 10})
        outputs = self.create_outputs(solution)
        
        print(f"\n✅ Demo completed successfully!")
        print(f"📁 Outputs created in: {self.agent_dir}")
        print(f"📄 Files created:")
        for output in outputs[-4:]:  # Show last 4 files (pitch-specific)
            print(f"  • {output.name}")
        
        # Show status
        status = self.get_status()
        print(f"\n📊 Agent Status:")
        print(f"  • Outputs: {status['outputs_count']} files")
        print(f"  • Sessions: {status['sessions_count']} logged")
        print(f"  • Status: {status['status']}")
        
        return True


# Main execution
if __name__ == "__main__":
    # Create and run Pitch Designer agent
    pitch_designer = PitchDesignerAgent()
    
    # Run demo
    success = pitch_designer.run_demo()
    
    if success:
        print(f"\n{'='*60}")
        print(f"🎯 Pitch Designer ready for Treqe presentation preparation!")
        print(f"{'='*60}")
        print(f"\nNext steps:")
        print(f"1. Review generated files in: {pitch_designer.agent_dir}/outputs")
        print(f"2. Convert markdown to PowerPoint template")
        print(f"3. Create visual assets based on design guidelines")
        print(f"4. Practice presentation using speaker notes")
        print(f"5. Prepare for investor Q&A using Q&A document")
    else:
        print(f"\n❌ Demo failed. Check logs for details.")