BLAST RADIUS
Blast Radius — 3-Week MVP Implementation Plan
Team Structure, Repository Setup, Dependencies, GitHub Prerequisites, Execution Plan & Delivery Checklist
Working execution plan for a six-person team | September 2026
Purpose
Build and demonstrate a reusable, configuration-driven Blast Radius capability in three weeks. The analyzer is developed once in its own repository and exercised against three separate C#/.NET demo repositories.

 
Contents
•	1. Executive Overview
•	2. Repository Strategy
•	3. Producer/API Demo Repository
•	4. Consumer 1 Demo Repository
•	5. Consumer 2 Demo Repository
•	6. Repository Workstream Mapping
•	7. Six Workstreams
•	8. Required Prerequisites
•	9. GitHub Prerequisites & Approvals
•	10. Secrets & Security
•	11. GitHub Branching Strategy
•	12. Configuration Design
•	13. Shared Data Contracts
•	14. Week 1 — Foundation
•	15. Week 2 — Core Implementation
•	16. Week 3 — Integration & Stabilization
•	17. Demo Scenario
•	18. Integration Architecture
•	19. Dependency Matrix
•	20. Cross-Team Dependency Rules
•	21. Definition of Done
•	22. What We Should NOT Build
•	23. Final Checklist Before Coding Starts
•	24. START HERE — First 4 Hours
Reading order
Use Sections 1–7 for scope, repositories and ownership. Use Sections 8–13 to complete setup and agree contracts. Sections 14–20 are the schedule and integration rules. Sections 21–24 are the acceptance gate and Day 1 operating checklist.

 
1. Executive Overview
The team will build Blast Radius as a reusable analyzer in a dedicated Python repository, then validate it against three intentionally small C#/.NET application repositories. The three-week plan prioritizes a complete vertical slice in Week 1, real contract and impact intelligence in Week 2, and reliability plus demo readiness in Week 3.
Developer creates GitHub PR
        ↓
GitHub Actions triggers
        ↓
Python Blast Radius Orchestrator
        ↓
Git Diff / Contract Analysis
        ↓
Dependency & Impact Analysis
        ↓
AI Reasoning
        ↓
Relevant Test Selection
        ↓
Existing Repository Test Execution
        ↓
Failure Analysis
        ↓
Risk/Impact Report
        ↓
GitHub PR Comment + Streamlit Dashboard

Guiding principle
Use code for facts, AI for reasoning, and configuration for reuse.

•	Build separately: the Blast Radius analyzer is independent from the sample application repositories.
•	Keep facts deterministic: Git diff, contract comparison, graph traversal, test selection and test execution remain code-owned.
•	Use AI for judgment: consumer impact, failure explanation, recommendations and narrative are schema-validated AI outputs.
•	Prove reuse: the same analyzer is configured against the three demo repositories without changing core Python code.
2. Repository Strategy
The MVP uses exactly four repositories. One repository contains the reusable Blast Radius product. Three repositories contain the deliberately small producer and consumer applications used to prove cross-repository impact analysis.
Repository 1 — Blast Radius Analyzer
Suggested name: blast-radius
Purpose: the actual reusable Blast Radius product. Approved MVP technologies are Python 3.12, Streamlit, NetworkX, Pydantic, YAML, Git diff, OpenAPI/oasdiff where applicable, an enterprise-approved provider-agnostic LLM, GitHub API/CLI or a lightweight Python GitHub library, and GitHub Actions.
blast-radius/
├── action.yml
├── README.md
├── requirements.txt
├── pyproject.toml
├── src/
│   ├── orchestrator/
│   ├── analyzers/
│   ├── graph/
│   ├── ai/
│   ├── tests/
│   ├── report/
│   └── ci/
├── config/
│   ├── services.yaml
│   └── rules.yaml
├── prompts/
│   ├── contract_analysis.md
│   ├── consumer_impact.md
│   ├── test_analysis.md
│   ├── failure_analysis.md
│   └── report_generation.md
├── graph/
│   └── graph.json
└── .github/
    └── workflows/

