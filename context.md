Flight 217 is a fictional Aster Air flight from Paris to New York. Its destination, Harbor International Airport, is also fictional. The gates, terminals, operating rules, organizations, people, and events are teaching constructs.

The aircraft leaves Paris on time. During the Atlantic crossing, its progress and changing weather indicate that it will reach New York later than planned. The revised arrival creates a gate conflict. Flight 217's assigned gate will be occupied.

An Aster operations assistant searches the gate schedule. It proposes Gate 41 because the schedule marks the gate open.

Elena Park, an Aster network operations controller, rejects the proposal. Gate 41's secure international-arrival corridor is closed for maintenance. The gate is empty, but Flight 217 cannot use it.

The assistant did not make an arithmetic error. It reasoned from a representation that omitted a decisive constraint.

Elena's screens show fragments:

aircraft position and progress reports;
planned and estimated arrival times;
weather observations and forecasts;
runway, gate, and ground-resource status;
passenger connections and service requests;
aircraft and crew schedules; and
messages from people in the aircraft, airline, airport, and terminal.
No screen contains the whole system. Some values describe the past. Some report the present. Some predict the future. Some are stale, missing, or wrong. Elena must distinguish among them while the aircraft continues toward New York.

The same flight returns throughout the book, but its boundary expands only when the question requires it:

one aircraft
→ observations and forecasts
→ a trajectory and arrival process
→ a gate and ground-resource problem
→ passenger and baggage connections
→ aircraft, crew, and flight networks
→ simulated arrival worlds
→ optimized but unresolved tradeoffs
→ bounded agents and coordinated action
→ feedback and revision
No participant controls the entire response. The flight crew, airline, airport, terminal personnel, ground teams, and air traffic organization have different information and authority. The assistant may help them coordinate, but capability does not create permission.

All Flight 217 observations, model results, and decisions are fictional. The course datasets are generated from explicit assumptions and recorded seeds. Synthetic data lets readers inspect the generating process. It does not provide evidence about a real airline, airport, or aviation system.

The case keeps one question visible:

What must humans and machines preserve as observations become predictions, predictions become decisions, and decisions change the world?

A prediction before an explanation
Flight 217 is now crossing the Atlantic. Strong headwinds and difficult destination conditions suggest that it will arrive late.

Elena Park needs more than an impression. A late arrival could create a gate conflict, missed passenger connections, displaced crews, and delays for later flights. She asks a narrow question:

Given what Aster knows at this point in the flight, will Flight 217 reach its gate at least 30 minutes late?

Aster has a teaching dataset containing 720 synthetic flights on the same fictional service. Each row represents one historical service day. Every record describes the information available at a common prediction snapshot and the outcome generated later.

The records are synthetic. They were created by a documented program with a fixed random seed. They are not evidence about a real airline, airport, or aviation process.

Load the data:

import pandas as pd

flights = pd.read_csv("flight217_build_zero.csv")
print(flights.head())
print(flights.shape)
The table has identifiers, observations, forecasts, realized outcomes, and one label. These are not the same kind of thing merely because they share a file.

Field	Provisional meaning	Status at prediction time
flight_id	Synthetic service-day identifier	known
departure_delay_min	Difference between actual and scheduled departure	observed
headwind_kts	Estimated route headwind at the snapshot	forecast-derived
destination_weather_index	Synthetic severity index from 0 to 10	forecast-derived
arrival_demand_index	Synthetic arrival congestion index from 0 to 10	forecast-derived
weather_snapshot_age_min	Age of the weather snapshot	observed metadata
final_gate_wait_min	Waiting time after landing	not yet known
arrival_delay_min	Difference between scheduled and actual gate arrival	later outcome
late_30	Whether gate arrival was at least 30 minutes late	later label
Already, a choice has been made. Late means late to the gate, not late to the runway. Thirty minutes is a policy threshold, not a property of nature.

For now, keep moving.

Look before fitting
A model should not be the first thing you run on an unfamiliar table. Begin with a few checks:

print(flights.dtypes)
print(flights.isna().sum())
print(flights["late_30"].value_counts(normalize=True))
Then draw one graph:

import matplotlib.pyplot as plt

colors = flights["late_30"].map({0: "#4C78A8", 1: "#E45756"})
flights.plot.scatter(
    x="headwind_kts",
    y="arrival_delay_min",
    c=colors,
    alpha=0.55,
)
plt.axhline(30, color="black", linestyle="--")
plt.show()
The dashed line defines the label. Flights above it count as late. The graph suggests that stronger headwinds accompany larger delays, but it does not show that headwind alone determines the outcome. Flights with similar headwinds can finish on different sides of the threshold.

That variation is not an inconvenience to remove. It is part of the problem.

Establish a baseline
Suppose most flights are not 30 minutes late. A system could predict not late for every row and appear competent.

majority_class = flights["late_30"].mode().iloc[0]
baseline_accuracy = (flights["late_30"] == majority_class).mean()
print(baseline_accuracy)
The baseline is intentionally unimpressive. It establishes the performance a model must beat before complexity earns attention.

Accuracy also hides the direction of error. Predicting that a seriously late flight will be on time may have different consequences from issuing a false warning. We will return to that problem.

Fit the tree
Use four fields that exist at the prediction snapshot:

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

features = [
    "departure_delay_min",
    "headwind_kts",
    "destination_weather_index",
    "arrival_demand_index",
]

X = flights[features]
y = flights["late_30"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=217,
    stratify=y,
)

