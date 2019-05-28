# tensor-DFAs

Functions to investigate learning deterministic finite automata (DFA). Summer 2019 Harvey Mudd College AMISTAD lab.

*Represent DFA as a tensor*
- **DfaTensor:** Contains class to represent DFA as a q\*q\*a tensor, where q is the number of states and a is the size of the alphabet of input characters. The [i][j][k] entry of this tensor is 1 if there is a transition from the i<sup>th</sup> to the j<sup>th</sup> state on the k<sup>th</sup> input character in the alphabet, 0 otherwise.
- **TensorGenerator:** Expands on DfaTensor class to contain functions that read an input string and output whether or not it is accepted.

*Find accepting strings*
- **AcceptingStringsGenerator:** Generates all accepting strings of a given length. Uses a dynamic programming approach. 
- **STPTools:** Generates all accepting strings of a given length. Code is based on algorithm 1, pg. 952 of Yan, Chen, and Liu’s “Semi-tensor product of matrices approach to reachability of finite automata with application to language recognition.” See also **STP**, **SwapMatrix**. 
- **StringGenerator:** Generates the subset of all accepting strings for which no state in the DFA is visited twice while reading the string. This is implemented by a path-finding algorithm for graphs. See also **Graph**, a modification of the adjacency list graph class from geeks for geeks. 
