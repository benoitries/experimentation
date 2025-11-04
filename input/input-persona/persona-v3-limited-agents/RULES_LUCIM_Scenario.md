<RULES-LUCIM-SCENARIO>

# LUCIM Scenario Rules (strict)

## Quantitative Rules


## Ordering Rules


## Message Flow Constraints

<LEM3-SYS-ACT-ALLOWED-EVENTS>
Events must always be from System (resp. Actor) to an Actor (resp. the System). System → Actor or Actor → System
</LEM3-SYS-ACT-ALLOWED-EVENTS>

<LEM4-SYS-NO-SELF-LOOP>
Events must never be from System to System. System → System
</LEM4-SYS-NO-SELF-LOOP>

<LEM6-ACT-NO-ACT-ACT-EVENTS>
Events must never be from Actor to Actor. Actor → Actor
Canonical semantics for message directionality is specified in <SS1-MESSAGE-DIRECTIONALITY>.
</LEM6-ACT-NO-ACT-ACT-EVENTS>

<AS3-SYS-ACT-ALLOWED-EVENTS>
Events must always be from System (resp. Actor) to an Actor (resp. the System). System → Actor or Actor → System
Canonical semantics for message directionality is specified in <SS1-MESSAGE-DIRECTIONALITY>.
</AS3-SYS-ACT-ALLOWED-EVENTS>

<AS4-SYS-NO-SELF-LOOP>
Events must never be from System to System. System → System
Canonical semantics for message directionality is specified in <SS1-MESSAGE-DIRECTIONALITY>.
</AS4-SYS-NO-SELF-LOOP>

<AS6-ACT-NO-ACT-ACT-EVENTS>
Events must never be from Actor to Actor. Actor → Actor
Canonical semantics for message directionality is specified in <SS1-MESSAGE-DIRECTIONALITY>.
</AS6-ACT-NO-ACT-ACT-EVENTS>

## Consistency Constraints

<CONS1-ACT-NAME-CONSISTENCY>
Actor names must be stricly the same names as defined in <LUCIM-OPERATION-MODEL>.
</CONS1-ACT-NAME-CONSISTENCY>

<CONS2-EVENT-NAME-CONSISTENCY>
Event names must be stricly the same names as defined in <LUCIM-OPERATION-MODEL>.
</CONS2-EVENT-NAME-CONSISTENCY>

<CONS3-ACT-NAME-CONSISTENCY>
The scenario must contain solely actors and events as defined in <LUCIM-OPERATION-MODEL>.
</CONS3-ACT-NAME-CONSISTENCY>

## Glossary

- LUCIM: Limited Use-Case Instance Model
- System: The unique reactive system participant
- Actor: External domain role interacting with the System
- Output Event (OE): Actor→System message
- Input Event (IE): System→Actor message
- ExecutionSpecification: UML concept rendered as "activation bar"
- Lifeline: UML participant in sequence diagram

## Summary of Rules

All rules are normative. Rules start with a placeholder <RULE-ID> and are followed by a description and closed by a placeholder </RULE-ID>. e.g. AS1-SYS-UNIQUE is a rule identifier and the text contained between <AS1-SYS-UNIQUE> and </AS1-SYS-UNIQUE> is the rule description.

</RULES-LUCIM-SCENARIO>
