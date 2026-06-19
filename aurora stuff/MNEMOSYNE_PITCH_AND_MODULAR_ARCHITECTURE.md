# Mnemosyne Pitch and Modular Soul Architecture

## Purpose

This document replaces the older high-level pitch with a cleaner, more defensible product description and a scalable package architecture for future development.

Mnemosyne should be positioned as a local, open-source narrator engine for persistent AI roleplay and long-form story creation. The core product thesis is simple:

> The LLM should not be the database. The LLM should be the writer.

Mnemosyne manages memory, continuity, state, and compression outside the model. The model receives a curated context brief and produces narration.

---

## Improved Pitch

**Mnemosyne is an open-source narrator engine for persistent AI roleplay and long-form story creation.**

Most AI roleplay fails because the model is expected to be the character, the memory, the world tracker, and the writer all at once. Mnemosyne separates those jobs. The LLM acts as the narrator. The engine manages the character's Soul.

A Soul is a portable, structured character state file that tracks identity, relationships, memories, emotional patterns, and long-term development. A separate World Log tracks the scene, plot, location, time, and shared events. Before each turn, Mnemosyne compiles only the relevant pieces into a compact context brief, keeping token use lean while preserving continuity across long campaigns.

Characters remember what matters, forget what fades, and change at a believable pace. Stories can run for dozens or hundreds of sessions without collapsing into contradiction or emotional reset.

Mnemosyne runs locally, is AGPL open source, and lets users bring their own model provider. It is built for roleplayers, worldbuilders, and writers who want AI stories with memory, consequence, and character growth.

---

## Short Landing Page Version

**Roleplay that remembers.**

Mnemosyne is a local, open-source engine for persistent AI roleplay. Instead of making the AI pretend to be the character and hoping it remembers, Mnemosyne separates the narrator from the character's persistent Soul.

The narrator writes the scene.  
The Soul remembers what matters.  
The World Log tracks what is happening.  
The engine decides what context the model actually needs.

This creates long-running AI stories with continuity, emotional consequence, and characters that grow over time.

---

## One-Sentence Pitch

Mnemosyne is a local, open-source narrator engine that gives AI roleplay persistent memory, compressed world tracking, and character growth through portable Soul files.

---

## Tagline Options

1. **Remember who you are.**
2. **Roleplay that remembers.**
3. **The narrator writes. The Soul remembers.**
4. **Persistent Souls for long-running AI stories.**
5. **AI roleplay with memory, consequence, and character growth.**
6. **Stop chatting. Start remembering.**
7. **A memory engine for living stories.**

Recommended default:

> **The narrator writes. The Soul remembers.**

---

## Public Positioning

Mnemosyne should not be pitched as a narrow chatbot replacement. It should be pitched as a **state engine for long-running AI stories**.

Good public framing:

- Local-first
- Open source
- Bring your own model provider
- Persistent character memory
- World-state compression
- Long-form roleplay
- Novel and campaign export potential
- Configurable boundaries and genre extensions

Avoid public framing that makes the project sound like only an adult chatbot, a prompt jailbreak tool, or a narrow replacement for one specific platform. Mnemosyne can support many genres, but the core repo should remain broadly useful and defensible.

---

## Technical Pitch

Mnemosyne is a local narrator and GM engine for AI-assisted roleplay, built around externalized memory and structured state.

The LLM does not need to see the full chat history every turn. Instead, Mnemosyne stores character and world state outside the model, then compiles a compact briefing before each generation.

The core loop is:

```text
User Message
    |
    v
State Engine compiles relevant context
    |
    v
Narrator Prompt + Soul Summary + World Log + Recent Chat
    |
    v
LLM generates narration and hidden patch
    |
    v
Engine parses and validates patch
    |
    v
Soul, World Log, memory, and conversation state update
    |
    v
Clean narration is shown to user
```

This makes Mnemosyne closer to an application-level memory manager than a normal chatbot wrapper.

---

## Core Design Thesis

### Old approach

```text
System prompt
Character card
Full chat history
User message
```

This grows linearly with session length. It wastes tokens, dilutes attention, and eventually causes contradiction or forgetting.

### Mnemosyne approach

```text
System prompt
Character card
Compiled Soul summary
Compiled World Log
Relevant retrieved memories
Last few messages
User message
```

This keeps token use flatter. The model receives a curated briefing instead of an entire transcript.

---

## System Split

Mnemosyne should be organized around three major runtime systems.

| System | Purpose | Update Frequency | Prompt Role |
|---|---|---:|---|
| Soul | Character identity, relationships, emotional state, long-term memory | Every turn | Keeps character consistent |
| World Log | Location, plot, key objects, time, shared events | Scene shifts or every 3 to 5 turns | Keeps story coherent |
| Recent Chat | Immediate dialogue and narration continuity | Every turn | Keeps local flow natural |

