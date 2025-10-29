<LUCIM-DSL-DESCRIPTION>

# LUCIM DSL — Limited Use-Case Instance Model - Domain-Specific Language

## 1. Overview

### 1.1 Background
The LUCIM DSL captures single use-case instances as constrained UML Sequence Diagrams, enforcing a system-centered interaction discipline (Actor↔System only) and well-formedness rules suitable for automated validation and documentation.

### 1.2 LUCIM DSL Identity
- Base language: UML Sequence Diagram
- DSL extension mechanism: UML subsetting with constraints

### 1.3 Purpose
Define the LUCIM (Limited Use-Case Instance Model) DSL as a constrained subset of UML Sequence Diagrams for modeling system–actor interactions in reactive system scenarios.

### 1.4 General Modeling Assumptions and Constraints
- Single reactive system with external actors
- Linear temporal ordering of interactions
- PlantUML is the primary concrete syntax

### 1.5 Terminology 
See the Sections "Abstract Syntax" and Section "Glossary" for definitions and abbreviations.

### 1.6 MDE Level Note (M2 vs M1)
This document separates metamodel-level constraints (M2, Abstract Syntax and Static Semantics) from model-level constraints (M1, Concrete Syntax and Naming/Style). Normative Abstract Syntax (AS) and Static Semantics (SS) rules belong to M2. Normative Concrete Syntax (TCS) and Naming/Style (NAM) and Graphical Concrete Syntax (GCS) rules belong to M1. Examples and glossary are informative.


## 2. Metamodel Level (M2) — Abstract Syntax and Static Semantics

### 2.1 Abstract Syntax (AS)

#### 2.1.1 Element Inventory
- `Interaction`: Root container for the LUCIM model
- `Lifeline`: System and Actor participants
- `Message`: Actor↔System communications only
- `OccurrenceSpecification`: Message send/receive events
- `ExecutionSpecification`: Actor activation intervals

#### 2.1.2 Forbidden UML Concepts
- `CombinedFragment`: No combined fragments
- `InteractionOperand`: No interaction operands
- `Constraint`: No constraint
- `InteractionUse`: No interaction references
- `StateInvariant`: No state constraints
- `Gate`: No interface gates
- `GeneralOrdering`: Temporal order is textual order
- `DestructionOccurrenceSpecification`: No object destruction
- `CreationEvent`: No object creation during interaction

#### 2.1.3 Mapping to UML Metamodel
The following mapping is used to map the LUCIM DSL abstract syntax concepts to the UML metamodel abstract syntax concepts in the format  LUCIM_CONCEPTS → UML_CONCEPTS.
- Scenario (SCE) → UML Interaction: exactly one per model, root container
- System (SYS) → UML Lifeline: exactly one, named "System"
- Actor (ACT) → UML Lifeline: not "System"; type matches `Act[A-Z][A-Za-z0-9]*`
- Output Event (OE) → UML Message: sender Actor, receiver System
- Input Event (IE) → UML Message: sender System, receiver Actor
- Activation Bar (AB) → UML ExecutionSpecification: only on Actors; no nesting/overlap; none on System
- Event Parameter (EP) → UML ValueSpecification(s): ordered arguments on Messages

#### 2.1.4 Abstract Syntax Rules (AS)

**AS — System (SYS)**

<AS1_SYS_UNIQUE>
There must be exactly one System per model that is always named System
</AS1_SYS_UNIQUE>

<AS2_SYS_DECLARED_FIRST>
The System must be declared first before all actors.
</AS2_SYS_DECLARED_FIRST>

<AS3_SYS_ACT_ALLOWED_EVENTS>
Events must always be from System (resp. Actor) to an Actor (resp. the System). System → Actor or Actor → System
Canonical semantics for message directionality is specified in <SS1_MESSAGE_DIRECTIONALITY>.
</AS3_SYS_ACT_ALLOWED_EVENTS>

