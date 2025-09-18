#!/usr/bin/env python3
"""MIT AI Studio - Crew AI Agent tailored to a public interest technologist.

This script configures a CrewAI system with two agents that reflect a
technology policy expert's background.  The research agent synthesises
insights across ethics, governance, and emerging technology, while the
writer agent produces a polished article suitable for civic, academic, and
policy audiences.

Run the module directly from the terminal to interactively provide a topic
for the crew to research and write about.
"""

from __future__ import annotations

import os
from typing import List

from crewai import Agent, Crew, Process, Task
from crewai_tools import FileWriterTool, SerperDevTool

BACKGROUND_CONTEXT = """You bring together experiences such as:
- Guiding Stanford's Ethics, Technology, and Public Policy cohort alongside
  Professors Mehran Sahami, Jeremy Weinstein, and Rob Reich
- Examining artificial intelligence and software innovations as a U.S. Patent
  Examiner and GAO technology auditor
- Advising Federal leaders across the White House, OMB, SBA, GSA, and the
  Department of Education on data transparency, emerging technology, and
  digital service delivery
- Championing human-centered design at IDEO and launching civic technology and
  economic development initiatives with governments, nonprofits, and industry
- Supporting academic and civic communities at the University of Pennsylvania,
  University of Michigan, USC, and international forums such as UNICEF USA
Use this lived experience to ground every analysis, highlight ethical and
equity implications, and surface cross-sector collaboration opportunities."""


def _maybe_create_serper_tool() -> List[SerperDevTool]:
    """Return a Serper search tool if the API key is available."""

    if os.getenv("SERPER_API_KEY"):
        return [SerperDevTool()]
    return []


def create_research_agent() -> Agent:
    """Create the research agent grounded in a public interest tech profile."""

    return Agent(
        role="Ethics and Emerging Technology Research Lead",
        goal=(
            "Synthesize cross-sector research into AI governance, civic technology,"
            " and human-centered innovation so complex topics are ready for policy"
            " and design discussions."
        ),
        backstory=(
            "You guide conversations on technology ethics at Stanford, advise on AI"
            " accountability from service at the U.S. Government Accountability Office"
            " and the U.S. Patent and Trademark Office, and"
            " translate research for public servants, engineers, and designers."
        ),
        tools=_maybe_create_serper_tool(),
        verbose=True,
        allow_delegation=False,
    )

def create_writer_agent() -> Agent:
    """Create the writing agent that reflects long-form policy experience."""

    tools = [FileWriterTool()]
    return Agent(
        role="Policy Communicator and Storyteller",
        goal=(
            "Transform nuanced research into compelling narratives with"
            " clear recommendations for civic leaders, technologists, and academics."
        ),
        backstory=(
            "Drawing on experience moderating discussions with global leaders,"
            " crafting GAO reports for Congress, and briefing White House stakeholders,"
            " you excel at weaving evidence, ethics, and inclusive"
            " design into accessible writing."
        ),
        tools=tools,
        verbose=True,
        allow_delegation=False,
    )

def create_research_task(agent: Agent, topic: str) -> Task:
    """Create a task that captures the research workflow."""

    description = f"""Investigate the topic: {topic}

    Anchor your thinking in the following background:
    {BACKGROUND_CONTEXT}

    Focus your review on:
    1. Ethical, societal, and economic implications across government, industry, and civil society
    2. Practical case studies from Federal initiatives, academia, and mission-driven organizations
    3. Key policy, legal, and governance debates shaping the technology's deployment
    4. Opportunities to align innovation with public interest outcomes and inclusive design

    Deliver concise, sourced findings suitable for collaboration with product, policy, and research partners."""

    expected_output = """A structured research memo that includes:
    - Executive summary highlighting the most relevant developments
    - Table of key benefits, risks, and mitigation strategies
    - Case studies with short annotations on impact and lessons learned
    - Policy or governance considerations with references
    - Bibliography of credible sources consulted"""

    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent,
        async_execution=False,
    )

def create_writing_task(agent: Agent, research_task: Task, topic: str) -> Task:
    """Create the writing task that depends on the research task output."""

    description = f"""Using the research findings, craft a policy-oriented article on: {topic}

    Keep this lived experience in mind while writing:
    {BACKGROUND_CONTEXT}

    Requirements:
    1. Open with a concise briefing that situates the issue for technology and policy leaders
    2. Organize sections for context, current state of the field, governance considerations, and future outlook
    3. Showcase real-world examples that resonate with multi-sector stakeholders
    4. Recommend actionable steps for researchers, product teams, and public officials
    5. Save the article to 'article.md' in Markdown format

    Aim for 800-1000 words with clear headings and accessible explanations.
    Maintain a tone that reflects a collaborative civic technologist."""

    expected_output = """A Markdown article saved as 'article.md' containing:
    - Briefing-style introduction
    - Thematic sections with descriptive headings
    - Integrated examples and stakeholder perspectives
    - Actionable recommendations and closing reflection
    - Reference list for further reading"""

    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent,
        context=[research_task],
        async_execution=False,
    )


def _print_intro() -> None:
    """Welcome."""

    print("Welcome")
    print("=" * 50)


def _warn_about_missing_keys() -> None:
    """Inform the user if critical API keys are absent."""

    missing = []
    if not os.getenv("OPENAI_API_KEY"):
        missing.append("OPENAI_API_KEY")
    if missing:
        print("Warning: the following environment variables are not set:")
        for key in missing:
            print(f" - {key}")
        print(
            "Set the required keys before running the crew to avoid runtime errors."
        )
    if os.getenv("SERPER_API_KEY") is None:
        print(
            "Note: SERPER_API_KEY is not configured. Web search will be skipped,"
            " but the crew can still operate with available context."
        )


def main() -> None:
    """Execute the crew with a user-supplied topic."""

    _print_intro()
    _warn_about_missing_keys()

    topic = input("Enter a topic to explore: ").strip()
    if not topic:
        topic = "Public interest safeguards for generative AI systems"
        print(f"No topic provided. Using default: {topic}")

    print(f"\nTopic: {topic}")
    print("=" * 50)

    print("\nConfiguring agents based on public service and design experience...")
    researcher = create_research_agent()
    writer = create_writer_agent()

    print("Defining tasks aligned to research and storytelling workflows...")
    research_task = create_research_task(researcher, topic)
    writing_task = create_writing_task(writer, research_task, topic)

    print("\nLaunching the sequential crew...")
    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, writing_task],
        process=Process.sequential,
        verbose=True,
    )

    try:
        final_output = crew.kickoff()
    except Exception as exc:
        print("\nCrew execution did not complete successfully.")
        print(f"Reason: {exc}")
        print(
            "Verify API credentials and network access, then re-run the script."
        )
        return

    print("\nCrew execution completed successfully.")
    print("=" * 50)
    print("Final Output:\n")
    print(final_output)

    if os.path.exists("article.md"):
        with open("article.md", "r", encoding="utf-8") as file:
            article = file.read()
        print("\nArticle saved to 'article.md'.")
        print(f"Article length: {len(article)} characters")
    else:
        print(
            "\nThe file 'article.md' was not created. Confirm that the"
            " FileWriterTool is configured correctly."
        )


if __name__ == "__main__":
    main()
