README.txt

		Fast Synchronization Likelihood algorithm.

	This tarball contains the source code reference implementation of the
	Fast Synchronization Likelihood algorithm, as presented in the following paper:

	"An efficient implementation of the synchronization likelihood algorithm
	for functional connectivity" 
	By Francisco Rosales, Antonio Garcia-Dopico, Ricardo Bajo, Angel Nevado


Included files:

	COPYING               GNU General Public License.
	COPYING.LESSER        GNU Lesser General Public License.
	FSL.c                 main os the FSL executable.
	FSL_delta.c           The FSL_delta and FSL functions.
	Makefile              To construct the executable.
	README.txt            This file.
	args.c                Arguments management.
	matrix.c              Matrices module.
	matrix.h              Matrices module.
	da.dat                Small data example.
	da.out                Extected results.
	pt.dat.gz             Large data example.
	pt.out.gz             Extected results.


Howto:

	To compile the sources:

		make

	To verify the sources:

		make check
		make check2

	For help:

		./FSL -h

---
