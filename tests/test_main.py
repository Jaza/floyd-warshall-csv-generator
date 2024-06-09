from typer.testing import CliRunner

from floyd_warshall_csv_generator.main import app


runner = CliRunner()


TEST_INPUT_FILE_CONTENTS = """point_a,point_b,cost
a,b,5
b,c,8
c,d,23
d,e,6
"""

EXPECTED_OUTPUT_GRAPH_EDGES = {
    ("a", "b", 5.0),
    ("a", "c", 13.0),
    ("b", "c", 8.0),
    ("b", "d", 31.0),
    ("c", "d", 23.0),
    ("c", "e", 29.0),
    ("d", "e", 6.0),
}


def test_app():
    with runner.isolated_filesystem():
        with open("test_input_data.csv", "w") as f:
            f.write(TEST_INPUT_FILE_CONTENTS)

        result = runner.invoke(
            app,
            [
                "test_input_data.csv",
                "--vertex-i-column-name",
                "point_a",
                "--vertex-j-column-name",
                "point_b",
                "--weight-column-name",
                "cost",
                "--no-directed",
                "--max-weight",
                "35",
            ],
        )

    assert result.exit_code == 0

    graph_edges = {
        (f"{x.split(',')[0]}", f"{x.split(',')[1]}", float(x.split(",")[2]))
        for i, x in enumerate(result.output.split("\n"))
        if i and x
    }
    assert graph_edges == EXPECTED_OUTPUT_GRAPH_EDGES
