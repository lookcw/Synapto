/*
 * FSL_delta.c
 * Fast Synchronization Likelihood delta.
 *
 * This module implements the FSL_delta method as described in the article:
 *	"An efficient implementation of the synchronization likelihood algorithm for functional connectivity"
 *	Francisco Rosales, Antonio Garcia-Dopico, Ricardo Bajo, Angel Nevado
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
#include <math.h>
#include <omp.h>
#include <string.h>

#ifdef ENTROPY
#define ENTROPY
#endif

static inline int FSL_delta(const int I0,const int Ix,const int Jx,const int Ib,const int Ie,const int K,double **data/*[K][Ix-I0]*/,const int L,const int M,const int W1,const int W2,const double Pref,const int W,const int N,const int S,double sync_like[K][K])
{
	int i;
	int ret = 0;

#ifdef ENTROPY
	long long histogram[N+1];
	memset(histogram,0,sizeof(histogram));
#endif

#ifdef _OPENMP
	#pragma omp parallel for default(shared) private(i)
#endif
	for (i=Ib; i<Ie; i+=S)
	{
		int k;
		int j;
		int n;
		int h;
		int wt = 0;
		short nearest[K][N];
		j = i-W2;
		const int Jbs[2] = { j<I0 ? I0 : j, i+W1+1 };
		j = i+W2+1;
		const int Jes[2] = { i-W1, j>Jx ? Jx : j };

		for (k=0; k<K; k++)
		{
			double distance[N];
			short * nearestk = nearest[k];
			int w = 0;
			int p = 0;
			int C = 0;

			for (w=p=0; p<2; p++)
			{
				const int Jb = Jbs[!p];
				const int Je = Jes[!p];

				for (j=Jb; j<Je; j++,w++)
				{
					// Euclidean distance.
					double sum = 0;
					double dif;
					int x = i;
					int y = j;
					int m;

					for (m=M; m; m--)
					{
						if (x >= Ix) break;	// Fade-out
						if (y >= Ix) break;	// Fade-out
						assert((x-I0)>=0);
						assert((y-I0)>=0);
						dif = data[k][x-I0] - data[k][y-I0];
						sum += dif*dif;
						x += L;
						y += L;
					}
			//		sum = SQRT(sum);
					// Ordered insertion.
					for (n=C; n; n--)
					{
						if (sum >= distance[n-1])
							break;
						if (n < N) {
							distance[n] = distance[n-1];
							nearestk[n] = nearestk[n-1];
						}
					}
					if (n < N) {
						distance[n] = sum;
						nearestk[n] = w;
					}
					// Remember only the N closer pairs.
					if (C < N) C++;
				}
			}
			wt = w;		/* Real number of pairs */
		}

		const int W = wt;		/* Real number of pairs */
		const int N = ceil(Pref*W);	/* Number of nearest */
		for (k=0; k<K; k++)
		{
			short * nearestp;
			char boolmap[W];
			memset(boolmap,0,sizeof(boolmap));
			nearestp = nearest[k];
			for (n=N; n; n--)
				boolmap[*nearestp++] = 1;
			// Compute the full symmetric matrix.
			for (h=0; h<K; h++)
			{
				nearestp = nearest[h];
				int nhits = 0;
				for (n=N; n; n--)
					nhits += boolmap[*nearestp++];
#ifdef _OPENMP
				double*where = &sync_like[k][h];
				double value = (double)nhits/N;
				#pragma omp atomic
				*where += value;
#else
				sync_like[k][h] += (double)nhits/N;
#endif
#ifdef ENTROPY
#ifdef _OPENMP
				#pragma omp atomic
#endif
				// How many times each value appears
				histogram[nhits]++;
#endif
			}
		}
#ifdef _OPENMP
		#pragma omp atomic
#endif
		ret++;
	}

#ifdef ENTROPY
	// Entropy Hs
	double xaM = 1.0 / (K*K*(ret?ret:-1)); /* Avoid division by zero */
	double Pi;
	double Hs = 0.0;
	// Total number of hits.
	long long total = 0;

	int n;
	for (n=N; n>=0; n--)
	{
		if (!histogram[n]) continue;
		Pi = histogram[n] * xaM;
		Hs -= Pi * log(Pi);

		total += n * histogram[n];
	}
	Hs /= log(2.0);

	i = Ib+ret*S;
	fprintf(stderr,"[%d]\t"real_t_fmt"\t"real_t_fmt"\n",i,(double)total/W,Hs);
#endif

	return ret;
}

/* Command line arguments */
int S = 1;	/* "speed" factor = increment between computed samples. */
int T = 0;	/* "trigger" =  how many samples between snapshots. */
int F = 0;	/* "fadeout" =  Fadeout the (m-1)*l last embedded vectors. */

void FSL(const int I,const int K,double **data/*[K][I]*/,const int L,const int M,const int W1,const int W2,const double Pref,double sync_like[K][K])
{
	const	int W = 2*(W2-W1);	/* Number of pairs. */
	const	int N = ceil(Pref*W);	/* Number of nearest. */
		int I0 = 0;		/* Absolute index of the first data stored in each dataK[]. */
		int Ix = I;		/* Absolute index of the limit data stored in each dataK[]. */
		int IE = I;		/* Limit i sample to compute. */
		int Jx = I;		/* Limit i vector to use. */
		int Ib = 0;		/* First i sample to compute in each call. */
		int Ie = I;		/* Limit i sample to compute in each call. */
		int cnt = 0;		/* Samples computed in a single call. */
		int total = 0;		/* Total number of samples computed. */

	memset(sync_like,0,sizeof(sync_like[0][0])*K*K);

	int k;
	int h;
	int i, len;
	double *dataK[K];

	for(k=0;k<K;k++) dataK[k] = &data[k][I0];

	if (!F) {
		/*
		 * Do not fadeout the last embedded vectors.
		 * Do not use the last data.
		 * This is Stam's 2002 compatibility.
		 */
		IE = I-(M-1)*L;
		Jx = I-(M-1)*L;
	}

	for (i=0; i<IE; i+=S*cnt)
	{
		len = T ? T : (IE-i);
		Ib = i;
		Ie = Ib + len;
		if (Ie > IE) Ie = IE; // Keep inside.
		cnt = FSL_delta(I0,Ix,Jx,Ib,Ie,K,dataK,L,M,W1,W2,Pref,W,N,S,sync_like);
		total += cnt;
		if (T) {
			; // printing middle values
		}
		if (i>W2) {
			for(k=0;k<K;k++) dataK[k] += len;
			I0 += len;
		}
	}

	double factor = 1.0/total;

	for (k=0; k<K; k++)
		for (h=0; h<K; h++)
			sync_like[k][h] *= factor;
}