A fourth system should be added as the project matures:

| System | Purpose | Update Frequency | Prompt Role |
|---|---|---:|---|
| Retrieval Layer | Pulls relevant older facts, memories, objects, and relationships | Every turn | Prevents forgotten callbacks |

---

## Why This Matters

The goal is not to make the LLM permanently learn. The goal is to build an external memory and state-management layer that keeps the working context clean.

Mnemosyne should treat the LLM as a narrator that receives a briefing. The engine is responsible for memory, state, retrieval, compression, decay, and validation.

This improves:

- Long-session continuity
- Character consistency
- Cost control
- Context-window efficiency
- Emotional pacing
- Plot tracking
- Multi-character scalability
- Future manuscript export

---

## Memory Design

Mnemosyne memory should be structured into tiers.

| Tier | Description | Example |
|---|---|---|
| Core memory | High-salience long-term memories that shape identity | A betrayal, promise, rescue, loss, oath |
| Recent memory | Detailed short-term events that may decay | Last few important exchanges |
| Schema memory | Compressed repeated patterns | Prison routine, training cycle, daily ritual |
| Retrieved memory | Relevant old memory selected for current context | Callback to a promise made 80 turns ago |
| World memory | Shared plot and setting facts | Escaped the city, obtained the key, met the rival |

Memory should survive when it is:

- Emotionally intense
- Repeated
- Important to identity
- Important to relationship
- Important to active plot
- Recently retrieved
- Connected to the current scene

Memory should decay when it is:

- Ordinary
- Unreinforced
- Not plot-relevant
- Not relationship-relevant
- Not retrieved for a long time

---

## Patch-Based Updates

The LLM should not directly rewrite the whole Soul.

Bad pattern:

```text
LLM outputs complete Soul file
Engine accepts everything
```

Good pattern:

```text
LLM outputs small hidden patch
Engine validates fields
Engine clamps values
Engine applies deterministic update rules
Engine records audit metadata
```

Example patch shape:

```json
{
  "soul_patch": {
    "relationship_delta": {
      "user": {
        "trust": 2,
        "fear": -1
      }
    },
    "new_memory": {
      "content": "The character felt safer after the user kept a promise.",
      "tag": "trust_building",
      "salience_hint": 72
    }
  },
  "world_patch": {
    "location": "abandoned station",
    "recent_event": "They moved deeper into the station after hearing footsteps.",
    "active_plot": "find a safe exit"
  }
}
```

The engine should treat LLM patches as suggestions, not authority.

---

## Token Budget Strategy

Mnemosyne should not aim for the smallest possible prompt. It should aim for the smallest sufficient prompt.

A practical target:

| Context Block | Target Tokens |
|---|---:|
| System prompt | 400 to 900 |
| Character card | 200 to 500 |
| Soul summary | 250 to 500 |
| World Log | 250 to 500 |
| Retrieved memories | 300 to 800 |
| Recent chat | 500 to 1,200 |
| User message | Variable |

Target total:

```text
2,000 to 4,500 tokens per turn
```

This is small enough to stay efficient but large enough to preserve story texture.

---

## Dynamic Context Allocation

Different scenes need different context.

| Scene Type | More Context For | Less Context For |
|---|---|---|
| Combat | Body state, injuries, location, objects | Long emotional reflection |
| Emotional scene | Relationship memories, recent dialogue, Soul state | Inventory and location details |
| Investigation | World Log, clues, objects, prior discoveries | Body state unless relevant |
| Travel | Location, time, objectives, companions | Minor old memories |
| Political scene | Factions, promises, leverage, relationships | Sensory details unless relevant |
| Recovery scene | Body state, comfort cues, trust, trauma state | Combat details |

The context compiler should allocate tokens dynamically based on scene type and current user message.

---

## Modular Soul Architecture

Splitting the Soul into multiple files is not a bad idea. It is likely the correct direction once the system grows beyond MVP.

The rule should be:

> Many modules internally, one Soul package externally, one compiled context brief sent to the LLM.

---

## Recommended Package Format

During active play, the source of truth should be database-backed runtime state.

For sharing and backup, export a portable package:

```text
Aurora.soul.mne
```

A `.mne` file can be a zipped bundle containing multiple JSON modules.

Suggested layout:

```text
aurora.soul/
 ├─ manifest.json
 ├─ identity.json
 ├─ psyche.json
 ├─ relationships.json
 ├─ memory.json
 ├─ world_links.json
 ├─ body_state.json
 ├─ sensory_state.json
 ├─ boundaries.json
 ├─ provider_notes.json
 └─ audit.json
```

