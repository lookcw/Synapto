

CC = gcc
CFLAGS += -Wall -O3 -fopenmp
LDFLAGS = -lm -fopenmp

BIN  = FSL
OBJS = FSL.o FSL_delta.o args.o matrix.o

all	: $(BIN)
$(BIN)	: $(OBJS)
	$(CC) $(OBJS) -o $(BIN) $(LDFLAGS)

check	: $(BIN)
	# This should take no time.
	./$(BIN) -l 1 -m 10 -x 100 -w 410 -p 0.049 -i da.dat -o da.tmp
	diff da.tmp da.out && rm da.tmp

check2	: $(BIN)
	# This can take a while.
	gzip -cd pt.dat.gz | ./$(BIN) -l 1 -m 10 -x 100 -w 410 -p 0.049 -F -o pt.tmp
	gzip -cd pt.out.gz | diff - pt.tmp && rm pt.tmp

clean	:
	-@rm $(OBJS)
cleanall: clean
	-@rm $(BIN)
