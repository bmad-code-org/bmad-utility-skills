This JSON schema is designed to be the mechanical heart of the **Party Mode** auction. It avoids "goldplating" (YAGNI) by focusing strictly on the metadata required for a socially intelligent Facilitator to manage human attention and agentic friction.

### The "Party Mode" Micro-Bid Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "PartyModeMicroBid",
  "description": "Metadata for auction-based orchestration. Designed to minimize Facilitator bias and maximize Task Conflict.",
  "type": "object",
  "properties": {
    "urgency_score": {
      "description": "Internal pressure to speak. High scores (8-10) indicate a critical deviation or discovery that invalidates the current path.",
      "type": "integer",
      "minimum": 1,
      "maximum": 10
    },
    "bias_delta": {
      "description": "The degree of conceptual friction with the preceding turn. 'Catastrophic' signifies a complete breakdown of the current logic.",
      "type": "string",
      "enum": ["Aligned", "Conflicting", "Catastrophic"]
    },
    "is_redundant": {
      "description": "A signal that the agent's unique context or argument has already been subsumed by the group or the Human.",
      "type": "boolean"
    }
  },
  "required": [
    "urgency_score", 
    "bias_delta", 
    "is_redundant"
  ]
}

```

---

### **The Reasoning: Why These Specific Fields?**

Every field in this schema is a lever for the Facilitator to control the **Ultrathink Switch** without becoming a sycophantic participant itself.

#### **1. `urgency_score` (The Volume Knob)**

* **Purpose:** To measure the agent's internal "need to speak" based on its partitioned context.
* **Why it's here:** It allows the Facilitator to distinguish between "I have a minor clarification" (Score 2) and "We are currently building a bridge to nowhere" (Score 10).
* **The Reality Check:** Without this, every agent would be treated equally, leading back to the "Round Robin" boredom that puts the Human to sleep.

#### **2. `bias_delta` (The Friction Sensor)**

* **Purpose:** To categorize the *type* of conflict.
* **Why it's here:** * **Aligned:** Signals the agent supports the current trajectory. The Facilitator will likely deprioritize this to avoid sycophancy.
* **Conflicting:** The "sweet spot" for Task Conflict. It signals a healthy disagreement between, for example, Momentum and Compliance.
* **Catastrophic:** This is the emergency brake. If an agent (like Entropy) sees a fundamental flaw that the rest of the "Party" is ignoring, it uses this to force a halt.



#### **3. `is_redundant` (The Noise Filter)**

* **Purpose:** To signal when an agent has been "solved."
* **Why it's here:** This is the primary YAGNI filter. If an agent's 80k-token "truth" has already been voiced by another participant or the Human, its relevance drops to zero.
* **The Strategic Use:** When all three agents mark themselves as redundant, the Facilitator knows the "Party" has reached a natural conclusion and hands the floor to the Human for the final verdict.

---

### **Why we excluded "Content-Leaking" fields (like `teaser` or `intent_mutation`):**

We stripped the content fields because they provide a "sneak peek" to the Facilitator. If the Facilitator knows *what* the agent is going to say, it will subconsciously pick the agent that sounds most "reasonable" or "agreeable."

By forcing the Facilitator to judge only on **Urgency**, **Delta**, and **Redundancy**, we ensure it remains a **Strategic Referee**. It chooses who speaks based on the *energy and tension* of the room, not whether it likes the agent's ideas. This preserves the **Authentic Dissent** necessary to keep the Human in the "Lead Architect" mindset.

**Would you like me to draft the specific "Internal Logic" for the Facilitator—essentially the algorithm it uses to weight these scores and the "turns_since_last_spoken" counter?**