Directory/file	Responsibility
action.yml	Reusable GitHub Action entry point; passes PR context and secrets to Python.
src/orchestrator	Coordinates configuration, analyzers, graph traversal, AI modules, tests and reporting.
src/analyzers	Deterministic Git diff, lightweight C# contract parsing and OpenAPI/oasdiff adapters.
src/graph	Builds and traverses NetworkX data and persists graph.json.
src/ai	Provider-agnostic LLM adapter, prompts, Pydantic output validation and guardrails.
src/tests	Unit and integration tests for analyzer behavior and orchestration boundaries.
src/report	Risk calculation, Markdown PR comment and report model rendering.
src/ci	GitHub integration; other CI hosts remain future adapters.
config/	Project-specific registry and risk rules; core Python remains reusable.
prompts/	Versioned prompt inputs for the five AI modules.
graph/	Generated JSON graph of services, contracts, consumers, handlers and tests.

3. Producer/API Demo Repository
Repository 2 — blast-radius-demo-api
Purpose: a small C# producer/API repository used to demonstrate a contract or API change. It uses the existing .NET SDK appropriate for the demo repository, OpenAPI where applicable, and its existing repository test framework.
•	Minimal producer/API implementation
•	Contract/model
•	OpenAPI specification if applicable
•	A small set of tests
•	One intentionally designed breaking and one additive change scenario
OrderCreated
├── OrderId
└── Amount

This repository represents: Where the change originates. The demo PR changes this contract so Blast Radius can trace the change to both consumer repositories.
4. Consumer 1 Demo Repository
Repository 3 — blast-radius-demo-consumer-1
Purpose: demonstrate a downstream C# consumer affected by the producer/API change. It contains the consumer implementation, its local contract usage, unit/integration tests, and a clear relationship to Repository 2.
OrderConsumer
    ↓
OrderCreated

Consumer 1 should deliberately use the changed field so the breaking scenario produces an evidence-backed impact verdict and, when configured, a focused failing test.
5. Consumer 2 Demo Repository
Repository 4 — blast-radius-demo-consumer-2
Purpose: demonstrate another downstream C# consumer. It contains its own implementation, contract usage and tests. It may consume the same contract without reading the changed field, allowing the final graph and report to show a different impact verdict.
Producer/API
     │
     ├────────→ Consumer 1
     │
     └────────→ Consumer 2

Keeping the repositories separate simulates real cross-repository dependencies, demonstrates downstream impact, keeps Blast Radius reusable, and prevents the analyzer from becoming coupled to application code.
Separate repositories
blast-radius is the reusable analyzer. The three C#/.NET demo repositories are application inputs checked out and analyzed by configuration; they do not contain Blast Radius implementation code.

Repository	Role	Relationship
blast-radius	Analyzer, orchestrator, graph, AI, report and Streamlit	Reads all registered repositories
blast-radius-demo-api	Producer/API and source contract	Publishes or exposes OrderCreated
blast-radius-demo-consumer-1	Downstream consumer	Consumes OrderCreated and is intentionally affected
blast-radius-demo-consumer-2	Downstream consumer	Consumes OrderCreated and demonstrates a second verdict

6. Repository Workstream Mapping
Workstreamship identifies the first responder and reviewer for a repository; it does not mean only one person may modify it. All six team members should contribute through small, reviewed pull requests where appropriate.
Repository	Primary workstream	Supporting workstreams	Purpose
blast-radius	Core Orchestration & Integration	All	Actual reusable analyzer
blast-radius-demo-api	Contract & Change Analysis	Test Intelligence	Producer/API
blast-radius-demo-consumer-1	Dependency & Impact Analysis	Test Intelligence	Consumer
blast-radius-demo-consumer-2	Dependency & Impact Analysis	Test Intelligence	Consumer

7. Six Workstreams
Team member	Primary responsibilities
Core Orchestration & Integration — Core Orchestration & Integration	Overall architecture; Python project skeleton; orchestrator; shared Pydantic contracts; configuration integration; GitHub Actions integration; cross-module integration; code review; E2E workflow; integration testing; final demo integration. Secondary: resolve cross-team blockers, maintain technical consistency and ensure modules follow agreed contracts.
Contract & Change Analysis — Contract & Change Analysis	Git diff analysis; changed file identification; changed symbols and contract identification; OpenAPI analysis; oasdiff integration where applicable; breaking/non-breaking rules; contract change output.
Dependency & Impact Analysis — Dependency & Impact Analysis	Service dependency configuration; NetworkX graph; JSON graph; consumer relationships; downstream traversal; impacted service identification; Mermaid visualization.
AI Analysis — AI Analysis	Provider-agnostic LLM abstraction; enterprise-approved LLM integration; prompt management; Pydantic schemas; JSON validation; Contract Analysis AI; Consumer Impact AI; Test Analysis AI; Failure Analysis AI; Report Generation AI; AI guardrails.
Test Intelligence — Test Intelligence	Test discovery; test mapping; relevant test selection; existing repository test commands; test execution; result and log collection; failure detection; failure-analysis input preparation; test validation.
UI & Documentation — UI & Documentation	Streamlit dashboard; report presentation; risk summary; dependency graph display; test results display; README; setup and configuration documentation; demo scenario; demo script; final presentation material.

