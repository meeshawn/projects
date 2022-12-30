# Robot Localization in a windy 2D maze using Hidden Markov Model

## Developed an algorithm that solves the problem of robot localization in a 2D maze in a windy situation using Hidden Markov process.

### The 2-D Maze:
![image](https://user-images.githubusercontent.com/34864587/210102650-69801437-a988-4312-9607-4939030c2ac8.png | scale = 0.5)

### We assume that the robot aims to locate itself in the windy maze as shown in the above. The robot will perform two kinds of actions, sensing and moving:

### Sensing: In a square, the robot will sense the four directions to see if there is an obstacle in this direction. We assume that the whole maze is surrounded by obstacles and the black squares are obstacles as well. However, the sensing is not perfect. We assume that the robot can detect an obstacle with 80% confidence if there is one and might mistake an open square for an obstacle with 15% confidence. The detections in all directions are done independently.

### Moving: In the windy situation, the robot can drift to the left or the right with probability 0.1. If there's an obstacle in the drifting direction, it will bounce back to the original position. For example, in the square of left bottom, if the robot moves northward, it will reach the square to the north with 80% confidence and reach the square to the east with 10% confidence and be bounced back to the original position with 10% confidence.
