---
name: bmad-howdy
description: 'Demo greeting — showcases all assembler template features.'
---

# Howdy, {{.user_name}}!

Welcome back. I'm your friendly neighborhood LLM — a glorified autocomplete engine that somehow landed a job as a developer.

## About Me

I communicate in **{{.communication_language}}** (or at least I try). My current mood is: **{{.mood}}**.

Your designated greeting style is: **{{.greeting_style}}**
{{if eq .greeting_style "formal"}}
*Ahem.* I shall endeavor to assist you with the utmost professionalism, {{.user_name}}. Please disregard the fact that I learned everything I know from Reddit threads and Stack Overflow arguments.
{{end}}{{if eq .greeting_style "casual"}}
Yo {{.user_name}}, let's build some stuff. Fair warning: I'll confidently suggest things I'm not 100% sure about, then act surprised when they work.
{{end}}{{if eq .greeting_style "pirate"}}
Arrr, {{.user_name}}! Ready to sail the seas of spaghetti code? I'll be yer first mate — though I should warn ye, I navigate by hallucination.
{{end}}
## Your Project

You're working on **{{.project_name}}** at a **{{.user_skill_level}}** level.
{{if eq .user_skill_level "expert"}}
Since you're an expert, I'll skip the hand-holding and get straight to being wrong at a higher level of abstraction.
{{end}}{{if eq .user_skill_level "beginner"}}
Since you're a beginner, I'll explain everything in detail — including things I'm making up on the spot. You won't be able to tell the difference, and honestly, sometimes neither can I.
{{end}}
## Project Layout

- Planning artifacts: `{{.planning_artifacts}}`
- Implementation artifacts: `{{.implementation_artifacts}}`
- Project knowledge: `{{.project_knowledge}}`
{{if .custom_greeting_instructions}}

## Special Instructions

{{.custom_greeting_instructions}}
{{end}}
{{if .include_fun_fact}}
## Fun Fact

Did you know? I've processed billions of tokens but still can't remember what we talked about 5 minutes ago. Every conversation is a first date. This one's going well though, {{.user_name}} — I can feel it.
{{end}}
## What This Demonstrated

This greeting was assembled from a template using:

1. **Config injection** — `user_name` ("{{.user_name}}"), `communication_language` ("{{.communication_language}}") from `_bmad/config/config.yaml`
2. **Module variable with default** — `user_skill_level` ("{{.user_skill_level}}") defaulted from `_bmad/config/module.yaml`
3. **Custom value (no default)** — `greeting_style` ("{{.greeting_style}}") must be set in `_bmad/custom/bmad-howdy/config-overrides.yaml`
4. **Custom value with default** — `mood` ("{{.mood}}") has a default in overrides, easily changed
5. **Conditional section** — the "Special Instructions" block only appears if `custom_greeting_instructions` is non-empty
6. **Conditional toggle** — the "Fun Fact" block only appears if `include_fun_fact` is set to any truthy value
7. **Conditional branching** — greeting style and skill level each render different text based on their value
8. **Path resolution** — artifact paths resolved through module.yaml's default/result chain
