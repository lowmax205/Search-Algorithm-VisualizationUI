import pytest
from uninformed.ids import IDSLogic


class TestIDS:
    @pytest.fixture
    def ids_logic(self):
        mock_canvas = type(
            "MockCanvas",
            (),
            {
                "create_text": lambda *args, **kwargs: None,
                "update": lambda *args, **kwargs: None,  # Updated to accept arguments
            },
        )()

        def mock_update_node_color(*args):
            pass

        def mock_show_goal_message(*args):
            pass

        mock_node_lines = {}

        return IDSLogic(
            canvas=mock_canvas,
            update_node_color=mock_update_node_color,
            show_goal_message=mock_show_goal_message,
            node_lines=mock_node_lines,
        )

    def test_ids_simple_path(self, ids_logic):
        # Define a simple graph
        ids_logic.graph = {
            "A": ["B", "C"],
            "B": ["D", "E"],
            "C": ["F", "G"],
            "D": ["H", "I"],
            "E": [],
            "F": ["J", "K"],
            "G": [],
            "H": ["L"],
            "I": ["M"],
            "J": ["N"],
            "K": [],
            "L": [],
            "M": [],
            "N": [],
        }

        # Run IDS
        path = ids_logic.ids("A", "F")

        # Assert the correct path is found
        assert path == ["A", "C", "F"]

    def test_ids_no_path(self, ids_logic):
        # Define a graph with no path to the goal
        ids_logic.graph = {
            "A": ["B", "C"],
            "B": ["D", "E"],
            "C": ["F", "G"],
            "D": ["H", "I"],
            "E": [],
            "F": ["J", "K"],
            "G": [],
            "H": ["L"],
            "I": ["M"],
            "J": ["N"],
            "K": [],
            "L": [],
            "M": [],
            "N": [],
        }

        # Run IDS
        path = ids_logic.ids("A", "O")

        # Assert that no path is found
        assert path is None

    def test_ids_goal_not_in_graph(self, ids_logic):
        # Define a graph where the goal is not present
        ids_logic.graph = {
            "A": ["B", "C"],
            "B": ["D", "E"],
            "C": ["F", "G"],
            "D": ["H", "I"],
            "E": [],
            "F": ["J", "K"],
            "G": [],
            "H": ["L"],
            "I": ["M"],
            "J": ["N"],
            "K": [],
            "L": [],
            "M": [],
            "N": [],
        }
        # Run IDS
        path = ids_logic.ids("A", "")

        # Assert that no path is found
        assert path is None

    # Add more test cases as needed