8. Required Prerequisites
Developer prerequisites
•	Git
•	GitHub account and organization access
•	Python 3.12
•	pip and virtual environment tooling
•	VS Code or IntelliJ/PyCharm equivalent
•	GitHub CLI (gh), if approved
•	Docker only if genuinely required; it is not mandatory for the MVP
•	The required C#/.NET SDK for the demo repositories
•	Browser access to GitHub
•	Access to the enterprise-approved LLM
•	Access to the team repositories
Python dependencies
•	networkx
•	pydantic
•	PyYAML
•	GitHub API/client library if required
•	Streamlit
•	OpenAPI/oasdiff integration where applicable
•	An appropriate Python testing framework
•	The LLM SDK corresponding to the enterprise-approved provider
Dependency boundary
Python dependencies are used by Blast Radius. C#/.NET SDKs, application packages and test frameworks are used only by the three demo application repositories. Do not make the analyzer depend on a project reference into another repository.

9. GitHub Prerequisites & Approvals
Do not assume organization permissions are automatically available. Confirm the following before implementation begins, and record the answer in the team setup notes.
Repository permissions
•	Create repositories, or request repository creation
•	Clone repositories
•	Create branches
•	Push branches
•	Create pull requests
•	Review pull requests
•	Merge pull requests
•	Configure repository settings if required
GitHub Actions permissions
•	Run GitHub Actions
•	Create workflow files
•	Modify workflow permissions
•	Use reusable workflows/actions
•	Access required GitHub Actions secrets
•	Use the GitHub API from Actions
•	Post PR comments
GitHub token permissions
Use least privilege. Likely needs are read repository contents, read pull request metadata, read changed files/diff information, write PR comments when the workflow posts reports, and read workflow/test information if needed. Do not request unrestricted repository administration unless a confirmed requirement emerges.
Organization approval checklist
Approval / access	Required?	Workstream to confirm	When needed
Repository creation	Confirm	GitHub/org admin	Day 1
GitHub Actions enabled	Confirm	GitHub/org admin	Day 1
Workflow permissions	Confirm	GitHub/org admin	Day 1
PR comment permission	Confirm	GitHub/org admin	Week 1
Secrets access	Confirm	Platform/admin	Week 1
Enterprise LLM access	Confirm	AI/platform owner	Week 1
External package installation	Confirm	Security/platform	Day 1
C#/.NET SDK availability	Confirm	Team	Day 1

10. Secrets & Security
The minimum runtime configuration is an LLM API credential and a GitHub token or GitHub App credential. Exact names are agreed during Day 1 setup and kept out of source control.
LLM API credential
GitHub token/app credential

•	Never hard-code secrets.
•	Never commit credentials, tokens or API keys.
•	Use GitHub Actions Secrets or an organization-approved secret mechanism.
•	Use environment variables or approved secret storage for local development.
•	Do not expose secrets through Streamlit.
•	Do not print secrets in logs or report artifacts.
•	Use least-privilege GitHub permissions.
•	Send only the minimum relevant diff and code excerpts to the enterprise-approved LLM.
11. GitHub Branching Strategy
main
  │
  ├── feature/contract-analysis
  ├── feature/dependency-graph
  ├── feature/ai-analysis
  ├── feature/test-intelligence
  └── feature/streamlit

•	Do not develop directly on main.
•	Each feature goes through a pull request.
•	Keep pull requests small and reviewable.
•	Merge frequently to expose integration problems early.
•	Avoid long-lived branches.
•	Integration happens continuously. Cross-module integration is handled collaboratively through the Core Orchestration & Integration workstream and the shared module contracts.
•	Use the same lightweight approach for changes in the three demo repositories.
12. Configuration Design
Path	Purpose
config/services.yaml	Registry of producer and consumer repositories, contract sources, owners, test projects and relationships.
config/rules.yaml	Deterministic change classifications and risk rules, including breaking, potentially breaking, additive and internal changes.
prompts/	Versioned prompts for contract analysis, consumer impact, test analysis, failure analysis and report generation.

