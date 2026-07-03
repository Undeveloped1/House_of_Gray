---
name: ai-companion-product-design
category: product-design
description: Design principles, systems, and architecture for sophisticated AI companion and digital relationship simulation products.
---

# AI Companion Product Design

## Overview
This skill covers the design of sophisticated AI companion / digital relationship simulation products. It focuses on systems that prioritize emotional depth, meaningful progression, persistent memory, and ethical considerations over instant gratification.

## Core Principles
- 60% emotional/character depth, 40% erotic content
- Hard-coded progression that cannot be easily bypassed
- Per-relationship memory isolation (no memory transfer between companions)
- Self-hosted architecture with user data ownership
- Nuanced intimacy preference tracking (frequency + emotional context)

## Key Design Areas
- Progression systems with specific unlock criteria
- Memory architecture (User Corpus, RAG, per-relationship storage)
- Communication layers (multi-channel, preference adaptation)
- Intimacy preference systems
- Technical considerations for self-hosted deployments

## Progression System Design
- Each companion has 4–5 stages
- Unlock criteria include: days messaged, affection score, references to past information, emotional conversations
- High-difficulty companions (Ice Queen, Faith-Based) have significant long-term rewards
- No memory transfer between relationships

## Memory Architecture
- Five core categories: People, Places, Things, Pets, Preferences
- Hybrid real-time + cron-driven updates
- Monthly consolidation with compressed output
- Hidden User Corpus completion system

## Intimacy Preference Tracking
- Tracks nuanced preferences (not just yes/no)
- Records frequency and emotional context
- Prevents immersion-breaking suggestions
- Learned through trial and error

## Communication Layer
- Multi-channel support (text, email, photos, voice)
- Companions have preferred channels with bonuses
- System adapts to user communication habits

## Anti-Patterns
- Do not allow memory transfer between relationships
- Do not make progression easily bypassable
- Do not store raw long-term conversation logs without consolidation
- Avoid making all companions sexually available from the start

## References
- `references/progression-tables.md` — Full 10-archetype progression tables with unlock criteria
- `references/memory-architecture.md` — Detailed memory system design
- `references/technical-considerations.md` — Self-hosted technical requirements

## Notes
This skill was seeded from an extended design session focused on creating a high-quality, ethical, and engaging digital relationship simulation product.