# Convergence Guard — Explained Simply

> This document is not the canonical protocol and is not a replacement for [`SKILL.md`](../SKILL.md).
> It explains the architecture of Convergence Guard v0.2.2 in plain language and through child-friendly analogies.

## 1. The shortest possible idea

Imagine that you need to solve a difficult mystery.

A bad approach is to hear the first plausible explanation and immediately say:

> "It is probably this."

After that, the mind starts looking for evidence that confirms exactly that version.

Convergence Guard exists to prevent that from happening too early.

It makes the process go roughly like this:

1. First separate facts from guesses.
2. State precisely what actually needs to be decided.
3. Have several independent "investigators" search for different explanations.
4. Do not let them peek at one another's conclusions in advance.
5. Separately check which explanations fit the facts and which merely sound convincing.
6. Compare the remaining strong explanations.
7. Check whether they rest on a single fragile assumption.
8. Decide separately which explanation seems most plausible and which action is best to take now.
9. If there is too little evidence, do not pretend the answer is already known.
10. End with the cheapest worthwhile, feasible test that could change the decision, or explicitly state that no such test was identified.

In brief:

> Do not grab onto the first reasonable explanation. First check what other explanations are possible, which of them survive the facts, and what can be tested quickly before making an expensive decision.

The five phases can be remembered as five simple images:

> **A — crime-scene investigator:** first collects the traces and does not rush to accuse anyone.
>
> **B — several detectives take different streets:** each searches in a different direction instead of following the first lead.
>
> **C — two librarians independently sort the same stack of books:** one evaluates quality, while the other groups by topic and similarity without seeing the first librarian's ratings.
>
> **D — load-testing rig:** strong explanations are not admired; they are deliberately loaded and tested for failure.
>
> **E — captain choosing a course in fog:** separately decides which map seems more plausible and which direction is safer to take now.

---

## 2. Why one very smart answer is sometimes not enough

Imagine a school mystery:

> A classroom window is broken. Who is responsible?

There is a ball on the floor.

The first child immediately says:

> "Someone was probably playing with the ball and hit the window."

That is perfectly reasonable.

But then a danger appears: everyone starts discussing only the ball.

Even though the window could have broken in another way:

- it was struck from outside;
- it had cracked earlier and fell apart because of a draft;
- someone pushed a table;
- the ball only ended up nearby after the window had already broken.

The problem is not that the first explanation is bad.

The problem is that it can become an **anchor** too early.

Convergence Guard tries to delay that moment.

---

## 3. Phase A — the crime-scene investigator

The main image for this phase is: **do not accuse Vasya before you understand what actually happened**.

First we collect traces, separate facts from reports and guesses, and only then formulate the real question.

### 3.1. Facts separate from guesses

Suppose we are investigating the broken window.

We need to distinguish:

**Confirmed fact:**

> The window is broken.

**A person's report:**

> Petya says he heard the impact of a ball.

**A strong inference, but not a direct observation:**

> The impact probably happened recently because the glass is still on the floor and nobody has cleaned it up yet.

**Hypothesis:**

> The ball broke the window.

**Constraint:**

> The camera cannot be checked because it is broken.

**Open question:**

> Was the ball in the classroom before the window broke?

This matters because otherwise a guess very quickly starts to look like a fact.

### 3.2. Have we even framed the problem correctly?

Suppose the teacher asks:

> "How do we stop children from playing ball in the classroom so they do not break windows anymore?"

The answer is already hidden inside that question:

> the cause is ball play.

But we have not proved that yet.

Convergence Guard should ask:

> "Are we sure we are solving the right problem?"

Perhaps the real problem is old glass.

Or the sports field is too close to the windows.

Or the window opens in a dangerous way.

So before choosing a solution, we need to test the question itself.

---

## 4. Phase B — several detectives take different streets

The main image for this phase is: **not three people standing in one line, but three search teams**.

Now imagine three child detectives.

All of them receive the same facts:

> the window is broken; there is a ball nearby; Petya heard a bang; the camera does not work.

