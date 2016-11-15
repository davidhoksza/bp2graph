# bp2graph
Tool for converting secondary structure of RNA into the dot format used by [Graphviz](http://www.graphviz.org/). 
The secondary structure is expected to be pseudoknot-free (currently pseudoknotted structures will raise exception). 
The conversion turns the input structure in the Vienna/DBN format into a tree where inner nodes correspond to base-paired nucleotides while non-paired nucleotides correspond to leafs.
The output is in the dot format which can then be forwarded to Graphviz to obtain the visualization in the required format (pdf, png, svg, ...).

## Installation

### Requirements

- Python 2.7 or 3.5

### Download bp2graph

```
git clone https://github.com/davidhoksza/bp2graph.git
```

## Usage

To carry out the conversion, run:

```
python bp2dot.py -i tests/structure.bp -o tests/structure.dot
```

To get PDF with the graph, you need to have Graphviz installed and run:

```
dot -Tpdf tests/structure.dot -o tests/structure.pdf
```