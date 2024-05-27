/************************************************************
   bridgen.c
   UNSW CSE
   COMP3411/9814
   Generate a random hashi puzzle of specified size.
*/

#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <time.h>

#define MAX_ROW     100
#define MAX_COL     100
#define MAX_HUB     500
#define MAX_BRIDGE 1000

#define NONE         -1
#define HORIZONTAL    0
#define VERTICAL      1

#define FALSE         0
#define TRUE          1

#define EAST          0
#define NORTH         1
#define WEST          2
#define SOUTH         3

//#define SPROUT
#define SPARSE
//#define TREE

/************************************************************
   Print the input map in character format.
*/
void print_map( int nrow, int ncol, int map[MAX_ROW][MAX_COL] )
{
  int r,c;

  for( r=0; r < nrow; r++ ) {
    for( c=0; c < ncol; c++ ) {
      if( map[r][c] > 0 ) {
        if( map[r][c] > 9 ) {
          putchar( map[r][c] + 'a' - 10 );
        }
        else {
          putchar( '0' + map[r][c] );
        }
      }
      else {
        putchar('.');
      }
    }
    putchar('\n');
  }
}

/************************************************************
   Return TRUE if location (r,c) is next to an existing island.
*/
int island_neighbor(
                    int r,
                    int c,
                    int nrow,
                    int ncol,
                    int map[MAX_ROW][MAX_COL]
                   )
{
  if(  ( c < ncol-1 && map[r][c+1] > 0 )
     ||( r >  0     && map[r-1][c] > 0 )
     ||( c >  0     && map[r][c-1] > 0 )
     ||( r < nrow-1 && map[r+1][c] > 0 )) {
     return( TRUE );
  }
  else {
    return( FALSE );
  }
}

/************************************************************
   Find a random start and end location and add a new bridge.
*/
int add_bridge(
               int map_empty,
               int nrow,
               int ncol,
               int max_plank,
               int    map[MAX_ROW][MAX_COL],
               int   dirn[MAX_ROW][MAX_COL],
               int nplank[MAX_ROW][MAX_COL]
              )
{
  int num_plank;
  int r0,c0,r1,c1;
  int r,c;

  if( map_empty == TRUE ) { // this will be the first bridge
    r = random() % nrow;
    c = random() % ncol;
  }
  else { // look for an existing island or bridge which can
         // be used as the starting point for a new bridge
    do {
      r = random() % nrow;
      c = random() % ncol;
#ifdef SPROUT
    } while( map[r][c] == 0 );
#else
    } while( dirn[r][c] == NONE && map[r][c] == 0 );
#endif
    if( island_neighbor(r,c,nrow,ncol,map)) {
      return( FALSE );
    }
  }

  // choose number of planks
  num_plank = 1 + ( random() % max_plank );

  // choose direction and end location for new bridge
  switch( random() % 4 ) {

  case EAST:
    c0 = c;
    r0 = r1 = r;
    c  = c0+1;
    while( c < ncol-1 && dirn[r][c] == NONE && map[r][c] == 0 ) {
      c++;
    }
#ifdef SPARSE
    if( dirn[r][c] != NONE ) {
      c--;
    }
#else
#ifdef TREE
    c--;
#endif
#endif
    if( c < c0+2 ) {    // too short
      return( FALSE );
    }
    c1 = c0 + 2 + (random() % ( c - c0 - 1 ));
    if( island_neighbor(r1,c1,nrow,ncol,map)) {
      return( FALSE );
    }
    for( c = c0+1; c < c1; c++ ) {
      dirn[r][c] = HORIZONTAL;
      nplank[r][c] = num_plank;
    }
    break;

  case NORTH:
    c0 = c1 = c;
    r1 = r;
    r  = r1-1;
    while( r > 0 && dirn[r][c] == NONE && map[r][c] == 0 ) {
      r--;
    }
#ifdef SPARSE
    if( dirn[r][c] != NONE ) {
      r++;
    }
#else
#ifdef TREE
    r++;
#endif
#endif
    if( r > r1-2 ) {
      return( FALSE );
    }
    r0 = r1 - 2 - (random() % ( r1 - r - 1 ));
    if( island_neighbor(r0,c0,nrow,ncol,map)) {
      return( FALSE );
    }
    for( r = r0+1; r < r1; r++ ) {
      dirn[r][c] = VERTICAL;
      nplank[r][c] = num_plank;
    }
    break;

  case WEST:
    c1 = c;
    r0 = r1 = r;
    c  = c1-1;
    while( c > 0 && dirn[r][c] == NONE && map[r][c] == 0 ) {
      c--;
    }
#ifdef SPARSE
    if( dirn[r][c] != NONE ) {
      c++;
    }
#else
#ifdef TREE
    c++;
#endif
#endif
    if( c > c1-2 ) {
      return( FALSE );
    }
    c0 = c1 - 2 - (random() % ( c1 - c - 1 ));
    if( island_neighbor(r0,c0,nrow,ncol,map)) {
      return( FALSE );
    }
    for( c = c0+1; c < c1; c++ ) {
      dirn[r][c] = HORIZONTAL;
      nplank[r][c] = num_plank;
    }
    break;

  case SOUTH:
    c0 = c1 = c;
    r0 = r;
    r  = r0+1;
    while( r < nrow-1 && dirn[r][c] == NONE && map[r][c] == 0 ) {
      r++;
    }
#ifdef SPARSE
    if( dirn[r][c] != NONE ) {
      r--;
    }
#else
#ifdef TREE
    r--;
#endif
#endif
    if( r < r0+2 ) {
      return( FALSE );
    }
    r1 = r0 + 2 + (random() % ( r - r0 - 1 ));
    if( island_neighbor(r1,c1,nrow,ncol,map)) {
      return( FALSE );
    }
    for( r = r0+1; r < r1; r++ ) {
      dirn[r][c] = VERTICAL;
      nplank[r][c] = num_plank;
    }
    break;
  }

  // re-compute number of planks at start of new bridge
  nplank[r0][c0] = 0;
  map[r0][c0] = 0;
  if( c0 < ncol-1 && dirn[r0][c0+1] == HORIZONTAL )
    map[r0][c0] += nplank[r0][c0+1];
  if( r0 >  0     && dirn[r0-1][c0] ==  VERTICAL  )
    map[r0][c0] += nplank[r0-1][c0];
  if( c0 >  0     && dirn[r0][c0-1] == HORIZONTAL )
    map[r0][c0] += nplank[r0][c0-1];
  if( r0 < nrow-1 && dirn[r0+1][c0] ==  VERTICAL  )
    map[r0][c0] += nplank[r0+1][c0];

  // re-compute number of planks at end of new bridge
  nplank[r1][c1] = 0;
  map[r1][c1] = 0;
  if( c1 < ncol-1 && dirn[r1][c1+1] == HORIZONTAL )
    map[r1][c1] += nplank[r1][c1+1];
  if( r1 >  0     && dirn[r1-1][c1] ==  VERTICAL  )
    map[r1][c1] += nplank[r1-1][c1];
  if( c1 >  0     && dirn[r1][c1-1] == HORIZONTAL )
    map[r1][c1] += nplank[r1][c1-1];
  if( r1 < nrow-1 && dirn[r1+1][c1] ==  VERTICAL  )
    map[r1][c1] += nplank[r1+1][c1];

  return( TRUE );
}

