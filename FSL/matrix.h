/*
 * matrix.h
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

#ifndef ___MATRIX_H___
#define ___MATRIX_H___

#include <stdio.h>

void * MATRIX1D(int T, int I);
void * MATRIX2D(int T, int I, int J);
void * MATRIX3D(int T, int I, int J, int K);

void Free_M1D(void * M);
void Free_M2D(void * M);
void Free_M3D(void * M);

void * C2M1D(void*data,int D1,int T);
void * C2M2D(void*data,int D1,int D2,int T);
void * C2M3D(void*data,int D1,int D2,int D3,int T);

void * M2DT_scan(FILE*where, int*F, int*C);
void * M2D_scan(FILE*where, int*F, int*C);

int M1D_print(FILE*where,double*data,int D1);
int M2D_print(FILE*where,double**data,int D1,int D2);
int M3D_print(FILE*where,double***data,int D1,int D2,int D3);
int M3D_fprintf(FILE*where,char*fmt,int***data,int D1,int D2,int D3);

#endif/*___MATRIX_H___*/
