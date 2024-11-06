import pytest
from uninformed.ucs import UCSLogic


class TestUCS:
    @pytest.fixture
    def ucs_logic(self):
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

        def mock_update_cost_display(*args):
            pass

        mock_node_lines = {}

        # Initialize UCSLogic with all required arguments
        return UCSLogic(
            canvas=mock_canvas,
            update_node_color=mock_update_node_color,
            show_goal_message=mock_show_goal_message,
            update_cost_display=mock_update_cost_display,
            node_lines=mock_node_lines,
        )

    def test_ucs_simple_path(self, ucs_logic):
        # Define a simple graph
        ucs_logic.graph = {
            "A": [("B", 1), ("C", 2)],
            "B": [("D", 4), ("E", 2)],
            "C": [("F", 3), ("G", 2)],
            "D": [("H", 7), ("I", 3)],
            "E": [],
            "F": [("J", 5), ("K", 4)],
            "G": [],
            "H": [("L", 6)],
            "I": [("M", 3)],
            "J": [("N", 2)],
            "K": [],
            "L": [],
            "M": [],
            "N": [],
        }

        # Run UCS
        path = ucs_logic.ucs("A", "F")

        # Assert the correct path is found
        assert path == ["A", "C", "F"]

    def test_ucs_no_path(self, ucs_logic):
        # Define a graph with no path to the goal
        ucs_logic.graph = {
            "A": [("B", 1), ("C", 2)],
            "B": [("D", 4), ("E", 2)],
            "C": [("F", 3), ("G", 2)],
            "D": [("H", 7), ("I", 3)],
            "E": [],
            "F": [("J", 5), ("K", 4)],
            "G": [],
            "H": [("L", 6)],
            "I": [("M", 3)],
            "J": [("N", 2)],
            "K": [],
            "L": [],
            "M": [],
            "N": [],
        }
        # Run UCS
        path = ucs_logic.ucs("A", "O")

        # Assert that no path is found
        assert path is None

    def test_ucs_goal_not_in_graph(self, ucs_logic):
        # Define a graph where the goal is not present
        ucs_logic.graph = {
            "A": [("B", 1), ("C", 2)],
            "B": [("D", 4), ("E", 2)],
            "C": [("F", 3), ("G", 2)],
            "D": [("H", 7), ("I", 3)],
            "E": [],
            "F": [("J", 5), ("K", 4)],
            "G": [],
            "H": [("L", 6)],
            "I": [("M", 3)],
            "J": [("N", 2)],
            "K": [],
            "L": [],
            "M": [],
            "N": [],
        }

        # Run UCS
        path = ucs_logic.ucs("A", "Z")

        # Assert that no path is found
        assert path is None

    # Add more test cases as needed