int main( int argc, char *argv[] )
{
  int    map[MAX_ROW][MAX_COL]; // islands
  int   dirn[MAX_ROW][MAX_COL]; // NONE, HORIZONTAL or VERTICAL
  int nplank[MAX_ROW][MAX_COL];
  int max_plank = 3;
  int nrow, ncol;
  int nfail;
  int r,c;

  if( argc < 2 || !isdigit(argv[1][0])) {
    printf("Usage: %s <nrow> [ncol]\n",argv[0]);
    printf("Generate a random Hashi puzzle of size nrow x ncol;\n");
    printf("can be run repeatedly, producing different puzzles each time;\n");
    printf("ncol defaults to nrow.\n");
    return 0;
  }
  else {
    nrow =  atoi(argv[1]);
  }
  if( nrow < 3 ) {
    nrow = 3;
  }
  if( nrow > MAX_ROW ) {
    nrow = MAX_ROW;
  }
  if( argc < 3 ) {
    ncol = nrow;
  }
  else {
    ncol = atoi(argv[2]);
  }
  if( ncol < 3 ) {
    ncol = 3;
  }
  if( ncol > MAX_COL ) {
    ncol = MAX_COL;
  }
  srandom(time(NULL));

  for( r=0; r < nrow; r++ ) {
    for( c=0; c < ncol; c++ ) {
      map[r][c] = 0;
      nplank[r][c] = 0;
      dirn[r][c] = NONE;
    }
  }

  // add the first bridge
  while( !add_bridge( TRUE, nrow, ncol, max_plank, map, dirn, nplank ))
    ;

  // keep adding bridges until it becomes too difficult
  nfail = 0;
  while( nfail < 200 ) {
    nfail=0;
    while( nfail < 200 && !add_bridge( FALSE, nrow, ncol, max_plank, map, dirn, nplank )) {
      nfail++;
    }
  }

  print_map( nrow, ncol, map );

  return 0;
}

