#include <iostream>
#include <vector>
#include <iomanip>
/* Author: Meeshawn Marathe
 * Windy Maze Robot Localization using HMM
*/
class RobotLocHMM{
    std::vector<std::vector<char>> maze;
    std::vector<std::vector<float>> posDist;
    std::vector<std::vector<char>> actionSpace;
    std::vector<std::vector<float>> transitionN;
    std::vector<std::vector<float>> transitionW;

public:    
    RobotLocHMM(std::vector<std::vector<char>> mat1,
                std::vector<std::vector<float>> mat2,
                std::vector<std::vector<char>> mat3)
                 : maze{mat1}, posDist{mat2}, actionSpace{mat3}{
// Constructor: Initializes the Maze matrix, the initial position
//              distribution, and the action space of the robot. 
//              It also prints the maze and the initial position
//              distribution. Additionally, it calls a function
//              to compute the transition matrices for North
//              and West directions and initialzes class attributes
//              with these values since these matrices are constants.
        printMaze();
        printPosDist();
        transitionN = computeTransitionMat('N');
        transitionW = computeTransitionMat('W');
    }
    
    void printMaze(){
        std::cout<< "The Maze: " << std::endl;
        for(const auto& row: maze){
            for(const auto& col: row){
                std::cout << std::setw(4) << col << " ";
            }
            std::cout << std::endl;
        }
        std::cout<< std::endl;
    }
    
    void printPosDist(){
         std::cout<< std::endl <<"The Position Distribution: " << std::endl;
        for(const auto& row: posDist){
            for(const auto& col: row){
                std::cout << std::setw(10) << std::setprecision(4) << 100*col << " ";
            }
            std::cout << std::endl;
        }
        std::cout<< std::endl;
    }
    
    auto realStateCalc(int row, int col){
    // Finds the immediate neighbors (W,N,E,S) of a given position
    // in the maze.
        std::vector<char> realState;
        // West Direction
        if(col-1 < 0)// Left Boundary Wall
            realState.push_back('#');
        else
            realState.push_back(maze[row][col-1]);
            
        // North Direction
        if(row-1 < 0)// Top Boundary Wall
            realState.push_back('#');
        else
            realState.push_back(maze[row-1][col]);
            
        // East Direction
        if(col+1 > 6)// Right Boundary Wall
            realState.push_back('#');
        else
            realState.push_back(maze[row][col+1]);         

        // South Direction
        if(row+1 > 5)// Bottom Boundary Wall
            realState.push_back('#');
        else
            realState.push_back(maze[row+1][col]);    
        
        return realState;                
    }
    
    auto computeLikelihood(std::vector<char> ObState, std::vector<char> realState){
    // Computes the likelihood of the sensing action for the observed state from 
    // the sensor given the actual position of the maze.
        std::vector<float> prob {};
        float likelihood {1.0};
        
        for(size_t i=0; i < ObState.size(); ++i){
            // P('0'|'0') = 0.85
            if(ObState[i] == '0' && realState[i]== '0')
                prob.push_back(0.85);
            // P('0'|'#') = 0.20
            else if(ObState[i] == '0' && realState[i]== '#')
                prob.push_back(0.20);
            // P('#'|'0') = 0.15
            else if(ObState[i] == '#' && realState[i]== '0')
                prob.push_back(0.15);  
            // P('#'|'#') = 0.80
            else if(ObState[i] == '#' && realState[i]== '#')
                prob.push_back(0.80); 
        }
        
        // Total Probability of the sensed action equals the product
        // of the probabilities in the individual directions.
        for(const auto& val: prob)
            likelihood*=val;
            
        return likelihood;                
      }
      
    void sensing(std::vector<char> ObState){
    // Computes the posterior of the sensing action given the 
    // initial position distribution and the likelihood of observing
    // the sensor position value given the actual position.
    
        float normFactor {};
        float likelihood {};
        std::vector<char> realState;
        
        // Compute P(sensed action) by normalization
        for(int i =0; i < maze.size(); ++i){
            for(int j =0; j < maze[0].size(); ++j){
                realState = realStateCalc(i,j);
                likelihood = computeLikelihood(ObState,realState);
                posDist[i][j] = likelihood*posDist[i][j];
                normFactor+=posDist[i][j];
            }
        }

        // Update the position distribution using the norm factor
        for(size_t i =0; i < maze.size(); ++i){
            for(size_t j =0; j < maze[0].size(); ++j)
                posDist[i][j]/=normFactor;
        }
    }   

