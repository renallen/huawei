#include "Deliver.h"

Deliver::Deliver(void)
{
	x=0;
	y=0;
	num=100;
	limit=100;
}

Deliver::update_xy(char s){
	    if (s=='N'){
	    	x-=1;
		}else if (s=='S'){
			x+=1;
		}else if (s='W'){
			y-=1; 
		}
        else if (s=='E'){
        	y+=1;
		}
        else{
		}
}

Deliver::set_xy(int x1, int y1){
	x=x1;
	y=y1;
}
Deliver::set_num(int n){
	num=n;
}

