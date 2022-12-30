#include <iostream>
#include <vector>
#include <algorithm>
#include <queue>
#include <map>


class WindyEightPuzzle{
    std::vector<std::vector<char>> currMatrix;
    std::vector<std::vector<char>> goalMatrix;
    int north;
    int south;
    int east_or_west;
    
public:
    
    WindyEightPuzzle(std::vector<std::vector<char>> IMAT, std::vector<std::vector<char>> GMAT)
        : currMatrix{IMAT}, goalMatrix{GMAT}, north{1}, south{3}, east_or_west{2}{}

    void display(const std::vector<std::vector<char>> &M) const{
        std::cout << std::endl;
        for(auto i = 0; i < 3; ++i){
            for(auto j = 0; j < 3; ++j)
                std::cout << M[i][j] << " ";
            std::cout << std::endl;    
        }
    }
    
    void displayCurrMat() const{
        std::cout << "\nCurrent Matrix";
        display(currMatrix);
    }

    void displayGoalMat() const{
        std::cout << "\nGoal Matrix";
        display(goalMatrix);
    }
    
    auto findIndex(char item, const std::vector<std::vector<char>> &M) const{
        std::vector<int> idx;
        for(auto row = M.begin(); row!= M.end(); ++row){
            auto col = std::find((*row).begin(), (*row).end(),item);
            if(col != (*row).end()){
                idx.push_back(row - M.begin());
                idx.push_back(col - (*row).begin());
            }
        }
        return idx;
    }
    
    int heuristicFunction(int row_curr, int col_curr, int row_goal, int col_goal){
        int hVal {0};
        if(row_goal >= row_curr)
            hVal = (row_goal - row_curr)*south + abs(col_goal - col_curr)*east_or_west;
        else
            hVal = abs(row_goal - row_curr)*north + abs(col_goal - col_curr)*east_or_west;
        return hVal;
    }
    
    int heuristicSum(){
        int hSum {0};
//        std::vector<int> currIdx;
        std::vector<int> goalIdx;
        char item {};
        for(auto i = 0; i < 3; ++i){
            for(auto j = 0 ; j < 3; ++j){
                item = currMatrix[i][j];
                if(item != '-'){
                    goalIdx = findIndex(item, goalMatrix);
                    hSum += heuristicFunction(i, j, goalIdx[0], goalIdx[1]);
                }
            }
        }
        return hSum;   
    }
    
    void swap(char &a, char &b){
        char temp {};
        temp = a;
        a = b;
        b = temp;        
    }
    
