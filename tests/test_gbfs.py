import pytest
from informed.gbfs import GBFSLogic


class TestGBFS:
    @pytest.fixture
    def gbfs_logic(self):
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

        # Initialize GBFSLogic with all required arguments
        gbfs = GBFSLogic(
            canvas=mock_canvas,
            update_node_color=mock_update_node_color,
            show_goal_message=mock_show_goal_message,
            node_lines=mock_node_lines,
        )

        return gbfs

    def test_gbfs_simple_path(self, gbfs_logic):
        path = gbfs_logic.greedy_bfs("A", "F")
        assert path == ["A", "C", "F"]

    def test_gbfs_no_path(self, gbfs_logic):
        # We can't modify the graph structure directly, so we'll test with an unreachable goal
        path = gbfs_logic.greedy_bfs("A", "Z")
        assert path is None

    def test_gbfs_goal_not_in_graph(self, gbfs_logic):
        path = gbfs_logic.greedy_bfs("A", "Z")
        assert path is None

    def test_gbfs_start_is_goal(self, gbfs_logic):
        path = gbfs_logic.greedy_bfs("A", "A")
        assert path == ["A"]

    def test_gbfs_heuristic_order(self, gbfs_logic):
        path = gbfs_logic.greedy_bfs("A", "K")
        assert path == ["A", "C", "F", "K"]

    def test_gbfs_set_heuristics(self, gbfs_logic):
        new_heuristics = {
            "A": 3,
            "B": 2,
            "C": 4,
            "D": 1,
            "E": 3,
            "F": 5,
            "G": 3,
            "H": 0,
            "I": 2,
        }
        gbfs_logic.set_heuristics(new_heuristics)
        for node, value in new_heuristics.items():
            assert gbfs_logic.heuristics[node] == value

    def test_gbfs_get_neighbors(self, gbfs_logic):
        neighbors = gbfs_logic.get_neighbors("B")
        assert set(neighbors) == {"D", "E"}
