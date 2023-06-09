##
##  Makefile for Standard, Profile, Debug, and Release version of MiniSat
##

CSRCS     = $(wildcard *.c)
CHDRS     = $(wildcard *.h)
COBJS     = $(addsuffix .o, $(basename $(CSRCS)))

PCOBJS    = $(addsuffix p,  $(COBJS))
DCOBJS    = $(addsuffix d,  $(COBJS))
RCOBJS    = $(addsuffix r,  $(COBJS))

EXEC      = nbc_minisat_all

CC        = gcc
CFLAGS    = -std=c99
COPTIMIZE = -O3 -fomit-frame-pointer


.PHONY : s p d r build clean depend lib libd

s:	WAY=standard
p:	WAY=profile
d:	WAY=debug
r:	WAY=release
rs:	WAY=release static

# The solver can not count a huge number of solutions beyond a cerntain threshold.
# To count precisely, install the GNU MP bignum library and uncomment the following GMPFLAGS and define GMP in MYFLAGS.
GMPFLAGS =
GMPFLAGS += -lgmp

MYFLAGS	= 

# select at most one of the following backtrack methods: if none of them is selected, BJ+CBJ is selected.
#MYFLAGS	+= -D BT				# Chronological backtracking
MYFLAGS	+= -D BJ				# Non-chronological backtracking with level limit
#MYFLAGS	+= -D CBJ				# Conflict-directed Back Jumping

# if DLEVEL is not defined, sublevel-based analysis is performed.
MYFLAGS += -D DLEVEL	# decision level-based first UIP scheme

#MYFLAGS += -D FIXEDORDER		# Variable selection ordering is fixed (only for experiments).

MYFLAGS += -D GMP 				# GNU MP bignum library is used

s:	CFLAGS+=$(COPTIMIZE) -ggdb -D NDEBUG $(MYFLAGS) 
p:	CFLAGS+=$(COPTIMIZE) -pg -ggdb -D DEBUG $(MYFLAGS)
d:	CFLAGS+=-O0 -ggdb -D DEBUG  $(MYFLAGS)
r:	CFLAGS+=$(COPTIMIZE) -D NDEBUG $(MYFLAGS)
rs:	CFLAGS+=$(COPTIMIZE) -D NDEBUG $(MYFLAGS)

s:	build $(EXEC)
p:	build $(EXEC)_profile
d:	build $(EXEC)_debug
r:	build $(EXEC)_release
rs:	build $(EXEC)_static

build:
	@echo Building $(EXEC) "("$(WAY)")"

clean:
	@rm -f $(EXEC) $(EXEC)_profile $(EXEC)_debug $(EXEC)_release $(EXEC)_static \
	  $(COBJS) $(PCOBJS) $(DCOBJS) $(RCOBJS) depend.mak

## Build rule
%.o %.op %.od %.or:	%.c
	@echo Compiling: $<
	@$(CC) $(CFLAGS) -c -o $@ $<

## Linking rules (standard/profile/debug/release)
$(EXEC): $(COBJS)
	@echo Linking $(EXEC)
	@$(CC) $(COBJS) $(GMPFLAGS) -lz -lm -ggdb -Wall -o $@ 

$(EXEC)_profile: $(PCOBJS)
	@echo Linking $@
	@$(CC) $(PCOBJS) $(GMPFLAGS) -lz -lm -ggdb -Wall -pg -o $@

$(EXEC)_debug:	$(DCOBJS)
	@echo Linking $@
	@$(CC) $(DCOBJS) $(GMPFLAGS) -lz -lm -ggdb -Wall -o $@

$(EXEC)_release: $(RCOBJS)
	@echo Linking $@
	@$(CC) $(RCOBJS) $(GMPFLAGS) -lz -lm -Wall -o $@

$(EXEC)_static: $(RCOBJS)
	@echo Linking $@
	@$(CC) --static $(RCOBJS) $(GMPFLAGS) -lz -lm -Wall -o $@

lib:	libnbc_minisat_all.a
libd:	libnbc_minisat_alld.a

libnbc_minisat_all.a:	solver.or csolver.or
	@echo Library: "$@ ( $^ )"
	@rm -f $@
	@ar cq $@ $^

libnbc_minisat_alld.a:	solver.od csolver.od
	@echo Library: "$@ ( $^ )"
	@rm -f $@
	@ar cq $@ $^


## Make dependencies
depend:	depend.mak
depend.mak:	$(CSRCS) $(CHDRS)
	@echo Making dependencies ...
	@$(CC) -MM $(CSRCS) > depend.mak
	@cp depend.mak /tmp/depend.mak.tmp
	@sed "s/o:/op:/" /tmp/depend.mak.tmp >> depend.mak
	@sed "s/o:/od:/" /tmp/depend.mak.tmp >> depend.mak
	@sed "s/o:/or:/" /tmp/depend.mak.tmp >> depend.mak
	@rm /tmp/depend.mak.tmp

include depend.mak
