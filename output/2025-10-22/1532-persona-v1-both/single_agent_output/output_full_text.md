[START_INITIAL_DIAGRAM]
@startuml
participant System as system
participant "actController:ActSimulator" as controller

controller -> system : oeSetupSphere(shape-size=37.6, num-turtles=800)
activate controller
deactivate controller

system --> controller : ieSphereReady()
activate controller
deactivate controller

controller -> system : oeGo()
activate controller
deactivate controller

system --> controller : ieGoTick()
activate controller
deactivate controller
@enduml
[END_INITIAL_DIAGRAM]

[START_INITIAL_AUDIT]
{
  "verdict": "compliant",
  "non-compliant-rules": []
}
[END_INITIAL_AUDIT]