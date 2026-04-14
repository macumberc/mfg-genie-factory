# Databricks notebook source
import os as _os
_nb_path = dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()
_icon_path = _os.path.normpath(_os.path.join("/Workspace", _nb_path, "..", "..", "assets", "genie-icon.svg"))
try:
    with open(_icon_path) as _f:
        _icon_svg = _f.read()
except Exception:
    _icon_svg = ""
displayHTML(f"""
<div style="text-align: center; padding: 32px 0 16px 0;">
  <div style="display: inline-flex; align-items: center; gap: 16px;">
    <div style="width: 48px; height: 48px;">{_icon_svg}</div>
    <span style="font-size: 32px; font-weight: 800; color: #1B3139;">Genie Factory &mdash; Cleanup</span>
  </div>
  <p style="color: #555; font-size: 14px; margin-top: 8px;">Remove schemas, tables, and Genie spaces created by Genie Factory</p>
</div>
""")

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC #### Install the library
# MAGIC Run this cell once per cluster session if not already installed.

# COMMAND ----------

# MAGIC %pip install git+https://github.com/macumberc/genie-factory.git@manufacturing -q
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ### Option 1 &mdash; Tear down using the result from a deploy
# MAGIC If you still have the `result` variable from your deploy session, uncomment and run:

# COMMAND ----------

# from genie_factory import teardown
# teardown(**result)

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ### Option 2 &mdash; Tear down by schema name
# MAGIC If your session ended and you no longer have the `result` variable, you can clean up by specifying the catalog and schema directly. Find your schema name in the Unity Catalog browser or run the cell below to list Genie Factory schemas.

# COMMAND ----------

# List all schemas created by Genie Factory in the current catalog
schemas = spark.sql("""
    SELECT s.catalog_name, s.schema_name, s.comment, s.created
    FROM system.information_schema.schemata s
    WHERE s.schema_name LIKE '%_' || REPLACE(CURRENT_USER(), '@', '_at_') || '%'
       OR s.comment LIKE '%demo data%'
    ORDER BY s.created DESC
    LIMIT 20
""")
display(schemas)

# COMMAND ----------

# MAGIC %md
# MAGIC Edit the catalog and schema below to match the deployment you want to remove, then run the cell.

# COMMAND ----------

# from genie_factory import teardown

# teardown(
#     catalog="main",
#     schema="your_schema_name_here",
#     fqn="main.your_schema_name_here",
# )