But each receives a somewhat different search area.

### Detective A

Looks for causes inside the classroom.

For example:

> someone was playing with the ball;
> someone pushed a table;
> an object fell from a shelf.

### Detective B

Looks for causes outside the classroom.

For example:

> something flew in from outside;
> the window had been damaged from the outside;
> vibration or construction nearby.

### Detective C

Looks for causes in the window itself and in the conditions around it.

For example:

> old glass;
> a temperature change;
> a previous crack.

The important point is that these are not "three characters with different personalities."

They are three different directions for causal search.

---

## 5. Why you cannot simply ask three children one after another in the same room

Suppose Petya says first:

> "It was Vasya."

Then Masha hears that and starts thinking.

Even if she tries to be objective, the idea about Vasya is already in her head.

So if she later says:

> "I also think it was Vasya."

we no longer know whether she really arrived at that conclusion independently.

This gives us an important principle:

> Several answers do not become independent merely because they were given several times.

---

## 6. Phase C — two librarians independently sort the same stack of books

After the detectives bring back many explanations, two different checks begin.

They are deliberately separated.

Imagine two librarians who are given the same stack of books.

The first librarian checks each book for quality: whether it fits our task, how reliable it is, and whether it has obvious problems.

The second does not see the first librarian's ratings. They sort the books by topic: which are really about the same thing, which are different, and which complement one another.

Only after both have finished can their results be combined.

### 6.1. Reviewer #1: how good is each explanation?

They ask:

- does the explanation fit the task;
- is it supported by facts;
- does it contain a reasonable causal chain;
- can it be tested;
- how dangerous would it be to be wrong.

For example:

> "The ball broke the window" — plausible, but not yet proved.

> "Aliens broke the window" — barely connected to the available facts and difficult to test.

### 6.2. Reviewer #2: which explanations are actually different?

They must not know in advance which explanation received good ratings.

Their job is different.

They build a map:

> These two explanations are almost the same.

> These two can both be true at the same time.

> These two contradict each other.

> This explanation is part of a broader explanation.

For example:

> "old glass" and "a previous crack" may belong to the same causal family.

While:

> "the ball hit the window" and "the glass had been weakened by a crack" may both be true at the same time.

So the problem cannot always be turned into:

> either A or B.

Sometimes the right answer is:

> A and B together.

---

## 7. Why the two librarians must not peek at each other's work

Imagine the first librarian has already put a bright note on one book:

> "Best explanation!"

Then the second librarian is told:

> "Now independently sort the books by topic and similarity."

But they have already seen that note.

They may start unconsciously building categories around the favorite.

So Convergence Guard first freezes two independent pieces of work:

1. the quality evaluation;
2. the map of causal families.

And only then combines them.

---

## 8. Keep only real finalists

If only two genuinely strong explanations remain after review, Convergence Guard does not have to invent a third "for symmetry."

The same rule applies if only one viable explanation remains after checking whether missing evidence or search coverage caused the collapse. Keep that one, but still stress-test its assumptions and shared blind spots. A lone survivor is not automatically confirmed.

If none remain supportable, do not rescue a rejected explanation just to keep the process moving. Say that causal attribution is insufficient and judge any low-regret action separately.

For example:

1. the ball really did hit the window;
2. the glass was already badly damaged and failed under ordinary stress.

That is enough.

There is no need to add:

3. a secret act of sabotage,

just because the template looks nicer with three items.

---

## 9. Phase D — the load-testing rig

The main image for this phase is: **do not admire the bridge — drive a truck onto it**.

Now the strong explanations are deliberately attacked to see whether they survive the load.

A separate dossier is created for each finalist.

Suppose the explanation is:

> "The ball broke the window."

We need to ask:

- what exactly must be true for this explanation to work;
- what should we observe if it is true;
- what could disconfirm it;
- what happens if we believe it and are wrong.

For example:

Assumption:

> the ball was heavy enough and moving fast enough.

Prediction:

