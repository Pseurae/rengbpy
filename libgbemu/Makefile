CXX 			:= $(TOOLCHAIN)c++
CXXFLAGS 		:= -std=c++17 -MMD

GBEMU_SRCS 		:= $(shell find gbemu/src -name "*.cc")

OBJ_DIR 		:= build-$(LIB_SUFFIX)
GBEMU_OBJ_NAMES	:= $(GBEMU_SRCS:.cc=.o)
GBEMU_OBJ_PATHS	:= $(GBEMU_OBJ_NAMES:gbemu/src/%=$(OBJ_DIR)/%)
GBEMU_DEP_NAMES	:= $(GBEMU_OBJ_PATHS:%.o=%.d)

.PHONY: all clean

all: ${GBEMU_OBJ_PATHS} $(OBJ_DIR)/bindings.o
	$(CXX) $(CXXFLAGS) -shared ${GBEMU_OBJ_PATHS} $(OBJ_DIR)/bindings.o -o libgbemu-$(LIB_SUFFIX)

clean:
	rm -rf build-*

$(OBJ_DIR)/%.o: gbemu/src/%.cc
	@mkdir -p $(shell dirname "$@")
	$(CXX) $(CXXFLAGS) -c $< -o $@

$(OBJ_DIR)/bindings.o: bindings.cc
	@mkdir -p $(shell dirname "$@")
	$(CXX) $(CXXFLAGS) -c $< -o $@

-include $(GBEMU_DEP_NAMES) $(OBJ_DIR)/bindings.d
