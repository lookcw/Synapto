/*
 * matrix.c
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

#include <assert.h>
#include <stdarg.h>
#include <stdlib.h>
#include <string.h>

#include "matrix.h"

#define real_t_fmt	" %lf"


void * xcalloc(size_t nmemb, size_t size)
{
	void * mem = calloc(nmemb, size);
	assert(mem);
	return mem;
}

// double M1D[I];
void * MATRIX1D(int T, int I)
{
	return xcalloc(I,T);
}

void Free_M1D(void * M)
{
	free(M);
}

// double M1D[I][J];
// double*M2D[I];
void * MATRIX2D(int T, int I, int J)
{
	void ** M2D;
	int i;
	M2D = xcalloc(I, sizeof(void*));
	M2D[0] = MATRIX1D(T,I*J);
	for (i=1; i < I; i++)
		M2D[i] = ((void*)(M2D[i-1])) + J*T;
	return M2D;
}

void Free_M2D(void * M)
{
	Free_M1D(((void **)M)[0]);
	free(M);
}

// double  M1D[I][J][K];
// double* M2D[I][J];
// double**M3D[I];
void * MATRIX3D(int T, int I, int J, int K)
{
	void *** M3D;
	int i;
	M3D = xcalloc(I, sizeof(void**));
	M3D[0] = MATRIX2D(T,I*J,K);
	for (i=1; i < I; i++)
		M3D[i] = ((void*)(M3D[i-1])) + J*sizeof(void*);
	return M3D;
}

void Free_M3D(void * M)
{
	Free_M2D(((void **)M)[0]);
	free(M);
}


static char *afgets(char**lnpr, int *lnsz, FILE *where)
{
	char * line = *lnpr;
	int size = *lnsz;
	int len = 0;

	if (!size)
		size = *lnsz = 1;
	if (!line)
		line = *lnpr = malloc(size);
	if (!line) return NULL;

	while(fgets(line,size,where))
	{
		line = *lnpr;
		len = strlen(line);
		assert(len);
		if (line[len-1]=='\n') {
			if (line[0] == '#') { // Comment from # to EOL
				line[0] = '0';
				continue;
			} else {
				break;
			}
		}
		// double the space.
		size = (*lnsz *= 2);
		
		line = *lnpr = realloc(line,size);
		if (!line) return NULL;

		line += len;
		size -= len;
	}

	return len ? *lnpr : NULL;
}

/*
 * M2DT_scan: scan 'where' for a double MATRIX2DT, auto-detecting
 * its number of columns (C) (== #of %g per line)
 * and number of rows (F) (== # of lines)
 * and while scanning also tranposes
 */
void * M2DT_scan(FILE*where,int*F,int*C)
{
	double ** M2DT = NULL;
	static int lnsz = 64;
	char * line = NULL;
	int nlines = 0;
	int ncolms = 0;
	int chunck = 0;
	int chunckC = 0;
	int size = 0;

	while (afgets(&line,&lnsz,where)) // Reading a line
	{
		char * spcs=",	\n";
		char * token;
		char * pntr = line;
		int cntr = 0;
		char reajustar = 0;
	
		while ((token = strtok(pntr,spcs))) // we make tokens with the values from the line
		{
			pntr = NULL;
			double value;
			if(!sscanf(token,real_t_fmt, &value)) break; // Read value from token
			if(!cntr) size += sizeof(double); // Calculate size for result matrix rows (the old columns size)
			cntr++;
			if(!nlines && cntr>chunckC) { // During the first line we adjust the column size (the old rows size) 
				if(!chunckC)	chunckC = 128; // size_column =  chunckC x double 
				else		chunckC <<= 1; // we double the size if need more 
				M2DT = realloc(M2DT,chunckC*sizeof(double));
			}
			if (reajustar || size > chunck) // If need more size for rows we increase it
			{
				if (!chunck) chunck = 1024;
				else if(size>chunck) chunck <<= 1; // doubled
	
				M2DT[cntr-1] = realloc(M2DT[cntr-1],chunck);
				reajustar = 1; // the resize will does in all rows
			}
			M2DT[cntr-1][nlines] = value; // Finally we copy the value
		}
		if (pntr) break;
		if (!nlines) *C = ncolms = cntr; // set the numbers of readed columns
		else assert(ncolms == *C);
		nlines++;
	}

	free(line);

	*F = nlines; // set the numbers of readed rows
	M2DT = realloc(M2DT,sizeof(void*)*ncolms);
	int nfilas;

	for (nfilas=0; nfilas < ncolms; nfilas++)
		M2DT[nfilas] = realloc(M2DT[nfilas],nlines*sizeof(double));

	return M2DT;
}

