"""Tests for _fix_boolean_arithmetic() -- deterministic, pure function.

This function rewrites SQL expressions where a boolean predicate is
multiplied by a number (unsupported in Spark SQL) into an equivalent
CASE WHEN ... THEN ... ELSE 0 END expression.
"""

from genie_factory.data import _fix_boolean_arithmetic


class TestFixBooleanArithmetic:
    def test_simple_in_multiply(self):
        expr = "(col IN (1,2)) * 8.0"
        result = _fix_boolean_arithmetic(expr)
        assert "CASE WHEN" in result
        assert "THEN 8.0" in result
        assert "ELSE 0 END" in result

    def test_no_boolean_passes_through(self):
        expr = "(a + b) * 2"
        result = _fix_boolean_arithmetic(expr)
        assert result == expr  # No boolean ops, no transformation

    def test_and_compound(self):
        expr = "((col1 IN (1,2)) AND (col2 > 5)) * 10"
        result = _fix_boolean_arithmetic(expr)
        assert "CASE WHEN" in result
        assert "THEN 10" in result

    def test_or_compound(self):
        expr = "(status IN ('A','B') OR flag = 1) * 5.0"
        result = _fix_boolean_arithmetic(expr)
        assert "CASE WHEN" in result
        assert "THEN 5.0" in result

    def test_nested_parens(self):
        expr = "((a IN (1,2,3))) * 7"
        result = _fix_boolean_arithmetic(expr)
        assert "CASE WHEN" in result
        assert "THEN 7" in result

    def test_no_change_needed(self):
        expr = "ROUND(price * 1.08, 2)"
        assert _fix_boolean_arithmetic(expr) == expr

    def test_empty_string(self):
        assert _fix_boolean_arithmetic("") == ""

    def test_comparison_operator_gte(self):
        expr = "(score >= 80) * 1.5"
        result = _fix_boolean_arithmetic(expr)
        assert "CASE WHEN" in result
        assert "THEN 1.5" in result

    def test_comparison_operator_lt(self):
        expr = "(price < 10) * 0.5"
        result = _fix_boolean_arithmetic(expr)
        assert "CASE WHEN" in result
        assert "THEN 0.5" in result

    def test_equality_operator(self):
        expr = "(status = 'active') * 100"
        result = _fix_boolean_arithmetic(expr)
        assert "CASE WHEN" in result
        assert "THEN 100" in result

    def test_not_equal_operator(self):
        expr = "(type != 'internal') * 3.0"
        result = _fix_boolean_arithmetic(expr)
        assert "CASE WHEN" in result

    def test_plain_multiplication_untouched(self):
        """Pure arithmetic with no boolean keywords should not be rewritten."""
        expr = "quantity * unit_price"
        assert _fix_boolean_arithmetic(expr) == expr

    def test_multiple_boolean_multiplies_in_expression(self):
        """If there are multiple (bool)*N segments, both should be rewritten."""
        expr = "(a IN (1,2)) * 5 + (b > 3) * 10"
        result = _fix_boolean_arithmetic(expr)
        # Both occurrences should be transformed
        assert result.count("CASE WHEN") == 2

    def test_preserves_surrounding_context(self):
        """Text before and after the boolean*number should be preserved."""
        expr = "base_amt + (category IN ('A','B')) * 8.0 + tax"
        result = _fix_boolean_arithmetic(expr)
        assert result.startswith("base_amt + ")
        assert result.endswith(" + tax")
        assert "CASE WHEN" in result

    def test_decimal_value(self):
        expr = "(flag IN (1)) * 0.15"
        result = _fix_boolean_arithmetic(expr)
        assert "THEN 0.15" in result

    def test_integer_value(self):
        expr = "(is_premium IN (1)) * 50"
        result = _fix_boolean_arithmetic(expr)
        assert "THEN 50" in result

    def test_deeply_nested_and_or(self):
        expr = "((month(dt) IN (6,7,8)) AND (category = 'X')) * 8.0"
        result = _fix_boolean_arithmetic(expr)
        assert "CASE WHEN" in result
        assert "ELSE 0 END" in result
