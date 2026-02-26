from agents.evaluation_agent import judge_grounding, parse_judge_output
from governance.policy import governance_decision
from governance.pii_detector import detect_pii
from governance.audit_log import write_audit_log


class MCPRouter:
    def __init__(self, threshold: float = 0.7):
        self.threshold = threshold

    def route(self, question: str, context: str, answer: str):
        pii_hits = detect_pii(answer)

        raw_judge = judge_grounding(question, context, answer)
        judge_result = parse_judge_output(raw_judge)

        decision = governance_decision(judge_result, threshold=self.threshold)

        final_decision = {
            "allow": decision["allow"] and not pii_hits,
            "escalate": decision["escalate"] or bool(pii_hits),
            "pii_hits": pii_hits,
            "judge": judge_result
        }

        event = {
            "question": question,
            "answer": answer,
            "decision": final_decision
        }
        write_audit_log(event)

        if final_decision["allow"]:
            return {"status": "allowed", "response": answer}
        else:
            return {
                "status": "blocked",
                "response": "⚠️ Your request has been escalated for human review due to governance policy.",
                "details": final_decision
            }