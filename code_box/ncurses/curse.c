#include <ncurses.h>
#include <stdlib.h>

WINDOW *fensterA, *fensterB;


int main ()
{

  initscr();
  cbreak();
  start_color();
  init_pair(1,COLOR_BLUE,COLOR_RED);
  init_pair(2,COLOR_BLACK,COLOR_GREEN);

  fensterA = newwin(20, 20, 2, 2);
  waddstr(fensterA, "Fenster A");
  wbkgd(fensterA, COLOR_PAIR(1));
  getch();
  wrefresh(fensterA);
  getch();

  fensterB = newwin(10,10,4,4);
  wbkgd(fensterB,COLOR_PAIR(2));
  waddstr(fensterB,"Fenster B");
  wrefresh(fensterB);
  getch();
  delwin(fensterB);
  refresh();
  getch();


  


  endwin();
  system("clear");
return (0);
}