<AS4_SYS_NO_SELF_LOOP>
Events must never be from System to System. System → System
Canonical semantics for message directionality is specified in <SS1_OEIE_MESSAGE_DIRECTIONALITY>.
</AS4_SYS_NO_SELF_LOOP>

**AS — Actors (ACT)**

<AS5_ACT_DECLARED_AFTER_SYS>
The actors must be declared after the System.
</AS5_ACT_DECLARED_AFTER_SYS>

<AS6_ACT_NO_ACT_ACT_EVENTS>
Events must never be from Actor to Actor. Actor → Actor
Canonical semantics for message directionality is specified in <SS1_OEIE_MESSAGE_DIRECTIONALITY>.
</AS6_ACT_NO_ACT_ACT_EVENTS>

<AS7_ACT_TYPE_FORMAT>
Actor type name must be human-readable, in FirstCapitalLetterFormat and prefixed by "Act"
Example 1 : ActMsrCreator
Example 2 : ActEcologist
</AS7_ACT_TYPE_FORMAT>

**AS — Input Events (IE)**

<AS8_IE_EVENT_DIRECTION>
System sends event TO actor (System → Actor) — Input Event FROM System TO actor
Note. The "ie" prefix refers to the actor's perspective, not the system's perspective
Canonical semantics for message directionality is specified in <SS1_MESSAGE_DIRECTIONALITY>.
</AS8_IE_EVENT_DIRECTION>

**AS — Output Events (OE)**

<AS9_OE_EVENT_DIRECTION>
Actor sends event TO System (Actor → System) — Output Event FROM actor TO System
Canonical semantics for message directionality is specified in <SS1_MESSAGE_DIRECTIONALITY>.
</AS9_OE_EVENT_DIRECTION>

**AS — Activation Bars (AB)**

<AS10_AB_NO_NESTING>
Activator bars must never be nested.
</AS10_AB_NO_NESTING>

<AS11_AB_ORDER>
For each event, an activator bar must be defined that is always beginning just after the event.
Activation bars must always be located on the side of the actor lifeline, never on the side of the System.
See <SS2_AB_PLACEMENT_ORDERING> for the normative ordering and placement constraint.
</AS11_AB_ORDER>

<AS12_AB_NO_OVERLAPPING>
Activation bars must never overlap. Following sequence is forbidden: an event, start of activation bar of this event, another event before the end of the activation bar.
</AS12_AB_NO_OVERLAPPING>

### 2.2 Static Semantics (SS)

**SS — Message Directionality **

<SS1_MESSAGE_DIRECTIONALITY>
Every message in a LUCIM interaction SHALL connect exactly one Actor lifeline and the unique System lifeline. Messages between two Actors and messages from System to System are FORBIDDEN.
</SS1_MESSAGE_DIRECTIONALITY>

**SS — Activation Bars (AB)**

<SS2_AB_PLACEMENT_ORDERING>
For each message, if an activation is used, it SHALL occur on the receiving Actor lifeline immediately after the message occurrence. No activations SHALL occur on the System lifeline. The activation SHALL start right after the message and SHALL end before any subsequent message that depends on its completion.
</SS2_AB_PLACEMENT_ORDERING>

**SS — System (SYS)**

<SS3_SYS_UNIQUE_IDENTITY>
There SHALL be exactly one logical System lifeline in the interaction, and its canonical rendered name SHALL be "System".
</SS3_SYS_UNIQUE_IDENTITY>


## 3. Model Level (M1) — Concrete Syntax and Naming

### 3.1 Textual Concrete Syntax (TCS)

**TCS — Scenario (SCE)**

<TCS1_SCE_LUCIM_REPRESENTATION>
A LUCIM use case instance must be represented as a UML Sequence Diagram using strictly PlantUML textual syntax.
</TCS1_SCE_LUCIM_REPRESENTATION>

<TCS2_SCE_ALLOW_BLANK_LINES>
In PlantUML diagrams, blank lines may safely be ignored.
</TCS2_SCE_ALLOW_BLANK_LINES>

