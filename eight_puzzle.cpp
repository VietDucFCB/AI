#include <iostream>
#include <queue>
#include <vector>
#include <cstring>
#include <climits>
#include <algorithm>
using namespace std;
#define N 3

struct Node
{
    Node* parent; // stores the parent node of the current node
    int mat[N][N]; // stores matrix
    int x, y; // stores blank tile coordinates
    int cost; // stores the number of misplaced tiles
    int level; // stores the number of moves so far
};


void printMatrix(int mat[N][N])
{
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++)
            printf("%d ", mat[i][j]);
        printf("\n");
    }
}

// Function to allocate a new node
Node* newNode(int mat[N][N], int x, int y, int newX, int newY, int level, Node* parent)
{
    Node* node = new Node;
    node->parent = parent;
    memcpy(node->mat, mat, sizeof node->mat); // copy data from parent node to current node
    swap(node->mat[x][y], node->mat[newX][newY]); // move tile by 1 position
    node->cost = INT_MAX; // set number of misplaced tiles
    node->level = level; // set number of moves so far
    node->x = newX; // update new blank tile coordinates
    node->y = newY;
    return node;
}

// bottom, left, top, right
int row[] = { 1, 0, -1, 0 };
int col[] = { 0, -1, 0, 1 };

// Function to calculate the number of misplaced tiles
int calculateCost(int initial[N][N], int final[N][N])
{
    int count = 0;
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++)
            if (initial[i][j] && initial[i][j] != final[i][j])
                count++;
    return count;
}

// Function to check if (x, y) is a valid matrix coordinate
bool isSafe(int x, int y)
{
    return (x >= 0 && x < N && y >= 0 && y < N);
}

// print path from root node to destination node, including the step number
void printPath(Node* root)
{
    static int step = 1; // Initialize step counter
    if (root == NULL)
        return;

    printPath(root->parent); // Recursive call to print previous steps

    // Print current matrix state with step number
    printf("Sau trạng thái thứ %d:\n", step++);
    printMatrix(root->mat);
    printf("\n");
}

// Comparison object to be used to order the heap
struct comp
{
    bool operator()(const Node* lhs, const Node* rhs) const
    {
        return (lhs->cost + lhs->level) > (rhs->cost + rhs->level);
    }
};

// Function to solve N*N - 1 puzzle algorithm using Branch and Bound
void solve(int initial[N][N], int x, int y, int final[N][N])
{
    priority_queue<Node*, vector<Node*>, comp> pq; // Create a priority queue

    Node* root = newNode(initial, x, y, x, y, 0, NULL); // create root node
    root->cost = calculateCost(initial, final); // calculate cost

    pq.push(root); // Add root to list of live nodes

    while (!pq.empty())
    {
        Node* min = pq.top();
        pq.pop();

        if (min->cost == 0) // if min is the answer node
        {
            printPath(min); // Print the path from root to the solution
            return;
        }

        for (int i = 0; i < 4; i++) // do for each child of min (max 4 children)
        {
            if (isSafe(min->x + row[i], min->y + col[i]))
            {
                Node* child = newNode(min->mat, min->x, min->y, min->x + row[i], min->y + col[i], min->level + 1, min);
                child->cost = calculateCost(child->mat, final);
                pq.push(child); // Add child to list of live nodes
            }
        }
    }
}

// Driver code
int main()
{
    // Initial configuration (Value 0 is used for empty space)
    int initial[N][N] =
    {
        {7, 2, 4},
        {5, 0, 6},
        {8, 3, 1}
    };

    // Solvable Final configuration (Value 0 is used for empty space)
    int final[N][N] =
    {
        {0, 1, 2},
        {3, 4, 5},
        {6, 7, 8}
    };

    int x = 1, y = 2; // Blank tile coordinates in initial configuration

    solve(initial, x, y, final);

    return 0;
}
