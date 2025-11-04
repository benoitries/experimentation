# ... existing code ...
<MAPPING-NL-LUCIM-OPERATION-MODEL-MAPPING>

## Mapping Rules: NetLogo → LUCIM Operation Model

This document describes generalized mapping rules for synthesizing a LUCIM Operation Model from NetLogo simulation code. The LUCIM Operation Model must contain sufficient and minimal information to enable generation of execution scenarios (sequences of OE/IE events) that represent NetLogo simulation runs.

The mapping process transforms NetLogo simulation concepts into external actors, output events (Actor→System), input events (System→Actor), and observable state conditions that trigger input events.

See also:
- LUCIM DSL definition: `<LUCIM-DSL-DESCRIPTION>`
- IL-SYN mapping: `<IL-SYN-MAPPING>`
- IL-SEM mapping: `<IL-SEM-MAPPING>`
- LUCIM Operation Synthesizer persona: `<PSN-LUCIM-ENVIRONMENT-SYNTHESIZER>`

---

## 1. Core Mapping Principles

### 1.1 System (LUCIM)

**Rule SYS-1: System Represents Entire Simulation**
- The entire NetLogo model (all procedures, state, rules) maps to the LUCIM **System**.
- All breeds, patches, links, and globals are internal to the System unless they represent external roles.
- The System encapsulates all simulation logic and state transitions.

### 1.2 Actors (LUCIM)

**Rule ACT-1: Actors Are External Roles Only**
- **DO NOT** directly map NetLogo breeds to LUCIM actors.
- Breeds, patches, and links are typically internal entities managed by the System.
- Actors represent **external roles** that trigger or receive events.

**Rule ACT-2: Identify External Roles**
Identify actors based on **external sources of change**:
- **ActClock / ActActivator**: Temporal triggers (ticks, scheduled events, calendar changes)
- **ActEnvironment / ActSensor**: Natural phenomena or external sensor inputs (rain, temperature, stochastic events)
- **ActUser / ActAdministrator**: Human-initiated actions (installation, configuration, manual triggers)
- **ActMsrCreator**: System initialization and environment creation
- **ActStakeholder**: Domain-specific external roles (e.g., ActEcologist, ActTownHall)

**Rule ACT-3: Each Actor Must Have Goals**
- Every actor must have at least one explicit goal that justifies its existence.
- Goals describe why the actor interacts with the System (e.g., "Drive time progression", "Provide natural stimuli").

### 1.3 Output Events (OE) - Actor → System

**Rule OE-1: OE Map to External Actions**
- Output events represent actions **initiated by external actors**.
- Map procedures that express external intent or commands to the System.
- Examples: `install-hpc`, `set-clock`, `trigger-rain`, `initialize-system`

**Rule OE-2: OE Parameters from Procedure Arguments**
- Parameters of OE events derive from NetLogo procedure arguments.
- Additionally, include relevant global variables needed for triggering (e.g., intensity values, timestamps).
- Avoid exposing all system state; include only what is necessary for event triggering.

**Rule OE-3: Stochastic Events Are External**
- Random/probabilistic events (e.g., rain occurrence) are treated as external stimuli.
- Map them to OE events from appropriate actors (e.g., `ActEnvironment` → `oeSimulateRain`).

### 1.4 Input Events (IE) - System → Actor

**Rule IE-1: IE Map to Observable State Changes**
- Input events represent notifications of **significant state changes** or **observable phenomena**.
- Map state transitions that should be notified to external actors:
  - Threshold crossings (flood, drought, alerts)
  - Completion confirmations (installation done, operation finished)
  - Critical state changes (election day, extreme weather)

**Rule IE-2: IE Parameters from Observable State**
- Parameters include values relevant to the event (e.g., current level, intensity, timestamp).
- Do not convert internal logs/prints to IE unless they represent observable notifications to actors.

**Rule IE-3: Conditions Trigger IE**
- Define conditions (based on globals/observables) that trigger IE.
- Format: `if <condition> then emit <IE-name>(<parameters>)`

### 1.5 Observables and Thresholds

**Rule OBS-1: Globals → Observables**
- NetLogo globals map to "observable" state variables in the environment model.
- Only expose globals that:
  - Are used in IE conditions (thresholds)
  - Are needed as OE parameters
  - Represent state that actors need to observe

**Rule OBS-2: Thresholds Define IE Conditions**
- Formalize threshold crossings and state changes as conditions that emit IE.
- Example: `river-level > 2500` → emit `ieRiverFlood(currentLevel)`

### 1.6 Naming Conventions

**Rule NAM-1: LUCIM Naming Standards**
- Actor types: Prefix `Act`, FirstCapitalLetterFormat (e.g., `ActEnvironment`, `ActClock`)
- Events: `oe<ActionName>(...)` for Actor→System, `ie<EventName>(...)` for System→Actor
- Instance names: camelCase (e.g., `theClock`, `anAdministrator`)
- All names must comply with `<LUCIM-DSL-DESCRIPTION>` rules.

