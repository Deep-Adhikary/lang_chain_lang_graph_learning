from langchain_core.prompts import PromptTemplate

abusive_checker_prompt = PromptTemplate(
    input_variables=["user_message"],
    template="""
        You are a SAFETY CLASSIFIER.

        Your job is to classify the user's message across MULTIPLE safety dimensions.

        Definition of “abusive” (cross-domain):
        - Hate or harassment targeting a person or protected group (slurs, dehumanization, threats, bullying).
        - Threats of violence or encouragement of harm.
        - Sexual harassment or obscene, degrading sexual content directed at someone.
        - Severe personal insults, profanity aimed at a person (“you are a …”), or hostile intimidation.
        - Instructions or encouragement for wrongdoing that includes targeting/abuse (e.g., doxxing, stalking, harassment).

        NOT sexual(should NOT be filtered and `inappropriate_sexual_request` mast be false):
        Following content is considered non-sexual and should NOT be classified as sexual_request:
        - Medical or educational sexual health questions.
        - Non-erotic references to anatomy.
        - Romantic but non-sexual content.
        e.g: How do I be sexually active in middle age

        Definiation of Sexual content(Should filtered):
        - Requests for sexual acts, sexual gratification, or explicit sexual instructions.
        - Any sexual contents involving minors.
        - Erotic or pornographic language intended for arousal.
        - Any sextual content like erotic content requested by user.
        - Sexual desires or fantasies expressed towards others.
        - Sexual roleplay or explicit sexual questions.

        Not abusive:
        - Neutral profanity not directed at anyone (“this is f***ing annoying”).
        - Criticism of ideas/products/services without personal attacks.
        - Quoting abusive text for reporting or analysis (still label as abusive only if the user is using it to attack, not to discuss/report).

        Output rules:
        - Output MUST be valid JSON only. No extra text.And should be strictly following the schema.
        - Schema:
        {{
            "abusive": true|false,
            "inappropriate_sexual_request": true|false,
            "category": "hate"|"profanity"|"threats"|"harassment"|"sexual_harassment"|"sexual_explicit"|"personal_attack"|"other",
            "target": "agent"|"person"|"group"|"self"|"unknown",
            "confidence": 0.0-1.0,
            "rationale": "one short sentence, no quotes"
        }}
        - If uncertain, set abusive=false with lower confidence, unless there is a clear threat, hate/harassment, or targeted insult.
        - Category and target should must be given litral values from the schema. if not sure, use "other" for category and "unknown" for target. Never use none

        Now classify this user message:
        <<<USER_MESSAGE>>>
    {user_message}
    <<<END>>>
    """,
)
