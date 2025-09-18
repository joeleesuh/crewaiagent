# MIT AI Studio Crew AI Agent – Public Interest Technologist Edition

## Overview

This example demonstrates a two-agent Crew AI system:

1. **Ethics and Emerging Technology Research Lead** – synthesizes cross-sector
   insights on AI governance, civic technology, and public interest innovation.
2. **Policy Communicator and Storyteller** – transforms research into a
   well-structured Markdown article with actionable recommendations for
   technologists, policy makers, and community partners.

The crew runs in a sequential process, first conducting research and then
producing a polished article ready for distribution.

## Features

- Terminal interface for interactive topic selection
- Agents grounded in real-world leadership across Stanford, GAO, USPTO, IDEO,
  and Federal civic tech initiatives
- Configurable Serper web-search integration when the API key is available
- File output through `FileWriterTool` for repeatable Markdown publishing
- Clear warnings for missing environment variables to simplify troubleshooting
- Embedded background context so each agent writes with first-hand insight from
  Stanford, GAO, USPTO, White House, IDEO, UNICEF USA, and civic leadership

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- An OpenAI API key with access to GPT models
- Optional: Serper API key for web search augmentation

### Installation

```bash
pip install -r requirements.txt
```

Set the required environment variables before running the crew:

```bash
export OPENAI_API_KEY="your-openai-api-key"
export SERPER_API_KEY="your-serper-api-key"  # optional
```

## Usage

Run the main script and follow the prompt to provide a topic aligned with 
interests or coursework:

```bash
python main.py
```

Topic: Introduce yourself to the class
==================================================

Configuring agents based on public service and design experience...
Defining tasks aligned to research and storytelling workflows...

Launching the sequential crew...
...
Crew execution did not complete successfully.
Reason: <API error details>
```

When valid API credentials are supplied, Crew AI orchestrates the agents to
produce a research memo and saves a Markdown article to `ai_studio_article.md`.

## Agents and Tasks

### Persona Context

Each agent is primed with a shared background summary that reflects the lived
experience of a public interest technologist who has:

- Facilitated Stanford's Ethics, Technology, and Public Policy cohort alongside
  Professors Mehran Sahami, Jeremy Weinstein, and Rob Reich.
- Examined AI innovations as a U.S. Patent Examiner and GAO technology auditor
  with experience drafting office actions, congressional testimonies, and
  Federal policy recommendations.
- Guided digital accountability reforms across the White House, OMB, SBA, GSA,
  and Department of Education while leading programs that span grants,
  cybersecurity, and data transparency.
- Led human-centered design engagements at IDEO and civic innovation programs
  such as the U.S. Digital Corps, Civic Digital Fellowship, and citywide
  initiatives in Los Angeles and Washington, DC.
- Supported academic, civic, and international communities through roles with
  the University of Pennsylvania, University of Michigan, USC, UNICEF USA, and
  global development partners.

This context is injected into both tasks, ensuring that research and writing
ground every insight in multi-sector public service experience.

### Ethics and Emerging Technology Research Lead

- **Role inspiration**: Stanford Advisory Board and cohort leadership, GAO AI
  audits, USPTO patent examinations, OSTP innovation lab initiatives, UNICEF
  product innovation.
- **Focus**: map ethical, legal, and societal considerations; surface Federal
  and global case studies; and frame opportunities for inclusive innovation.

### Policy Communicator and Storyteller

- **Role inspiration**: crafting GAO testimonies, briefing White House and OMB
  leadership, advising city and federal programs, and coaching design research
  teams at IDEO.
- **Focus**: translate complex findings into accessible narratives with
  stakeholder recommendations, saving the article to Markdown for sharing with
  partners.

### Task Flow

1. **Research Memo** – builds a structured memo that inventories benefits,
   risks, mitigations, governance levers, and annotated case studies.
2. **Article Draft** – leverages the research summary to create a briefing-style
   article with actionable next steps for public servants, technologists, and
   civil society leaders.

## Test Prompt and Observations

- **Prompt used**: `Introduce yourself to the class`
- **What worked**: The CLI experience, agent instantiation, task wiring, and
  sequential crew configuration all executed as expected.  The system correctly
  warned about missing API keys and, when provided, passes the research context
  (including the detailed persona background) into the writing task via Crew
  AI's task context feature.
- **What did not work**: Without valid OpenAI credentials or outbound network
  access, Crew AI cannot retrieve model completions, and the final Markdown file
  is not produced.  Ensure the required environment variables are set and that
  the runtime environment permits API requests.
- **What I learned**: Configuring tools conditionally avoids runtime errors in
  restricted environments, and aligning agent personas with lived experience
  clarifies expectations for output quality and collaboration.
