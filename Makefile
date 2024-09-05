# - Makefile -
# (C) 2023 Joerg Jungermann, GPLv2 see LICENSE

DEPDIR              = .deps
$(shell mkdir -p $(DEPDIR) >/dev/null)

PY_FILES := $(shell find ./ -name "*.py" 2>/dev/null | sed -e '/^.\/.env/ d' -e 's|^./||' )
PY_PUSH_FLAGS := $(PY_FILES:%=$(DEPDIR)/%.pushed)

SERIAL = /dev/ttyACM0
SPEED = 115200

# allow local config overrides, like in main Makefile used above
-include config

V = 0
E = @ :
Q =
ifeq ($(V), 0)
	Q = @
	E = $(Q)echo
endif



all: push repl

force-push fp:
	$(E) "FORCE PUSH"
	$(Q) rm -f $(DEPDIR)/*.pushed
	$(Q) $(MAKE) push

push p: reset $(PY_PUSH_FLAGS)

repl term t:
	$(E) TERM
	$(Q) rshell -p "$(SERIAL)" -b "$(SPEED)" repl 

$(DEPDIR)/%.pushed: %
	$(E) "PUSH $<"
	$(Q) ampy -p "$(SERIAL)" -b "$(SPEED)" put "$<" /"$<" > "$@" || rm -f "$@"

reset rst r:
	$(E) "RESET $(SERIAL) @ $(SPEED)"
	$(Q) sleep .3 | pyserial-miniterm --dtr 0 "$(SERIAL)" "$(SPEED)" 2> /dev/null 1>&2 || :

.PHONY: all push force-push fp repl term t reset rst r

# vim: ts=2 sw=2 noet ft=make
