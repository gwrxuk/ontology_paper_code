import re

PREFIX = re.compile(r'^[A-Za-z&.\s]+\|\s*')  # publisher prefixes: "PYMNTS | ..."
EXPLAINER = re.compile(r'(^\s*(here\s+)?(how|why|what|which|guide|top\s+\d+)\b)|\?|(\bvs\b\.?)|(\b\d+\s+ways\b)', re.I)
AI_SUBJ = re.compile(r'^(the\s+|new\s+|these\s+)?(healthcare\s+|enterprise\s+)?(ai\s+agents?|agentic\s+ai|autonomous\s+(ai|agents?)|ai|agents?|chatbots?|bots?)\s+\w+', re.I)
ORG_VERBS = (r'launch|unveil|introduc|debut|roll|release|deploy|bring|add|partner|invest|bet|build|expand|'
             r'acquir|announc|open|integrat|offer|push|plan|report|say|warn|use|get|becom|put|lead|throw|'
             r'want|showcase|aim|make|team|sign|help|win|buy|sell|adopt|test|pilot|hire|cut|move|turn|give|see|reveal')
ORG_SUBJ = re.compile(r'^([A-Z][\w&.\-]*(\s+(?:[A-Z&][\w&.\-]*|\d+|of|and|the|for))*?)\s+(?i:((may|might|will|could|to)\s+)?(' + ORG_VERBS + r'))')

def code_v2(t):
    t = PREFIX.sub('', t.strip())
    if EXPLAINER.search(t): return "explainer"
    if AI_SUBJ.match(t): return "machine"
    if ORG_SUBJ.match(t): return "org"
    return "other"