Externally, users see one file. Internally, developers and modders get clean modules.

---

## Module Responsibilities

### `manifest.json`

Stores package identity and versioning.

```json
{
  "package_id": "pkg_aurora_001",
  "character_id": "char_aurora",
  "schema_version": 1,
  "created_with_engine_version": "0.1.0",
  "module_versions": {
    "identity": 1,
    "psyche": 1,
    "relationships": 1,
    "memory": 1,
    "body_state": 1,
    "sensory_state": 1,
    "boundaries": 1
  }
}
```

### `identity.json`

Static or slow-changing character foundation.

```json
{
  "character_name": "Aurora",
  "appearance": "",
  "personality": "",
  "backstory": "",
  "scenario": "",
  "creator_notes": ""
}
```

### `psyche.json`

Psychological and emotional state.

```json
{
  "global": {
    "fear_baseline": 35,
    "resolve": 40,
    "shame": 35,
    "openness": 35
  },
  "needs": {
    "physiological": 70,
    "safety": 55,
    "belonging": 35,
    "esteem": 35,
    "actualization": 20
  },
  "self_determination": {
    "autonomy": 55,
    "competence": 45,
    "relatedness": 25
  },
  "trauma": {
    "phase": 1,
    "hypervigilance": 30,
    "flashbacks": 15,
    "numbing": 20,
    "avoidance": 35
  }
}
```

### `relationships.json`

Per-target relationship state.

```json
{
  "relationships": {
    "user": {
      "trust": 10,
      "affection": 20,
      "intimacy": 10,
      "commitment": 10,
      "fear": 10,
      "desire": 20,
      "notes": []
    }
  }
}
```

### `memory.json`

Character memory tiers.

```json
{
  "core": [],
  "recent": [],
  "schemas": [],
  "retrieval_index": []
}
```

### `world_links.json`

Character-specific links to shared world state.

```json
{
  "current_setting_id": "setting_001",
  "known_locations": [],
  "known_factions": [],
  "known_objects": [],
  "active_personal_plots": []
}
```

### `body_state.json`

General physical state and adaptation. This should remain neutral and genre-agnostic in the official schema.

```json
{
  "health": {
    "fatigue": 0,
    "injury": 0,
    "pain": 0,
    "stress": 0
  },
  "regions": [],
  "active_conditions": []
}
```

### `sensory_state.json`

Associations between sensory cues and emotional or memory responses.

```json
{
  "smell": [],
  "taste": [],
  "touch": [],
  "sound": [],
  "sight": []
}
```

### `boundaries.json`

Content rating, creator rules, and extension permissions.

```json
{
  "rating": "mature",
  "allowed_themes": [],
  "blocked_themes": [],
  "creator_rules": [],
  "marketplace_allowed": true,
  "commercial_export_allowed": true
}
```

### `audit.json`

Change history and package integrity.

```json
{
  "last_updated": 0,
  "last_engine_version": "0.1.0",
  "change_history": [],
  "integrity_hashes": {}
}
```

---

## Why Multi-File Soul Packages Are Good

| Benefit | Why It Matters |
|---|---|
| Cleaner architecture | Identity, memory, body, psyche, and relationships evolve differently |
| Easier debugging | Inspect one subsystem without reading a giant JSON file |
| Easier modding | Users can replace or edit one module |
| Better retrieval | Context compiler can load only relevant modules |
| Better migrations | Each module can have its own schema version |
| Better privacy | Sensitive modules can be encrypted or excluded from export |
| Better marketplace packaging | Creators can ship character, setting, images, and metadata together |

---

## Risks of Multi-File Soul Packages

| Risk | Mitigation |
|---|---|
| Files get out of sync | Use `manifest.json` with module versions and checksums |
| Import/export gets harder | Use `.mne` zipped bundle format |
| Migrations become complex | Version each module separately |
| References break | Use stable IDs, not display names |
| Runtime race conditions | Use SQLite during active sessions, export snapshots only |
| Prompt bloat | Never inject raw modules, only compiled summaries |

---

## Recommended Runtime Model

Use this during active play:

```text
SQLite
 ├─ souls
 ├─ settings
 ├─ conversations
 ├─ messages
 ├─ memories
 ├─ world_events
 ├─ body_state
 ├─ sensory_state
 └─ audit_log
```

Use this for export:

```text
.mne bundle
 ├─ manifest.json
 ├─ identity.json
 ├─ psyche.json
 ├─ relationships.json
 ├─ memory.json
 ├─ body_state.json
 ├─ sensory_state.json
 ├─ boundaries.json
 └─ audit.json
```

Do not make JSON files the only runtime source of truth once the project becomes complex. JSON is good for portability. SQLite is better for active play, querying, indexing, migrations, and transactional safety.

---