> the glass should show an impact point consistent with being struck by an object.

Disconfirmation:

> it turns out the ball was locked in a cabinet until after the incident.

---

## 10. Test the most important assumptions

Imagine a house of cards.

Some cards support almost nothing.

One card, however, supports half the tower.

If that card falls, everything collapses.

Convergence Guard tries to find those "load-bearing cards" in the reasoning.

For example:

> The entire ball explanation depends on the assumption that the ball was even in the room.

That assumption matters more than ten minor details.

---

## 11. Look for a blind spot shared by all finalists

Imagine three detectives arguing:

> Vasya.

> Petya.

> Masha.

Then someone asks:

> "Did you even check whether a person broke the window?"

And it turns out nobody did.

That is a shared blind spot.

A very important part of Convergence Guard is not only comparing explanations, but also asking:

> "What mistake could all of our best explanations be making at the same time?"

---

## 12. Phase E — the captain chooses a course in fog

The main image for this phase is: **you do not need to know the whole ocean in order to choose the next safe turn**.

The captain may consider one sea chart the most plausible, yet choose a course that is safer even if that chart is wrong.

### Model judgment and Decision judgment are not the same thing

This is one of the most important ideas in the skill.

### Question 1

> Which explanation seems most plausible?

### Question 2

> What is the most sensible thing for us to do now?

The answers may differ.

Example.

We think the ball is the most likely cause of the broken window.

But replacing every window in the school with expensive shatter-resistant glass right now is costly and hard to reverse.

Installing a camera for a week is cheap, reversible, and produces new information.

So we can say:

> The most plausible explanation is the ball.

But:

> The best action right now is to install a camera first and collect data.

---

## 13. Sometimes the right answer is "we do not know yet"

A bad system feels obliged to choose a winner.

Convergence Guard should not do that.

If we have two good explanations and insufficient evidence, a normal answer is:

> There is not enough evidence to choose.

But the work does not stop there.

The next question is:

> What is the cheapest test we can run that could change the choice?

If no ethical, obtainable test is identified, say so and explain the search limits. Do not invent one. The explanation may remain unresolved even when a robust action is justified. A known test deferred because the analysis budget ran out is still an outstanding test.

---

## 14. The minimum discriminating test

Suppose two explanations are competing:

**Explanation A:** the ball broke the window.

**Explanation B:** the glass failed because of an old crack.

We do not need to collect a hundred new facts.

We need one fact that genuinely distinguishes these explanations.

For example:

> Have a specialist inspect the fracture pattern in the glass.

If the pattern looks like a point impact, A becomes stronger.

If the crack propagated from an old defect, B becomes stronger.

That is much more useful than simply "learning something else."

---

## 15. Why Convergence Guard should not run on every small problem

Imagine the program contains:

```text
x = 5
if x = 6 ...
```

and everything breaks because of it.

The cause is directly visible.

If Convergence Guard calls nine independent analysts, constructs five causal families, and stages a major debate, that is a bad use of the method.

A good result is:

> The cause was found directly. Full Mode is unnecessary. Fix the error and add a check so it does not return.

This is called a negative control: a check of whether the skill can recognize when the skill itself is barely needed.

---

# Part II. Why "different workers" are not necessarily independent

## 16. Three children in different rooms

Imagine a teacher wants three independent opinions.

The teacher puts Petya, Masha, and Kolya in three separate rooms.

That sounds fine.

But before they begin, the teacher tells each of them:

> "By the way, Petya thinks Vasya is responsible."

The rooms are separate, but now they share the same anchoring thought.

That is why the new Convergence Guard v0.2.1 rule is:

> A different chat or a separate worker does not, by itself, prove independence.

What matters is not where the worker sits, but **what actually entered its mind before the work began**.

---

## 17. The same blackboard in every classroom

Imagine an exam.

Three children are seated in different classrooms.

But the blackboard in every classroom already says:

> "Try answer 42."

Formally, they are not communicating.

But the experiment has already been contaminated.

