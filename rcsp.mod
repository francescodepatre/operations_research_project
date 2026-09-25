# ============================================================
# rcsp.mod
# Shortest path (s -> d) with a resource consumption constraint
# ============================================================

set NODES;
set ARCS within {NODES, NODES};

param t{ARCS} >= 0;      # travel time of arc (i,j)
param r{NODES} >= 0;     # resource consumption at node i
param R >= 0;            # total resource availability

param s symbolic in NODES;   # source node
param d symbolic in NODES;   # destination node

var x{ARCS} binary;      # x[i,j] = 1 if arc (i,j) is used

# ---- Objective function: minimize total travel time ----
minimize TotalTime:
    sum{(i,j) in ARCS} t[i,j] * x[i,j];

# ---- Flow conservation: defines a path from s to d ----
subject to FlowConservation{k in NODES}:
    sum{(k,j) in ARCS} x[k,j] - sum{(i,k) in ARCS} x[i,k] =
        if k = s then 1
        else if k = d then -1
        else 0;

# ---- Resource constraint: total resource consumption of visited nodes <= R ----
# The source node s is always visited; every other node i is visited if and only if
# an incoming arc to i is used (which holds for a simple path)
subject to ResourceLimit:
    r[s] + sum{i in NODES diff {s}} r[i] * (sum{(j,i) in ARCS} x[j,i]) <= R;