    std::vector<std::vector<float>> computeTransitionMat(char dir){
    // Computes the transition matrices for North and West directions
    // as per the windy navigation situation. For North direction movement,
    // 80% probability is alloted to North direction (0% to South) and 10%
    // each to East and West. For West direction movement, 80% probability is 
    // assigned to West direction (0% to East) and 10% each to North and South 
    // directions.
    
        std::vector<std::vector<float>> mat(42, std::vector<float> (42, 0.0));
        std::vector<char> realState;
        for(int row = 0; row < mat.size(); ++row){
            int i1 = row / 7;
            int j1 = row % 7;
            // Ignore the blockades in the maze
            if(maze[i1][j1] == '#')
                continue;
            for(int col = 0; col < mat.size(); ++col){
                int i2 = col / 7;
                int j2 = col % 7;
                // Bouncing back or stay put!
                if(row == col){
                    realState = realStateCalc(i1,j1);
                    // idx = 0->W 1->N 2->E and 3->S
                    int idx = 0;
                    float prob {0.0};
                    for(const auto& val: realState){
                        if(val=='#' && dir == 'N' ){
                            if(idx == 1)
                                prob += 0.8;
                            else if(idx == 0 || idx == 2)
                                prob += 0.1;             
                        }
                        if(val=='#' && dir == 'W' ){
                            if(idx == 0)
                                prob += 0.8;
                            else if(idx == 1 || idx == 3)
                                prob += 0.1;
                        }
                        idx++;
                    }
                    mat[row][col] = prob;
                }
                // Moving to the immediate neighbors (W,N,E,S) 
                else if( (abs(i1-i2) == 1 && j1==j2) || (abs(j1-j2) == 1 && i1==i2) ){
                    float prob {0.0};
                    // North Neighbor
                    if(i1-i2 == 1 && j1==j2  && maze[i2][j2] == '0'){
                        if(dir == 'N')
                            prob = 0.8;
                        else if(dir == 'W')
                            prob = 0.1;
                    }
                    // West Neighbor
                    else if(j1-j2 == 1 && i1==i2 && maze[i2][j2] == '0'){
                        if(dir == 'N')
                            prob = 0.1;
                        else if(dir == 'W')
                            prob = 0.8;
                    }
                    // East Neighbor
                    else if(j1-j2 == -1 && i1==i2 && maze[i2][j2] == '0'){
                        if(dir == 'N')
                            prob = 0.1;
                        else if(dir == 'W')
                            prob = 0.0;
                    }
                    // South Neighbor
                    if(i1-i2 == -1 && j1==j2  && maze[i2][j2] == '0'){
                        if(dir == 'N')
                            prob = 0.0;
                        else if(dir == 'W')
                            prob = 0.1;
                    }
                    
                    mat[row][col] = prob;
                }
            }
        }
        return mat;
    }
    
    auto flatten(std::vector<std::vector<float>> mat){
    // Utility function to flatten a 2D matrix to a 1D vector
        std::vector<float> flat;
        for(const auto& row: mat){
            for(const auto& col: row)
                flat.push_back(col);
        }
        return flat;
    }
    
    auto reshape(std::vector<float> flat){
    // Utility function to reshape the flatted 1x42 vector
    // to a 7x6 2-D matrix
        std::vector<std::vector<float>> mat(6, std::vector<float> (7, 0.0));
        int idx = 0;
        
        while(idx<42){
            mat[idx/7][idx%7] = flat[idx];
            idx++;            
        }
        
        return mat;        
    }
    
    void moving(char dir){
    // Computes the posterior of finding the new position given
    // the filtered position distribution with the help of the
	// transition matrix for the appropriate direction.
        std::vector<std::vector<float>> transition;
        if(dir == 'N')
            transition = transitionN;
        if(dir == 'W')
            transition = transitionW;
            
        std::vector<float> result;
        std::vector<float> prior_flat = flatten(posDist);
        // Posterior computation
        for(int col = 0; col < 42; col++){
            float sum {};
            for(int row = 0; row < 42; row++){
                sum+=transition[row][col]*prior_flat[row];               
            }
            result.push_back(sum);
        }
        posDist = reshape(result);        
    }
    
    void printVect(std::vector<char> v){
        std::cout << "[";
        for(const auto &val: v)
            std::cout << val << " ";
        std::cout << "]";
    }
    
    void action(){
        int idx = 0;
        for(const auto& act: actionSpace){
            // Alternatively call 'sensing' and 'moving' functions
            if(idx%2 == 0){
                sensing(act);
                std::cout << "Sensing: ";
                printVect(act);                
            }
            else{
                moving(act[0]);
                std::cout << "Moving: " << act[0];
            }
            printPosDist();
            idx++;
        }
    }
           
};

int main(){
    // Defining the Maze
    std::vector<std::vector<char>> maze(6, std::vector<char> (7, '0'));
    maze[1][1] = '#';
    maze[1][4] = '#';
    maze[3][1] = '#';
    maze[3][4] = '#';
    
    // Defining the Initial Position Probability Distribution of the Maze
    // 4 out of 42 positions are blockades; hence P = 1/38
    std::vector<std::vector<float>> posDist(6, std::vector<float> (7, 1.0/38));
    posDist[1][1] = 0.0;
    posDist[1][4] = 0.0;
    posDist[3][1] = 0.0;
    posDist[3][4] = 0.0;
    
    // Defining the Action Space
     std::vector<std::vector<char>> actionSpace = {{'0','0','0','0'},
                                                   {'N'},
                                                   {'#','0','0','0'},
                                                   {'N'},
                                                   {'0','0','0','0'},
                                                   {'W'},
                                                   {'0','#','0','#'},
                                                   {'W'},
                                                   {'#','0','0','0'}};
    
    // Creating an object of the RobotLocHMM class
    RobotLocHMM hmm(maze, posDist, actionSpace);

    // Actuating the robot based on the action space
    hmm.action();
    
}
