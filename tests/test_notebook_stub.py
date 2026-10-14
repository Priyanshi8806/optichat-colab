"""Executes the notebook's non-Colab cells with a STUB generate(): 'qwen' = oracle, 'llama' = deliberately flawed.
Purpose: verify notebook plumbing, tools, scoring and scoreboard. Says nothing about real Qwen/Llama quality."""
import json, re, sys, nbformat, traceback
nb = nbformat.read(sys.argv[1], as_version=4)
ns = {"__name__": "__main__"}
ns["LLMS_KEYS"] = ["qwen", "llama"]; ns["FAST"] = False

def generate(key, role, system, user, history=None, max_new_tokens=0):
    g = ns; bad = key == "llama"
    if role == "component_interpretation":
        names = json.loads(re.search(r"Components to describe:\n-----\n(.*?)\n-----", system, re.S).group(1))
        d = {n: g["DESC"].get(n, "a model component") for n in names}
        if bad: d.pop(names[0])
        return json.dumps(d)
    if role == "model_illustration": return "This model helps suppliers and roasteries plan capacity and contracts to minimise cost per kg."
    if role == "iis_inference": return "The roasteries' need exceeds total supplier capacity, so the need and capacity constraints conflict." if not bad else "Something is wrong."
    if role == "coordinator":
        conv = user.split("Conversation:\n", 1)[1]
        if "Explainer:" in conv: return json.dumps({"agent_name": "Explainer", "task": "DONE"})
        if "What is this model about" in conv or "mean" in conv: return json.dumps({"agent_name": "Explainer", "task": "explain"})
        if bad and "S1 ship" in conv: return json.dumps({"agent_name": "Explainer", "task": "explain"})
        return json.dumps({"agent_name": "Engineer", "task": "run tool"})
    if role == "explainer":
        res = json.loads(user.split("Tool results: ", 1)[1])
        txt = f"Objective moves from {res.get('objective_before')} to {res.get('objective_after')}."
        return txt + (" That is about 7.5% higher." if bad else "")
    if role == "syntax_reminder":
        q = user.split("User query: ", 1)[1]
        for mk, qq, f, c in g["SYN"]:
            if qq == q: return json.dumps({"function": f, "component": ("capacity" if bad and c == "need" else c)})
        if "How much should" in q: return json.dumps({"function": "feasibility_restoration", "component": "need"})
        if "What if" in q: return json.dumps({"function": "evaluate_modification", "component": "demand"})
        if "sensitive" in q: return json.dumps({"function": "sensitivity_analysis", "component": "demand"})
        return json.dumps({"function": "external_tools", "component": None})
    if role == "operator":
        f = re.search(r"reminder: (\w+)", user).group(1)
        a = {"feasibility_restoration": {"component": "need", "index": ["roastery2"]},
             "components_retrieval": {"component": "capacity_in_supplier", "index": ["S3"]},
             "sensitivity_analysis": {"component": "demand", "index": ["west"]},
             "evaluate_modification": {"component": "demand", "index": ["east"], "operation": "+", "delta": 100}}[f]
        if bad and f == "components_retrieval": a = {"component": "capacity_in_supplier", "index": ["S9"]}
        return json.dumps({"function": f, "args": a})
    if role == "programmer":
        for cid, mk, inp, q, snip in g["WHYNOT"]:
            if q in user:
                if bad and cid == "ex2": snip = snip.replace(">=", "<=")
                return "```python\n" + snip + "\n```"
    if role == "evaluator":
        return json.dumps({"decision": "reject" if '"error"' in user.split("Execution result:")[1] else "accept", "comment": "stub"})
    raise RuntimeError("stub: unhandled " + role)
ns["generate"] = generate

for i, c in enumerate(nb.cells):
    if c.cell_type != "code" or "colab-only" in c.metadata.get("tags", []): continue
    try: exec(compile(c.source, f"<cell {i}>", "exec"), ns)
    except Exception:
        print(f"!!! CELL {i} FAILED\n{c.source[:200]}\n"); traceback.print_exc(); sys.exit(1)
print("\nNOTEBOOK STUB RUN OK")
