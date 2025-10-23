{
  "actors": {
    "actActivator": {
      "name": "actActivator",
      "type": "ActActivator",
      "description": "Logical actor for time automatic message sending based on system's or environment status"
    },
    "actAdministrator": {
      "name": "actAdministrator", 
      "type": "ActAdministrator",
      "description": "Actor responsible of administration tasks for the iCrash system. Extends icrash.environment.actAuthenticated"
    },
    "actAuthenticated": {
      "name": "actAuthenticated",
      "type": "ActAuthenticated", 
      "description": "Abstract actor providing reusable input and output interfaces for actors that need to authenticate themselves"
    },
    "actComCompany": {
      "name": "actComCompany",
      "type": "ActComCompany",
      "description": "Communication company stakeholder ensuring the input/output of textual messages with humans having communication devices"
    },
    "actCoordinator": {
      "name": "actCoordinator",
      "type": "ActCoordinator",
      "description": "Actor responsible of handling one or several crisis for the iCrash system. Extends icrash.environment.actAuthenticated"
    },
    "actMsrCreator": {
      "name": "actMsrCreator",
      "type": "ActMsrCreator",
      "description": "Creator stakeholder in charge of state and environment initialization"
    }
  },
  "input_events": {
    "ieCoordinatorAdded": {
      "name": "ieCoordinatorAdded",
      "source": "System",
      "target": "actAdministrator",
      "parameters": []
    },
    "ieCoordinatorDeleted": {
      "name": "ieCoordinatorDeleted", 
      "source": "System",
      "target": "actAdministrator",
      "parameters": []
    },
    "ieMessage": {
      "name": "ieMessage",
      "source": "System",
      "target": "actAuthenticated",
      "parameters": ["AMessage:ptString"]
    },
    "ieSmsSend": {
      "name": "ieSmsSend",
      "source": "System", 
      "target": "actComCompany",
      "parameters": ["AdtPhoneNumber:dtPhoneNumber", "AdtSMS:dtSMS"]
    },
    "ieSendAnAlert": {
      "name": "ieSendAnAlert",
      "source": "System",
      "target": "actCoordinator", 
      "parameters": ["ActAlert:ctAlert"]
    },
    "ieSendACrisis": {
      "name": "ieSendACrisis",
      "source": "System",
      "target": "actCoordinator",
      "parameters": ["ActCrisis:ctCrisis"]
    }
  },
  "output_events": {
    "oeSollicitateCrisisHandling": {
      "name": "oeSollicitateCrisisHandling",
      "source": "actActivator",
      "target": "System",
      "parameters": []
    },
    "oeSetClock": {
      "name": "oeSetClock",
      "source": "actActivator", 
      "target": "System",
      "parameters": ["AcurrentClock:dtDateAndTime"]
    },
    "oeAddCoordinator": {
      "name": "oeAddCoordinator",
      "source": "actAdministrator",
      "target": "System", 
      "parameters": ["AdtCoordinatorID:dtCoordinatorID", "AdtLogin:dtLogin", "AdtPassword:dtPassword"]
    },
    "oeDeleteCoordinator": {
      "name": "oeDeleteCoordinator",
      "source": "actAdministrator",
      "target": "System",
      "parameters": ["AdtCoordinatorID:dtCoordinatorID"]
    },
    "oeLogin": {
      "name": "oeLogin",
      "source": "actAuthenticated",
      "target": "System",
      "parameters": ["AdtLogin:dtLogin", "AdtPassword:dtPassword"]
    },
    "oeLogout": {
      "name": "oeLogout", 
      "source": "actAuthenticated",
      "target": "System",
      "parameters": []
    },
    "oeAlert": {
      "name": "oeAlert",
      "source": "actComCompany",
      "target": "System",
      "parameters": ["AetHumanKind:etHumanKind", "AdtDate:dtDate", "AdtTime:dtTime", "AdtPhoneNumber:dtPhoneNumber", "AdtGPSLocation:dtGPSLocation", "AdtComment:dtComment"]
    },
    "oeInvalidateAlert": {
      "name": "oeInvalidateAlert",
      "source": "actCoordinator",
      "target": "System", 
      "parameters": ["AdtAlertID:dtAlertID"]
    },
    "oeCloseCrisis": {
      "name": "oeCloseCrisis",
      "source": "actCoordinator",
      "target": "System",
      "parameters": ["AdtCrisisID:dtCrisisID"]
    },
    "oeGetAlertsSet": {
      "name": "oeGetAlertsSet",
      "source": "actCoordinator",
      "target": "System",
      "parameters": ["AetAlertStatus:etAlertStatus"]
    },
    "oeGetCrisisSet": {
      "name": "oeGetCrisisSet", 
      "source": "actCoordinator",
      "target": "System",
      "parameters": ["AetCrisisStatus:etCrisisStatus"]
    },
    "oeSetCrisisHandler": {
      "name": "oeSetCrisisHandler",
      "source": "actCoordinator",
      "target": "System",
      "parameters": ["AdtCrisisID:dtCrisisID"]
    },
    "oeReportOnCrisis": {
      "name": "oeReportOnCrisis",
      "source": "actCoordinator", 
      "target": "System",
      "parameters": ["AdtCrisisID:dtCrisisID", "AdtComment:dtComment"]
    },
    "oeSetCrisisStatus": {
      "name": "oeSetCrisisStatus",
      "source": "actCoordinator",
      "target": "System",
      "parameters": ["AdtCrisisID:dtCrisisID", "AetCrisisStatus:etCrisisStatus"]
    },
    "oeSetCrisisType": {
      "name": "oeSetCrisisType",
      "source": "actCoordinator",
      "target": "System",
      "parameters": ["AdtCrisisID:dtCrisisID", "AetCrisisType:etCrisisType"]
    },
    "oeValidateAlert": {
      "name": "oeValidateAlert",
      "source": "actCoordinator",
      "target": "System",
      "parameters": ["AdtAlertID:dtAlertID"]
    },
    "oeCreateSystemAndEnvironment": {
      "name": "oeCreateSystemAndEnvironment",
      "source": "actMsrCreator",
      "target": "System",
      "parameters": ["AqtyComCompanies:ptInteger"]
    }
  }
}