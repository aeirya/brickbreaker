#include <stdio.h>
#include <time.h>
#include <stdlib.h>

int N;

typedef struct Blocks
{
    int health; //health
    int isBomb;

} Block;

Block **bricks;

int Rand(int s)
{
    srand(s);
    return rand()%10;
}

void descend()
{
    
}

void generateBricks()
{
    Block b;
    bricks[0][1] = 
    
}

void init()
{
    bricks = (Block**) malloc( 6*N*N * sizeof(Block*));
    for(int i =0; i< 3*N; i++)
        bricks[i] = (Block*) malloc( 2*N * sizeof(Block) );
    
    //scanf("%d", %N);

    N = 2;
}

void Update()
{
    
}

int main()
{
    init();

    int phi;
    while(1)
    {
        printf("\tphi:");
        scanf("%d", &phi);
    }

    Update();

    return 0;
}

