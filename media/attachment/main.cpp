#include <iostream>
using namespace std;
#include <cstdlib>
#include <cmath>

/* run this program using the console pauser or add your own getch, system("pause") or input loop */
int isTriangle(int, int, int); 
int leepYear(int);
int main(int argc, char** argv) {
	int m,n,k;
	cin>>m>>n>>k;
	cout<<isTriangle(m,n,k);
	int l;
	cin>>l;
	leepYear(l);
	
}

int isTriangle(int m, int n, int k) {
	if( ( a > abs(b-c) && a < b+c  ) && ( b > abs(a-c) && b < a+c ) && ( c > abs(a-b) && c < a+b ) ) {
		cout<<"That is Triangle"<<endl;
		if( (pow(a,2) == pow(b,2) + pow(c,2)) || ( pow(b,2) == pow(c,2) + pow(a,2) ) || ( pow(c,2) == pow(a,2) + pow(b,2) ) ) {
		cout<<"That is Rectangular\n";
		return 0;
	} else {
		cout<<"Not rectangular";
	}
		return 0;
	} else {
		cout<<"Not triangle";
	}
	
	
}

int leepYear(int f) {
	if(f%4==0) {
		cout<<"Year is leep";
		return 0;
	} else {
		cout<<"Year is not leep";
		return 0;
	}
	
}
