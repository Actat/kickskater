CONTROLLER=MyController.so
SRC=controller.cpp
OBJ=$(SRC:%.cpp=%.o)

$(CONTROLLER): $(OBJ)
	g++ --shared -std=c++11 -o $(CONTROLLER) $(OBJ) `pkg-config --libs choreonoid-body`

%.o: %.cpp
	g++ -std=c++11 -fPIC `pkg-config --cflags choreonoid-body` -c $<

clean:
	rm -f *.o *.so

