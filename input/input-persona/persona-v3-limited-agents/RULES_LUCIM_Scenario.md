<RULES-LUCIM-SCENARIO>

# LUCIM Scenario Rules (strict)




## Valid JSON format

<LSC0-JSON-BLOCK-ONLY>
The Scenario <SCENARIO> must be a solely a  JSON block. <SCENARIO> must not include Markdown code fences or any text outside the JSON object.
</LSC0-JSON-BLOCK-ONLY>


## Quantitative Rules


## Ordering Rules


## Message Flow Constraints

<LSC3-SYS-ACT-ALLOWED-EVENTS>
Events must always be from System (resp. Actor) to an Actor (resp. the System). System → Actor or Actor → System
</LSC3-SYS-ACT-ALLOWED-EVENTS>

<LSC4-SYS-NO-SELF-LOOP>
Events must never be from System to System. System → System
</LSC4-SYS-NO-SELF-LOOP>

<LSC6-ACT-NO-ACT-ACT-EVENTS>
Events must never be from Actor to Actor. Actor → Actor
Canonical semantics for message directionality is specified in <SS1-MESSAGE-DIRECTIONALITY>.
</LSC6-ACT-NO-ACT-ACT-EVENTS>

<LSC3-SYS-ACT-ALLOWED-EVENTS>
Events must always be from System (resp. Actor) to an Actor (resp. the System). System → Actor or Actor → System
Canonical semantics for message directionality is specified in <SS1-MESSAGE-DIRECTIONALITY>.
</LSC3-SYS-ACT-ALLOWED-EVENTS>

<LSC4-SYS-NO-SELF-LOOP>
Events must never be from System to System. System → System
Canonical semantics for message directionality is specified in <SS1-MESSAGE-DIRECTIONALITY>.
</LSC4-SYS-NO-SELF-LOOP>

<LSC6-ACT-NO-ACT-ACT-EVENTS>
Events must never be from Actor to Actor. Actor → Actor
Canonical semantics for message directionality is specified in <SS1-MESSAGE-DIRECTIONALITY>.
</LSC6-ACT-NO-ACT-ACT-EVENTS>

## Consistency Constraints

<LSC1-ACT-NAME-CONSISTENCY>
Actor names must be stricly the same names as defined in <LUCIM-OPERATION-MODEL>.
</LSC1-ACT-NAME-CONSISTENCY>

<LSC2-EVENT-NAME-CONSISTENCY>
Event names must be stricly the same names as defined in <LUCIM-OPERATION-MODEL>.
</LSC2-EVENT-NAME-CONSISTENCY>

<LSC3-ACT-NAME-CONSISTENCY>
The scenario must contain solely actors and events as defined in <LUCIM-OPERATION-MODEL>.
</LSC3-ACT-NAME-CONSISTENCY>

## Glossary

- LUCIM: Limited Use-Case Instance Model
- System: The unique reactive system participant
- Actor: External domain role interacting with the System
- Output Event (OE): Actor→System message
- Input Event (IE): System→Actor message
- ExecutionSpecification: UML concept rendered as "activation bar"
- Lifeline: UML participant in sequence diagram

## Summary of Rules

All rules are normative. Rules start with a placeholder <RULE-ID> and are followed by a description and closed by a placeholder </RULE-ID>. e.g. LSC1-SYS-UNIQUE is a rule identifier and the text contained between <LSC1-SYS-UNIQUE> and </LSC1-SYS-UNIQUE> is the rule description.

</RULES-LUCIM-SCENARIO>
