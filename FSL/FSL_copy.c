/*
 * FSL.c
 * Fast Synchronization Likelihood main.
 */
/*
	Copyright (C) 2011,2014 Francisco ROSALES <frosal@fi.upm.es>

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU Lesser General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU Lesser General Public License for more details.

	You should have received a copy of the GNU Lesser General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#include <sys/resource.h>
#include <sys/time.h>
#include <sys/times.h>
#include <sys/types.h>
#include <assert.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sysexits.h>
#include <time.h>
#include <unistd.h>

#include "matrix.h"

#define MY_NAME	"synclike"

/* Command line arguments */
int D; 		// = 0;
int C;		// = 0;
int L;		// = 1;
int M;		// = 10;
int W1;		// = 100;
int W2;		// = 410;
double Pref;	// = 0.049;
extern int F;

char * input;
char * output;
FILE * wherein;
FILE * whereout;

extern int parse_args(int argc, char *argv[]);

extern void FSL (const int I,const int K,double**data,const int L,const int M,const int W1,const int W2,const double Pref,double sync_like[K][K]);

int main(int argc, char ** argv)
{
	argc = parse_args(argc, argv);

	double**resul = NULL;	// = MATRIX2D(sizeof(double),C,C);
	double**datos = NULL;	// = MATRIX2D(sizeof(double),D,C);

	if (!(wherein = (input ? fopen(input,"r") : stdin))) {
		fprintf(stderr,"%s: Open.input(\"%s\"): %m", argv[0], input);
		exit(1);
	}

	if (!(whereout = (output ? fopen(output,"w") : stdout))) {
		fprintf(stderr,"%s: Open.output(\"%s\"): %m", argv[0], output);
		exit(1);
	}

	datos = M2DT_scan(wherein,&D,&C);
	fprintf(stderr,"#! %s -d %d -c %d -l %d -m %d -x %d -w %d -p %g %s\n",
		argv[0],D,C,L,M,W1,W2,Pref,F?"-F":"");

	double sync_like[C][C];
	memset(sync_like,0,sizeof(sync_like));

	FSL(D,C,datos,L,M,W1,W2,Pref,sync_like);

	if (!resul) resul = C2M2D(sync_like,C,C,sizeof(double));
	M2D_print(whereout,resul,C,C);

	if (input) fclose(wherein);
	if (output) fclose(whereout);

	return 0;
}