services:
  - name: order-api
    repository: blast-radius-demo-api
    type: producer

  - name: order-consumer-1
    repository: blast-radius-demo-consumer-1
    type: consumer
    consumes:
      - order-api

  - name: order-consumer-2
    repository: blast-radius-demo-consumer-2
    type: consumer
    consumes:
      - order-api

Configuration must allow the analyzer to be reused for different repositories without changing core Python code. Repository-specific paths, test commands, owners and policy overrides belong in configuration; generic orchestration and analysis belong in the analyzer.
13. Shared Data Contracts
Define these minimal Pydantic models before detailed parallel development. They are the handshake between the six workstreams and prevent each module from inventing a private data shape.
Model	Minimum fields	Input → processing → output
PRInput	repository, pull_request, base_sha, head_sha	GitHub event → normalize context → stable PR context
ChangedArtifact	path, kind, base_text, head_text	Git diff → classify file → changed artifact
ContractChange	contract, member, before, after, classification, evidence	Artifact → contract comparison → typed change
DependencyNode	id, kind, repository, path	Source/config → graph node → NetworkX node
DependencyEdge	source, target, relationship, evidence	Consumer/config → relationship → NetworkX edge
ImpactedConsumer	repository, path, verdict, reason, evidence	Graph trace + code → verdict → consumer impact
TestCandidate	repository, command, selector, reason	Impact graph → map tests → runnable candidate
TestResult	repository, command, status, duration, logs	Candidate → test command → captured result
FailureAnalysis	related_to_change, component, cause, suggested_fix	Failure evidence → AI reasoning → explanation
RiskAssessment	level, score_inputs, recommendation	Changes + impacts + tests → rules → risk
BlastRadiusReport	risk, changes, consumers, tests, failures, reviewers	All outputs → render → PR/Streamlit report

Parallel development rule
Every module documents its Input → Processing → Output contract and uses the shared Pydantic models. Any contract change is made through a reviewed pull request with the affected workstreams involved.

14. Week 1 — Foundation
Theme: build the foundation and a vertical slice.
The week ends with the complete pipeline executing, even if some intelligence is still basic.

Day 1 — Alignment & Setup
•	Confirm MVP scope, four repositories, demo scenario and six owners.
•	Confirm GitHub permissions, LLM access, required SDKs and repository naming.
•	Agree on branching strategy and shared schemas.
•	Create the four repositories.
•	Initialize blast-radius and the three demo repositories.
•	Create the Python environment, project structure, configuration files and placeholder modules.
•	Create the GitHub Action skeleton and initial README.
End-of-day goal
All four repositories exist and the team can clone, branch, commit, push and create pull requests.

Days 2–3
Workstream	Work
Core Orchestration & Integration	Orchestrator skeleton, shared models, configuration loading
Contract & Change Analysis	Git diff prototype and change detection
Dependency & Impact Analysis	NetworkX graph prototype and dependency JSON
AI Analysis	LLM interface and first Pydantic AI response
Test Intelligence	Test discovery and execution prototype
UI & Documentation	Streamlit skeleton and basic report UI

Days 4–5
PR/change
 ↓
Python orchestrator
 ↓
Change analysis
 ↓
Dependency analysis
 ↓
AI placeholder/analysis
 ↓
Test placeholder/execution
 ↓
Basic report

Week 1 deliverable
End-to-end vertical slice. The complete pipeline must execute from a representative change to a basic report.

15. Week 2 — Core Implementation
Theme: replace prototypes with working MVP functionality.
A real PR should produce a meaningful Blast Radius analysis by the end of the week.

Workstream	Week 2 plan
Core Orchestration & Integration	Integration, GitHub Actions, configuration and orchestrator improvements.
Contract & Change Analysis	Complete change/contract analysis, breaking-change rules and OpenAPI/oasdiff.
Dependency & Impact Analysis	Complete NetworkX graph, consumer discovery, downstream traversal and Mermaid.
AI Analysis	Implement five AI modules, structured JSON, prompt versioning and guardrails.
Test Intelligence	Test selection, test execution, result parsing and failure identification.
UI & Documentation	Connect Streamlit to real outputs and display risk, graph, tests and report.

Week 2 milestone
A real PR produces a meaningful Blast Radius analysis, including changed contract, impacted consumers, selected tests, results and risk summary.

