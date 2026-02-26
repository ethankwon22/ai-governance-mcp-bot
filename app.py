from mcp.router import MCPRouter
from agents.support_agent import support_answer

def main():
    question = "How can I reset my password?"
    context = "You can reset your password by clicking Forgot Password on the login page."

    answer = support_answer(question, context)

    router = MCPRouter(threshold=0.7)
    result = router.route(question, context, answer)

    print("Router Result:", result)


if __name__ == "__main__":
    main()