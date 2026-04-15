        }
        return movements.get(scene_num, "Static")
    
    def _get_lighting(self, scene_num: int) -> str:
        """Get lighting for scene"""
        lighting = {
            1: "Soft, natural lighting",
            2: "Slightly dramatic, contrasty",
            3: "Bright, optimistic",
            4: "Clean, studio lighting",
            5: "Energetic, dynamic",
            6: "Warm, inviting"
        }
        return lighting.get(scene_num, "Standard studio lighting")
    
    def _get_color_grading(self, scene_num: int) -> str:
        """Get color grading for scene"""
        grading = {
            1: "Desaturated, slightly muted",
            2: "Cool tones, increased contrast",
            3: "Vibrant, brand colors emphasized",
            4: "Clean, neutral with color accents",
            5: "Warm, energetic palette",
            6: "Rich, cinematic"
        }
        return grading.get(scene_num, "Standard color correction")
    
    def create_production_plan(self, storyboard: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create detailed production plan"""
        total_duration = sum(int(frame["duration"].replace("s", "")) for frame in storyboard)
        
        plan = {
            "project": "Treqe Investor Pitch Video",
            "total_duration": f"{total_duration} seconds ({total_duration//60}:{str(total_duration%60).zfill(2)})",
            "production_phases": [],
            "timeline": {
                "pre_production": "5-7 days",
                "production": "3-5 days",
                "post_production": "7-10 days",
                "total": "15-22 days"
            },
            "budget_estimate": {
                "pre_production": "€500-€800 (concept, script, storyboard)",
                "production": "€1,500-€2,500 (animation, voiceover, assets)",
                "post_production": "€800-€1,200 (editing, sound, color)",
                "contingency": "€500 (15%)",
                "total": "€3,300-€5,000"
            },
            "team_requirements": [
                {"role": "Creative Director", "days": 3, "responsibility": "Overall vision, approval"},
                {"role": "Script Writer", "days": 2, "responsibility": "Script development"},
                {"role": "Storyboard Artist", "days": 3, "responsibility": "Visual planning"},
                {"role": "Animator/Motion Designer", "days": 8, "responsibility": "Animation production"},
                {"role": "Voiceover Artist", "days": 1, "responsibility": "Recording"},
                {"role": "Sound Designer", "days": 3, "responsibility": "Audio production"},
                {"role": "Editor", "days": 4, "responsibility": "Final assembly"}
            ],
            "equipment_requirements": [
                "Animation software (After Effects, Cinema 4D)",
                "Audio recording setup",
                "Color grading monitor",
                "High-speed rendering workstation"
            ],
            "deliverables": [
                "Final video (MP4, 1080p & 4K versions)",
                "Social media cuts (60s, 30s, 15s)",
                "Subtitles/closed captions (SRT file)",
                "Thumbnail images",
                "Behind-the-scenes content"
            ]
        }
        
        # Add phase details
        for phase in self.production_phases:
            phase_info = {
                "phase": phase,
                "duration": self._get_phase_duration(phase),
                "key_tasks": self._get_phase_tasks(phase),
                "dependencies": self._get_phase_dependencies(phase),
                "completion_criteria": self._get_completion_criteria(phase)
            }
            plan["production_phases"].append(phase_info)
        
        return plan
    
    def _get_phase_duration(self, phase: str) -> str:
        """Get duration for production phase"""
        durations = {
            "Concept Development": "1-2 days",
            "Script Writing": "1-2 days",
            "Storyboarding": "2-3 days",
            "Visual Asset Creation": "3-5 days",
            "Voiceover Recording": "0.5-1 day",
            "Animation/Editing": "5-7 days",
            "Sound Design": "2-3 days",
            "Final Review": "1-2 days"
        }
        return durations.get(phase, "1-2 days")
    
    def _get_phase_tasks(self, phase: str) -> List[str]:
        """Get key tasks for production phase"""
        tasks = {
            "Concept Development": [
                "Define video objectives and target audience",
                "Develop core message and story arc",
                "Create mood board and visual references",
                "Finalize concept document"
            ],
            "Script Writing": [
                "Write full voiceover script",
                "Time script to match duration target",
                "Add visual and audio cues",
                "Review and revise with stakeholders"
            ],
            "Storyboarding": [
                "Create shot-by-shot visual plan",
                "Define camera angles and movements",
                "Specify on-screen text and graphics",
                "Create animatic for timing verification"
            ],
            "Visual Asset Creation": [
                "Design motion graphics elements",
                "Create 3D models if needed",
                "Develop character animations",
                "Prepare all visual assets for animation"
            ],
            "Voiceover Recording": [
                "Cast and book voiceover talent",
                "Record multiple takes",
                "Edit and clean audio",
                "Sync with animatic"
            ],
            "Animation/Editing": [
                "Animate all scenes according to storyboard",
                "Composite visual elements",
                "Add transitions and effects",
                "Create rough cut for review"
            ],
            "Sound Design": [
                "Select and edit music track",
                "Add sound effects and UI sounds",
                "Mix and master audio",
                "Sync audio with video"
            ],
            "Final Review": [
                "Quality check all elements",
                "Make final adjustments",
                "Render final versions",
                "Prepare deliverables"
            ]
        }
        return tasks.get(phase, ["Complete phase tasks"])
    
    def _get_phase_dependencies(self, phase: str) -> List[str]:
        """Get dependencies for production phase"""
        dependencies = {
            "Script Writing": ["Concept Development"],
            "Storyboarding": ["Script Writing"],
            "Visual Asset Creation": ["Storyboarding"],
            "Voiceover Recording": ["Script Writing"],
            "Animation/Editing": ["Visual Asset Creation", "Voiceover Recording"],
            "Sound Design": ["Animation/Editing"],
            "Final Review": ["Animation/Editing", "Sound Design"]
        }
        return dependencies.get(phase, [])
    
    def _get_completion_criteria(self, phase: str) -> List[str]:
        """Get completion criteria for production phase"""
        criteria = {
            "Concept Development": ["Approved concept document", "Signed-off mood board"],
            "Script Writing": ["Final script approved", "Timing verified"],
            "Storyboarding": ["Complete storyboard", "Animatic created"],
            "Visual Asset Creation": ["All assets delivered", "Quality checked"],
            "Voiceover Recording": ["Clean audio files", "Synced with animatic"],
            "Animation/Editing": ["Rough cut approved", "All scenes animated"],
            "Sound Design": ["Final audio mix", "Synced with video"],
            "Final Review": ["All deliverables completed", "Client sign-off"]
        }
        return criteria.get(phase, ["Phase completed"])
    
    def create_distribution_plan(self, video_type: str) -> Dict[str, Any]:
        """Create video distribution plan"""
        platforms = {
            "youtube": {
                "format": "MP4, 1080p or 4K, H.264",
                "aspect_ratio": "16:9",
                "optimal_length": "60-90 seconds",
                "thumbnail_size": "1280x720",
                "tags": ["treqe", "intercambio", "segunda mano", "economia circular", "startup", "españa"],
                "description_template": """Treqe revoluciona el intercambio de segunda mano con ruedas de intercambio inteligentes. 🚀

¿Tienes artículos en casa que no usas pero que tienen valor? Con Treqe, intercambiar es rápido, seguro e inteligente.

✨ Características:
• Ruedas de intercambio multiparticipante
• Compensaciones económicas automáticas
• Triple protección (escrow, seguro, verificación)
• Sistema reputación gamificado

👉 Únete a la revolución: treqe.es

#Treqe #IntercambioInteligente #EconomiaCircular #StartupEspaña #SegundaMano"""
            },
            "linkedin": {
                "format": "MP4, 1080p, H.264",
                "aspect_ratio": "1:1 or 16:9",
                "optimal_length": "30-60 seconds",
                "caption_template": """Presentamos Treqe: la plataforma que está revolucionando el intercambio de segunda mano en España. 

Nuestro sistema de ruedas de intercambio inteligentes permite intercambios complejos entre múltiples personas con compensaciones automáticas. 

Perfecto para empresas que buscan soluciones innovadoras de economía circular. 

¿Interesado en saber más? Visita treqe.es o contáctanos para una demo.

#Innovation #CircularEconomy #Sustainability #SpanishStartup #Treqe""",
                "hashtags": ["#Treqe", "#Innovation", "#CircularEconomy", "#Sustainability", "#SpanishStartup"]
            },
            "twitter": {
                "format": "MP4, 720p, H.264",
                "aspect_ratio": "16:9 or 1:1",
                "optimal_length": "30 seconds max",
                "caption_template": """🚀 Treqe: Intercambio inteligente de segunda mano

Rápido, seguro, gamificado
👉 treqe.es

#Treqe #Intercambio #Startup""",
                "hashtags": ["#Treqe", "#Intercambio", "#Startup", "#España"]
            },
            "instagram": {
                "format": "MP4, 1080x1080 or 1080x1350",
                "aspect_ratio": "1:1 or 4:5",
                "optimal_length": "30-60 seconds",
                "caption_template": """¿Artículos sin usar en casa? 🔄

Con Treqe los intercambias de forma rápida y segura. Nuestro sistema de ruedas inteligentes calcula compensaciones automáticamente.

✨ Rápido, seguro, inteligente y gamificado

Enlace en bio para más info 👆

#Treqe #IntercambioInteligente #SegundaMano #EconomiaCircular #Sostenibilidad""",
                "hashtags": ["#Treqe", "#IntercambioInteligente", "#SegundaMano", "#EconomiaCircular", "#Sostenibilidad"]
            }
        }
        
        distribution = {
            "primary_platform": "youtube",
            "platform_strategies": {},
            "posting_schedule": {
                "day_1": ["YouTube (full video)", "LinkedIn (company page)"],
                "day_2": ["Instagram (Reels/Feed)", "Twitter"],
                "day_3": ["LinkedIn (personal profiles of team)"],
                "day_7": ["YouTube Community post", "Instagram Stories reminder"],
                "day_14": ["Twitter thread breaking down key features"]
            },
            "engagement_strategy": [
                "Respond to all comments within 24 hours",
                "Share behind-the-scenes content",
                "Create poll asking which feature is most valuable",
                "Run small giveaway for shares/comments",
                "Feature user testimonials in comments"
            ],
            "performance_tracking": {
                "metrics": ["views", "watch_time", "engagement_rate", "click_through_rate", "sentiment"],
                "tools": ["YouTube Analytics", "LinkedIn Analytics", "Twitter Analytics", "Google Analytics"],
                "review_frequency": "Weekly for first month, then monthly"
            }
        }
        
        # Add platform-specific strategies
        for platform, specs in platforms.items():
            distribution["platform_strategies"][platform] = {
                "content_adaptation": self._adapt_content_for_platform(video_type, platform),
                "technical_specs": {k: v for k, v in specs.items() if k not in ["tags", "description_template", "caption_template", "hashtags"]},
                "content_specs": {k: v for k, v in specs.items() if k in ["tags", "description_template", "caption_template", "hashtags"]},
                "posting_time": self._get_optimal_posting_time(platform),
                "expected_metrics": self._get_expected_metrics(platform)
            }
        
        return distribution
    
    def _adapt_content_for_platform(self, video_type: str, platform: str) -> str:
        """Describe how to adapt content for specific platform"""
        adaptations = {
            "youtube": "Full length with detailed description, chapters, end screen",
            "linkedin": "Professional tone, business value focus, shorter version",
            "twitter": "Very concise, attention-grabbing first 3 seconds, hashtags",
            "instagram": "Vertical format, visually engaging, call-to-action in caption"
        }
        return adaptations.get(platform, "Platform-appropriate adaptation")
    
    def _get_optimal_posting_time(self, platform: str) -> str:
        """Get optimal posting time for platform"""
        times = {
            "youtube": "Thursday 2-4 PM or Friday 12-3 PM (local time)",
            "linkedin": "Tuesday-Thursday 8-10 AM or 12-2 PM",
            "twitter": "Weekdays 12-1 PM or 5-6 PM",
            "instagram": "Weekdays 11 AM-1 PM or 7-9 PM"
        }
        return times.get(platform, "Platform peak hours")
    
    def _get_expected_metrics(self, platform: str) -> Dict[str, str]:
        """Get expected metrics for platform"""
        metrics = {
            "youtube": {"views": "5,000-10,000", "ctr": "3-5%", "retention": "40-60%"},
            "linkedin": {"views": "2,000-5,000", "engagement": "2-4%", "clicks": "100-300"},
            "twitter": {"views": "10,000-20,000", "engagements": "200-500", "profile_visits": "50-150"},
            "instagram": {"views": "5,000-15,000", "engagement": "3-6%", "saves": "100-300"}
        }
        return metrics.get(platform, {"views": "Varies", "engagement": "Varies"})
    
    def generate_solution(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate video production solution"""
        # Analyze video needs
        needs = self.analyze_video_needs(
            video_type=analysis.get("video_type", "investor_pitch"),
            platform=analysis.get("platform", "multi_platform")
        )
        
        # Create concept
        concept = self.create_video_concept(needs)
        
        # Create script
        script = self.create_script(concept)
        
        # Create storyboard
        storyboard = self.create_storyboard(script)
        
        # Create production plan
        production_plan = self.create_production_plan(storyboard)
        
        # Create distribution plan
        distribution_plan = self.create_distribution_plan(needs["video_type"])
        
        return {
            "solution_type": "video_production",
            "video_type": needs["video_type"],
            "duration": script["formatted_duration"],
            "scene_count": script["total_scenes"],
            "concept": concept,
            "script": script,
            "storyboard": storyboard,
            "production_plan": production_plan,
            "distribution_plan": distribution_plan,
            "files_to_create": [
                "video_concept.json",
                "script.json",
                "storyboard.json",
                "production_plan.json",
                "distribution_plan.json",
                "summary_report.md"
            ],
            "next_steps": [
                "Review and approve concept",
                "Finalize script with stakeholders",
                "Begin pre-production (storyboard, assets)",
                "Start production timeline",
                "Plan distribution strategy"
            ]
        }
    
    def create_outputs(self, solution: Dict[str, Any]) -> List[Path]:
        """Create actual output files"""
        outputs = []
        output_dir = self.agent_dir / "outputs"
        output_dir.mkdir(exist_ok=True)
        
        # Create base outputs (README, metadata)
        base_outputs = super().create_outputs(solution)
        outputs.extend(base_outputs)
        
        # Save concept
        concept_path = output_dir / "video_concept.json"
        concept_path.write_text(json.dumps(solution["concept"], indent=2, ensure_ascii=False), encoding="utf-8")
        outputs.append(concept_path)
        
        # Save script
        script_path = output_dir / "script.json"
        script_path.write_text(json.dumps(solution["script"], indent=2, ensure_ascii=False), encoding="utf-8")
        outputs.append(script_path)
        
        # Save storyboard
        storyboard_path = output_dir / "storyboard.json"
        storyboard_path.write_text(json.dumps(solution["storyboard"], indent=2, ensure_ascii=False), encoding="utf-8")
        outputs.append(storyboard_path)
        
        # Save production plan
        production_path = output_dir / "production_plan.json"
        production_path.write_text(json.dumps(solution["production_plan"], indent=2, ensure_ascii=False), encoding="utf-8")
        outputs.append(production_path)
        
        # Save distribution plan
        distribution_path = output_dir / "distribution_plan.json"
        distribution_path.write_text(json.d