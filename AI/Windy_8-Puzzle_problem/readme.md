# Windy Eight Puzzle Solver using A-Star Traversal Algorithm

We consider a variant of the 8-puzzle problem (http://tristanpenman.com/demos/n-puzzle) under a windy condition. The initial state and the goal state are shown as follows: We assume that the wind

Intial state	Goal state

comes from the south. The step cost regarding the agent’s moving a non-blank tile to the neighboring blank tile is defined as follows: 1 for moving northward; 2 for moving westward or eastward; 3 for moving southward.
The evaluation function f (n) = g(n) + h(n), where g(n) is the path cost and h(n) is the heuristic function. g(n) is defined as the path cost until the current state n by considering the windy step cost.
For h(n), we use a modified total Manhattan distance used in class by considering the windy situation.
We define h(n) = L8	hi(n), where hi(n) is for each tile. For example, for the initial node, regarding
Tile 6, the agent has to move at least 1-step southward and 1-step eastward in order to reach the goal. Therefore, we have h6(n) = 3 ∗ 1 + 2 ∗ 1 = 5 at the initial state.
In your implementation, please use a priority queue for the frontier and a hash table for the expored
set. The priority is based on the evaluation function f (n). The smaller the value, the higher the priority. Use FIFO for the tie-break. In your testing output, please print out all expansion states in the sequence as shown on next page: For the printout of each state, the last 2nd row includes g(n) value at the left and h(n) value at the right, and the last row indicates the expansion order. The order of #4 and #5 in the output can be swapped; the order of #6 and #7 can be swapped too. They depends on the order in which you add the children to the expansion node.
