import streamlit as st
import json
import os

from mcp.router import MCPRouter
from agents.support_agent import support_answer

AUDIT_LOG_PATH = "data/audit_log.jsonl"

st.set_page_config(page_title="AI Governance MCP Bot", layout="wide")
st.title("🛡️ AI Governance MCP Bot – Live Demo")

router = MCPRouter(threshold=0.7)

tab_chat, tab_escalation = st.tabs(["💬 Live Chat", "🚨 Escalations"])

with tab_chat:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💬 Customer Chat")
        question = st.text_input("User question", "How can I reset my password?")
        context = st.text_area("RAG Context", "You can reset your password by clicking Forgot Password on the login page.")

        if st.button("Send"):
            answer = support_answer(question, context)
            result = router.route(question, context, answer)

            if result["status"] == "allowed":
                st.success("✅ Response allowed")
                st.write(result["response"])
            else:
                st.error("🚨 Blocked & Escalated by Governance")
                st.write(result["response"])
                st.json(result["details"])

    with col2:
        st.subheader("📊 Risk & Governance Signals")

        if os.path.exists(AUDIT_LOG_PATH):
            with open(AUDIT_LOG_PATH, "r") as f:
                lines = f.readlines()

            if lines:
                last_event = json.loads(lines[-1])
                judge = last_event["decision"]["judge"]

                confidence = judge.get("confidence", 0.0)
                grounded = judge.get("grounded", False)
                pii_hits = last_event["decision"].get("pii_hits", {})

                st.metric("Grounded", "Yes" if grounded else "No")
                st.metric("PII Detected", "Yes" if bool(pii_hits) else "No")

                st.write("Confidence Score")
                st.progress(min(max(confidence, 0.0), 1.0))

                if not grounded or confidence < 0.7 or pii_hits:
                    st.warning("⚠️ High Risk Output – Escalated")
                else:
                    st.success("Low Risk Output")
            else:
                st.info("No audit events yet.")
        else:
            st.info("No audit logs yet.")

with tab_escalation:
    st.subheader("🚨 Escalated Cases")

    if os.path.exists(AUDIT_LOG_PATH):
        escalations = []
        with open(AUDIT_LOG_PATH, "r") as f:
            for line in f.readlines():
                event = json.loads(line)
                if event["decision"].get("escalate"):
                    escalations.append(event)

        if escalations:
            st.dataframe(escalations[-50:])
        else:
            st.info("No escalated cases yet.")
    else:
        st.info("No audit logs yet.")