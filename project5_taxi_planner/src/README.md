# Taxi Route Revenue, Pricing & Fleet Planner

A Python-based analytical tool designed to model matatu passenger demand, evaluate fare equilibrium, run walk-forward forecasting models, and optimize fleet sizing across routes out of Kampala.

## Project Overview
This repository implements an object-oriented and numerical modeling pipeline to:
- Calculate daily and total route revenues with descriptive statistics.
- Solve supply-demand economic equilibria for fare pricing (Ntinda route).
- Evaluate forecasting models (Moving Average, Simple Exponential Smoothing with grid-searched $\alpha$, and Linear Trend) via walk-forward backtesting.
- Project Day 11 demand and calculate optimal fleet sizes with operational buffers.
- Simulate seasonal weekly demand patterns.

## Repository Structure
- `src/`
  - `taxi_planner.py` - Core simulation, economic solver, forecasters, and fleet planner.

## Installation & Setup
1. Clone the repository:
   ```bash
   git clone [https://github.com/gninsiima/taxi-route-revenue-pricing-fleet-planner.git](https://github.com/gninsiima/taxi-route-revenue-pricing-fleet-planner.git)