    void AStarTraversalHelper(int i, int j){
        
        std::map<std::vector<std::vector<char>>, bool> hashMap;
        hashMap[currMatrix] = true;
                
        int currCost {};
        int heuristicCost = heuristicSum();
        int totalCost = currCost + heuristicCost;
        
        std::priority_queue<int> frontier;
        std::map<int, std::vector<std::vector<std::vector<char>>>> frontier_matrix;
        std::map<int, std::vector<int>> frontier_currCost;
        std::vector<int> goalIdx;
        
        int states {1};
        while(heuristicCost!= 0){
            displayCurrMat();
            std::cout << currCost << " | " << heuristicCost << " | #" << states << std::endl;
            
            // Try East
            if(j-1 >= 0 && j-1 < 3){
                swap(currMatrix[i][j], currMatrix[i][j-1]);
                if(!hashMap[currMatrix]){
                    heuristicCost = heuristicSum();
                    totalCost = east_or_west + currCost + heuristicCost;
                    frontier.push(-totalCost);
                    frontier_matrix[-totalCost].push_back(currMatrix);
                    frontier_currCost[-totalCost].push_back(east_or_west + currCost);
                }                    
                swap(currMatrix[i][j], currMatrix[i][j-1]);
            }
            // Try South
            if(i-1 >= 0 && i-1 < 3){
                swap(currMatrix[i][j], currMatrix[i-1][j]);
                if(!hashMap[currMatrix]){
                    heuristicCost = heuristicSum();
                    totalCost = south + currCost + heuristicCost;
                    frontier.push(-totalCost);
                    frontier_matrix[-totalCost].push_back(currMatrix);
                    frontier_currCost[-totalCost].push_back(south + currCost);                    
                }  
                swap(currMatrix[i][j], currMatrix[i-1][j]);
            }
            // Try West
            if(j+1 >= 0 && j+1 < 3){
                swap(currMatrix[i][j], currMatrix[i][j+1]);
                if(!hashMap[currMatrix]){
                    heuristicCost = heuristicSum();
                    totalCost = east_or_west + currCost + heuristicCost;
                    frontier.push(-totalCost);
                    frontier_matrix[-totalCost].push_back(currMatrix); 
                    frontier_currCost[-totalCost].push_back(east_or_west + currCost);                   
                }  
                swap(currMatrix[i][j], currMatrix[i][j+1]);
            }
            // Try North
            if(i+1 >= 0 && i+1 < 3){
                swap(currMatrix[i][j], currMatrix[i+1][j]);
                if(!hashMap[currMatrix]){
                    heuristicCost = heuristicSum();
                    totalCost = north + currCost + heuristicCost;
                    frontier.push(-totalCost);
                    frontier_matrix[-totalCost].push_back(currMatrix);             
                    frontier_currCost[-totalCost].push_back(north + currCost);       
                }  
                swap(currMatrix[i][j], currMatrix[i+1][j]);
            }
            // Make a decision to move forward based on the priority queue containing min total cost
            int minCost = frontier.top();
            for(auto &pair: frontier_matrix){
                if(pair.first == minCost){
                        // Extracting in FIFO style for tie-breaker
                        currMatrix = frontier_matrix[minCost].front();
                        hashMap[currMatrix] = true;
                        currCost = frontier_currCost[minCost].front();
                        heuristicCost = -minCost - currCost;
                        goalIdx = findIndex('-', currMatrix);
                        i = goalIdx[0];
                        j = goalIdx[1];
                        frontier_matrix[minCost].erase(frontier_matrix[minCost].begin());
                        frontier_currCost[minCost].erase(frontier_currCost[minCost].begin());
                        break;                   
                }
            }
            frontier.pop();
            ++states;
        }
        
        displayCurrMat();
        std::cout << currCost << " | " << heuristicCost << " | #" << states << std::endl;
    }
    
    void AStarTraversal(){
        for(auto i = 0; i < 3; ++i){
            for(auto j = 0; j < 3; ++j){
                if(currMatrix[i][j] == '-'){
                    AStarTraversalHelper(i, j);
                    return;
                }
            }
        }
    }
    
};


int main(){
    std::vector<std::vector<char>> currMatrix {{'2', '8', '3'},{'6', '7', '4'},{'1', '5', '-'}};
    std::vector<std::vector<char>> goalMatrix {{'1', '2', '3'},{'8', '-', '4'},{'7', '6', '5'}};
    
//    std::vector<std::vector<char>> currMatrix {{'-', '2', '3'},{'1', '4', '5'},{'8', '7', '6'}};
//    std::vector<std::vector<char>> goalMatrix {{'1', '2', '3'},{'8', '-', '4'},{'7', '6', '5'}};
    
    WindyEightPuzzle puzzle(currMatrix, goalMatrix);
    puzzle.AStarTraversal();
    
// Testing helper functions
//    puzzle.displayCurrMat();
//    puzzle.displayGoalMat();
//    char item = '7';
//    auto idx = puzzle.findIndex(item, currMatrix);
//    std::cout << std::endl << "[" << idx[0] << ", " << idx[1] << "]";
//    idx = puzzle.findIndex(item, goalMatrix);
//    std::cout << std::endl << "[" << idx[0] << ", " << idx[1] << "]";
//    std::cout << std::endl;
//    std::cout << puzzle.heuristicSum();

    return 0;
}
