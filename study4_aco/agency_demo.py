"""Agency Configuration Ontology (ACO) — executable demonstration.

A minimal A2A-style agent system implementing the three mechanisms
identified in the document analysis: registration (AgentCards),
authorization (permissions shared by humans and agents), and
accountability (audit lineage). Run: python3 agency_demo.py
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
import json


class TaskState(Enum):  # A2A spec v1.0 lifecycle
    SUBMITTED = "submitted"
    WORKING = "working"
    INPUT_REQUIRED = "input-required"
    AUTH_REQUIRED = "auth-required"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"
    REJECTED = "rejected"


@dataclass
class AgentCard:  # registration: agency as a declarable, signable identity
    name: str
    provider: str
    skills: list
    security_schemes: list
    signature: str = "sig:demo"


@dataclass
class ActionType:  # authorization: verbs are pre-defined in the ontology
    verb: str
    required_permission: str
    requires_human_approval: bool = False


@dataclass
class AuditRecord:  # accountability: records without reasons
    time: str
    actor: str
    action: str
    outcome: str


class Ontology:
    """The schema layer where 'AI or I?' is answered before interaction."""

    def __init__(self):
        self.registry = {}          # AgentCards: who exists as an actor
        self.action_types = {}      # verbs: what can be done at all
        self.grants = set()         # (actor, permission): who may do it
        self.audit_log = []         # lineage: what was done, by whom, when

    # -- registration ------------------------------------------------
    def register(self, card: AgentCard):
        self.registry[card.name] = card
        self._audit(card.name, "register", "card published & verified")

    def define_action(self, at: ActionType):
        self.action_types[at.verb] = at

    # -- authorization -----------------------------------------------
    def grant(self, actor: str, permission: str):
        self.grants.add((actor, permission))
        self._audit("ontology-admin", f"grant:{permission}->{actor}", "granted")

    # -- action execution with full configuration check ---------------
    def execute(self, actor: str, verb: str, human_approver=None) -> TaskState:
        # 1. registration check: unregistered entities are not actors
        if actor not in self.registry:
            self._audit(actor, verb, "REJECTED: not a registered actor")
            return TaskState.REJECTED
        # 2. the verb must exist in the ontology
        if verb not in self.action_types:
            self._audit(actor, verb, "REJECTED: action type not in ontology")
            return TaskState.REJECTED
        at = self.action_types[verb]
        # 3. capability declaration: the card must declare the skill
        if verb not in self.registry[actor].skills:
            self._audit(actor, verb, "REJECTED: capability not declared on card")
            return TaskState.REJECTED
        # 4. authorization: permission must be granted to this actor
        if (actor, at.required_permission) not in self.grants:
            self._audit(actor, verb, "FAILED: permission not granted")
            return TaskState.FAILED
        # 5. institutionalized human checkpoint (auth-required)
        if at.requires_human_approval:
            if human_approver is None:
                self._audit(actor, verb, "AUTH-REQUIRED: awaiting human principal")
                return TaskState.AUTH_REQUIRED
            self._audit(human_approver, f"approve:{verb}", "human authorization given")
        self._audit(actor, verb, "COMPLETED")
        return TaskState.COMPLETED

    # -- accountability -----------------------------------------------
    def _audit(self, actor, action, outcome):
        self.audit_log.append(AuditRecord(
            datetime.now(timezone.utc).isoformat(timespec="seconds"),
            actor, action, outcome))


if __name__ == "__main__":
    onto = Ontology()

    # The schema is written BEFORE any interaction happens:
    onto.define_action(ActionType("summarize_report", "perm:read"))
    onto.define_action(ActionType("send_payment", "perm:pay",
                                  requires_human_approval=True))
    onto.register(AgentCard("assistant-agent", "DemoCorp",
                            skills=["summarize_report", "send_payment"],
                            security_schemes=["oauth2"]))
    onto.grant("assistant-agent", "perm:read")
    onto.grant("assistant-agent", "perm:pay")

    print("== Scenario 1: unregistered entity attempts to act")
    print("   ->", onto.execute("rogue-agent", "summarize_report").value)

    print("== Scenario 2: registered agent, authorized routine action")
    print("   ->", onto.execute("assistant-agent", "summarize_report").value)

    print("== Scenario 3: consequential action hits the human checkpoint")
    print("   ->", onto.execute("assistant-agent", "send_payment").value)

    print("== Scenario 4: same action after human approval")
    print("   ->", onto.execute("assistant-agent", "send_payment",
                                human_approver="human-principal").value)

    print("== Scenario 5: action outside the ontology's verb repertoire")
    print("   ->", onto.execute("assistant-agent", "delete_database").value)

    print("\n== Audit lineage (accountability: records without reasons)")
    for r in onto.audit_log:
        print(f"   {r.time}  {r.actor:<18} {r.action:<28} {r.outcome}")
