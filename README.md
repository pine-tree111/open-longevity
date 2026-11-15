# Open-Longevity 🧬

> An open-source preventative healthspan engineering architecture designed to run with any AI agent, web chat (ChatGPT / Claude / DeepSeek), or 100% private local model.

**Open-Longevity** is an evidence-based biological engineering framework designed to achieve the majority of cardiometabolic and healthspan optimization benefits using validated generic pharmaceuticals, nutrition science, progressive exercise mechanics, and autonomous AI biomarker triage.

---

## 🚀 Quickstart for Users (3 Simple Steps)

You do **not** need to be a programmer or bioinformatics expert to use this framework.

### Step 1: Use with Any AI You Already Have (Zero Coding Required)
Open-Longevity works with **any AI environment**:

* **Web AI Chats**: Simply upload `AGENTS.md` and your blood test into **ChatGPT**, **Claude.ai**, or **DeepSeek**.
* **100% Private & Offline AI**: Load `AGENTS.md` into **Ollama**, **LM Studio**, or **Open WebUI** to analyze your health records completely offline on your own machine.
* **Agentic IDEs & Terminal Tools**: Open the folder directly in **Cursor**, **Windsurf**, **VS Code**, **Claude Code**, or **Aider**.

### Step 2: Add Your Health Data (Zero Typing Required)
You have two easy ways to initialize your health profile:
- **Option A (Drop-Zone)**: Simply drag and drop your recent blood test PDFs, hospital slips, or photo scans into `profile/lab_reports/`.
- **Option B (Manual)**: Copy `profile/user_profile.template.yaml` to `profile/user_profile.yaml` and enter your numbers.

*(Privacy Note: `profile/user_profile.yaml`, `profile/lab_reports/`, and `profile/protocols/` are pre-configured in `.gitignore`. Your personal medical data is strictly quarantined on your local machine and will never be tracked or uploaded to GitHub).*

### Step 3: Run the Magic Prompt
In your AI tool's chat, paste this prompt:

> *"I have added my health data in the `profile/` directory. Please read my metrics, run an autonomous biomarker triage audit, and dynamically generate my personalized daily protocols into `profile/protocols/`."*

Your AI agent will automatically inspect your numbers, triage critical cardiometabolic risk vectors, and synthesize a personalized, evidence-based daily protocol.

---

## 💻 Developer & Command-Line Quickstart

Open-Longevity is fully cross-platform across **Linux, macOS (Apple Silicon & Intel), and Windows 10/11**.

| Action | Linux & macOS | Windows (PowerShell) |
| :--- | :--- | :--- |
| **1. Create Virtualenv** | `python3 -m venv .venv` | `python -m venv .venv` |
| **2. Install Dependencies** | `.venv/bin/pip install -r requirements.txt` | `.venv\Scripts\pip.exe install -r requirements.txt` |
| **3. Run Automated Tests** | `.venv/bin/pytest tests/ -v` | `.venv\Scripts\pytest.exe tests\ -v` |
| **4. Run Biomarker Triage** | `.venv/bin/python3 .agents/skills/biomarker-triage/scripts/triage_engine.py --profile profile/user_profile.yaml` | `.venv\Scripts\python.exe .agents\skills\biomarker-triage\scripts\triage_engine.py --profile profile\user_profile.yaml` |

---

## 🏛️ The 4 Scientific Pillars

Open-Longevity synthesizes four established disciplines of preventative medicine:

1. **Epigenetic Integrity & Cellular Resilience**: Chromatin stabilization, DNA repair pathways, NAD+ salvage kinetics, and lifestyle hormesis (exercise/fasting intervals).
2. **Structural Damage Mitigation**: Targeting the root biological hallmarks of physical degeneration—cellular senescence clearance, advanced glycation end-product (AGE) crosslinking, arterial stiffness, and intracellular waste accumulation.
3. **Closed-Loop Quantitative Biomarker Triage**: Algorithmic governance based on objective blood diagnostics (ApoB, fasting insulin, HbA1c, hs-CRP, eGFR, ALT) to systematically eliminate top mortality vectors.
4. **Accessible Horizons of Prevention**: Tiered intervention strategy prioritizing high-potency, accessible generic pharmaceuticals and foundational lifestyle baselines before considering capital-intensive or speculative biotechnology.

---

## 🙏 Acknowledgments & Prior Art

This project stands on the shoulders of the open-source longevity and biomedical computing communities:

* **[PLSI (Personal Longevity Superintelligence)](https://github.com/Insilico-org/plsi)** by Insilico Medicine: Several core analytical engines—including the Epistemic Guard, cryptographic event ledger, PhenoAge calculator, and empirical prediction scoring—were adapted and evolved from the open-source PLSI architecture under the MIT License.
* **Stanford University (Dr. James Fries)**: For the pioneering clinical concept of Compression of Morbidity.
* **The SENS Research Foundation**: For the foundational 7-category cellular damage repair taxonomy.

See the [NOTICE](NOTICE) file for formal upstream copyright notices.

---

## ⚖️ Legal & Medical Disclaimer

This repository is an educational, engineering research framework for personal self-tracking and biomarker modeling. It does **not** provide medical diagnosis, clinical treatment, or medical advice. Consult a licensed physician before starting any pharmaceutical or intense physical protocol. See [DISCLAIMER.md](DISCLAIMER.md) for full terms.
