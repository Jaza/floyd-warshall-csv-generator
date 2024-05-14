# floyd-warshall-csv-generator

Takes a CSV of graph edges as input, and generates a CSV of the edges that are the shortest paths between all pairs of vertices.

Calculates output edges using [scipy.sparse.csgraph.floyd_warshall](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csgraph.floyd_warshall.html).


## Getting started

1. Install a recent Python 3.x version (if you don't already have one).
2. Install [python-poetry](https://python-poetry.org/):
   ```sh
   curl -sSL https://install.python-poetry.org | python3 -
   ```
3. Install dependencies:
   ```sh
   poetry install
   ```


## Developing

To clone the repo:

```sh
git clone git@github.com:Jaza/floyd-warshall-csv-generator.git
```

To automatically fix code style issues:

```sh
./scripts/format.sh
```

To verify code style and static typing:

```sh
./scripts/verify.sh
```

To run tests:

```sh
./scripts/test.sh
```


## Building

To build the library:

```sh
poetry build
```
