/*
 * args.c
 * Parse comand line args.
 * Set parameters for the analisys.
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

static char * version = "Version 1.1";
static char * subject = "Fast Synchronization Likelihood algorithm";
static char * cpright = "Copyright (C) 2011,2014";
static char * author  = "Francisco Rosales <frosal@fi.upm.es>";
static char * license =
"License:\n"
"\n"
"	This program is free software: you can redistribute it and/or modify\n"
"	it under the terms of the GNU Lesser General Public License as published by\n"
"	the Free Software Foundation, either version 3 of the License, or\n"
"	(at your option) any later version.\n"
"\n"
"	This program is distributed in the hope that it will be useful,\n"
"	but WITHOUT ANY WARRANTY; without even the implied warranty of\n"
"	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n"
"	GNU Lesser General Public License for more details.\n"
"\n"
"	You should have received a copy of the GNU Lesser General Public License\n"
"	along with this program.  If not, see <http://www.gnu.org/licenses/>.\n"
;
static char * usage   = "Usage: [-cd number] -lmxw ticks -p prob [-io file] [-st ticks] [-ACh]";
static char * help    =
"%s\n"
"    -c  --channels     %%d  number of channels [auto detect (values per line)]\n"
"    -d  --datalength   %%d  length of data [auto detect (number of input lines)]\n"
"    -l  --vectstep     %%d  embedding vector lag or step [--]\n"
"    -m  --vectdimen    %%d  embedding vector dimension [--]\n"
"    -x  --excluded     %%d  autocorrelation time window [--]\n"
"    -w  --windowcmp    %%d  time  interval of compared vectors [--]\n"
"    -p  --pref         %%g  fraction of vectors considered close enough (0..1) [--]\n"
"    -i  --inputfile    %%s  file with the  input data [use standard  input]\n"
"    -o  --outputfile   %%s  file with the output data [use standard output]\n"
"    -s  --speed        %%d  increment between computed samples [1]\n"
"    -t  --trigger      %%d  how many samples between snapshots [not]\n"
"    -F  --fadeout          Fadeout the (m-1)*l last embedded vectors\n"
"    -A  --abstract         Abstract\n"
"    -C  --copyright        Copyright\n"
"    -h  --help             this Help\n"
"\n";
static char * abstract =
"Abstract:\n"
"    This implements the Fast Synchronization Likelihood algorithm\n"
"    as presented in the following paper:\n"
"\n"
"    [Rosales2014]\n"
"        An efficient implementation of the synchronization likelihood algorithm for functional connectivity\n"
"        Francisco Rosales, Antonio Garcia-Dopico, Ricardo Bajo, Angel Nevado\n"
"\n"
"    This implementation is based on those of the following papers:\n"
"\n"
"    [Stam2002]\n"
"        Synchronization likelihood: an unbiased measure of generalized synchronization in multivariate data sets\n"
"        C.J. Stam, B.W. van Dijk\n"
"        Physica D 163 (2002) 236--251\n"
"\n"
"    [Montez2006]\n"
"        Synchronization likelihood with explicit time-frequency priors.\n"
"        Montez T, Linkenkaer-Hansen K, van Dijk, BW, Stam CJ.\n"
"        NeuroImage, 2006; 33:1117--1125.\n"
"\n"
"    [Posthuma2005]\n"
"        Genetic Components of Functional Connectivity in the Brain: The Heritability of Synchronization Likelihood\n"
"        Danielle Posthuma, Eco J.C. de Geus, Elles J.C.M. Mulder, Dirk J.A. Smit, Dorret I. Boomsma, and Cornelis J. Stam\n"
"        Human Brain Mapping 26:191--198(2005)\n"
"\n"
"Contributors:\n"
"    Ricardo BAJO: First MatLab implementation.\n"
"    Francisco ROSALES: First translation to C.\n"
"    Francisco ROSALES: Complete rewritten from scratch.\n"
"    Antonio GARCIA: Initial adaptation to OpenMP.\n"
"    Francisco ROSALES: Further improvements.\n"
;

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

/*
 * str2int
 * Converts an string to an integer checking valid range [<min>, <max>).
 * Retuns 0 and updated <ip> or -1 on error.
 */
int str2int(char *str, int *ip, int min, int max)
{
	char * ptr = NULL;
	int i;

	i = (int) strtol(str, &ptr, 0);
	if (!ptr || *ptr)
		return -1;
	if (i < min || i >= max)
		return -1;
	*ip = i;
	return 0;
}

/*
 * str2double
 * Converts an string to a double checking valid range [<min>, <max>).
 * Retuns 0 and updated <dp> or -1 on error.
 */
int str2double(char *str, double *dp, double min, double max)
{
	char * ptr = NULL;
	double d;

	d =  strtod(str, &ptr);
	if (!ptr || *ptr)
		return -1;
	if (d < min || d >= max)
		return -1;
	*dp = d;
	return 0;
}

/*
 * Configurable parameters.
 */

extern int D;
extern int C;
extern int L;
extern int M;
extern int W1;
extern int W2;
extern double Pref;
extern char * input;
extern char * output;
extern int F;
extern int S;
extern int T;

/*
 * Internals.
 */

#if defined(sgi) || defined(__sun__) || defined(__osf__) || defined(_AIX)
	struct option {
		const char *name;
		int has_arg;
		int *flag;
		int val;
	};
#	define getopt_long(argc, argv, opts, lopts, lopts_ndx_ptr) \
		getopt(argc, argv, opts)
#else
#	include <getopt.h>
#endif

