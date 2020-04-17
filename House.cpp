#ifndef HOUSE_H
#define HOUSE_H

struct House{
	int x;
	int y;
	int num;
	bool isNeed;
	void set_info(int x1,int y1, int n){
		x=x1;y=y1;num=n;
	} 
	int update(int n){
		int left=num;
		if (isNeed){
        	if (num>=-n){
            	num=0;
            	isNeed=false;
            	return (n + left);
			}
        	else{
        		num =num+n;
            	return 0;
			}
		}else{
			
			if(num+n>=100){
				num=num+n-100;	
				return 100;
			}else{
				num=0;
				return left+n;
			} 

		}
	} 
	
};
#endif
