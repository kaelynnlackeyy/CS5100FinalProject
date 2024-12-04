# Fantasy Football Agent: Finding Optimal Draft Picks using a Genetic Algorithm


## Overview


This project provides an AI agent that uses a genetic algorithm to find optimal draft picks for the year. Additionall, it features a 

## Features

## Document Overview

## Getting Started

### Prequisites

### Installation

## Model and Tokenizer
# Genetic Algorithm and Validation Code: Quick Start Guide

## **Guideline for Genetic Algorithm Code**
Tips: all the document are in the geneticAlgo file

### **Quick Start Steps**
1. **Get the Data**
   - Run `datainjectionFromAWS.py` to fetch the cooked data from the AWS database.

2. **Save the Data**
   - Find a local path to store the source data.
   - Copy the path into your computer for easy reference.

3. **Run the Driver**
   - Execute `runWithADP.py`. This is the main driver for the genetic algorithm.

4. **Check the Output**
   - After running the driver, you will get the following results:
     1. **Chart**: A visual comparison between the final team and the ADP team.
     2. **Excel File**: The final picked team with its detailed data organized by years.
     3. **Excel File**: Recommended agent with its optimized weights.
     4. **Excel File**: ADP reference team with its detailed data organized by years.

---

## **Guideline for Validation of Genetic Algorithm Code**

### **Quick Start Steps**
1. **Environment Setup**
   - Ensure the following files are in place:
     - `validateAgent.py`
     - `runWithADP.py`
     - `recommended_agent_weights.xlsx` (output from the genetic algorithm code, representing the best agent).

2. **Run the Driver**
   - Execute `validateAgent.py`. 
   - It will fetch the 2023 data from AWS and use the recommended agent to run the team-picking process.

3. **Check the Output**
   - After running the validation, you will get the following results:
     1. **Chart**: A visual comparison between the final team and the ADP team.
     2. **Chart**: A pick-by-pick comparison between the ADP team and the optimized team.
     3. **Excel File**: The 2023 source meta data for reference.
     4. **Excel File**: The final picked team for both the ADP team and the optimized team based on the best agent.


## Acknowledgements
