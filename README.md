
# Athena Universe RPG

Welcome to the Athena Universe, a text-based, multiplayer RPG powered by a local AI Game Master. This document will guide you through setting up and running the game on your local machine.

## Installation Guide

This project uses a local AI model to generate the game's narrative. We recommend using KoboldCPP as a lightweight and efficient engine to run your own GGUF model files.

### 1. Install KoboldCPP

Download the latest version of [KoboldCPP](https://github.com/LostRuins/koboldcpp/releases) for your operating system.

### 2. Download a GGUF Model

You will need a GGUF model file to run the game. You can find a wide variety of models on [Hugging Face](https://huggingface.co/models?search=gguf).

## Local Development & Execution

### 1. Run the AI Game Master (KoboldCPP)

Open a PowerShell terminal and run the following command, replacing the file paths with the location of your KoboldCPP executable and GGUF model file:

```powershell
& "D:\Extra storage\koboldcpp.exe" --model "F:\LLM\unsloth.Q8_0.gguf" --context 8192 --port 5001
```

### 2. Run the Backend

In a new terminal, navigate to the `backend` directory and run the following command:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8282
```

### 3. Run the Frontend

In a third terminal, navigate to the `frontend` directory and run the following command:

```bash
npm run dev
```

The game will be accessible in your browser at `http://localhost:5173`.

## Multiplayer Deployment (Docker)

This project is fully containerized using Docker, allowing for a simple and consistent deployment experience.

### 1. Install Docker

Ensure you have [Docker](https://www.docker.com/products/docker-desktop) and [Docker Compose](https://docs.docker.com/compose/install/) installed on your machine.

### 2. Run the Game

Once Docker is running, open your terminal in the root of this project and run the following command:

```bash
docker-compose up
```

This will build the frontend and backend containers and start the application. You can then access the game in your browser at `http://localhost:5173`.

## Game Master Narrative Specification

The Athena Universe RPG uses a unique system to blend traditional tabletop RPG mechanics with the power of a large language model.

### The D100 System

When a player uses the `/roll` command (e.g., `/roll interface`), the backend system intercepts this command *before* it is sent to the AI. The system then performs the following actions:

1.  **Rolls a 1d100 die.**
2.  **Retrieves the player's corresponding stat value** (e.g., `interface: 150`).
3.  **Calculates the total:** `1d100_roll + stat_value`.
4.  **Broadcasts a system message** to all players, showing the full calculation:
    `[SYSTEM: The Hacker rolled 1d100 (87) + INTERFACE (150) = TOTAL: 237]`

This contextual information is then passed to the AI Game Master, which uses the result to inform its narrative description of the action's outcome.