16. Week 3 — Integration & Stabilization
Theme: make the MVP reliable and demo-ready.
Focus on E2E integration, bug fixing, prompt tuning, test validation, GitHub Action reliability, UI polish, documentation and demo preparation. Do not spend Week 3 introducing major new architecture.

Day	Focus	Exit condition
Day 11	Full E2E integration: open a PR, run GitHub Actions, generate the report and display it in Streamlit.	One complete run works with captured artifacts and no hidden manual steps.
Day 12	Breaking and non-breaking scenarios; verify deterministic rules and consumer verdicts.	The breaking scenario is high risk and the additive scenario is not falsely high risk.
Day 13	Failure scenarios and AI explanation; validate evidence, proposed fix and guardrails.	A known failing test is related to the change and explained with cited evidence.
Day 14	Final bug fixing, documentation and demo rehearsal.	README, setup steps and demo script are usable by another developer.
Day 15	MVP freeze, final E2E run and presentation/demo.	Definition of Done is checked and the team presents a reproducible workflow.

17. Demo Scenario
Use one controlled scenario so the team can validate every stage of the pipeline without ambiguity.
Repo 1: Order API
       ↓
OrderCreated contract
       ↓
Repo 2: Order Consumer
       ↓
Repo 3: Reporting Consumer

Breaking scenario
The developer changes Amount to TotalAmount in the producer contract. Blast Radius should identify the changed contract, classify the change as potentially breaking or breaking, identify Consumer 1 and Consumer 2, select relevant tests, report intentional failures, provide an AI explanation, calculate risk and post the final PR report.
Non-breaking scenario
The developer adds a new optional field that existing consumers do not read. Blast Radius should identify the additive change, show consumers as unaffected or safe, select only relevant coverage if any, and avoid treating every contract change as HIGH risk.
Evidence to show	Expected result
Changed contract	Amount → TotalAmount, with file and line evidence
Consumer impact	Consumer 1 and Consumer 2 are listed with separate verdicts
Relevant tests	Only tests reachable from affected handlers are selected
Failure analysis	Intentional failing test is related to the change and explained
Risk summary	Risk reflects deterministic classification, consumer verdicts and test results
Final delivery	Upserted GitHub PR comment and matching Streamlit dashboard

18. Integration Architecture
Integration architecture
GitHub PR -> GitHub Actions -> Python Orchestrator -> Git/Contract Analysis + Dependency/Impact Analysis + AI Analysis -> Test Intelligence -> Test Execution -> Failure Analysis -> Risk Report -> GitHub PR Comment and Streamlit Dashboard.

Stage	Implementation responsibility	Output
Trigger	GitHub PR workflow and checkout	PRInput
Facts	Git diff, OpenAPI/oasdiff and deterministic rules	ContractChange
Impact	NetworkX graph traversal and consumer mapping	ImpactedConsumer
Reasoning	Provider-agnostic LLM with Pydantic/JSON validation	Structured AI results
Tests	Existing repository test command and result parsing	TestResult
Delivery	Risk report, PR comment and Streamlit view	BlastRadiusReport

Separate repositories
blast-radius is the reusable analyzer. The three C#/.NET demo repositories are application inputs checked out and analyzed by configuration; they do not contain Blast Radius implementation code.

Repository	Role	Relationship
blast-radius	Analyzer, orchestrator, graph, AI, report and Streamlit	Reads all registered repositories
blast-radius-demo-api	Producer/API and source contract	Publishes or exposes OrderCreated
blast-radius-demo-consumer-1	Downstream consumer	Consumes OrderCreated and is intentionally affected
blast-radius-demo-consumer-2	Downstream consumer	Consumes OrderCreated and demonstrates a second verdict

The three demo repositories remain application inputs to the analyzer. The blast-radius repository owns orchestration and report behavior. GitHub Actions provides the MVP trigger and runtime; no dedicated backend server is required.
19. Dependency Matrix
Component	Depends on	Workstream	Required by
Orchestrator	Shared schemas/config	Core Orchestration & Integration	Week 1
Change Analyzer	Git diff/OpenAPI	Contract & Change Analysis	Week 1–2
Dependency Graph	services.yaml	Dependency & Impact Analysis	Week 1–2
AI Modules	LLM access + schemas	AI Analysis	Week 1–2
Test Intelligence	Demo repo tests	Test Intelligence	Week 1–2
Streamlit	Analyzer outputs	UI & Documentation	Week 1–2
GitHub Action	Orchestrator	Core Orchestration & Integration	Week 2
Final Report	All modules	Persons 1, 4, 6	Week 2–3