static int parse_an_arg(int argc, char *argv[])
{
	extern char *optarg;
	char *nvv_fmt = "parse(-%c %s): Not a valid value.\n";
	int ch;
	int lopts_ndx;
	char *opts = "c:d:m:l:x:w:p:i:o:s:t:FACh";
	struct option lopts [] = {
		{"channels"    , 1, 0, 'c'},
		{"datalength"  , 1, 0, 'd'},
		{"vectstep"    , 1, 0, 'l'},
		{"vectdimen"   , 1, 0, 'm'},
		{"excluded"    , 1, 0, 'x'},
		{"windowcmp"   , 1, 0, 'w'},
		{"pref"        , 1, 0, 'p'},
		{"inputfile"   , 1, 0, 'i'},
		{"outputfile"  , 1, 0, 'o'},
		{"speed"       , 1, 0, 's'},
		{"trigger"     , 1, 0, 't'},
		{"fadeout"     , 1, 0, 'F'},
		{"abstract"    , 0, 0, 'A'},
		{"copyright"   , 0, 0, 'C'},
		{"help"        , 0, 0, 'h'},
		{NULL, 0, 0, 0},
	};

	switch ((ch = getopt_long(argc, argv, opts, lopts, &lopts_ndx))) {
	case 'c':
		if (str2int(optarg, &C, 1, 100000) < 0) {
			fprintf(stderr, nvv_fmt, ch, optarg);
			return -1;
		}
		break;
	case 'd':
		if (str2int(optarg, &D, 1, 10000000) < 0) {
			fprintf(stderr, nvv_fmt, ch, optarg);
			return -1;
		}
		break;
	case 'l':
		if (str2int(optarg, &L, 1, 1000) < 0) {
			fprintf(stderr, nvv_fmt, ch, optarg);
			return -1;
		}
		break;
	case 'm':
		if (str2int(optarg, &M, 1, 100000) < 0) {
			fprintf(stderr, nvv_fmt, ch, optarg);
			return -1;
		}
		break;
	case 'x':
		if (str2int(optarg, &W1, 1, 100000) < 0) {
			fprintf(stderr, nvv_fmt, ch, optarg);
			return -1;
		}
		break;
	case 'w':
		if (str2int(optarg, &W2, 1, 100000) < 0) {
			fprintf(stderr, nvv_fmt, ch, optarg);
			return -1;
		}
		break;
	case 'p':
		if ((str2double(optarg, &Pref, 0, 0.5)) < 0) {
			fprintf(stderr, nvv_fmt, ch, optarg);
			return -1;
		}
		break;
	case 'i':
		if (input) {
			fprintf(stderr, "parse(-%c): Specified more than once.\n", ch);
			return -1;
		}
		input = optarg;
		break;
	case 'o':
		if (output) {
			fprintf(stderr, "parse(-%c): Specified more than once.\n", ch);
			return -1;
		}
		output = optarg;
		break;
	case 's':
		if (str2int(optarg, &S, 1, 1000) < 0) {
			fprintf(stderr, nvv_fmt, ch, optarg);
			return -1;
		}
		break;
	case 't':
		if (str2int(optarg, &T, 0, 1<<30) < 0) {
			fprintf(stderr, nvv_fmt, ch, optarg);
			return -1;
		}
		break;
	case 'F':
		F = !F;
		break;
	case 'A':
		fprintf(stderr, "%s, %s\n", version, subject);
		fprintf(stderr, "%s. %s\n", cpright, author);
		fprintf(stderr, "%s\n", abstract);
		exit(0);
	case 'C':
		fprintf(stderr, "%s, %s\n", version, subject);
		fprintf(stderr, "%s. %s\n", cpright, author);
		fprintf(stderr, "%s\n", license);
		exit(0);
	case 'h':
		fprintf(stderr, "%s, %s\n", version, subject);
		fprintf(stderr, "%s. %s\n", cpright, author);
		fprintf(stderr, help, usage);
		exit(0);
	case -1:
		return 0;
	case ':':
		fprintf(stderr, "parse: Missing parameter.\n");
		return -1;
	case '?':
		fprintf(stderr, "parse: Unknown option.\n");
		return -1;
	default:
		fprintf(stderr, "parse: Unknown return.\n");
		return -1;
		fprintf(stderr, "parse: Unknown return('%c'=0x%x).\n", (char)ch, ch);
	}
	return 1;
}

static int validate_usage(void)
{
	int ret = 0;

	if (L <= 0) {
		fprintf(stderr, "usage: -l should be greater than 0.\n");
		ret--;
	}	
	if (M <= 0) {
		fprintf(stderr, "usage: -m should be greater than 0.\n");
		ret--;
	}	
	if (W1 <= 0) {
		fprintf(stderr, "usage: -x (W1) should be greater than 0.\n");
		ret--;
	}	
	if (W2 <= W1) {
		fprintf(stderr, "usage: -w (W2) should be greater than -x (W1).\n");
		ret--;
	}
	if (Pref <= 0 || Pref >= 0.5) {
		fprintf(stderr, "usage: -p should be > 0 and < 0.5.\n");
		ret--;
	}

	return ret;
}

/*
 * Services.
 */

int parse_args(int argc, char *argv[])
{
	extern int optind;
	int err = 0;
	int ret;

	do {
		ret = parse_an_arg(argc, argv);
		if (ret == -1)
			err++;
	} while (ret);

	ret = validate_usage();
	if (ret < 0)
		err++;

	if (err)
		fprintf(stderr, "%s\n", usage), exit(1);

	for (ret = 1; (argv[ret] = argv[ret + optind - 1]); ret++);

	return ret;
}
