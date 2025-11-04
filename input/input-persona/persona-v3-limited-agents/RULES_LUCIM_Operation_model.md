<RULES-LUCIM-OPERATION-MODEL>

# LUCIM Operation Model Rules (strict)

## Naming Rules

<LEM1-ACT-TYPE-FORMAT>
All actor type names must be human-readable, in FirstCapitalLetterFormat and prefixed by "Act"
Example 1 : ActMsrCreator
Example 2 : ActEcologist
</LEM1-ACT-TYPE-FORMAT>

<LEM2-ACT-INSTANCE-FORMAT>
All actor instance names must be human-readable, in camelCase.
Example: actAdministrator, chris, joe, theClock, anEcologist.
</LEM2-ACT-INSTANCE-FORMAT>

<LEM2-IE-EVENT-NAME-FORMAT>
All input event names must be human-readable, in camelCase.
Example: ieSystemSetupComplete, ieElectionDay, ieRainUpdate, ieRainEvent.
</LEM2-IE-EVENT-NAME-FORMAT>

<LEM3-OE-EVENT-NAME-FORMAT>
All output event names must be human-readable, in camelCase.
Example: oeCreateSystemAndEnvironment, oeSetClock, oeAdvanceTick, oeSimulateRain.
</LEM3-OE-EVENT-NAME-FORMAT>

## Message Flow Rules

<LEM4-IE-EVENT-DIRECTION>
All input events must have their source from the System and their target to an Actor. 
</LEM4-IE-EVENT-DIRECTION>

<LEM5-OE-EVENT-DIRECTION>
All output events must have their source from an Actor and their target to the System. 
</LEM5-OE-EVENT-DIRECTION>


## Glossary

- LUCIM: Limited Use-Case Instance Model
- System: The unique reactive system participant
- Actor: External domain role interacting with the System
- Output Event (OE): Actor→System message
- Input Event (IE): System→Actor message
- ExecutionSpecification: UML concept rendered as "activation bar"
- Lifeline: UML participant in sequence diagram

## Summary of Rules

All rules are normative. Rules start with a placeholder <RULE-ID> and are followed by a description and closed by a placeholder </RULE-ID>. e.g. LEM1-SYS-UNIQUE is a rule identifier and the text contained between <LEM1-SYS-UNIQUE> and </LEM1-SYS-UNIQUE> is the rule description.

</RULES-LUCIM-OPERATION-MODEL>


