from agent.rag.rag_knowledge_base import RAG_KNOWLEDGE_BASE

def retrieve_rules(user_input: str):
    """
    Retrieve relevant pet care rules based on user input.
    This provides context without influencing scheduling decisions.
    """
    user_input = user_input.lower()
    results = []

    if "feed" in user_input or "food" in user_input:
        results.extend(RAG_KNOWLEDGE_BASE["feeding"])

    if "walk" in user_input:
        results.extend(RAG_KNOWLEDGE_BASE["walking"])

    if "med" in user_input or "medicine" in user_input:
        results.extend(RAG_KNOWLEDGE_BASE["medication"])

    if "schedule" in user_input or "time" in user_input:
        results.extend(RAG_KNOWLEDGE_BASE["scheduling"])

    return results