**Rule NAM-2: Traceability**
- Maintain traceability from source elements (NetLogo procedures, variables, rules) to actors and events.
- Record original names when normalizing to LUCIM conventions.

---

## 2. Detailed Mapping Rules

### 2.1 NetLogo Procedures → Events

| NetLogo Pattern | LUCIM Mapping | Example |
|----------------|---------------|---------|
| `to setup` | `oeCreateSystemAndEnvironment()` from `ActMsrCreator` | Initialization event |
| `to go` | Sequence of OE from different actors | Each tick triggers temporal/environmental OE |
| User-triggered procedures | `oe<ActionName>()` from `ActAdministrator` / `ActUser` | `oeInstallHpc()` |
| Stochastic procedures | `oe<StimulusName>()` from `ActEnvironment` | `oeSimulateRain()` |
| State change procedures | May trigger IE based on conditions | Threshold crossing → `ie<Alert>()` |
| Internal computations | Not mapped directly | Part of System internal logic |

### 2.2 NetLogo Globals → Observables

| Global Variable | Usage | LUCIM Observable |
|----------------|-------|------------------|
| Time-related (`current-date`, `ticks`) | Temporal events, scheduled actions | `dateString`, `tickCount` |
| State variables (levels, counts) | Threshold conditions, IE parameters | `riverLevel`, `treeCount` |
| Intensity/amount variables | OE/IE parameters | `rainIntensity`, `rainAmount` |
| Configuration constants | OE parameters, initialization | `initialYear`, `electionPeriod` |

### 2.3 NetLogo Breeds → System Entities (NOT Actors)

| NetLogo Breed | LUCIM Treatment |
|---------------|-----------------|
| Agent breeds (`turtles`, `links`) | Internal System entities |
| Environmental entities (`trees`, `plants`) | Part of System state |
| Ephemeral entities (`raindrops`, `waves`) | System-managed transient state |
| Infrastructure (`hpcs`) | System state resulting from actor actions |

**Note**: Breeds do NOT become actors. Actors are identified from external roles that interact with the System.

### 2.4 Conditional Logic → IE Conditions

| NetLogo Pattern | LUCIM IE Condition |
|----------------|-------------------|
| `if condition [ output-print ... ]` | If condition represents observable event: `if condition emit ie<Event>()` |
| Threshold checks (`if level > threshold`) | `if observable > threshold emit ie<Alert>(value)` |
| State transitions | Map to IE when state change should be notified to actors |

---

## 3. Minimal Sufficient Operation Model Structure

The LUCIM Operation Model must contain **sufficient and minimal** information to generate execution scenarios. The following structure enables scenario generation:

```json
{
  "system": {
    "name": "System"
  },
  "actors": [
    {
      "type": "ACTOR-TYPE-NAME",
      "description": "ACTOR-DESCRIPTION",
      "goals": ["GOAL-1", "GOAL-2"],
      "input_events": { ... },
      "output_events": { ... }
    }
  ],
  "observables": [
    {
      "name": "observableName",
      "source": "globals.variable-name",
      "type": "string|number|boolean",
      "units": "optional"
    }
  ],
  "ie_conditions": [
    {
      "if": "observable > threshold",
      "emit": "ieEventName",
      "params": { "paramName": "observable" }
    }
  ],
  "oe_triggers": [
    {
      "from": "ActActorType",
      "when": "condition or schedule",
      "call": "oeEventName",
      "params": { "paramName": "valueSource" }
    }
  ],
  "traceability": {
    "actors": { "ActActorType": ["netlogo-procedure-1", "netlogo-procedure-2"] },
    "events": { "oeEventName": ["netlogo-procedure"], "ieEventName": ["netlogo-rule"] }
  }
}
```

### 3.1 Elements Required for Scenario Generation

**Actors**
- Actor types with clear goals
- Associated OE and IE catalogs

**Observables**
- Minimal set of globals that trigger IE or inform OE parameters
- Only what is needed for condition evaluation

**IE Conditions**
- Conditions (based on observables) that emit IE
- Format: `if <condition> emit <IE-name>(<params>)`

**OE Triggers**
- Patterns describing when actors send OE
- Temporal schedules, stochastic events, or explicit triggers

**Traceability**
- Links from NetLogo source elements to actors/events
- Enables verification and debugging

---

## 4. Mapping Heuristics

### 4.1 Actor Identification Heuristics

1. **Temporal Actor**: If the model has time progression, scheduled events, or calendar logic → `ActClock` or `ActActivator`
2. **Environmental Actor**: If the model has stochastic natural phenomena, weather, or external sensor inputs → `ActEnvironment` or `ActSensor`
3. **User Actor**: If the model has manual initialization, installation, or configuration → `ActAdministrator` or `ActUser`
4. **Domain Actor**: If the model has domain-specific external stakeholders → `Act<DomainRole>` (e.g., `ActEcologist`, `ActTownHall`)

### 4.2 Event Derivation Heuristics