/*
 * M2D_scan scan where for a double MATRIX2D, auto-detecting
 * its number of columns (C) (== # of %g per line)
 * and number of rows (F) (== # of lines)
 */
void * M2D_scan(FILE*where,int*F,int*C)
{
	double * data = NULL;
	static int lnsz = 64;
	char * line = NULL;
	int nlines = 0;
	int ncolms = 0;
	int chunck = 0;
	int size = 0;

	while (afgets(&line,&lnsz,where))
	{
		char * spcs=" 	\n";
		char * token;
		char * pntr = line;
		int cntr = 0;
		while ((token = strtok(pntr,spcs)))
		{
			pntr = NULL;
			double value;
			if(!sscanf(token,real_t_fmt, &value)) break;
			cntr++;
			size += sizeof(double);
			if (size > chunck)
			{
				if (!chunck)	chunck = 1024;
				else		chunck *= 2;
				data = realloc(data,chunck);
			}
//			data = realloc(data,sizeof(double)*(nlines*ncolms+cntr));
			data[nlines*ncolms+cntr-1] = value;
		}
		if (pntr) break;
		if (!nlines) *C = ncolms = cntr;
		else assert(ncolms == *C);
		nlines++;
	}

	free(line);

	if (!data) return NULL;
	*F = nlines;
	data = realloc(data,sizeof(double)*(nlines*ncolms));

	void ** M2D;
	M2D = xcalloc(*F, sizeof(void*));
	for (nlines=0; nlines < *F; nlines++)
	{
		M2D[nlines] = data;
		data += *C;
	}

	return M2D;
}

void * C2M1D(void*data,int D1,int T)
{ //       T data [D1]
	if (!data)
		data = xcalloc(D1,T);
	return data;
} 

void * C2M2D(void*data,int D1,int D2,int T)
{ //       T data [D1][D2]
	void**M2D;
	M2D = xcalloc(D1,sizeof(void*));
	M2D[0] = C2M1D(data,D1*D2,T);
	int d;
	for (d=1; d<D1; d++)
		M2D[d] = M2D[d-1] + D2*T;
	return M2D;
} 

void * C2M3D(void*data,int D1,int D2,int D3,int T)
{ //       T data [D1][D2][D3]
	void***M3D;
	M3D = xcalloc(D1,sizeof(void**));
	M3D[0] = C2M2D(data,D1*D2,D3,T);
	int d;
	for (d=1; d<D1; d++)
		M3D[d] = M3D[d-1] + D2;   // pointer arithmetic!!
	return M3D;
} 

int M1D_print(FILE*where,double*data,int D1)
{
	int d1;
	int cntr = 0;
	for (d1=0; d1<D1; d1++)
	{
		cntr += fprintf(where,real_t_fmt,data[d1]);
	}
	fprintf(where,"\n");

	return cntr;
}

int M2D_print(FILE*where,double**data,int D1,int D2)
{
	int d1;
	int d2;
	int cntr = 0;
	for (d1=0; d1<D1; d1++)
	{
		for (d2=0; d2<D2; d2++)
		{
			cntr += fprintf(where,real_t_fmt,data[d1][d2]);
		}
		fprintf(where,"\n");
	}
	fprintf(where,"\n");

	return cntr;
}

int M3D_print(FILE*where,double***data,int D1,int D2,int D3)
{
	int d1;
	int d2;
	int d3;
	int cntr = 0;
	for (d1=0; d1<D1; d1++)
	{
		for (d2=0; d2<D2; d2++)
		{
			for (d3=0; d3<D3; d3++)
			{
				cntr += fprintf(where,real_t_fmt,data[d1][d2][d3]);
			}
			fprintf(where,"\n");
		}
		fprintf(where,"\n");
	}
	fprintf(where,"\n");

	return cntr;
}

int M3D_fprintf(FILE*where,char*fmt,int***data,int D1,int D2,int D3)
{
	int d1;
	int d2;
	int d3;
	int cntr = 0;
	for (d1=0; d1<D1; d1++)
	{
		for (d2=0; d2<D2; d2++)
		{
			for (d3=0; d3<D3; d3++)
			{
				cntr += fprintf(where,fmt,data[d1][d2][d3]);
			}
			fprintf(where,"\n");
		}
		fprintf(where,"\n");
	}
	fprintf(where,"\n");

	return cntr;
}

