# Pythagorean Harmony Dev Log - Phase Map

## Source Material
- Main transcript: 227 KB, 9,115 lines, 57 user turns
- Split into 11 files (_1 through _11), ~828 lines each
- Devlog target: 2,000-3,500 words each
- Total estimated devlogs: 11

---

## Devlog 000 - Origin Story
**Pre-repository. The idea, the tools, the decision to build.**
- Source: Stupid Fun Ideas.txt, 수학 판타지 게임 설계.txt (early design)
- Phase: Brainstorming -> GDD creation -> tool chain decisions
- Key moments:
  - "Stupid fun ideas" brainstorm (enemies screaming wrong answers, trolls throwing rocks)
  - Two-axis difficulty concept born: equation difficulty vs combat pattern difficulty
  - Duelist/Scholar/Execution/Panic enemy archetypes
  - Pitch refinement: from card battler to action RPG
  - Tool chain: Unreal Engine 5 + Codex + Cursor + NVIDIA Kidmo

---

## Devlog 001 - Project Setup & Codex Onboarding
**Turns 1-3 | Lines 0-265 | Split file _1**
- **Thesis**: Project born, Codex connected, first instruction file written
- Key moments:
  - Initial request: "Tell me what to do, simply"
  - Phase 0: project scaffolding, AGENTS.md creation
  - AGENTS.md content: UE5 Third Person C++ template, prototype scope definition
  - GitHub Desktop setup, Codex app connected to E:\UE Project\PythagoreanHarmony
  - First Codex prompt: analyze docs, propose 5 C++ classes
  - Codex proposes: EquationComponent, NumberInputComponent, EnemyActor, WeaponComponent, CombatLogWidget

---

## Devlog 002 - First Enemy Actor & Equation System
**Turns 4-8 | Lines 491-726 | Split file _1 (cont)**
- **Thesis**: First C++ code compiled and running in-editor
- Key moments:
  - Codex task: create FEquationDefinition struct + UEnemyEquationComponent
  - EPrototypeEquationType enum: Direct, Add, Subtract, Multiply, Divide
  - Goblin equation: x + 5 = 10, rank-based evolution
  - Ctrl+Alt+F11 Live Coding test: green log text appears
  - APrototypeEquationEnemy created: cube body, text component, AXIOM EXECUTION
  - Emotional turning point: "It works" -- first real validation

---

## Devlog 003 - Player Number Input & Answer Submission
**Turns 9-10 | Lines 863-1050 | Split file _2**
- **Thesis**: Player can now type numbers and submit answers
- Key moments:
  - UPlayerNumberInputComponent hooked into ThirdPersonCharacter
  - Number input display in top-left, 6-digit max, C to clear, backspace works
  - SubmitAnswer connected to enemy equation component
  - Correct answer -> AXIOM EXECUTION
  - Wrong answer -> equation evolves to next rank
  - Log: "Returned to normal attack. Input cleared."

---

## Devlog 004 - Difficulty System & Equation Evolution Debate
**Turns 11-14 | Lines 1051-1555 | Split file _2 (cont) + _3**
- **Thesis**: Questioning whether the difficulty system actually scales
- Key moments:
  - "Does this system evolve well? Or is it just 3 hardcoded equations?"
  - Debate: infinite procedural equations vs. rank-capped system
  - Difficulty concern: hard equation -> easy problem is bad UX
  - Player stance: prototype is fine for now, will refine later
  - "Difficulty scales weird" -- the two-axis concept revisited
  - Field notes in Korean about design intent

---

## Devlog 005 - Deeper Design Refinement & Live Combat
**Turns 15-17 | Lines 1785-2203 | Split file _3 (cont) + _4**
- **Thesis**: Difficulty mechanics questioned, enemy typing debated
- Key moments:
  - "How does difficulty setting actually work? Are you a genius or did AI cheat?"
  - Operation-type lock vs. species-based typing debate
  - "Operation type Rank lock is because there's only one enemy so far"
  - Discussion of enemy factions: Addicts, Subtractive Monks, Multiplication Cult
  - Live combat test: "It works" -- movement confirmed

---

## Devlog 006 - Engine Crash: CastChecked Purge
**Turns 18-19 | Lines 2405-2580 | Split file _4 (cont)**
- **Thesis**: Fatal engine crash forces systematic C++ safety audit
- Key moments:
  - Fatal error log: CastChecked failure in UE5 engine
  - Systematic search for CastChecked, Cast<AActor>, GetDefaultObject
  - Fix: replace unsafe casts with safe alternatives
  - Lesson: Unreal C++ is unforgiving with raw casts
  - Recovery: confirmed working after fix

---