## Suggested Context Compiler Modules

```text
ContextCompiler
 ├─ SoulCompressor
 ├─ WorldCompressor
 ├─ MemoryRetriever
 ├─ BodyStateSelector
 ├─ SensoryCueSelector
 ├─ RecentChatSelector
 ├─ TokenBudgetAllocator
 ├─ BoundaryFilter
 └─ PromptAssembler
```

Each module should output a small text block. The final prompt should be assembled from only the blocks that matter this turn.

---

## Example Compiled Context

```text
[CURRENT STATE]
Location: abandoned station.
Active plot: find a safe exit.
Time: late night, shortly after the alarm.

[CHARACTER STATE]
Aurora is tired, guarded, and trying to stay composed. Her trust toward the user has improved slightly after a promise was kept, but she still scans for danger before relaxing.

[RELEVANT MEMORIES]
- The user previously promised not to abandon her during danger.
- Aurora reacts strongly to confined spaces after an earlier capture.
- Repeated quiet cooperation has made her less openly hostile.

[RECENT EVENTS]
- They entered the station after hearing movement outside.
- A locked service door blocked the safest route.
- Footsteps echoed from the lower platform.

[RECENT CHAT]
user: We need to move before they find us.
assistant: Aurora glances toward the stairwell, weighing the sound of distant boots.
```

The raw Soul files are not shown to the LLM. Only the compiled briefing is.

---

## Roadmap Additions

The old roadmap can be expanded with these architecture phases.

| Phase | Feature Area | Notes |
|---|---|---|
| Phase 2 | Provider profiles and streaming | Save provider settings, stream output, support cancellation |
| Phase 3 | Retrieval layer | Query relevant memories instead of only fixed top memories |
| Phase 4 | Modular Soul package | Export and import `.mne` bundles |
| Phase 5 | Multi-character settings | Compile multiple Souls in shared World Log |
| Phase 6 | Manuscript export | Convert sessions into scenes, chapters, summaries, and drafts |
| Phase 7 | Marketplace-safe packaging | Creator profiles, ratings, metadata, package validation |
| Phase 8 | Extension system | Local/user-defined modules, genre packs, optional advanced state systems |

---

## Creator and Novel Export Direction

The long-term creator pitch should be:

> Roleplay for 100 sessions, then turn the campaign into a structured manuscript.

Possible export pipeline:

```text
Conversation history
    |
    v
Scene splitter
    |
    v
Scene summaries
    |
    v
Continuity checker
    |
    v
Chapter outline
    |
    v
Manuscript draft
    |
    v
DOCX / Markdown / EPUB / PDF export
```

This creates a real business layer without locking the open-source core.

---

## Monetization Direction

Because Mnemosyne is AGPL open source, monetization should come from services and creator infrastructure rather than trying to lock down the local engine.

Potential paid layers:

- Hosted sync
- Encrypted backups
- Cloud character library
- Creator marketplace
- Premium export templates
- Collaborative campaign hosting
- Model routing convenience
- Package validation
- Commercial publishing workflow
- Creator storefronts

Commission should apply only to official marketplace transactions, not local private use.

---

## Licensing Note

Mnemosyne currently uses AGPL-3.0-or-later. This is compatible with open-source development, but it has obligations around source availability, especially for modified network-accessible versions. This document is not legal advice.

---

## Recommended README Summary

```markdown
# Mnemosyne

Mnemosyne is an open-source narrator engine for persistent AI roleplay and long-form story creation.

Instead of asking the LLM to be the character, memory, world tracker, and writer all at once, Mnemosyne separates those jobs. The model acts as the narrator. The engine manages character state, memory, relationships, world continuity, and context compression.

Characters live in portable Soul files. A Soul tracks identity, relationships, memories, emotional patterns, and long-term change. A World Log tracks location, plot threads, key objects, time, and recent events. Before each turn, Mnemosyne compiles only the relevant state into a compact prompt brief.

The result is AI roleplay that can continue across long campaigns without collapsing into amnesia, contradiction, or emotional reset.

Mnemosyne runs locally, is AGPL open source, and lets users bring their own model provider.
```

---

## Final Design Rule

> Mnemosyne should be many modules internally, one portable package externally, and one concise context brief at generation time.

That rule keeps the engine scalable without overwhelming the LLM.

---

## External References

These are included as architecture references, not as claims that Mnemosyne directly implements these systems.

- MemGPT, "Towards LLMs as Operating Systems": https://research.memgpt.ai/
- Tauri 2 official site: https://v2.tauri.app/
- GNU AGPLv3 license text: https://www.gnu.org/licenses/agpl-3.0.html
- Retrieval-Augmented Generation overview: https://link.springer.com/article/10.1007/s41019-025-00335-5
