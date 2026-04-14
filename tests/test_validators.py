"""Tests for validator utility functions -- pure, no Spark needed."""

import pytest

from genie_factory.validators import (
    validate_identifier,
    normalize_user_slug,
    sanitize_sql_identifier,
    sql_string,
    default_schema_name,
    Namespace,
)


class TestValidateIdentifier:
    def test_valid_simple(self):
        assert validate_identifier("my_table", "test") == "my_table"

    def test_valid_starts_with_underscore(self):
        assert validate_identifier("_private", "test") == "_private"

    def test_valid_mixed_case(self):
        assert validate_identifier("MyTable", "test") == "MyTable"

    def test_valid_alphanumeric_with_underscore(self):
        assert validate_identifier("table_123", "test") == "table_123"

    def test_invalid_starts_with_number(self):
        with pytest.raises(ValueError, match="not a valid identifier"):
            validate_identifier("123abc", "field")

    def test_invalid_hyphen(self):
        with pytest.raises(ValueError, match="not a valid identifier"):
            validate_identifier("my-table", "field")

    def test_invalid_space(self):
        with pytest.raises(ValueError, match="not a valid identifier"):
            validate_identifier("my table", "field")

    def test_empty_raises(self):
        with pytest.raises(ValueError, match="must not be empty"):
            validate_identifier("", "field")

    def test_invalid_special_chars(self):
        with pytest.raises(ValueError):
            validate_identifier("drop;--", "field")

    def test_single_letter(self):
        assert validate_identifier("x", "test") == "x"


class TestNormalizeUserSlug:
    def test_email(self):
        result = normalize_user_slug("chad.macumber@databricks.com")
        assert result == "chad_macumber"

    def test_simple_name(self):
        result = normalize_user_slug("john_doe")
        assert result == "john_doe"

    def test_special_chars_replaced(self):
        result = normalize_user_slug("user+test@example.com")
        # The + becomes _, producing "user_test"
        assert "_" in result
        assert result == "user_test"

    def test_uppercase_lowered(self):
        result = normalize_user_slug("Chad.Macumber@databricks.com")
        assert result == result.lower()
        assert result == "chad_macumber"

    def test_dots_replaced(self):
        result = normalize_user_slug("first.last")
        assert result == "first_last"

    def test_empty_after_strip_raises(self):
        with pytest.raises(ValueError, match="Could not derive"):
            normalize_user_slug("@@@")

    def test_numeric_parts_preserved(self):
        result = normalize_user_slug("user123@test.com")
        assert result == "user123"


class TestSqlString:
    def test_escapes_single_quote(self):
        assert sql_string("it's") == "it''s"

    def test_plain_string(self):
        assert sql_string("hello") == "hello"

    def test_multiple_quotes(self):
        assert sql_string("it's a 'test'") == "it''s a ''test''"

    def test_empty_string(self):
        assert sql_string("") == ""

    def test_no_quotes(self):
        assert sql_string("abc123") == "abc123"


class TestDefaultSchemaName:
    def test_basic(self):
        result = default_schema_name("chad.macumber@databricks.com", "retail_demo")
        assert result == "retail_demo_chad_macumber"

    def test_custom_basename(self):
        result = default_schema_name("john.doe@example.com", "supply_chain")
        assert result == "supply_chain_john_doe"

    def test_result_is_valid_identifier(self):
        result = default_schema_name("user@test.com", "demo")
        # Should not raise
        validate_identifier(result, "schema")


class TestSanitizeSqlIdentifier:
    def test_clean_input(self):
        result = sanitize_sql_identifier("my_table", "table")
        assert result == "my_table"

    def test_hyphen_replaced(self):
        result = sanitize_sql_identifier("my-table", "table")
        assert result == "my_table"

    def test_space_replaced(self):
        result = sanitize_sql_identifier("my table", "table")
        assert result == "my_table"

    def test_invalid_after_sanitize_raises(self):
        with pytest.raises(ValueError, match="Invalid SQL identifier"):
            sanitize_sql_identifier("123-bad!", "table")

    def test_leading_trailing_whitespace_stripped(self):
        result = sanitize_sql_identifier("  my_table  ", "table")
        assert result == "my_table"


class TestNamespace:
    def test_fqn_property(self):
        ns = Namespace(
            username="chad.macumber@databricks.com",
            user_slug="chad_macumber",
            catalog="main",
            schema="retail_demo_chad_macumber",
        )
        assert ns.fqn == "main.retail_demo_chad_macumber"

    def test_frozen(self):
        ns = Namespace(
            username="user@test.com",
            user_slug="user",
            catalog="main",
            schema="demo_user",
        )
        with pytest.raises(AttributeError):
            ns.catalog = "other"
