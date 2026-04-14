"""Tests for result dataclass serialization -- pure, no external deps."""

from genie_factory.results import (
    DeploymentResult,
    GenieSpaceResult,
    CleanupResult,
)


class TestDeploymentResult:
    def _make_result(self, **overrides):
        """Helper to create a DeploymentResult with sensible defaults."""
        defaults = dict(
            catalog="main",
            schema="demo",
            fqn="main.demo",
            seed=123,
            schema_created=True,
            catalog_attempted=True,
            tables={"orders": 1000, "products": 50},
            table_fqdns={"orders": "main.demo.orders", "products": "main.demo.products"},
        )
        defaults.update(overrides)
        return DeploymentResult(**defaults)

    def test_as_dict_basic(self):
        r = self._make_result()
        d = r.as_dict()
        assert d["catalog"] == "main"
        assert d["schema"] == "demo"
        assert d["fqn"] == "main.demo"
        assert d["seed"] == 123
        assert d["tables"]["orders"] == 1000
        assert d["tables"]["products"] == 50
        assert "genie_url" in d

    def test_genie_url_none_by_default(self):
        r = self._make_result()
        d = r.as_dict()
        assert d["genie_url"] is None

    def test_genie_url_present(self):
        genie = GenieSpaceResult(
            status="created",
            requested=True,
            space_id="abc",
            url="https://workspace.databricks.com/genie/abc",
        )
        r = self._make_result(genie=genie)
        d = r.as_dict()
        assert d["genie_url"] == "https://workspace.databricks.com/genie/abc"

    def test_warnings_included(self):
        r = self._make_result(
            warnings=[{"category": "metric_view", "name": "mv1", "error": "fail"}],
        )
        d = r.as_dict()
        assert len(d["warnings"]) == 1
        assert d["warnings"][0]["category"] == "metric_view"

    def test_warnings_empty_by_default(self):
        r = self._make_result()
        d = r.as_dict()
        assert d["warnings"] == []

    def test_genie_payload_excluded(self):
        r = self._make_result(
            genie_payload={"some": "payload"},
        )
        d = r.as_dict()
        assert "genie_payload" not in d

    def test_table_fqdns_included(self):
        r = self._make_result()
        d = r.as_dict()
        assert d["table_fqdns"]["orders"] == "main.demo.orders"

    def test_metric_view_fqdns_default_empty(self):
        r = self._make_result()
        d = r.as_dict()
        assert d["metric_view_fqdns"] == {}

    def test_metric_view_fqdns_populated(self):
        r = self._make_result(
            metric_view_fqdns={"mv_revenue": "main.demo.mv_revenue"},
        )
        d = r.as_dict()
        assert d["metric_view_fqdns"]["mv_revenue"] == "main.demo.mv_revenue"


class TestGenieSpaceResult:
    def test_as_dict(self):
        g = GenieSpaceResult(status="created", requested=True, space_id="abc")
        d = g.as_dict()
        assert d["status"] == "created"
        assert d["space_id"] == "abc"
        assert d["requested"] is True

    def test_default_values(self):
        g = GenieSpaceResult(status="skipped", requested=False)
        d = g.as_dict()
        assert d["warehouse_id"] is None
        assert d["title"] is None
        assert d["url"] is None
        assert d["reason"] is None
        assert d["replaced_space_ids"] == []

    def test_replaced_space_ids(self):
        g = GenieSpaceResult(
            status="replaced",
            requested=True,
            space_id="new_id",
            replaced_space_ids=["old_1", "old_2"],
        )
        d = g.as_dict()
        assert len(d["replaced_space_ids"]) == 2
        assert "old_1" in d["replaced_space_ids"]


class TestCleanupResult:
    def test_as_dict_includes_count(self):
        c = CleanupResult(
            catalog="main",
            schema="demo",
            fqn="main.demo",
            dropped_schema=True,
            deleted_space_ids=["s1", "s2"],
            skipped_genie_cleanup=False,
        )
        d = c.as_dict()
        assert d["deleted_space_count"] == 2
        assert d["dropped_schema"] is True

    def test_zero_deleted_spaces(self):
        c = CleanupResult(
            catalog="main",
            schema="demo",
            fqn="main.demo",
            dropped_schema=True,
            deleted_space_ids=[],
            skipped_genie_cleanup=False,
        )
        d = c.as_dict()
        assert d["deleted_space_count"] == 0

    def test_skipped_genie_cleanup(self):
        c = CleanupResult(
            catalog="main",
            schema="demo",
            fqn="main.demo",
            dropped_schema=False,
            deleted_space_ids=[],
            skipped_genie_cleanup=True,
        )
        d = c.as_dict()
        assert d["skipped_genie_cleanup"] is True

    def test_notes_default_empty(self):
        c = CleanupResult(
            catalog="main",
            schema="demo",
            fqn="main.demo",
            dropped_schema=True,
            deleted_space_ids=[],
            skipped_genie_cleanup=False,
        )
        d = c.as_dict()
        assert d["notes"] == []

    def test_notes_populated(self):
        c = CleanupResult(
            catalog="main",
            schema="demo",
            fqn="main.demo",
            dropped_schema=True,
            deleted_space_ids=["s1"],
            skipped_genie_cleanup=False,
            notes=["Schema dropped successfully", "Genie space s1 deleted"],
        )
        d = c.as_dict()
        assert len(d["notes"]) == 2

    def test_none_fields(self):
        c = CleanupResult(
            catalog=None,
            schema=None,
            fqn=None,
            dropped_schema=False,
            deleted_space_ids=[],
            skipped_genie_cleanup=True,
        )
        d = c.as_dict()
        assert d["catalog"] is None
        assert d["fqn"] is None
        assert d["deleted_space_count"] == 0
