#include <iostream>
#include "Deliver.h"
#include "House.h" 
using namespace std;

int main()
{
	House h;
	Deliver deliver;
	deliver.x=5;
	h.set_info(1,2,1000);
    cout << "num: " << h.num<< endl;
    getchar();
    return 0;
}
