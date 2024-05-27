/************************************************************
   bridgecheck.c
   UNSW CSE
   COMP3411/9814
   Check whether a solution to the hashi puzzle is correct.
*/
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

#define MAX_ROW  100
#define MAX_COL  100

#define FALSE      0
#define TRUE       1

/************************************************************
   Return TRUE if the character is an island.
*/
int is_island( char ch )
{
  return(( ch >= '1' && ch <= '9' )||( ch >= 'a' && ch <= 'c' ));
}

/************************************************************
   Return TRUE if the character is part of a bridge.
*/
int is_bridge( char ch )
{
  switch( ch ) {
    case '-': case '|': case '=': case '\"': case 'E': case '#':
      return TRUE;
    default:
      return FALSE;
  }
}

/************************************************************
   Convert island character to number of bridges.
*/
int island2num( char ch )
{
  int num;
  if( ch >= 'a' && ch <= 'c' ) {
    num = 10 + ch - 'a';
  }
  else {
    num =  0 + ch - '0';
  }
  return( num );
}

/************************************************************
   Scan map into a 2-D array of characters.
   Return (implicitly) the number of rows and columns,
   and the location of the first (top left) island.
*/
void scan_map(
              FILE *fp,
              int *p_nrow,
              int *p_ncol,
              int *p_row0,
              int *p_col0,
              char map[MAX_ROW][MAX_COL]
             )
{
  int ch;
  int r=0,c=0;

  *p_ncol = 1;

  while(( ch = getc(fp)) != EOF ) {
    if( ch == '\n') {
      if( c >= *p_ncol ) {
        *p_ncol = c;
        r++;
      }
      c=0;
    }
    else {
      if( *p_row0 < 0 && is_island(ch)) {
        *p_row0 = r;
        *p_col0 = c;
      }
      map[r][c++] = ch;
    }
  }
  *p_nrow = r;
}

/************************************************************
   scan the proposed solution into a 2-D array of characters.
*/
void scan_solution(
                   FILE * fp,
                   int nrow,
                   int ncol,
                   int row0,
                   int col0,
                   char  map[MAX_ROW][MAX_COL],
                   char soln[MAX_ROW][MAX_COL]   
                  )
{
  int ch;
  int r,c;
  
  for( r=0; r < nrow; r++ ) {
    for( c=0; c < ncol; c++ ) {
      soln[r][c] = ' ';
    }
  }

  r = row0;
  c = col0;
  
  // scan for the first island
  while(( ch = getc(fp)) != EOF && !is_island(ch))
    ;
  
  if( !is_island( ch )) {
    if( isprint(ch)) {
      printf("Unexpected character in input: %c\n",ch);
    }
    else if( ch == EOF ) {
      printf("EOF\n");
    }
    else {
      printf("Non-printable character in input (ascii #%d)\n",ch);
    }
    exit( 1 );
  }
  soln[r][c++] = ch;

  while(( ch = getc(fp)) != EOF && r < nrow ) {
    if( c >= ncol ) {
      while( ch != '\n' && ch != EOF ) {
        ch = getc(fp);
      }
    }
    if( ch == '\n') {
      c=0;
      r++;
    }
    else if( is_island(ch) || is_bridge(ch) || ch == ' ' ) {
      soln[r][c++] = ch;
    }
    else {
      if( isprint(ch)) {
        printf("Unexpected character in input: %c\n", ch );
      }
      else {
        printf("Non-printable character in input (ascii #%d)\n", ch );
      }
      exit( 1 );
    }
  }
  if( r < nrow ) {
    printf("Expected %d rows, found %d.\n", nrow, r );
    exit(1);
  }
}