tree = DecisionTreeClassifier(max_depth=4, random_state=217)
tree.fit(X_train, y_train)
The tree learns a sequence of questions. A simplified branch might ask whether departure delay exceeds one value, then whether weather severity exceeds another. The program selects those questions to reduce classification error in the training data.

The code is short. The commitments behind it are not.

We selected one target, four features, a random split, a maximum depth, and an implicit treatment of every row as comparable. We did not ask the algorithm to decide whether those choices were meaningful.

Inspect the result
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.tree import export_text

predictions = tree.predict(X_test)

print("Tree accuracy:", accuracy_score(y_test, predictions))
print(confusion_matrix(y_test, predictions))
print(export_text(tree, feature_names=features))
The confusion matrix separates four outcomes:

Actual condition	Model prediction	Common name
not late	not late	true negative
not late	late	false positive
late	not late	false negative
late	late	true positive
The model should outperform the majority baseline on this synthetic test set. That is evidence about these rows under this procedure. It does not establish that the model will generalize to next year, another route, a changed weather system, or a real airline.

Let an agent make one bounded change
You do not need to wait until Chapter 13 to work with an agent. Ask one now to add a labeled display of the confusion matrix.

Use a bounded request:

In the supplied Build Zero program, add a readable confusion-matrix display.
Do not change the dataset, feature list, target, split, random seed, model, or
predictions. Show me the proposed edit and explain how I can test that the
underlying four counts did not change.
Before accepting its code, record what must remain true:

the same test rows are used;
the same model produces the same predictions;
the four displayed cells sum to the test-set size;
the cells equal the original confusion_matrix output; and
the axes make actual and predicted classes unambiguous.
Run the change. Compare the counts. Read the edited lines. If the agent quietly refits the model, changes a label order, or reports percentages without counts, repair the result or reject it.

This small exercise introduces the course's working relationship with AI:

specify
→ delegate
→ inspect
→ test
→ accept, repair, or reject
The agent can produce code quickly. It cannot decide that the task was the right one, that the test is sufficient, or that the result deserves authority. Those obligations remain with you.

Now give it the current Flight 217 snapshot:

current_flight = pd.DataFrame(
    [{
        "departure_delay_min": 0,
        "headwind_kts": 48,
        "destination_weather_index": 7.5,
        "arrival_demand_index": 8.5,
    }]
)

prediction = tree.predict(current_flight)[0]
probability = tree.predict_proba(current_flight)[0, 1]

print("Predicted late_30:", prediction)
print("Tree-leaf late share:", probability)
The program returns a classification and a number. It has completed the task we gave it.

What, exactly, has it told us?

The questions the score cannot answer
The model has no understanding of a passenger, a gate, or an airport. It sees four numerical columns and a label. That limitation does not make the model useless. It defines what remains to be established.

What world did the table describe?
The model treats each row as a flight. Is the relevant object a scheduled flight, an aircraft movement, a passenger journey, or an evolving arrival process? Flight 217's consequences extend beyond its row.

Chapter 1 will establish the domain and boundary.

How did the values become data?
headwind_kts looks precise. Was it observed by the aircraft, estimated from a weather model, averaged across a route, or copied from a stale report? The answer changes what the value can support.

Chapter 2 will reconstruct the observation process.

What do the columns mean?
The weather and demand indices run from 0 to 10. Does a difference from 8 to 6 mean twice as much as a difference from 3 to 2? Is late_30 an observed property or a label created from two timestamps and a policy threshold?

Chapter 3 will separate meaning, measurement, type, and encoding.

What did the table hide?
Rows and columns make fitting convenient. They can hide temporal updates, flight dependencies, passenger connections, gate compatibility, and the age of each observation.

Chapter 4 will compare representations and their losses.

What kind of claim did the model produce?
The output is not a fact about the future. It is a result from a trained artifact applied to a represented state. Its warrant depends on evidence, assumptions, and use.

Chapters 5–8 will distinguish information, belief, models, inference, and uncertainty.

Was the prediction honestly evaluated?
The random split may place nearby service days in both training and test data. Conditions may change over time. Accuracy may hide costly false negatives. The number printed by predict_proba is a leaf proportion, not automatically a well-calibrated probability.

Chapter 8 will rebuild and evaluate the prediction.

Did the model explain the delay?
A feature used by a successful predictor is not necessarily a cause. Changing that feature in a row does not prove that an intervention would change the world.

Chapter 9 will separate prediction from causal reasoning.

What should anyone do?
Even a reliable warning would not identify the best response. The system must explore possible arrival plans, expose tradeoffs, and respect constraints and authority.

Chapters 10–16 will move from simulation and optimization to action, feedback, and responsibility.

A deliberate omission
The table includes final_gate_wait_min. Adding it to the feature list may improve the score. Do not add it yet.

At the prediction snapshot, the aircraft has not landed. Final gate waiting time does not exist as an observed value. Using it would allow the model to learn from part of the outcome it claims to predict. This is leakage.

The column is present because stored data often combines values that became known at different times. A dataframe does not enforce chronology. The analyst must.

Save the first artifact
Record five items:

the prediction question;
the target and four features;
the baseline and tree result;
one useful capability the program demonstrated; and
three questions that must be answered before anyone acts on its output.
Keep this one-page record. You will revise it as the book proceeds. By Chapter 8, you should be able to rebuild the predictive task. By Chapter 17, the model should occupy a traceable place inside a knowledge system rather than standing alone as a score.

For now, we have a smaller and stranger problem.

The tree classified a flight, but the table did not explain what world its rows selected, what the observations omitted, or what its values meant. Chapter 1 begins there: with the boundary between the world and the representation. Chapter 12 later returns to the harder question of which capabilities, if any, we should call intelligent.