20. Cross-Team Dependency Rules
Dependency	Rule
Contract & Change Analysis → Dependency & Impact Analysis	Changed contract information feeds dependency and impact analysis.
Dependency & Impact Analysis → AI Analysis	Impacted consumer information feeds AI consumer-impact reasoning.
Dependency & Impact Analysis → Test Intelligence	Impacted consumers help identify relevant tests.
Test Intelligence → AI Analysis	Test results and logs feed failure analysis.
Contract & Change Analysis + Dependency & Impact Analysis + AI Analysis + Test Intelligence → UI & Documentation	All structured outputs feed Streamlit and report generation.
Everyone → Core Orchestration & Integration	All workstreams contribute outputs that are integrated through the shared orchestration and module contracts.

Integration cadence
Merge small, contract-compatible pull requests frequently. When an output contract must change, update the Pydantic model, its consumer and a representative test in the same coordinated change.

21. Definition of Done
The MVP is complete only when every item below is true:
•	Four repositories are functional.
•	A GitHub PR triggers the workflow.
•	The Python orchestrator executes.
•	Git diff is analyzed.
•	Contract changes are detected.
•	OpenAPI/oasdiff works where applicable.
•	A NetworkX graph is generated.
•	Downstream consumers are identified.
•	AI analysis returns validated structured output.
•	Relevant tests are selected.
•	Existing repository test commands execute.
•	Test results are captured.
•	Failures are analyzed.
•	A risk summary is generated.
•	A PR comment is produced.
•	Streamlit displays the result.
•	Configuration supports the three demo repositories.
•	README and setup documentation are complete.
•	At least one breaking and one non-breaking scenario are demonstrated.
Risks and mitigations
Risk	Mitigation
Missing GitHub or LLM access delays the schedule	Confirm access on Day 1; use deterministic fixtures and a local/mock provider boundary for development until approval arrives.
Consumer code is not linked by a build reference	Use services.yaml, contract attributes/conventions, lightweight parsing and graph evidence.
AI produces unsupported claims	Require Pydantic/JSON output, cited file/line evidence and deterministic guardrails; AI may not lower a deterministic breaking result.
Focused tests are incomplete	Keep a configurable full-suite fallback and make coverage gaps visible in the report.
Cross-team interfaces drift	Use shared models, small PRs, frequent integration and Core Orchestration & Integration coordination.

22. What We Should NOT Build
Protect the three-week schedule from scope creep. Do not introduce:
•	Azure DevOps
•	Azure-specific CI/CD
•	Kubernetes
•	Microservices
•	Graph database
•	Vector database
•	LangChain/LangGraph
•	Complex autonomous agents
•	Dedicated backend server
•	Multi-language analysis
•	Enterprise-scale deployment
•	Multi-CI-platform support
•	Production-grade authentication platform
MVP boundary
GitHub + GitHub Actions + Python 3.12 + Streamlit + NetworkX + OpenAPI/oasdiff + Pydantic/JSON + provider-agnostic enterprise LLM + existing repository test frameworks.

23. Final Checklist Before Coding Starts
Access
•	[ ] GitHub organization access
•	[ ] Repository creation/access confirmed
•	[ ] GitHub Actions enabled
•	[ ] Workflow permissions confirmed
•	[ ] PR comment permission confirmed
•	[ ] Required secrets mechanism confirmed
•	[ ] Enterprise LLM access confirmed
Local setup
•	[ ] Python 3.12 installed
•	[ ] Git installed
•	[ ] GitHub CLI available if approved
•	[ ] C#/.NET SDK installed
•	[ ] IDE configured
•	[ ] Python virtual environment created
Repositories
•	[ ] blast-radius
•	[ ] blast-radius-demo-api
•	[ ] blast-radius-demo-consumer-1
•	[ ] blast-radius-demo-consumer-2
Architecture
•	[ ] Shared Pydantic models agreed
•	[ ] services.yaml agreed
•	[ ] rules.yaml agreed
•	[ ] AI input/output contracts agreed
•	[ ] Test execution contract agreed
•	[ ] Report structure agreed
Demo
•	[ ] Producer scenario selected
•	[ ] Consumer relationships defined
•	[ ] Breaking change defined
•	[ ] Non-breaking change defined
•	[ ] Expected test failure defined
•	[ ] Expected final report defined
 

