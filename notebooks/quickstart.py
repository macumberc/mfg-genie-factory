# Databricks notebook source
# MAGIC %md
# MAGIC <div style="text-align: center; padding: 32px 0 16px 0;">
# MAGIC   <div style="display: inline-flex; align-items: center; gap: 16px;">
# MAGIC     <img src="https://raw.githubusercontent.com/macumberc/genie-factory/manufacturing/assets/genie-icon.svg" width="72" height="72" />
# MAGIC     <span style="font-size: 48px; font-weight: 800; color: #1B3139; letter-spacing: -0.5px;">Genie Factory</span>
# MAGIC   </div>
# MAGIC   <p style="color: #555; font-size: 16px; margin-top: 8px;">Deploy a Genie room for any manufacturing use case in minutes</p>
# MAGIC </div>
# MAGIC
# MAGIC > **Requirement:** This notebook must be run on **Serverless** compute or a cluster with **Databricks Runtime 14.3+** and Unity Catalog enabled.

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC #### Install the library
# MAGIC Run this cell once per cluster session. Takes about 30 seconds.

# COMMAND ----------

# MAGIC %pip install git+https://github.com/macumberc/genie-factory.git@manufacturing -q
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ### Step 1 &mdash; Pick a subindustry
# MAGIC Run the cell below. A **Subindustry** dropdown will appear at the top of the notebook. Select your subindustry from that dropdown, then continue to Step 2.

# COMMAND ----------

from genie_factory.presets import SUBINDUSTRIES, USE_CASES

dbutils.widgets.dropdown("subindustry", SUBINDUSTRIES[0], SUBINDUSTRIES, "Subindustry")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Step 2 &mdash; Pick a use case
# MAGIC Run the cell below. A **Use Case** dropdown will appear at the top of the notebook next to the subindustry dropdown. Select a use case, then continue to Step 3.

# COMMAND ----------

sub = dbutils.widgets.get("subindustry")
cases = [uc["label"] for uc in USE_CASES[sub]]
dbutils.widgets.dropdown("use_case", cases[0], cases, "Use Case")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Step 3 &mdash; Deploy your Genie room
# MAGIC Run the cell below. This creates your data tables and Genie space. Usually takes **about 1 minute**. When it finishes, you'll see a card with a button to open your new Genie room.

# COMMAND ----------

from genie_factory import deploy_use_case, teardown

result = deploy_use_case(
    dbutils.widgets.get("subindustry"),
    dbutils.widgets.get("use_case"),
)

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ### Cleanup
# MAGIC When you're done with the demo, uncomment the line below and run it to remove everything that was created. For more cleanup options, use the [cleanup notebook](https://github.com/macumberc/genie-factory/blob/manufacturing/notebooks/cleanup.py).

# COMMAND ----------

# teardown(**result)