**TCS — System (SYS)**

<TCS3_SYS_DECLARATION>
Declare the System participant first using the syntax: participant System as system.
See <SS3_SYS_UNIQUE_IDENTITY> for uniqueness and canonical naming.
</TCS3_SYS_DECLARATION>

**TCS — Input Events (IE)**

<TCS4_IE_SYNTAX>
All ie event names are prefixed with "ie".
ie event names may be generic.
ie events must be modeled using dashed arrows and following this declaration syntax:
system --> theParticipant : ieMessageName(EP)
Example 1 : system --> jen : ieValidationFromTownHall()
Example 2 : system --> jen : ieMessage("Congratulations jen for your 6-years mandate as a major of the town !")
See <SS1_MESSAGE_DIRECTIONALITY> for the normative message directionality constraint.
</TCS4_IE_SYNTAX>

**TCS — Output Events (OE)**

<TCS5_OE_SYNTAX>
All oe event names are prefixed with "oe"
oe event names may be generic.
oe events must be modeled using continuous arrows and following this declaration syntax:
the participant -> system : oeMessage(EP)
Example: alex -> system : oeConstructionRequest("hpc")
See <SS1_MESSAGE_DIRECTIONALITY> for the normative message directionality constraint.
</TCS5_OE_SYNTAX>

**TCS — Event Parameters (EP)**

<TCS6_EP_TYPE>
Event parameters format may be of any type.
</TCS6_EP_TYPE>

