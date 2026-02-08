# Verity

**Verity** is a Perplexity-style AI search and answer engine that runs fully locally on AI PCs.  
It combines SearXNG-powered search, retrieval, and local LLM reasoning to generate grounded, verifiable answers — without relying on cloud-based LLM providers.

![Verity screenshot](https://raw.githubusercontent.com/rupeshs/verity/refs/heads/main/docs/images/verity-screenshot.png)



## ✨ Key Features
- Fully Local, AI-PC Ready -  Optimized for Intel AI PCs using OpenVINO (CPU / iGPU / NPU), Ollama (CPU / CUDA / Metal)
- Fast inference on  CPU,GPU,NPU using OpenVINO
- Designed for fact-grounded, explorable answers
- Privacy by Design - Search and inference can be fully self-hosted
- SearXNG-Powered Search - Self-hosted, privacy-friendly meta search engine
- RAG-First Architecture
- CLI and WebUI support
- API server support
- Powered by Jan-nano 4B model,or configure any model

Supported LLM runtimes:
- **OpenVINO** - CPU / iGPU / NPU
- **Ollama** - CPU / CUDA / Apple Metal

## 📦Dependencies 
- Python 3.10 or higher
- uv - fast Python package and project manager
- Node.js

## How to Install and Run 
Follow the steps to install and run on Windows.
- Step 1: Install SearXNG by following [this guide](https://nolowiz.com/how-to-use-searxng-as-a-private-search-api-step-by-step-guide/)
- Step 2: Clone/Download verity repo
- Step 3: Double click `install.bat` to install

To run CLI interactive app double click `start.bat`.
To run WebUI start the webserver by double clicking `webserver.bat`.
OpenVINO models will be downloaded in the first run.

### Manual installation
Ensure that you have Python 3.x and Node.js installed.

- Install SearXNG by following [this guide](https://nolowiz.com/how-to-use-searxng-as-a-private-search-api-step-by-step-guide/)
- Clone Verity repo, enter into verity dirctory
- Create a virtual environment and activate it
- Run the below commands :
```
pip install -r requirements.txt
playwright install
cd src/frontend
npm install
```
For backend configurations create a `.env` file refer the `.env.sample` file.

To run interactive CLI app run the below 
`python src/app.py`

#### Run WebUI
First run the API server
`python src/api_server.py`

Start the WebUI
```
cd src/frontend
npm run dev
```


## Models

We have tested the following models.

| LLM Provider          | Recommended Model                 | Processor   |
| --------------------- | ----------------------------------|------------
| OpenVINO              | rupeshs/jan-nano-int4-ov          |  CPU/GPU    |
| OpenVINO              | rupeshs/jan-nano-int4-npu-ov      |  NPU (Intel)|
| Ollama                | mannix/jan-nano:latest            |  CPU/CUDA   |

Tested using Intel AI PC with Intel Core Ultra Series 1 processor with CPU/GPU/NPU.

### How to use Ollama models with Verity

Use the below config in `.env` file. update LLM provider(LLM_PROVIDER) as ollama and use model(LLM_MODEL_PATH) as  `mannix/jan-nano:latest`.

Run the below command to pull the model.

`ollama pull mannix/jan-nano:latest`