int main( int argc, char *argv[] )
{
  char  map[MAX_ROW][MAX_COL];
  char soln[MAX_ROW][MAX_COL];
  char mark[MAX_ROW][MAX_COL];
  FILE *fp;
  int valid = TRUE;
  int erroneous_island = 0;
  int missing_island = 0;
  int wrong_island = 0;
  int wrong_count = 0;
  int wrong_bridge = 0;
  int nplank;
  int nrow, ncol;
  int row0=-1, col0=0; // co-ordinates of top left island
  int r,c;
  
  if( argc < 2 ) {
    printf("Usage: %s sX.in < sX.out\n", argv[0] );
    return 0;
  }
  fp = fopen( argv[1],"r" );
  if( fp == NULL ) {
    printf("Failed to open file: %s\n", argv[1] );
    return 0;
  }

  scan_map( fp, &nrow, &ncol, &row0, &col0, map );
  
  scan_solution( stdin, nrow, ncol, row0, col0, map, soln );

  for( r=0; r < nrow; r++ ) {
    for( c=0; c < ncol; c++ ) {
      mark[r][c] = soln[r][c];
    }
  }

  for( r=0; r < nrow; r++ ) {
    for( c=0; c < ncol; c++ ) {
      if( is_island(soln[r][c]) && !is_island(map[r][c])) {
        mark[r][c] = 'x';   // erroneous island
        erroneous_island++; valid = FALSE;
      }
      else if( is_island(map[r][c]) && !is_island(soln[r][c])) {
        mark[r][c] = 'o';   // missing island
        missing_island++; valid = FALSE;
      }
      else if( soln[r][c] == '-' || soln[r][c] == '=' || soln[r][c] == 'E' ) {
        if( c == 0 || c == ncol-1 ) {
          mark[r][c] = '%'; // disconnected bridge
          wrong_bridge++; valid = FALSE;
        }
        else if( soln[r][c+1] != soln[r][c] && !is_island(soln[r][c+1])) {
          mark[r][c] = '%'; // disconnected bridge
          wrong_bridge++; valid = FALSE;
        }
        else if( soln[r][c-1] != soln[r][c] && !is_island(soln[r][c-1])) {
          mark[r][c] = '%'; // disconnected bridge
          wrong_bridge++; valid = FALSE;
        }
      }
      else if( soln[r][c] == '|' || soln[r][c] == '\"' || soln[r][c] == '#' ) {
        if( r == 0 || r == nrow-1 ) {
          mark[r][c] = '%'; // disconnected bridge
          wrong_bridge++; valid = FALSE;
        }
        else if( soln[r+1][c] != soln[r][c] && !is_island(soln[r+1][c])) {
          mark[r][c] = '%'; // disconnected bridge
          wrong_bridge++; valid = FALSE;
        }
        else if( soln[r-1][c] != soln[r][c] && !is_island(soln[r-1][c])) {
          mark[r][c] = '%'; // disconnected bridge
          wrong_bridge++; valid = FALSE;
        }
      }
      else if( is_island( map[r][c] )) {
        if( soln[r][c] != map[r][c] ) {
          mark[r][c] = '?'; // island with wrong number
          wrong_island++; valid = FALSE;
        }
        else {
          nplank = 0;
          if( r > 0 ) {
            if( soln[r-1][c] == '|' ) {
              nplank += 1;
            }
            else if( soln[r-1][c] == '\"' ) {
              nplank += 2;
            }
            else if( soln[r-1][c] == '#' ) {
              nplank += 3;
            }
          }
          if( r < nrow-1 ) {
            if( soln[r+1][c] == '|' ) {
              nplank += 1;
            }
            else if( soln[r+1][c] == '\"' ) {
              nplank += 2;
            }
            else if( soln[r+1][c] == '#' ) {
              nplank += 3;
            }
          }
          if( c > 0 ) {
            if( soln[r][c-1] == '-' ) {
              nplank += 1;
            }
            else if( soln[r][c-1] == '=' ) {
              nplank += 2;
            }
            else if( soln[r][c-1] == 'E' ) {
              nplank += 3;
            }
          }
          if( c < ncol-1 ) {
            if( soln[r][c+1] == '-' ) {
              nplank += 1;
            }
            else if( soln[r][c+1] == '=' ) {
              nplank += 2;
            }
            else if( soln[r][c+1] == 'E' ) {
              nplank += 3;
            }
          }
          if( nplank != island2num( map[r][c] )) {
            mark[r][c] = '+'; // wrong plank count
            wrong_count++; valid = FALSE;
          }
        }
      }
    }
  }

  if( valid ){
    printf("Valid Solution.\n");
  }
  else {

    for( r=0; r < nrow; r++ ) {
      for( c=0; c < ncol; c++ ) {
        putchar( mark[r][c] );
      }
      putchar('\n');
    }

    if( erroneous_island > 0 ) {
      printf(" x : Erroneous Island\n");
    }
    if( missing_island > 0 ) {
      printf(" o : Missing Island\n");
    }
    if( wrong_island > 0 ) {
      printf(" ? : Island with Wrong Number\n");
    }
    if( wrong_bridge > 0 ) {
      printf(" %% : Disconnected Bridge\n");
    }
    if( wrong_count > 0 ) {
      printf(" + : Bridges not Adding Up\n");
    }
    putchar('\n');
  }
  
  return 0;
}

