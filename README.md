# 🚚 NovaRetail CrisisOps AI

An AI-powered multi-agent supply chain crisis management system that helps organizations monitor, analyze, and respond to supply chain disruptions using Large Language Models (LLMs).

Built with **LangGraph**, **LangChain**, **Ollama (Llama 3.2)**, and **Streamlit**, the application enables multiple AI agents to collaborate and solve different supply chain tasks through a centralized Supervisor Agent.

---

# 📌 Project Overview

NovaRetail CrisisOps AI simulates an intelligent enterprise supply chain management system capable of handling inventory issues, shipment tracking, supplier management, incident resolution, operational reporting, risk assessment, and recovery planning.

Instead of relying on a single AI model, the project uses a **multi-agent architecture**, where each agent specializes in a specific business function. A Supervisor Agent understands the user's request and routes it to the appropriate specialist agent, enabling accurate and efficient responses.

---

# ✨ Features

- Multi-Agent AI Architecture
- Supervisor Agent for intelligent routing
- Inventory Management
- Shipment Tracking
- Supplier Management
- Incident Detection & Resolution
- Recovery Planning
- Supply Chain Risk Analysis
- Operational Reporting
- Streamlit-based interactive UI
- LangGraph workflow orchestration
- Local LLM support using Ollama (Llama 3.2)
- Modular and scalable project structure

---

# 🏗️ System Architecture

```
                     User
                       │
                       ▼
              Supervisor Agent
                       │
 ┌──────────┬──────────┼──────────┬──────────┐
 │          │          │          │          │
 ▼          ▼          ▼          ▼          ▼
Inventory Shipment Supplier Incident Recovery
 Agent      Agent      Agent      Agent      Agent
                       │
                       ▼
                 Reporting Agent
                       │
                       ▼
                    Response
```

---

# 🤖 AI Agents

### Supervisor Agent
- Understands user queries
- Routes requests to the correct specialist agent

### Inventory Agent
- Monitors stock levels
- Handles inventory-related queries

### Shipment Agent
- Tracks deliveries
- Provides shipment updates

### Supplier Agent
- Manages supplier information
- Evaluates supplier performance

### Incident Agent
- Detects operational issues
- Suggests incident resolutions

### Recovery Agent
- Generates recovery strategies
- Helps restore disrupted operations

### Risk Agent
- Identifies operational risks
- Provides mitigation suggestions

### Reporting Agent
- Generates business summaries
- Produces operational reports

---

# 🛠️ Tech Stack

- Python
- Streamlit
- LangChain
- LangGraph
- Ollama
- Llama 3.2
- LangSmith
- JSON
- python-dotenv

---

# 📂 Project Structure

```
NovaRetail-Group/
│
├── agents/                 # AI specialist agents
├── graph/                  # LangGraph workflow
├── prompts/                # Prompt templates
├── tools/                  # Business tools
├── utils/                  # Utility functions
├── data/                   # Sample datasets
│
├── app.py                  # Streamlit application
├── main.py                 # Main entry point
├── llm.py                  # LLM configuration
│
├── test.py
├── test_workflow.py
├── test_supervisor.py
├── test_inventory.py
├── test_supplier.py
├── test_shipment_agent.py
├── test_reporting_agent.py
└── ...
```

---

# ⚙️ Installation

## Clone the repository

```bash
git clone <repository-url>
cd NovaRetail-Group
```

## Create virtual environment

```bash
python -m venv .venv
```

## Activate environment

Windows

```bash
.venv\Scripts\activate
```

Linux/Mac

```bash
source .venv/bin/activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🚀 Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

or

```bash
streamlit run main.py
```

---

# 💬 Example Queries

- Show current inventory status.
- Track shipment SHP102.
- List delayed shipments.
- Generate an operational report.
- Identify high-risk suppliers.
- Suggest a recovery plan for delayed deliveries.
- Show supply chain incidents.
- Summarize today's operations.

---

# 📈 Key Highlights

- Multi-Agent Collaboration
- Intelligent Query Routing
- Enterprise Supply Chain Simulation
- Local LLM Deployment
- Modular Design
- Easy to Extend
- Interactive User Interface

---

# 🔮 Future Enhancements

- Database integration (PostgreSQL/MySQL)
- Authentication & Authorization
- Real-time ERP integration
- Live shipment APIs
- Predictive demand forecasting
- Interactive analytics dashboard
- Docker deployment
- Kubernetes support
- Cloud deployment

---

# 🎯 Use Cases

- Supply Chain Monitoring
- Inventory Management
- Shipment Tracking
- Supplier Analysis
- Incident Management
- Business Reporting
- Crisis Response
- Operational Decision Support

---

# 👩‍💻 Authors

Developed as a Multi-Agent AI application demonstrating:

- LangGraph Workflows
- LangChain Agents
- Local Large Language Models
- AI-powered Supply Chain Management
- Enterprise AI Application Development

---
```