The same thing can happen with extra context from:

- the parent chat;
- shared memory;
- other conversations in the same project;
- saved history from an old worker;
- a shared summary or handoff.

---

## 18. What a context allowlist means in plain language

It is a list of what the child is allowed to place on the desk before the exam.

For example:

```text
ALLOWED

✓ facts
✓ question
✓ real constraints
✓ own assignment

NOT ALLOWED

✗ other students' answers
✗ previous winner
✗ "the teacher thinks the correct answer is B"
✗ an old conclusion that the student is supposed to discover independently
```

A separate room does not matter if a cheat sheet is already on the desk.

---

## 19. The Vasya example: three people, but one source

Suppose:

Petya says:

> "There is a dinosaur outside!"

Masha says:

> "There is a dinosaur outside!"

Kolya says the same:

> "There is a dinosaur outside!"

It looks like we have three witnesses.

But then we discover:

- Petya heard it from Vasya;
- Masha heard it from Vasya;
- Kolya read Vasya's message.

We do not have three independent sources.

We have one Vasya repeated three times.

This explains the principle:

> Reasoning independence is not evidential independence.

Even several agents reasoning independently do not turn one data source into several independent pieces of evidence.

---

## 20. The news example

Five websites report the same story.

It may look like:

> "Five sources confirmed it."

But if all five simply rewrote Reuters, the true independent source is one.

The number of repetitions is not the number of independent pieces of evidence.

### A famous source is not automatically the truth

There is a second trap.

Suppose one article comes from a famous newspaper, one from a government agency, one from a peer-reviewed journal, and one from a strange activist blog.

Convergence Guard does **not** say:

> famous / official / peer reviewed = true

and it also does **not** say:

> fringe / partisan / anonymous = false

Instead it asks:

> What exactly is the claim, and what inspectable evidence carries that claim?

For example, if a government report says:

> "We assess that X probably happened."

we may be able to confirm that the agency really made that assessment. But if the supporting evidence is classified, we have **not** independently confirmed X itself.

Likewise, if a dubious blog links to a genuine original document, the blog is only a lead. We inspect the original document and let the document — not the blog's reputation — carry the evidential weight.

Useful roles are:

- **EVIDENCE** — directly bears on the claim;
- **CORROBORATION** — independently supports existing evidence;
- **CONTEXT** — helps interpret the situation;
- **LEAD ONLY** — tells us where to look next;
- **UNSUPPORTED** — currently too weak to affect the decision.

The rule is:

> Source reputation can tell us where to look first. It cannot replace claim-level provenance.

And the reverse shortcut is also forbidden: funding, ideology, institutional interest, missing raw data, or a low-prestige origin may justify extra checking, but they do not automatically make a claim false. For broad scientific questions, a transparent synthesis of many primary studies can also be more informative than any one study.

---

## 21. What runtime isolation testing taught us

Runtime testing of fresh worker contexts showed two different things.

### Between sibling workers

One fresh worker did not see another sibling worker's conclusion.

That is a good sign.

In simplified form:

```text
Worker A ──X──> Worker B
```

### Between parent context and a fresh worker

A fresh worker reported that its initial context contained additional material beyond the explicitly supplied assignment.

So this topology is possible:

```text
               shared context
                ↙        ↘
           Worker A    Worker B
```

Therefore, for now, we cannot automatically say:

> "Fresh worker = completely clean worker."

A more accurate statement is:

> Workers appear separated from one another, but strict isolation from parent/history/memory/project context must be checked separately.

---

## 22. Can leakage happen through a Project?

Yes. This is a separate potential channel.

Imagine a shared school project:

```text
Project "Investigation"
├── chat 1: "Vasya is probably responsible"
├── chat 2: "Vasya had a ball"
├── documents
└── new worker
```

If a new worker automatically receives useful context from the project, it may learn about Vasya before conducting its own investigation.

So the possible contamination channels need to be distinguished:

1. parent chat → worker;
2. account memory/history → worker;
3. project context → worker;
4. sibling worker → worker;
5. old worker history → revived worker.

