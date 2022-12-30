# Windy Eight Puzzle Solver using A-Star Traversal Algorithm

We consider a variant of the 8-puzzle problem (http://tristanpenman.com/demos/n-puzzle) under a windy condition. The initial state and the goal state are shown as follows: 

**Intial state**	  &emsp;  &emsp;               **Goal state** <br />
   2 8 3     &emsp;  &emsp; &emsp; &emsp;          1 2 3 <br />
   6 7 4     &emsp;  &emsp; &emsp; &emsp;          8 - 4 <br />
   1 5 -     &emsp;  &emsp; &emsp; &emsp;          7 6 5 <br />


- We assume that the wind comes from the south. The step cost regarding the agent’s moving a non-blank tile to the neighboring blank tile is defined as follows: 1 for moving northward; 2 for moving westward or eastward; 3 for moving southward.
- The evaluation function f (n) = g(n) + h(n), where g(n) is the path cost and h(n) is the heuristic function. g(n) is defined as the path cost until the current state n by considering the windy step cost.
- For h(n), we use a modified total Manhattan distance used in class by considering the windy situation. We define h(n) = L8	hi(n), where hi(n) is for each tile. For example, for the initial node, regarding Tile 6, the agent has to move at least 1-step southward and 1-step eastward in order to reach the goal. Therefore, we have h6(n) = 3 ∗ 1 + 2 ∗ 1 = 5 at the initial state.

- Priority queue will be used for the frontier and a hash table for the expored set. 

- The priority is based on the evaluation function f (n). The smaller the value, the higher the priority. FIFO will be used for a tie-breaking situation.
