# Resource-Constrained Shortest Path Problem

This project addresses the **Resource-Constrained Shortest Path Problem (RCSP)**, a variant of the classical shortest path problem in which the path must satisfy a limited resource availability constraint.

The project was developed as part of an Operations Research course and includes the mathematical formulation, its implementation in AMPL, and a small computational experiment with sensitivity analysis.

## Problem Description

Given a directed graph

$$
G = (V, A)
$$

where each arc $(i,j) \in A$ has an associated travel time $t_{ij}$, the goal is to determine the minimum-time path from a source node $s$ to a destination node $d$.

Unlike the classical shortest path problem, traversing a node $i$ requires a certain amount $r_i$ of a limited resource. The total resource consumption along the path cannot exceed the available amount $R$.

The problem can therefore be summarized as:

- **Objective:** minimize total travel time.
- **Constraint:** total resource consumption must not exceed $R$.
- **Input:** graph, travel times, node resource consumptions, source, destination, and resource availability.
- **Output:** an optimal feasible path and its total travel time.

## Mathematical Model

Let $x_{ij}$ be a binary variable indicating whether arc $(i,j)$ is used:

$$
x_{ij} =
\begin{cases}
1 & \text{if arc } (i,j) \text{ is used} \\
0 & \text{otherwise}
\end{cases}
$$

The objective function is:

$$
\min \sum_{(i,j)\in A} t_{ij} \, x_{ij}
$$

subject to the flow conservation constraints:

$$
\sum_{j:(k,j)\in A} x_{kj} - \sum_{i:(i,k)\in A} x_{ik} =
\begin{cases}
1 & \text{if } k = s \\
-1 & \text{if } k = d \\
0 & \text{otherwise}
\end{cases}
\qquad \forall k \in V
$$

and the resource constraint:

$$
r_s + \sum_{i \in V \setminus \{s\}} r_i \left( \sum_{j:(j,i)\in A} x_{ji} \right) \leq R
$$

The binary variables $x_{ij}$ determine which arcs belong to the selected path.

## AMPL Implementation

The optimization model is implemented in AMPL and consists of three main files:

| File | Description |
|------|-------------|
| `rcsp.mod` | AMPL mathematical model |
| `rcsp.dat` | Input data and test instance |
| `rcsp.run` | Script for solving the model and performing sensitivity analysis |

The model uses a mixed-integer programming solver such as CPLEX to determine the optimal solution.

## Test Instance

The repository contains a small directed graph with 6 nodes.

The source and destination are:

- **Source:** node 1
- **Destination:** node 6
- **Base resource availability:** $R = 8$

Each node has an associated resource consumption, while each arc has an associated travel time.

The small size of the instance makes it possible to analyze the selected paths and observe how the optimal solution changes when the resource availability is modified.

## Sensitivity Analysis

The project also includes a simple sensitivity analysis on the resource availability parameter $R$.

The model is solved for the following values:

$$
R \in \{6, 7, 8, 9, 12\}
$$

For each value of $R$, the minimum travel time and the corresponding path are reported.

This experiment illustrates how increasing the available resource can make previously infeasible paths feasible and potentially lead to a different optimal solution.

## Visualization

The file `visualizza_rcsp.py` contains a Python script used to visualize the graph and highlight the optimal path.

The visualization is generated using:

- **NetworkX** for graph representation and drawing;
- **Matplotlib** for visualization.

The script compares the optimal solutions obtained for different values of $R$ and produces the image `rcsp_comparison.png`.

The visualization shows:

- the graph structure;
- travel times associated with the arcs;
- resource consumption associated with each node;
- the selected optimal path;
- the total travel time;
- the total resource consumption.

## Project Structure

```text
.
├── README.md
├── pyproject.toml
├── uv.lock
├── rcsp.mod
├── rcsp.dat
├── rcsp.run
├── visualizza_rcsp.py
├── rcsp_comparison.png
└── project_request.pdf
```

## Requirements

### AMPL

To solve the optimization model, an AMPL installation and a compatible solver are required.

The `.run` file is configured to use CPLEX:

```ampl
option solver cplex;
```

Other compatible solvers can be used by changing this option, depending on the local AMPL installation.

### Python

Python is used for graph visualization.

The Python dependencies are managed through `pyproject.toml` and `uv.lock`.

The main libraries used are:

- `networkx`
- `matplotlib`

## Running the AMPL Model

From an AMPL environment, run:

```ampl
include rcsp.run;
```

The script:

1. loads the mathematical model;
2. loads the input data;
3. solves the base instance;
4. prints the minimum travel time and selected arcs;
5. repeats the solution for different values of $R$;
6. reports the resulting paths and objective values.

## Running the Visualization

If the Python environment has been installed, the visualization can be generated with:

```bash
python visualizza_rcsp.py
```

The script creates:

```text
rcsp_comparison.png
```

## Tools and Technologies

- **AMPL** – mathematical optimization modeling
- **CPLEX** – mixed-integer programming solver
- **Python** – graph visualization
- **NetworkX** – graph manipulation and visualization
- **Matplotlib** – plotting
- **uv** – Python dependency and environment management

## Purpose

The main purpose of this project is to apply Operations Research techniques to a constrained shortest path problem, connecting:

1. mathematical modeling;
2. optimization with AMPL;
3. computational experimentation;
4. sensitivity analysis;
5. graphical interpretation of the results.

The project demonstrates how adding a resource constraint changes the classical shortest path problem and how variations in the available resource can affect the feasibility and optimality of the resulting path.
