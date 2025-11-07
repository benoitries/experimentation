<RULES-LUCIM-OPERATION-MODEL>

# LUCIM Operation Model Rules (strict)


## Valid JSON format

<LOM0-JSON-BLOCK-ONLY>
The Operation Model <OPERATION-MODEL> must be a solely a  JSON block. <OPERATION-MODEL> must not include Markdown code fences or any text outside the JSON object.
</LOM0-JSON-BLOCK-ONLY>

## Naming Rules

<LOM1-ACT-TYPE-FORMAT>
All actor type names must be human-readable, in FirstCapitalLetterFormat and prefixed by "Act"
Example 1 : ActMsrCreator
Example 2 : ActEcologist
</LOM1-ACT-TYPE-FORMAT>

<LOM2-ACT-INSTANCE-FORMAT>
All actor instance names must be human-readable, in camelCase.
Example: actAdministrator, chris, joe, theClock, anEcologist.
</LOM2-ACT-INSTANCE-FORMAT>

<LOM2-IE-EVENT-NAME-FORMAT>
All input event names must be human-readable, in camelCase.
Example: ieSystemSetupComplete, ieElectionDay, ieRainUpdate, ieRainEvent.
</LOM2-IE-EVENT-NAME-FORMAT>

<LOM3-OE-EVENT-NAME-FORMAT>
All output event names must be human-readable, in camelCase.
Example: oeCreateSystemAndEnvironment, oeSetClock, oeAdvanceTick, oeSimulateRain.
</LOM3-OE-EVENT-NAME-FORMAT>

## Message Flow Rules

<LOM4-IE-EVENT-DIRECTION>
All input events must have their source from the System and their target to an Actor. 
</LOM4-IE-EVENT-DIRECTION>

<LOM5-OE-EVENT-DIRECTION>
All output events must have their source from an Actor and their target to the System. 
</LOM5-OE-EVENT-DIRECTION>


## Condition Rules

<LOM6-CONDITIONS-DEFINITION>
For each input and output event, its event conditions are defined as follows:
- preF (optional): functional preconditions that must hold before processing for the postF condition to be met.
- preP (optional): conditions that must hold for the event to be accessible.
- postF (required): functional guarantees after successful processing of the event.
</LOM6-CONDITIONS-DEFINITION>

<LOM7-CONDITIONS-VALIDATION>
Validation:
- postF: present and array is not empty, at least one condition must be present.
- preF/preP: present, arrays are present and may be empty.
</LOM7-CONDITIONS-VALIDATION>


## Glossary

- LUCIM: Limited Use-Case Instance Model
- System: The unique reactive system participant
- Actor: External domain role interacting with the System
- Output Event (OE): Actor→System message
- Input Event (IE): System→Actor message
- ExecutionSpecification: UML concept rendered as "activation bar"
- Lifeline: UML participant in sequence diagram

## Summary of Rules

All rules are normative. Rules start with a placeholder <RULE-ID> and are followed by a description and closed by a placeholder </RULE-ID>. e.g. LOM1-SYS-UNIQUE is a rule identifier and the text contained between <LOM1-SYS-UNIQUE> and </LOM1-SYS-UNIQUE> is the rule description.

</RULES-LUCIM-OPERATION-MODEL>


