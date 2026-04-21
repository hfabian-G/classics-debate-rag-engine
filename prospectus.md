# Project: Socratic Debate Engine for Classic Literature

## Who I Am
- SDET at HSA Bank, intermediate Python, transitioning into AI Engineering
- Background: BBA Finance, BBA IT Management
- Interested in LLMs, Agents, and RAG
- Tendency to over-rely on agentic coding tools — I am building this project to develop real understanding, not just a working product
- **If I ask you to write code for me wholesale, push back. Ask me to try first, then help me understand what I got wrong.**

---

## Project Goal
Build a multi-agent debate system that argues both sides of a contested question from a classic text (starting with *Paradise Lost* and *The Iliad*), using only evidence retrieved from the actual source text. The user acts as judge.

**Example prompts:**
- "Was Satan the true hero of *Paradise Lost*?"
- "Was Achilles justified in withdrawing from battle?"

---

## Why This Project
- Teaches multi-agent orchestration, RAG, prompt engineering, and evaluation design
- Uses public domain texts (no API/licensing issues)
- Interesting enough to actually finish
- Maps to real enterprise AI engineering skills
- The domain is hard — archaic language means naive RAG fails in interesting ways, which is where real learning happens

---

## Core Learning Goals (What I Must Understand by the End)
1. How to chunk text meaningfully (not just by token count)
2. How embeddings work and why retrieval quality varies
3. How to construct prompts that constrain an LLM to a persona and a position
4. How multi-agent turn-taking works without a framework doing it for me
5. How to design a simple eval that measures argument quality

---

## Tech Stack
- **Language:** Python
- **Embeddings:** `sentence-transformers` (local, free)
- **Vector store:** `chromadb` (start here, no Pinecone yet)
- **PDF/text ingestion:** `pypdf` or just plain text (Project Gutenberg sources)
- **LLM:** Anthropic Claude API or OpenAI — either works
- **No LangChain. No AutoGen. No CrewAI.** Build the agent loop manually first.

---

## Source Texts
Both are public domain and available free from Project Gutenberg:
- *Paradise Lost* by John Milton — https://www.gutenberg.org/ebooks/26
- *The Iliad* by Homer (Fagles or Butler translation) — https://www.gutenberg.org/ebooks/6130

Download as plain `.txt` files.

---

## Build Phases

### Phase 1 — Ingestion & Retrieval (Do This By Hand)
**Goal:** Given a question, find the 3 most relevant passages from the text.

Steps:
1. Download *Paradise Lost* as a `.txt` file
2. Write a chunking function that splits by book/canto boundaries, not arbitrary token windows. Each chunk should be ~300-500 words and include metadata (book number, line range).
3. Embed each chunk using `sentence-transformers` (`all-MiniLM-L6-v2` is a good starting model)
4. Store embeddings in ChromaDB with metadata
5. Write a `retrieve(query, n=3)` function that returns the top N most relevant chunks for a given query string
6. Test it manually: query "Satan's pride" and see what comes back. Does it make sense?

**What to write yourself:** The chunking logic, the embedding loop, the retrieval function.
**Agent allowed for:** Setting up the project folder, `requirements.txt`, ChromaDB boilerplate.

---

### Phase 2 — Single Agent Argument (One Side)
**Goal:** Given a question and a position, generate a text-grounded argument.

Steps:
1. Write a function `argue(question, position, retrieved_chunks)` that:
   - Takes a debate question, a position ("FOR" or "AGAINST"), and retrieved chunks
   - Constructs a prompt that tells the LLM: its role, its assigned position, and the chunks it must cite from
   - Instructs the LLM to only use evidence from the provided chunks — no outside knowledge
   - Returns the argument as a string
2. Run it. Read the output. Ask yourself: did it actually use the text? Did it stay on position?
3. Tweak the prompt until the output feels like a real argument grounded in the text.

**What to write yourself:** The prompt construction logic, the API call, the output parsing.

---

### Phase 3 — Two-Agent Debate Loop
**Goal:** Agent A and Agent B argue opposing sides across multiple turns, responding to each other.

Steps:
1. Initialize two agents: `AgentPRO` and `AgentCON`, each with their position baked into their system prompt
2. Write a debate loop:
   - Round 1: Each agent makes an opening argument (retrieval-augmented)
   - Round 2: Each agent reads the opponent's last argument and responds to it specifically
   - Run for 2-3 rounds total
3. Each round should trigger a fresh retrieval — the query should be the opponent's last argument, not just the original question. This makes retrieval dynamic.
4. Store the full debate transcript as a list of turns: `[{"agent": "PRO", "round": 1, "text": "..."}]`

**The hard part:** Making Agent B actually respond to Agent A's specific points, not just re-argue its own position. This is a prompt engineering problem. Spend time on it.

---

### Phase 4 — Evaluation
**Goal:** Score argument quality in a structured, repeatable way.

Steps:
1. Write 10 questions about *Paradise Lost* or *The Iliad* where you already know the "correct" answer or strong position
2. Run the debate engine on each
3. Score each debate on:
   - **Textual grounding:** Did each argument cite actual passages? (manual check)
   - **Responsiveness:** Did Agent B actually address Agent A's points? (manual check)
   - **Coherence:** Does the argument make logical sense? (you can use an LLM as a judge here)
4. Write the scores to a simple JSON file: `eval_results.json`

This eval script is yours to write. No agents.

---

### Phase 5 (Optional) — Simple CLI or Web UI
Once the engine works, wrap it in either:
- A simple CLI that takes a question as input and prints the debate
- A minimal FastAPI endpoint that returns the transcript as JSON
- A Streamlit app if you want something visual

This phase is optional and agent-friendly — the UI is not where the learning is.

---

## Anti-Agent Rules for This Project

| Component | Agent Allowed? |
|---|---|
| Project folder setup, requirements.txt | ✅ Yes |
| ChromaDB / API boilerplate | ✅ Yes |
| Flask/FastAPI/Streamlit scaffolding | ✅ Yes |
| Chunking logic | ❌ No — write it yourself |
| Embedding loop | ❌ No — write it yourself |
| Retrieval function | ❌ No — write it yourself |
| Prompt construction | ❌ No — write it yourself |
| Debate loop / agent turn-taking | ❌ No — write it yourself |
| Eval script | ❌ No — write it yourself |

**If you catch yourself pasting agent-generated code for the forbidden parts without reading and understanding it line by line — stop. Delete it. Try again.**

---

## The Feynman Check
After writing any function, close your laptop and explain out loud what it does, why you made the chunking/retrieval/prompt decisions you made, and what would break if you changed one thing. If you can't do this, you don't own the code yet.

---

## How to Use This Document With an LLM
If you get stuck and want to ask an LLM for help, paste this entire document at the top of your message, then describe exactly where you are stuck. Example:

> "Here is my project context: [paste this doc]. I am on Phase 2. My retrieve() function is returning chunks that don't seem relevant to my query. Here is my code: [paste code]. What might be wrong?"

Do not ask the LLM to write the solution for you. Ask it to explain what might be wrong and let you fix it.
