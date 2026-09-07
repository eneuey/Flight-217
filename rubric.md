Your task:

Using the supplied synthetic Flight 217 data and starter code, construct two different warranted stories:

    1. one descriptive table or chart about represented flight conditions or outcomes; and
    2. one simple predictive model estimating whether a represented service day will arrive at least 30 minutes late.

Create a short analysis contract naming the audience, question, story mode, possible action, prediction boundary, and one claim the evidence cannot support. Use an agent for one bounded code change and preserve your instruction, the change, two checks, and your judgment.

Prediction boundary and claim discipline:

Use this target:

    Using information available four hours before scheduled gate arrival, will a synthetic Aster 217 service day finish at least 30 minutes late to the gate?

Determine what each row represents and distinguish fields known four hours before scheduled gate arrival from fields known only later. Calculate the majority-class baseline, fit the supplied shallow tree, and compare their held-out results. Do not add final_gate_wait_min or another field whose value would not exist at the prediction boundary.

You may conclude:

    The fitted tree classified held-out synthetic rows under this split.

The current evidence does not justify claiming:

    The model understands flight delay, explains its causes, will work for a real airline, or should control an operational decision.

Submission:

Submit the completed starter notebook or script and one concise record containing:

- descriptive story and artifact;
- predictive story, baseline, and result;
- analysis contract;
- agent contribution and two checks;
- one demonstrated capability; and
- at least three important questions the score does not answer.

Completion rubric — 100 points:

Criterion:	Full-credit evidence -> Points

Reproducible execution and required files:	Submitted files run with the specified data, reproduce the reported result, and include every required component. -> 20 points

Descriptive story and appropriate artifact:	The question is descriptive; the table or chart accurately shows a relevant pattern, uses clear labels and context, and supports a bounded claim. -> 20 points

Predictive model and baseline:	The majority-class baseline and shallow decision tree both run; the target and prediction boundary are correct; the held-out comparison is reported accurately. -> 20 points

Analysis contract and correct story modes:	The contract names the audience, question, story mode, possible action, prediction boundary, and unsupported claim, and it distinguishes description from prediction. -> 15 points

Agent-use record and two meaningful checks:	The submission preserves the exact instruction, bounded change, visible result, two independently reasoned checks, and the student's acceptance or rejection judgment. -> 15 points

Honest unsupported claim and unresolved questions:	The submission states one claim the evidence cannot support and at least three substantive questions the score does not answer. -> 10 points

Total -> 100
