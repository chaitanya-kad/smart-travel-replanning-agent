
# Smart Travel Replanning Agent

## Overview
This project implements a utility-based intelligent agent that dynamically replans travel itineraries under uncertain conditions such as delays, price changes, and closures.

## Features
- Dynamic itinerary generation
- Multi-objective optimization (cost, time, crowd)
- Event-based replanning
- Stability-aware decision making

## Tech Stack
- Python
- Streamlit (optional)
- Matplotlib

## How it works
The agent follows:
Perception → Evaluation → Decision → Action

It uses a utility function:
Utility = enjoyment − cost − crowd − time

Replanning happens only if improvement exceeds a threshold.

## Author
Chaitanya Kad
