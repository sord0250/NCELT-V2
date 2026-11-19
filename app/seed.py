from .db import SessionLocal, engine
from .models import Base, Owner, Outcome

def run():
    # User accounts are not seeded; create the first manager through /setup.
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if db.query(Owner).count() == 0:
        db.add_all([
            Owner(name="Security Team", 
                  email="security@example.local"),
            Owner(name="IT Ops", email="itops@example.local"),
        ])
    if db.query(Outcome).count() == 0:
                db.add_all([

# -------------------- GOVERN (GV) --------------------

Outcome(subcat_id="GV.OC-01", summary="Mission informs cybersecurity risk management.", category="Organizational Context", function="Govern"),
Outcome(subcat_id="GV.OC-02", summary="Stakeholder needs for cybersecurity risk are understood.", category="Organizational Context", function="Govern"),
Outcome(subcat_id="GV.OC-03", summary="Legal and regulatory cybersecurity requirements are managed.", category="Organizational Context", function="Govern"),
Outcome(subcat_id="GV.OC-04", summary="Critical services for external stakeholders are identified and communicated.", category="Organizational Context", function="Govern"),
Outcome(subcat_id="GV.OC-05", summary="Organizational dependencies and critical outcomes are understood.", category="Organizational Context", function="Govern"),

Outcome(subcat_id="GV.RM-01", summary="Risk management objectives are established with stakeholders.", category="Risk Management Strategy", function="Govern"),
Outcome(subcat_id="GV.RM-02", summary="Risk appetite and tolerance are defined and maintained.", category="Risk Management Strategy", function="Govern"),
Outcome(subcat_id="GV.RM-03", summary="Cyber risk is integrated into enterprise risk management.", category="Risk Management Strategy", function="Govern"),
Outcome(subcat_id="GV.RM-04", summary="Strategic risk response direction is established.", category="Risk Management Strategy", function="Govern"),
Outcome(subcat_id="GV.RM-05", summary="Cyber risk communication channels are established.", category="Risk Management Strategy", function="Govern"),
Outcome(subcat_id="GV.RM-06", summary="Standardized methods for assessing and prioritizing risk are used.", category="Risk Management Strategy", function="Govern"),
Outcome(subcat_id="GV.RM-07", summary="Strategic opportunities are included in risk discussions.", category="Risk Management Strategy", function="Govern"),

Outcome(subcat_id="GV.RR-01", summary="Leadership is accountable for cybersecurity risk.", category="Roles, Responsibilities and Authorities", function="Govern"),
Outcome(subcat_id="GV.RR-02", summary="Cybersecurity roles and responsibilities are defined and enforced.", category="Roles, Responsibilities and Authorities", function="Govern"),
Outcome(subcat_id="GV.RR-03", summary="Resources align with cybersecurity strategy and risk.", category="Roles, Responsibilities and Authorities", function="Govern"),
Outcome(subcat_id="GV.RR-04", summary="Cybersecurity is integrated into HR practices.", category="Roles, Responsibilities and Authorities", function="Govern"),

Outcome(subcat_id="GV.PO-01", summary="Cybersecurity risk policy is established and enforced.", category="Policy", function="Govern"),
Outcome(subcat_id="GV.PO-02", summary="Cybersecurity policy is reviewed and updated regularly.", category="Policy", function="Govern"),

Outcome(subcat_id="GV.OV-01", summary="Risk strategy outcomes are reviewed for adjustment.", category="Oversight", function="Govern"),
Outcome(subcat_id="GV.OV-02", summary="Risk strategy is adjusted for organizational coverage.", category="Oversight", function="Govern"),
Outcome(subcat_id="GV.OV-03", summary="Cybersecurity performance is evaluated and improved.", category="Oversight", function="Govern"),

Outcome(subcat_id="GV.SC-01", summary="Supply chain risk program is established.", category="Cybersecurity Supply Chain Risk Management", function="Govern"),
Outcome(subcat_id="GV.SC-02", summary="Supply chain roles and responsibilities are coordinated.", category="Cybersecurity Supply Chain Risk Management", function="Govern"),
Outcome(subcat_id="GV.SC-03", summary="Supply chain risk is integrated into enterprise risk.", category="Cybersecurity Supply Chain Risk Management", function="Govern"),
Outcome(subcat_id="GV.SC-04", summary="Suppliers are identified and prioritized by criticality.", category="Cybersecurity Supply Chain Risk Management", function="Govern"),
Outcome(subcat_id="GV.SC-05", summary="Supply chain risk requirements are built into contracts.", category="Cybersecurity Supply Chain Risk Management", function="Govern"),
Outcome(subcat_id="GV.SC-06", summary="Due diligence is performed before supplier engagement.", category="Cybersecurity Supply Chain Risk Management", function="Govern"),
Outcome(subcat_id="GV.SC-07", summary="Supplier risks are assessed and monitored.", category="Cybersecurity Supply Chain Risk Management", function="Govern"),
Outcome(subcat_id="GV.SC-08", summary="Suppliers are included in incident planning and response.", category="Cybersecurity Supply Chain Risk Management", function="Govern"),
Outcome(subcat_id="GV.SC-09", summary="Supply chain security is monitored across lifecycle.", category="Cybersecurity Supply Chain Risk Management", function="Govern"),
Outcome(subcat_id="GV.SC-10", summary="Post-engagement supply chain risk activities are defined.", category="Cybersecurity Supply Chain Risk Management", function="Govern"),

# -------------------- IDENTIFY (ID) --------------------

Outcome(subcat_id="ID.AM-01", summary="Hardware inventories are maintained.", category="Asset Management", function="Identify"),
Outcome(subcat_id="ID.AM-02", summary="Software and system inventories are maintained.", category="Asset Management", function="Identify"),
Outcome(subcat_id="ID.AM-03", summary="Network communication and data flows are documented.", category="Asset Management", function="Identify"),
Outcome(subcat_id="ID.AM-04", summary="Supplier-provided services are inventoried.", category="Asset Management", function="Identify"),
Outcome(subcat_id="ID.AM-05", summary="Assets are prioritized by classification and impact.", category="Asset Management", function="Identify"),
Outcome(subcat_id="ID.AM-07", summary="Data inventories and metadata are maintained.", category="Asset Management", function="Identify"),
Outcome(subcat_id="ID.AM-08", summary="Assets are managed through their lifecycle.", category="Asset Management", function="Identify"),

Outcome(subcat_id="ID.RA-01", summary="Vulnerabilities are identified and recorded.", category="Risk Assessment", function="Identify"),
Outcome(subcat_id="ID.RA-02", summary="Threat intelligence is received and utilized.", category="Risk Assessment", function="Identify"),
Outcome(subcat_id="ID.RA-03", summary="Internal and external threats are identified.", category="Risk Assessment", function="Identify"),
Outcome(subcat_id="ID.RA-04", summary="Threat likelihood and impact are assessed.", category="Risk Assessment", function="Identify"),
Outcome(subcat_id="ID.RA-05", summary="Inherent risk informs prioritization.", category="Risk Assessment", function="Identify"),
Outcome(subcat_id="ID.RA-06", summary="Risk responses are selected and tracked.", category="Risk Assessment", function="Identify"),
Outcome(subcat_id="ID.RA-07", summary="Changes and exceptions are risk assessed.", category="Risk Assessment", function="Identify"),
Outcome(subcat_id="ID.RA-08", summary="Vulnerability disclosure processes are established.", category="Risk Assessment", function="Identify"),
Outcome(subcat_id="ID.RA-09", summary="Hardware and software authenticity is verified.", category="Risk Assessment", function="Identify"),
Outcome(subcat_id="ID.RA-10", summary="Critical suppliers are assessed before acquisition.", category="Risk Assessment", function="Identify"),

Outcome(subcat_id="ID.IM-01", summary="Improvements are identified from evaluations.", category="Improvement", function="Identify"),
Outcome(subcat_id="ID.IM-02", summary="Improvements are identified from testing and exercises.", category="Improvement", function="Identify"),
Outcome(subcat_id="ID.IM-03", summary="Operational improvements are identified.", category="Improvement", function="Identify"),
Outcome(subcat_id="ID.IM-04", summary="Incident and cybersecurity plans are maintained and improved.", category="Improvement", function="Identify"),

# -------------------- PROTECT (PR) --------------------

Outcome(subcat_id="PR.AA-01", summary="Identities and credentials are managed.", category="Identity Management, Authentication, and Access Control", function="Protect"),
Outcome(subcat_id="PR.AA-02", summary="Identities are proofed and bound to credentials.", category="Identity Management, Authentication, and Access Control", function="Protect"),
Outcome(subcat_id="PR.AA-03", summary="Users and systems are authenticated.", category="Identity Management, Authentication, and Access Control", function="Protect"),
Outcome(subcat_id="PR.AA-04", summary="Identity assertions are protected and verified.", category="Identity Management, Authentication, and Access Control", function="Protect"),
Outcome(subcat_id="PR.AA-05", summary="Access is managed per least privilege principles.", category="Identity Management, Authentication, and Access Control", function="Protect"),
Outcome(subcat_id="PR.AA-06", summary="Physical access is controlled and monitored.", category="Identity Management, Authentication, and Access Control", function="Protect"),

Outcome(subcat_id="PR.AT-01", summary="Personnel receive cybersecurity awareness training.", category="Awareness and Training", function="Protect"),
Outcome(subcat_id="PR.AT-02", summary="Specialized roles receive targeted training.", category="Awareness and Training", function="Protect"),

Outcome(subcat_id="PR.DS-01", summary="Data-at-rest confidentiality, integrity, and availability are protected.", category="Data Security", function="Protect"),
Outcome(subcat_id="PR.DS-02", summary="Data-in-transit confidentiality, integrity, and availability are protected.", category="Data Security", function="Protect"),
Outcome(subcat_id="PR.DS-10", summary="Data-in-use confidentiality, integrity, and availability are protected.", category="Data Security", function="Protect"),
Outcome(subcat_id="PR.DS-11", summary="Data backups are created, protected, and tested.", category="Data Security", function="Protect"),

Outcome(subcat_id="PR.PS-01", summary="Configuration management is established and applied.", category="Platform Security", function="Protect"),
Outcome(subcat_id="PR.PS-02", summary="Software is maintained commensurate with risk.", category="Platform Security", function="Protect"),
Outcome(subcat_id="PR.PS-03", summary="Hardware is maintained commensurate with risk.", category="Platform Security", function="Protect"),
Outcome(subcat_id="PR.PS-04", summary="Logs are generated for monitoring.", category="Platform Security", function="Protect"),
Outcome(subcat_id="PR.PS-05", summary="Unauthorized software execution is prevented.", category="Platform Security", function="Protect"),
Outcome(subcat_id="PR.PS-06", summary="Secure development practices are integrated.", category="Platform Security", function="Protect"),

Outcome(subcat_id="PR.IR-01", summary="Networks are protected from unauthorized access.", category="Technology Infrastructure Resilience", function="Protect"),
Outcome(subcat_id="PR.IR-02", summary="Technology assets are protected from environmental threats.", category="Technology Infrastructure Resilience", function="Protect"),
Outcome(subcat_id="PR.IR-03", summary="Resilience mechanisms are implemented.", category="Technology Infrastructure Resilience", function="Protect"),
Outcome(subcat_id="PR.IR-04", summary="Capacity is maintained to ensure availability.", category="Technology Infrastructure Resilience", function="Protect"),

# -------------------- DETECT (DE) --------------------

Outcome(subcat_id="DE.CM-01", summary="Networks are monitored for adverse events.", category="Continuous Monitoring", function="Detect"),
Outcome(subcat_id="DE.CM-02", summary="Physical environments are monitored.", category="Continuous Monitoring", function="Detect"),
Outcome(subcat_id="DE.CM-03", summary="User activity and system usage are monitored.", category="Continuous Monitoring", function="Detect"),
Outcome(subcat_id="DE.CM-06", summary="External service providers are monitored.", category="Continuous Monitoring", function="Detect"),
Outcome(subcat_id="DE.CM-09", summary="Hardware, software, and runtime environments are monitored.", category="Continuous Monitoring", function="Detect"),

Outcome(subcat_id="DE.AE-02", summary="Adverse events are analyzed.", category="Adverse Event Analysis", function="Detect"),
Outcome(subcat_id="DE.AE-03", summary="Information is correlated across sources.", category="Adverse Event Analysis", function="Detect"),
Outcome(subcat_id="DE.AE-04", summary="Impact and scope of events are determined.", category="Adverse Event Analysis", function="Detect"),
Outcome(subcat_id="DE.AE-06", summary="Adverse event information is shared with authorized staff.", category="Adverse Event Analysis", function="Detect"),
Outcome(subcat_id="DE.AE-07", summary="Threat intelligence is integrated into analysis.", category="Adverse Event Analysis", function="Detect"),
Outcome(subcat_id="DE.AE-08", summary="Incidents are declared per defined criteria.", category="Adverse Event Analysis", function="Detect"),

# -------------------- RESPOND (RS) --------------------

Outcome(subcat_id="RS.MA-01", summary="Incident response plan is executed with stakeholders.", category="Incident Management", function="Respond"),
Outcome(subcat_id="RS.MA-02", summary="Incident reports are triaged and validated.", category="Incident Management", function="Respond"),
Outcome(subcat_id="RS.MA-03", summary="Incidents are categorized and prioritized.", category="Incident Management", function="Respond"),
Outcome(subcat_id="RS.MA-04", summary="Incidents are escalated as required.", category="Incident Management", function="Respond"),
Outcome(subcat_id="RS.MA-05", summary="Incident recovery criteria are applied.", category="Incident Management", function="Respond"),

Outcome(subcat_id="RS.AN-03", summary="Incident root cause analysis is performed.", category="Incident Analysis", function="Respond"),
Outcome(subcat_id="RS.AN-06", summary="Investigation actions are recorded and preserved.", category="Incident Analysis", function="Respond"),
Outcome(subcat_id="RS.AN-07", summary="Incident data integrity is preserved.", category="Incident Analysis", function="Respond"),
Outcome(subcat_id="RS.AN-08", summary="Incident magnitude is estimated and validated.", category="Incident Analysis", function="Respond"),

Outcome(subcat_id="RS.CO-02", summary="Stakeholders are notified of incidents.", category="Incident Response Reporting and Communication", function="Respond"),
Outcome(subcat_id="RS.CO-03", summary="Incident information is shared appropriately.", category="Incident Response Reporting and Communication", function="Respond"),

Outcome(subcat_id="RS.MI-01", summary="Incidents are contained.", category="Incident Mitigation", function="Respond"),
Outcome(subcat_id="RS.MI-02", summary="Incidents are eradicated.", category="Incident Mitigation", function="Respond"),

# -------------------- RECOVER (RC) --------------------

Outcome(subcat_id="RC.RP-01", summary="Recovery plan is executed after incident.", category="Incident Recovery Plan Execution", function="Recover"),
Outcome(subcat_id="RC.RP-02", summary="Recovery actions are prioritized and performed.", category="Incident Recovery Plan Execution", function="Recover"),
Outcome(subcat_id="RC.RP-03", summary="Backups are verified before restoration.", category="Incident Recovery Plan Execution", function="Recover"),
Outcome(subcat_id="RC.RP-04", summary="Post-incident operational norms are established.", category="Incident Recovery Plan Execution", function="Recover"),
Outcome(subcat_id="RC.RP-05", summary="Restored systems are validated and confirmed.", category="Incident Recovery Plan Execution", function="Recover"),
Outcome(subcat_id="RC.RP-06", summary="Recovery completion is declared and documented.", category="Incident Recovery Plan Execution", function="Recover"),

Outcome(subcat_id="RC.CO-03", summary="Recovery progress is communicated to stakeholders.", category="Incident Recovery Communication", function="Recover"),
Outcome(subcat_id="RC.CO-04", summary="Public recovery updates are issued appropriately.", category="Incident Recovery Communication", function="Recover"),

        ])
    db.commit()
    db.close()
    print("Seed complete.")

if __name__ == "__main__":
    run()
