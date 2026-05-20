"""Unit tests for Phase 0 engine upgrades in data.py:

- Rolling date range (CURRENT_DATE based, env-overridable).
- New noise placeholders ({qty_noise2}, {alt_status_noise}, {alt_status_noise2}).
- {seasonal_mult} per-column placeholder driven by ColumnSpec.seasonal_amplitude.
- {seed} % N forbidden-pattern validator.
- AVG measure auto-synthesis for every bare SUM(col) measure.

Pure tests, no Spark needed — they only inspect the generated SQL strings.
"""

from __future__ import annotations

import os

import pytest

from genie_factory.data import (
    _anchor_year,
    _end_date_sql,
    _start_year,
    _synthesize_avg_measures,
    _validate_no_seed_modulo,
    build_metric_view_sqls_from_spec,
    build_table_sqls_from_spec,
)
from genie_factory.generator import (
    BenchmarkSpec,
    ColumnSpec,
    DomainSpec,
    ExampleSQL,
    MetricViewSpec,
    SQLSnippets,
    TableSpec,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _minimal_table(columns: list[ColumnSpec], archetype: str = "transaction") -> TableSpec:
    return TableSpec(
        table_name="t1",
        description="test table",
        columns=columns,
        seasonal_patterns={},
        entity_dimension=archetype,
        dimension_values=[{"entity_id": "E1", "category": "A"}, {"entity_id": "E2", "category": "B"}],
        category_distribution={"A": 0.5, "B": 0.5},
    )


def _minimal_spec(table: TableSpec, measures: list[dict] | None = None) -> DomainSpec:
    return DomainSpec(
        company_name="Test Co",
        industry="Testing",
        use_case="Quality Probe",
        space_title="Test Space",
        space_description="",
        schema_basename="test_engine",
        tables=[table],
        metric_views=[MetricViewSpec(
            view_name="t1_metrics",
            source_table="t1",
            dimensions=[{"name": "dt", "expr": "dt"}],
            measures=measures or [],
        )],
        genie_instructions="",
        sample_questions=[],
        example_sqls=[],
        sql_snippets=SQLSnippets(filters=[], expressions=[], measures=[]),
        benchmarks=[],
    )


# ---------------------------------------------------------------------------
# Rolling date range
# ---------------------------------------------------------------------------


class TestRollingDateRange:
    def test_anchor_year_rolls_with_calendar(self, monkeypatch):
        monkeypatch.delenv("GENIE_FACTORY_END_DATE", raising=False)
        assert _anchor_year() >= 2026  # known floor; test continues to pass next year

    def test_anchor_year_honors_env_override(self, monkeypatch):
        monkeypatch.setenv("GENIE_FACTORY_END_DATE", "2030-06-15")
        assert _anchor_year() == 2030

    def test_anchor_year_invalid_env_falls_back(self, monkeypatch):
        monkeypatch.setenv("GENIE_FACTORY_END_DATE", "garbage")
        # Falls back to date.today().year
        from datetime import date
        assert _anchor_year() == date.today().year

    def test_start_year_uses_anchor_minus_scale(self, monkeypatch):
        monkeypatch.setenv("GENIE_FACTORY_END_DATE", "2026-05-19")
        assert _start_year(scale=3) == 2024
        assert _start_year(scale=1) == 2026

    def test_end_date_sql_uses_current_date_for_transaction(self, monkeypatch):
        monkeypatch.delenv("GENIE_FACTORY_END_DATE", raising=False)
        assert _end_date_sql("transaction") == "CURRENT_DATE()"

    def test_end_date_sql_extends_forecast_by_six_months(self, monkeypatch):
        monkeypatch.delenv("GENIE_FACTORY_END_DATE", raising=False)
        assert _end_date_sql("forecast") == "add_months(CURRENT_DATE(), 6)"

    def test_end_date_sql_pins_to_env(self, monkeypatch):
        monkeypatch.setenv("GENIE_FACTORY_END_DATE", "2026-05-19")
        assert _end_date_sql("transaction") == "DATE'2026-05-19'"
        assert _end_date_sql("forecast") == "add_months(DATE'2026-05-19', 6)"


# ---------------------------------------------------------------------------
# Noise placeholders
# ---------------------------------------------------------------------------


class TestNoisePlaceholders:
    def test_alt_status_noise_substituted(self, monkeypatch):
        monkeypatch.setenv("GENIE_FACTORY_END_DATE", "2026-05-19")
        table = _minimal_table([
            ColumnSpec(name="entity_id", sql_type="STRING", comment="", is_dimension=True, generation_expr=""),
            ColumnSpec(name="category", sql_type="STRING", comment="", is_dimension=True, generation_expr=""),
            ColumnSpec(
                name="primary_status",
                sql_type="STRING",
                comment="",
                is_dimension=False,
                generation_expr="CASE WHEN {status_noise} < 0.5 THEN 'A' ELSE 'B' END",
            ),
            ColumnSpec(
                name="secondary_status",
                sql_type="STRING",
                comment="",
                is_dimension=False,
                generation_expr="CASE WHEN {alt_status_noise} < 0.5 THEN 'X' ELSE 'Y' END",
            ),
        ])
        spec = _minimal_spec(table)
        sql = build_table_sqls_from_spec(spec, "cat.sch", seed=1, scale=1, target_rows=100)["t1"]
        # Both noise columns must be materialized in the skeleton CTE.
        assert "AS qty_noise" in sql
        assert "AS qty_noise2" in sql
        assert "AS alt_status_noise" in sql
        assert "AS alt_status_noise2" in sql
        # And they must be referenced in the column expressions (not as literal placeholders).
        assert "{status_noise}" not in sql
        assert "{alt_status_noise}" not in sql
        assert "WHEN status_noise < 0.5" in sql
        assert "WHEN alt_status_noise < 0.5" in sql

    def test_qty_noise2_substituted(self, monkeypatch):
        monkeypatch.setenv("GENIE_FACTORY_END_DATE", "2026-05-19")
        table = _minimal_table([
            ColumnSpec(name="entity_id", sql_type="STRING", comment="", is_dimension=True, generation_expr=""),
            ColumnSpec(name="category", sql_type="STRING", comment="", is_dimension=True, generation_expr=""),
            ColumnSpec(
                name="value_a",
                sql_type="DOUBLE",
                comment="",
                is_dimension=False,
                generation_expr="100.0 + {qty_noise} * 50.0",
            ),
            ColumnSpec(
                name="value_b",
                sql_type="DOUBLE",
                comment="",
                is_dimension=False,
                generation_expr="200.0 + {qty_noise2} * 50.0",
            ),
        ])
        spec = _minimal_spec(table)
        sql = build_table_sqls_from_spec(spec, "cat.sch", seed=1, scale=1, target_rows=100)["t1"]
        assert "100.0 + qty_noise * 50.0" in sql
        assert "200.0 + qty_noise2 * 50.0" in sql


# ---------------------------------------------------------------------------
# Seasonal multiplier
# ---------------------------------------------------------------------------


class TestSeasonalMult:
    def test_default_amplitude_makes_seasonal_mult_one(self, monkeypatch):
        monkeypatch.setenv("GENIE_FACTORY_END_DATE", "2026-05-19")
        table = _minimal_table([
            ColumnSpec(name="entity_id", sql_type="STRING", comment="", is_dimension=True, generation_expr=""),
            ColumnSpec(name="category", sql_type="STRING", comment="", is_dimension=True, generation_expr=""),
            ColumnSpec(
                name="flat_kpi",
                sql_type="DOUBLE",
                comment="",
                is_dimension=False,
                generation_expr="50.0 + {qty_noise} * 30.0 * {seasonal_mult}",
            ),
        ])
        spec = _minimal_spec(table)
        sql = build_table_sqls_from_spec(spec, "cat.sch", seed=1, scale=1, target_rows=100)["t1"]
        # With seasonal_amplitude unset (=0.0), {seasonal_mult} -> 1.0
        assert "50.0 + qty_noise * 30.0 * 1.0" in sql

    def test_nonzero_amplitude_injects_sin_curve(self, monkeypatch):
        monkeypatch.setenv("GENIE_FACTORY_END_DATE", "2026-05-19")
        table = _minimal_table([
            ColumnSpec(name="entity_id", sql_type="STRING", comment="", is_dimension=True, generation_expr=""),
            ColumnSpec(name="category", sql_type="STRING", comment="", is_dimension=True, generation_expr=""),
            ColumnSpec(
                name="seasonal_kpi",
                sql_type="DOUBLE",
                comment="",
                is_dimension=False,
                generation_expr="50.0 + {qty_noise} * 30.0 * {seasonal_mult}",
                seasonal_amplitude=0.20,
            ),
        ])
        spec = _minimal_spec(table)
        sql = build_table_sqls_from_spec(spec, "cat.sch", seed=1, scale=1, target_rows=100)["t1"]
        # With amplitude=0.20, {seasonal_mult} -> (1.0 + 0.2000 * SIN(2 * PI() * MONTH(dt) / 12.0))
        assert "0.2000 * SIN(2 * PI() * MONTH(dt) / 12.0)" in sql

    def test_yoy_growth_adds_year_term(self, monkeypatch):
        monkeypatch.setenv("GENIE_FACTORY_END_DATE", "2026-05-19")
        table = _minimal_table([
            ColumnSpec(name="entity_id", sql_type="STRING", comment="", is_dimension=True, generation_expr=""),
            ColumnSpec(name="category", sql_type="STRING", comment="", is_dimension=True, generation_expr=""),
            ColumnSpec(
                name="growing_kpi",
                sql_type="DOUBLE",
                comment="",
                is_dimension=False,
                generation_expr="100.0 * {seasonal_mult}",
                yoy_growth=0.05,
            ),
        ])
        spec = _minimal_spec(table)
        sql = build_table_sqls_from_spec(spec, "cat.sch", seed=1, scale=1, target_rows=100)["t1"]
        # Start year with anchor=2026 scale=1 is 2026.
        assert "0.0500 * (YEAR(dt) - 2026)" in sql


# ---------------------------------------------------------------------------
# Seed-modulo validator
# ---------------------------------------------------------------------------


class TestSeedModuloValidator:
    def test_seed_mod_pattern_rejected(self):
        err = _validate_no_seed_modulo("{seed} % 15", context="supplier_id")
        assert err is not None
        assert "supplier_id" in err
        assert "{id_seq}" in err

    def test_seed_mod_pattern_case_insensitive(self):
        assert _validate_no_seed_modulo("{SEED}%30") is not None
        assert _validate_no_seed_modulo("{ seed } % 100") is not None

    def test_clean_expression_passes(self):
        assert _validate_no_seed_modulo("{id_seq} % 15") is None
        assert _validate_no_seed_modulo("100.0 + {qty_noise} * 50.0") is None
        assert _validate_no_seed_modulo("") is None

    def test_validator_blocks_table_build(self, monkeypatch):
        monkeypatch.setenv("GENIE_FACTORY_END_DATE", "2026-05-19")
        table = _minimal_table([
            ColumnSpec(name="entity_id", sql_type="STRING", comment="", is_dimension=True, generation_expr=""),
            ColumnSpec(name="category", sql_type="STRING", comment="", is_dimension=True, generation_expr=""),
            ColumnSpec(
                name="bad_constant",
                sql_type="STRING",
                comment="",
                is_dimension=False,
                generation_expr="CONCAT('SUP-', CAST({seed} % 15 AS STRING))",
            ),
        ])
        spec = _minimal_spec(table)
        with pytest.raises(ValueError, match="Forbidden pattern"):
            build_table_sqls_from_spec(spec, "cat.sch", seed=1, scale=1, target_rows=100)


# ---------------------------------------------------------------------------
# AVG synthesizer
# ---------------------------------------------------------------------------


class TestAvgSynthesizer:
    def test_sum_gets_avg_companion(self):
        measures = [{"name": "total_revenue", "expr": "SUM(revenue)", "comment": "Total revenue"}]
        synth = _synthesize_avg_measures(measures)
        assert len(synth) == 1
        assert synth[0]["name"] == "avg_revenue"
        assert synth[0]["expr"] == "AVG(revenue)"

    def test_sum_with_existing_avg_skipped(self):
        measures = [
            {"name": "total_revenue", "expr": "SUM(revenue)", "comment": ""},
            {"name": "avg_revenue", "expr": "AVG(revenue)", "comment": ""},
        ]
        assert _synthesize_avg_measures(measures) == []

    def test_compound_sum_gets_avg_companion(self):
        # SUM(a * b) used to be skipped; now we synthesize AVG(a * b)
        # because "average revenue per row" is exactly what Genie needs.
        measures = [{"name": "total_value", "expr": "SUM(qty * price)", "comment": ""}]
        synth = _synthesize_avg_measures(measures)
        assert len(synth) == 1
        assert synth[0]["name"] == "avg_value"
        assert synth[0]["expr"] == "AVG(qty * price)"

    def test_compound_sum_with_existing_avg_skipped(self):
        measures = [
            {"name": "total_value", "expr": "SUM(qty * price)", "comment": ""},
            {"name": "avg_value", "expr": "AVG(qty * price)", "comment": ""},
        ]
        assert _synthesize_avg_measures(measures) == []

    def test_max_only_not_synthesized(self):
        measures = [{"name": "max_temp", "expr": "MAX(temp)", "comment": ""}]
        assert _synthesize_avg_measures(measures) == []

    def test_synthesizer_runs_in_metric_view_build(self, monkeypatch):
        monkeypatch.setenv("GENIE_FACTORY_END_DATE", "2026-05-19")
        table = _minimal_table([
            ColumnSpec(name="entity_id", sql_type="STRING", comment="", is_dimension=True, generation_expr=""),
            ColumnSpec(name="category", sql_type="STRING", comment="", is_dimension=True, generation_expr=""),
            ColumnSpec(name="gor_scf_bbl", sql_type="DOUBLE", comment="", is_dimension=False,
                       generation_expr="500.0 + {qty_noise} * 4500.0"),
        ])
        spec = _minimal_spec(table, measures=[
            {"name": "total_gor_scf_bbl", "expr": "SUM(gor_scf_bbl)", "comment": ""},
        ])
        view_sql = build_metric_view_sqls_from_spec(spec, "cat.sch")["t1_metrics"]
        assert "name: total_gor_scf_bbl" in view_sql
        assert "name: avg_gor_scf_bbl" in view_sql
        assert "expr: AVG(gor_scf_bbl)" in view_sql

    def test_auto_avg_opt_out(self, monkeypatch):
        monkeypatch.setenv("GENIE_FACTORY_END_DATE", "2026-05-19")
        table = _minimal_table([
            ColumnSpec(name="entity_id", sql_type="STRING", comment="", is_dimension=True, generation_expr=""),
            ColumnSpec(name="category", sql_type="STRING", comment="", is_dimension=True, generation_expr=""),
            ColumnSpec(name="revenue", sql_type="DOUBLE", comment="", is_dimension=False,
                       generation_expr="100.0 + {qty_noise} * 900.0"),
        ])
        spec = _minimal_spec(table, measures=[
            {"name": "total_revenue", "expr": "SUM(revenue)", "comment": ""},
        ])
        spec.metric_views[0].auto_avg = False
        view_sql = build_metric_view_sqls_from_spec(spec, "cat.sch")["t1_metrics"]
        assert "total_revenue" in view_sql
        assert "avg_revenue" not in view_sql


# ---------------------------------------------------------------------------
# Backward-compatibility: existing JSONs still load and build
# ---------------------------------------------------------------------------


class TestBackwardCompat:
    def test_all_specs_parse_and_build(self, monkeypatch):
        """Every JSON spec in genie_factory/specs/ must still load via from_dict
        and produce valid SQL through the new engine. The vehicle_recall spec
        is allowed to fail because it intentionally triggers the new {seed}%N
        validator — that bug gets fixed in Phase 1."""
        import json
        from pathlib import Path

        monkeypatch.setenv("GENIE_FACTORY_END_DATE", "2026-05-19")
        specs_dir = Path(__file__).resolve().parents[1] / "genie_factory" / "specs"
        known_seed_mod_specs = {"automotive/vehicle_recall_root_cause_analysis"}

        failed_unexpected: list[str] = []
        for spec_path in sorted(specs_dir.glob("*/*.json")):
            key = f"{spec_path.parent.name}/{spec_path.stem}"
            try:
                spec = DomainSpec.from_dict(json.loads(spec_path.read_text()))
                build_table_sqls_from_spec(spec, "cat.sch", seed=42, scale=3, target_rows=5000)
                build_metric_view_sqls_from_spec(spec, "cat.sch")
            except ValueError as exc:
                if key in known_seed_mod_specs and "Forbidden pattern" in str(exc):
                    continue
                failed_unexpected.append(f"{key}: {exc!s}"[:200])
            except Exception as exc:  # noqa: BLE001
                failed_unexpected.append(f"{key}: {exc!r}"[:200])

        assert not failed_unexpected, "Specs failed engine build:\n" + "\n".join(failed_unexpected)
