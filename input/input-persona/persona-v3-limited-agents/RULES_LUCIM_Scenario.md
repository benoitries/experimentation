<RULES-LUCIM-SCENARIO>

# LUCIM Scenario Rules (strict)

## Valid JSON format

<LSC0-JSON-BLOCK-ONLY>
The Scenario <SCENARIO> must be a solely a  JSON block. <SCENARIO> must not include Markdown code fences or any text outside the JSON object.
</LSC0-JSON-BLOCK-ONLY>


## Quantitative Rules

<LSC2-ACTORS-LIMITATION>
There must be at most *five* actors in the scenario.
</LSC2-ACTORS-LIMITATION>

<LSC3-INPUT-EVENTS-LIMITATION>
There must be *at least one input event* to each actor in the scenario.
</LSC3-INPUT-EVENTS-LIMITATION>

<LSC4-OUTPUT-EVENTS-LIMITATION>
There must be *at least one output event* from each actor in the scenario.
</LSC4-OUTPUT-EVENTS-LIMITATION>

## Temporal Rules

<LSC5-EVENT-SEQUENCE>
The sequence of events must be compliant with the conditions defined in the <LUCIM-OPERATION-MODEL>. preF, preP, postF.
</LSC5-EVENT-SEQUENCE>

<LSC6-PARAMETERS-VALUE>
The parameters of the events must be valid with respect to the conditions defined in the <LUCIM-OPERATION-MODEL> and to the sequence of events. The parameters must be of the same type as defined in the <LUCIM-OPERATION-MODEL>.
</LSC6-PARAMETERS-VALUE>


## Message Flow Constraints

<LSC7-SYSTEM-NO-SELF-LOOP>
Events must never be from System to System. System → System
</LSC7-SYSTEM-NO-SELF-LOOP>

<LSC8-ACTOR-NO-SELF-LOOP>
Events must never be from Actor to Actor. Actor → Actor
</LSC8-ACTOR-NO-SELF-LOOP>

<LSC9-INPUT-EVENT-ALLOWED-EVENTS>
Input events must always be from the System to Actors. System → Actor.
</LSC9-INPUT-EVENT-ALLOWED-EVENTS>

<LSC10-OUTPUT-EVENT-DIRECTION>
Output events must always be from Actors to the System. Actor → System.
</LSC10-OUTPUT-EVENT-DIRECTION>

## Naming Consistency Constraints

<LSC12-ACTOR-TYPE-NAME-CONSISTENCY>
Actor type names must be stricly the same type names as defined in <LUCIM-OPERATION-MODEL>.
</LSC12-ACTOR-TYPE-NAME-CONSISTENCY>

<LSC14-INPUT-EVENT-NAME-CONSISTENCY>
Input event names must be stricly the same names as defined in <LUCIM-OPERATION-MODEL>.
</LSC14-INPUT-EVENT-NAME-CONSISTENCY>

<LSC15-OUTPUT-EVENT-NAME-CONSISTENCY>
Output event names must be stricly the same names as defined in <LUCIM-OPERATION-MODEL>.
</LSC15-OUTPUT-EVENT-NAME-CONSISTENCY>

<LSC16-ACTORS-PERSISTENCE>
The scenario must contain solely actors types as defined in <LUCIM-OPERATION-MODEL>. Actors types must be persistent. Do not invent new actor types.
Note that actor instances are not persistent, because they are not defined <LUCIM-OPERATION-MODEL>.
</LSC16-ACTORS-PERSISTENCE>

<LSC17-EVENTS-PERSISTENCE>
The scenario must contain solely events as defined in <LUCIM-OPERATION-MODEL>. Events must be persistent. Do not invent new event names.
</LSC17-EVENTS-PERSISTENCE>


## Glossary

- LUCIM: Limited Use-Case Instance Model
- System: The unique reactive system participant
- Actor: External domain role interacting with the System
- Output Event (OE): Actor→System message
- Input Event (IE): System→Actor message
- ExecutionSpecification: UML concept rendered as "activation bar"
- Lifeline: UML participant in sequence diagram

## Summary of Rules

All rules are normative. Rules start with a placeholder <RULE-ID> and are followed by a description and closed by a placeholder </RULE-ID>. e.g. LSC1-ACTOR-INSTANCE-FORMAT is a rule identifier and the text contained between <LSC1-ACTOR-INSTANCE-FORMAT> and </LSC1-ACTOR-INSTANCE-FORMAT> is the rule description.

</RULES-LUCIM-SCENARIO>