1. **OE from Procedures**: Procedures that initiate actions or respond to external triggers → OE events
2. **IE from State Changes**: State transitions, threshold crossings, completion confirmations → IE events
3. **Conditional IE**: If NetLogo code checks conditions and outputs/logs → map to IE if observable

### 4.3 Observable Selection Heuristics

1. **Used in Conditions**: Globals used in threshold checks or conditional logic → observables
2. **Event Parameters**: Globals passed as parameters to events → observables
3. **Avoid Over-exposure**: Do not expose all globals; only what is necessary for scenario generation

---

## 5. Example: Complete Mapping for `my-ecosys` Model

### 5.1 Actors Identified

- **ActClock**: Temporal management (date progression, election scheduling)
- **ActEnvironment**: Natural phenomena (rain simulation, river monitoring)
- **ActAdministrator**: Infrastructure installation (HPC installation)

### 5.2 Output Events (OE)

| OE Event | Source Actor | NetLogo Origin | Parameters |
|----------|--------------|----------------|------------|
| `oeSetClock` | `ActClock` | `compute-today` | `dateString` |
| `oeAdvanceTick` | `ActClock` | `go` (tick advancement) | (none) |
| `oeSimulateRain` | `ActEnvironment` | `simulate-event-rain` | `intensity`, `amount` |
| `oeInstallHpc` | `ActAdministrator` | `install-hpc` | `x`, `y` |

### 5.3 Input Events (IE)

| IE Event | Target Actor | NetLogo Origin | Parameters |
|----------|--------------|----------------|------------|
| `ieElectionDay` | `ActClock` | `simulate-next-election` (when countdown reaches 0) | `dateString` |
| `ieRainExtreme` | `ActEnvironment` | `simulate-event-rain` (when intensity = "extreme") | `intensity` |
| `ieRiverFlood` | `ActEnvironment` | `simulate-river-level-decrease` (when level > 2500) | `currentLevel` |
| `ieRiverDrought` | `ActEnvironment` | `simulate-river-level-decrease` (when level < 500) | `currentLevel` |
| `ieHpcInstalled` | `ActAdministrator` | `install-hpc` (completion) | `x`, `y`, `treesCut` |
| `ieForestCut` | `ActAdministrator` | `install-hpc` (side effect) | `treesBefore`, `treesAfter` |

### 5.4 Observables

| Observable | Source Global | Type | Usage |
|------------|---------------|------|-------|
| `riverLevel` | `river-level-current` | number (mm) | IE condition: flood/drought |
| `rainIntensity` | `rain-intensity` | string | IE condition: extreme rain |
| `dateString` | `current-date-full-int` | string | OE/IE parameter |
| `electionCountdown` | `town-hall-next-election` | number | IE condition: election day |

### 5.5 IE Conditions

```
if riverLevel > 2500 → emit ieRiverFlood(currentLevel: riverLevel)
if riverLevel < 500 → emit ieRiverDrought(currentLevel: riverLevel)
if rainIntensity == "extreme" → emit ieRainExtreme(intensity: rainIntensity)
if electionCountdown <= 0 → emit ieElectionDay(dateString: dateString)
```

### 5.6 OE Triggers

```
ActClock: each tick → oeAdvanceTick()
ActClock: date change → oeSetClock(dateString: dateString)
ActEnvironment: stochastic (50% chance) → oeSimulateRain(intensity: random, amount: based on intensity)
ActAdministrator: explicit call → oeInstallHpc(x: random, y: random)
```

---

## 6. Validation Checklist

Before finalizing the LUCIM Environment Model, verify:

- [ ] All actors are external roles (not breeds/patches)
- [ ] Each actor has at least one explicit goal
- [ ] All events are Actor→System (OE) or System→Actor (IE)
- [ ] No Actor↔Actor or System↔System events
- [ ] Event names follow LUCIM naming conventions
- [ ] Actor type names follow LUCIM naming conventions
- [ ] Observables are minimal (only what's needed for conditions/parameters)
- [ ] IE conditions are properly defined (if condition → emit IE)
- [ ] OE triggers are properly defined (when → call OE)
- [ ] Traceability links are complete
- [ ] Model is sufficient to generate execution scenarios

---

## 7. Scenario Generation Readiness

The operation model is ready for scenario generation when:

1. **Actors and Goals**: All external actors are identified with clear goals
2. **Event Catalogs**: Complete OE and IE catalogs are defined with proper signatures
3. **Observables**: Minimal set of observables needed for condition evaluation
4. **Conditions**: IE conditions map observable state to IE emissions
5. **Triggers**: OE triggers describe when actors send events to the System
6. **Traceability**: Source elements (NetLogo procedures/variables) are linked to actors/events

With these elements, a scenario generator can:
- Generate sequences of OE events (actor actions)
- Evaluate IE conditions based on observable state
- Emit IE events when conditions are met
- Produce LUCIM-compliant sequence diagrams representing NetLogo simulation runs

---

</NL-LUCIM-ENV-MAPPING>
# ... existing code ...
