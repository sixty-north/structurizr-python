from structurizr.model.interaction_style import InteractionStyle
from structurizr.workspace import Workspace

TAG_ALERT = "Alert"

workspace = Workspace("Financial Risk System", "This is a simple (incomplete) example C4 model based upon the financial risk system architecture kata, which can be found at http://bit.ly/sa4d-risksystem")

model = workspace.get_model()

# create the basic model
financial_risk_system = model.add_software_system("Financial Risk System", "Calculates the bank's exposure to risk for product X.")

business_user = model.add_person("Business User", "A regular business user.")
business_user.uses(financial_risk_system, "View reports using")

configuration_user = model.add_person("Configuration User", "A regular business user who can also configure the parameters used in the risk calculations.")
configuration_user.uses(financial_risk_system, "Configures parameters using")

trade_data_system = model.add_software_system("Trade Data System", "The system of record for trades of type X.")
financial_risk_system.uses(trade_data_system, "Gets trade data from")

reference_data_system = model.add_software_system("Reference Data System", "Manages reference data for all counterparties the bank interacts with.")
financial_risk_system.uses(reference_data_system, "Gets counterparty data from")

reference_data_system_v2 = model.add_software_system("Reference Data System v2.0", "Manages reference data for all counterparties the bank interacts with.")
reference_data_system_v2.add_tags("Future State")
financial_risk_system.uses(reference_data_system_v2, "Gets counterparty data from").add_tags("Future State")

email_system = model.add_software_system("E-mail system", "The bank's Microsoft Exchange system.")
financial_risk_system.uses(email_system, "Sends a notification that a report is ready to")
email_system.delivers(business_user, "Sends a notification that a report is ready to", "E-mail message", InteractionStyle.Asynchronous)

central_monitoring_service = model.addSoftwareSystem("Central Monitoring Service", "The bank's central monitoring and alerting dashboard.")
financial_risk_system.uses(central_monitoring_service, "Sends critical failure alerts to", "SNMP", InteractionStyle.Asynchronous).addTags(TAG_ALERT)

active_directory = model.addSoftwareSystem("Active Directory", "The bank's authentication and authorisation system.")
financial_risk_system.uses(active_directory, "Uses for user authentication and authorisation")

