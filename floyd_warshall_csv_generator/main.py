import sys
from collections.abc import Iterable
from csv import DictReader, DictWriter
from typing import Any

from numpy import ndarray
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import floyd_warshall
from typer import FileText, Typer


app = Typer()


def get_input_edges(
    reader: Iterable[dict[str, Any]],
    vertex_i_column_name: str = "vertex_i",
    vertex_j_column_name: str = "vertex_j",
    weight_column_name: str = "weight",
    unweighted: bool = False,
) -> tuple[dict[str, dict[str, float]], set[str]]:
    input_edges: dict[str, dict[str, float]] = {}
    vertex_names: set[str] = set()

    for row in reader:
        vertex_i_name = f"{row[vertex_i_column_name]}"
        vertex_names.add(vertex_i_name)

        vertex_j_name = f"{row[vertex_j_column_name]}"
        vertex_names.add(vertex_j_name)

        weight = 0.0 if unweighted else float(row[weight_column_name])

        if vertex_i_name not in input_edges:
            input_edges[vertex_i_name] = {}

        input_edges[vertex_i_name][vertex_j_name] = weight

    return input_edges, vertex_names


def get_input_graph(
    input_edges: dict[str, dict[str, float]], vertex_name_list: list[str]
) -> list[list[float]]:
    input_graph: list[list[float]] = []

    for vertex_i_name in vertex_name_list:
        input_graph_for_i: list[float] = []

        for vertex_j_name in vertex_name_list:
            weight = input_edges.get(vertex_i_name, {}).get(vertex_j_name, 0.0)
            input_graph_for_i.append(weight)

        input_graph.append(input_graph_for_i)

    return input_graph


def write_output_graph(
    writer: DictWriter,
    output_graph: list[list[float]],
    vertex_name_list: list[str],
    vertex_i_column_name: str = "vertex_i",
    vertex_j_column_name: str = "vertex_j",
    weight_column_name: str = "weight",
    directed: bool = True,
    max_weight: float = 0.0,
):
    seen: set[tuple[str, str]] = set()

    for i, output_graph_for_i in enumerate(output_graph):
        for j, output_graph_for_j in enumerate(output_graph_for_i):
            weight = float(output_graph_for_j)

            if weight and (not max_weight or weight <= max_weight):
                vertex_i_name = vertex_name_list[i]
                vertex_j_name = vertex_name_list[j]
                vertex_names_sorted = sorted([vertex_i_name, vertex_j_name])
                vertex_names = (vertex_names_sorted[0], vertex_names_sorted[1])

                if directed or (vertex_names not in seen):
                    writer.writerow(
                        {
                            vertex_i_column_name: vertex_names[0],
                            vertex_j_column_name: vertex_names[1],
                            weight_column_name: weight,
                        }
                    )

                    if not directed:
                        seen.add(vertex_names)


@app.command()
def generate_floyd_warshall_csv(
    input_csv: FileText,
    vertex_i_column_name: str = "vertex_i",
    vertex_j_column_name: str = "vertex_j",
    weight_column_name: str = "weight",
    directed: bool = True,
    unweighted: bool = False,
    max_weight: float = 0.0,
):
    fieldnames = [vertex_i_column_name, vertex_j_column_name]

    if not unweighted:
        fieldnames.append(weight_column_name)

    reader = DictReader(input_csv)
    input_edges, vertex_names = get_input_edges(
        reader=reader,
        vertex_i_column_name=vertex_i_column_name,
        vertex_j_column_name=vertex_j_column_name,
        weight_column_name=weight_column_name,
        unweighted=unweighted,
    )

    vertex_name_list = list(vertex_names)

    input_graph = get_input_graph(
        input_edges=input_edges, vertex_name_list=vertex_name_list
    )

    input_matrix = csr_matrix(input_graph)

    output_matrix = floyd_warshall(
        input_matrix, directed=directed, unweighted=unweighted
    )

    if not isinstance(output_matrix, ndarray):  # pragma: no cover
        raise ValueError("output_matrix is not an ndarray")

    output_graph = output_matrix.tolist()
    writer = DictWriter(sys.stdout, fieldnames=fieldnames)
    writer.writeheader()

    write_output_graph(
        writer=writer,
        output_graph=output_graph,
        vertex_name_list=vertex_name_list,
        vertex_i_column_name=vertex_i_column_name,
        vertex_j_column_name=vertex_j_column_name,
        weight_column_name=weight_column_name,
        directed=directed,
        max_weight=max_weight,
    )