They are not the same thing.

---

## 23. An old worker that was woken up

Imagine a student who already took part in the first part of an exam.

They were sent home.

The next day they are brought back and told:

> "Now you are an independent reviewer and know nothing about the earlier work."

But they remember everything.

In the same way, a sleeping worker revived through `agents message` keeps its own history.

So it cannot be used as a fresh blind reviewer for material it has already seen.

---

## 24. Isolation preflight — check the walls before the exam

Before a serious benchmark, it is useful to run a small smoke test.

This is like checking:

> "Are the walls between the exam rooms really opaque?"

Several boundaries are checked:

### Parent boundary

Does extra material from the main conversation reach a fresh worker?

### Sibling boundary

Does Worker B see material from Worker A?

### Persistence boundary

Does a revived worker remember its own previous history?

The result can be recorded as:

- `NO LEAK OBSERVED` — this smoke test did not reveal forbidden context; a negative worker report alone means no more than this;
- `FAIL` — the test revealed forbidden context;
- `INCONCLUSIVE` — the test could not be evaluated reliably.

A boundary receives `PASS` only when runtime-level evidence supports isolation for both initial context and later retrieval/tool access. If a required boundary is `FAIL` or materially `INCONCLUSIVE`, the stage cannot be called Full Mode. Confirming that a revived worker retains history only shows that it is not fresh. See [boundary assurance](protocol-details.md#11-boundary-assurance).

---

# Part III. The entire skill as one story

## 25. The big story about school detectives

Something strange happens at school.

The team needs to decide what happened and what to do next.

### Step 1. The secretary records only the facts

They write down:

> what was directly observed;
> what was only reported by a witness;
> what is inferred;
> what we do not yet know.

### Step 2. The coordinator formulates the real question

Not:

> "How do we punish Vasya?"

But:

> "What happened, and what action would best reduce the risk of it happening again?"

### Step 3. Several detectives independently search for different causes

Each receives the same facts, but different search directions.

They should not know the others' conclusions.

### Step 4. One reviewer evaluates the quality of the explanations

They check how well each explanation fits the facts and whether it can be tested.

### Step 5. Another reviewer builds a map of the explanations

They determine which explanations duplicate one another, which are compatible, and which conflict.

They must not see the first reviewer's ratings.

### Step 6. Keep only real finalists

Not the prettiest or most popular ones, but the ones that are genuinely different and important to the decision.

### Step 7. Try to break each finalist separately

Look for its weak points, load-bearing assumptions, and signs that could disconfirm it.

### Step 8. A fresh judge looks at the final picture

They ask:

> Which assumptions is everything resting on?

> What could all the explanations have missed at the same time?

> Where do they actually lead to different actions?

### Step 9. Decide separately what to believe and what to do

Those answers may be different.

### Step 10. If the evidence is insufficient, do not manufacture certainty

Instead, choose a feasible, worthwhile test that could change the decision, or state that none was identified. Stop corrective work at the run budget or after a cycle without material progress; stopping does not make the evidence sufficient.

---

## 26. What Convergence Guard does NOT do

It should not:

- turn the number of agents into a vote;
- treat repetition of the same idea as new evidence;
- invent a third finalist merely for a neat structure;
- force compatible explanations to fight as though they were mutually exclusive;
- declare a decision correct merely because the workflow ended;
- run heavy Full Mode when the cause is already obvious;
- confuse a compelling causal story with demonstrated causality;
- hide insufficient evidence behind confident wording.

---

## 27. The most important idea

Convergence Guard is not meant to make an answer longer.

It is meant to reduce the chance of this kind of error:

> "We decided too early that we understood the problem, and after that all of our smart reasoning happened inside the wrong explanation."

A good result from the skill does not have to be complicated.

Sometimes the best result looks like this:

> "We do not yet know which of the two explanations is correct. Do not build an expensive system. Run this small one-day test; its result could genuinely change the decision."

That is the purpose of the method.