<TCS7_EP_FLEX_QUOTING>
Each event parameter may be surrounded by single-quote (') OR double-quote (") OR no quote at all. A mix of single-quote, double-quote, no quote IS allowed within a parameter list.
</TCS7_EP_FLEX_QUOTING>

<TCS8_EP_COMMA_SEPARATED>
Multiple parameters must be comma-separated.
</TCS8_EP_COMMA_SEPARATED>

**TCS — Activation Bars (AB)**

<TCS9_AB_SEQUENCE>
Strictly follow this sequence of instructions for activation bars declarations:
(1) an event declaration
(2) activate the participant related to the event
(3) deactive the participant related to the event
Procedural guidance for PlantUML; the normative ordering is defined by <SS2_AB_PLACEMENT_ORDERING>.
</TCS9_AB_SEQUENCE>

<TCS10_AB_NO_ACTIVATION_BAR_ON_SYSTEM>
There must be NO activation bar in the System lifeline. Never activate System.
Activation bar colors are specified in <GCS5_AB_IE_COLOR> and <GCS6_AB_OE_COLOR>.
</TCS10_AB_NO_ACTIVATION_BAR_ON_SYSTEM>

### 3.2 Graphical Concrete Syntax (GCS)

**GCS — System (SYS)**

<GCS1_SYS_PARTICIPANT_RECTANGLE>
System must be declared as a PlantUML participant, with a rectangle shape.
</GCS1_SYS_PARTICIPANT_RECTANGLE>

<GCS2_SYS_COLOR>
The System rectangle background must be #E8C28A
</GCS2_SYS_COLOR>

**GCS — Actors (ACT)**

<GCS3_ACT_PARTICIPANT_RECTANGLE>
Each actor is modelled as a PlantUML participant with a rectangle-shape.
</GCS3_ACT_PARTICIPANT_RECTANGLE>

<GCS4_ACT_COLOR>
The actors rectangle background must be #FFF3B3
</GCS4_ACT_COLOR>

**GCS — Activation Bars (AB)**

<GCS5_AB_IE_COLOR>
The background of an activation bar placed just after an input event must be #C0EBFD
</GCS5_AB_IE_COLOR>

<GCS6_AB_OE_COLOR>
The background of an activation bar placed just after an output event must be #274364
Note: Activation bars appear only on actor lifelines; see <SS2_AB_PLACEMENT_ORDERING> for normative placement.
</GCS6_AB_OE_COLOR>

### 3.3 Naming & Style (NAM)

**NAM — Actors (ACT)**

<NAM1_ACT_INSTANCE_FORMAT>
All actor instance names must be human-readable, in camelCase.
Example: actAdministrator, chris, joe, theClock, anEcologist.
</NAM1_ACT_INSTANCE_FORMAT>

<NAM2_ACT_TYPE_FORMAT>
Actor type name must be human-readable, in FirstCapitalLetterFormat and prefixed by "Act".
Example 1 : ActMsrCreator
Example 2 : ActEcologist
</NAM2_ACT_TYPE_FORMAT>

<NAM3_ACT_DECLARATION_SYNTAX>
Each actor must be modelled using this PlantUML syntax:
participant "anActorName:ActActorType" as anActorName
Example 1: participant "theCreator:ActMsrCreator" as theCreator
Example 2: participant "chris:ActEcologist" as chris
</NAM3_ACT_DECLARATION_SYNTAX>


## 4. Informative Examples and Counter-examples

### 4.1  Valid LUCIM PlantUML diagram
```plantuml
@startuml

skinparam participant {
    BorderColor #000000
    BorderThickness 0.2
    BackgroundColor #FFF3B3
}
skinparam sequenceArrow {
    Color #gray
}

participant System as system #E8C28A
participant "theCreator:actMsrCreator" as theCreator
participant "theClock:actActivator" as theClock
participant "bill:actAdministrator" as bill

theCreator -> system : oeCreateSystemAndEnvironment("4")
activate theCreator #274364
deactivate theCreator

theClock -> system : oeSetClock("2017:11:24 - 03:20:00")
activate theClock #274364
deactivate theClock

bill -> system : oeLogin("icrashadmin","7WXC1359")
activate bill #274364
deactivate bill

system --> bill : ieMessage("You are logged ! Welcome ...")
activate bill #C0EBFD
deactivate bill

bill -> system : oeAddCoordinator("1","steve","pwdMessirExcalibur2017")
activate bill #274364
deactivate bill

system --> bill : ieCoordinatorAddedreturned()
activate bill #C0EBFD
deactivate bill

bill -> system : oeLogout()
activate bill #274364
deactivate bill

system --> bill : ieMessage("You are logged out ! Good Bye ...")
activate bill #C0EBFD
deactivate bill

theClock -> system : oeSetClock("2017:11:26 - 10:15:00")
activate theClock #274364
deactivate theClock

@enduml
```

### 4.2 Common Violations

Violation AS6_ACT_NO_ACT_ACT_EVENTS (Actor→Actor):
```plantuml
actUser -> actAdmin : oeDirectMessage("hello")  // FORBIDDEN
```

Violation AS4_SYS_NO_SELF_LOOP (System self-loop):
```plantuml
system -> system : ieInternalProcess()  // FORBIDDEN
```

Violation TCS10_AB_NO_ACTIVATION_BAR_ON_SYSTEM (System activation):
```plantuml
activate system  // FORBIDDEN
```

Violation TCS4_IE_SYNTAX (System→Actor continuous arrows message):
```plantuml
system -> actUser : ieWelcomeMessage("Hello John!") // FORBIDDEN
```

Violation TCS5_OE_SYNTAX (Actor→System dashed arrows message):
```plantuml
actUser --> system : oeWelcomeMessage("Hello John!") // FORBIDDEN
```

Violation TCS9_AB_SEQUENCE (invalid activation bar sequence):
```plantuml
activate actUser 
actUser -> system : oeWelcomeMessage("Hello John!") //FORBIDDEN
deactivate actUser
```

## 5. Glossary

- LUCIM: Limited Use-Case Instance Model
- System: The unique reactive system participant
- Actor: External domain role interacting with the System
- Output Event (OE): Actor→System message
- Input Event (IE): System→Actor message
- ExecutionSpecification: UML concept rendered as "activation bar"
- Lifeline: UML participant in sequence diagram

</LUCIM-DSL-DESCRIPTION>