## Devlog 007 - Equation System Refactor to Polynomial Model
**Turns 20-25 | Lines 2789-4439 | Split files _5, _6**
- **Thesis**: Harddiscovered limitation forces complete equation system rewrite
- Key moments:
  - Discovery: x+5 equation with -13 input gives x-8, but system can't handle it
  - "We need real polynomial support: ax^n + bx^(n-1) + ..."
  - FEquationDefinition becomes data wrapper, not math model
  - New polynomial equation model implemented
  - Support for arbitrary degree equations
  - Test confirmed: complex equations now solvable

---

## Devlog 008 - Combat Modes: Equation Attack Toggle
**Turns 26-31 | Lines 4672-5718 | Split files _7, _8**
- **Thesis**: Player needs to switch between normal attack and equation attack
- Key moments:
  - Weapon system architecture discussion
  - F-key debates for mode switching (F1-F4 too aggressive)
  - Equation attack mode: active weapon determines operation
  - Auto-return to normal attack after equation submission
  - Cancel option discussion
  - PrototypeWeaponData + Equipped Slots v0 implemented

---

## Devlog 009 - Mathematical Armor System Design
**Turns 32-35 | Lines 6174-7020 | Split file _8 (cont) + _9**
- **Thesis**: Armor system creates second layer of math combat
- Key moments:
  - Mathematics Armor: (x + 5) x 2 = 20 display format
  - "Does /2 destroy chest armor? Does -2 destroy helmet?"
  - ArmorBreak key debate: manual vs. automatic
  - Body-part targeting: head/chest/arms/legs radial UI design
  - "I don't want forced armor-breaking -- that's not how combat works in any game"
  - Final rule: normal operations don't break armor, dedicated Armor Break only

---

## Devlog 010 - Stamina, HUD, Dodge & Revive
**Turns 36-50 | Lines 7527-7852 | Split files _9 (cont), _10**
- **Thesis**: Player gets survival mechanics; second crash recovered from
- Key moments:
  - Fatal crash #2: LoginId/EpicAccountId error
  - Stamina system design: max-resource HUD bar
  - UMG Widget Blueprint: PrototypePlayerHUDWidget
  - Dodge/evasion mechanic: "No attack windup signal, hard to react"
  - Spam dodge works but feels wrong -- needs telegraphing
  - Revive system: "Character controllable after death -- was this intended?"
  - Weapon draw stance functions: R/F/T keys for right/left/two-handed

---

## Devlog 011 - Weapon Equipment System & Carry Visuals
**Turns 51-57 | Lines 7859-8873 | Split files _10 (cont), _11**
- **Thesis**: Weapons become visible on character, draw system completed
- Key moments:
  - Prototype Weapon Data + Equipped Slots v0
  - Weapon meshes attached to body sockets
  - Draw modes: OneHanded, TwoHanded (no Dark Souls restrictions)
  - Carry slot visuals: rear hip, shoulder, back
  - "Active weapon carry visual hidden while drawn"
  - Hand restriction layer moved from weapon data to character state
  - Final state: 17 systems confirmed working (dummy enemy, equation display, number input, X execution, math armor, armor break, attacks, stamina, dodge, guard, parry, windup, gore hit reaction, death/reset)

---

## Summary

| # | Devlog Title | Turn Range | Split File(s) | Key Thesis |
|---|---|---|---|---|
| 000 | Origin Story | Pre-repo | Design docs | Idea born, tools chosen, scope defined |
| 001 | Project Setup & Codex Onboarding | 1-3 | _1 | First instruction file, Codex connected |
| 002 | First Enemy Actor & Equation System | 4-8 | _1 | First C++ code runs in-editor |
| 003 | Player Number Input & Answer Submission | 9-10 | _2 | Player can type and submit answers |
| 004 | Difficulty System & Equation Evolution | 11-14 | _2, _3 | Does difficulty actually scale? |
| 005 | Deeper Design & Live Combat | 15-17 | _3, _4 | Enemy typing debate, combat works |
| 006 | Engine Crash: CastChecked Purge | 18-19 | _4 | Fatal crash forces safety audit |
| 007 | Equation System Refactor | 20-25 | _5, _6 | Harddiscovered limitation forces rewrite |
| 008 | Combat Modes: Attack Toggle | 26-31 | _7, _8 | Normal vs equation attack switching |
| 009 | Mathematical Armor System | 32-35 | _8, _9 | Second layer of math combat |
| 010 | Stamina, HUD, Dodge & Revive | 36-50 | _9, _10 | Survival mechanics, second crash fix |
| 011 | Weapon Equipment & Carry Visuals | 51-57 | _10, _11 | Weapons become visible on character |
