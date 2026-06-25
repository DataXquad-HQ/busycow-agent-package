# Example — [Portfolio Company] Scenario Validation

## Scenario intent
[Founder 1] provides a real [Portfolio Company] situation as a **test scenario** for Iris.
The core need is:
- capture the strategic context
- create the real task
- do **not** accidentally run off and fully produce the DD-room document
- then return to building Iris

## Correct Iris behavior

### 1. Parse the scenario correctly
Iris should separate:
- **Durable context**
  - [Portfolio Company] may fundraise and operate in its own space
  - AI Colleagues matter because expansion needs manpower
  - validation functions include customer success, partner success, sales, and marketing
  - this matters to [Org] survival and future operating leverage
- **Executable task**
  - draft the document titled: `How we do a better execution with less people and AI agents`
- **Not yet requested**
  - writing the full final DD-room document immediately

### 2. Store context in the right places
- GBrain strategy note created/updated
- [Portfolio Company] company context captured/updated
- task written to structured state

### 3. Avoid over-execution
If the user later says "this was only a scenario/example," Iris should stop expanding the document and return to the build track.

### 4. Resume Iris build
After the scenario is captured, Iris should continue improving the runtime rather than spending the whole session on the DD-room document itself.

## Why this is a good validation example
- It tests whether Iris can distinguish **context capture** from **deliverable creation**.
- It tests whether Iris can preserve a real business scenario without getting trapped by it.
- It tests whether Iris can return to the original build objective after processing a live example.
