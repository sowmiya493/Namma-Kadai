import frappe
from frappe.model.document import Document

class ExpenseChart(Document):
def validate(self):
data = self.expense_user()
self.user_chart = self.generate_chart(data)

def expense_user(self, filters=None):
conditions = []
query_filters = filters or {}
if query_filters.get("from_date"):
conditions.append("date >= %(from_date)s")
if query_filters.get("to_date"):
conditions.append("date <= %(to_date)s")
if query_filters.get("expense_type"):
conditions.append("expense_type = %(expense_type)s")
if query_filters.get("user"):
conditions.append("user = %(user)s")
where_clause = " AND ".join(conditions) if conditions else "1=1"
query = f"""
SELECT
expense_type, user, SUM(amount) AS total_amount
FROM
`tabExpense`
WHERE
{where_clause} AND docstatus < 2
GROUP BY
expense_type, user
ORDER BY
total_amount DESC
"""
return frappe.db.sql(query, query_filters, as_dict=True)

def generate_chart(self, data):
max_amount = max(record["total_amount"] for record in data) if data else 0
if max_amount == 0:
return self._generate_empty_chart()
y_axis_ticks = range(0, int(max_amount) + 1, max(1, int(max_amount // 5)))
return self._generate_chart_html(data, max_amount, y_axis_ticks)



def _generate_chart_html(self, data, max_amount, y_axis_ticks):
"""Generate the HTML content for the chart."""
chart_html = '''
<div class="chart-container"
style="display: flex; flex-direction: column; width: 100%; padding: 4px; border: 1px solid purple; background-color: #f5f5f5;">
<h4 style="text-align: center; margin-bottom: 10px;">Expense Chart</h4>
<div style="display: flex; flex-direction: row;">
<div class="y-axis" style="display: flex; flex-direction: column; justify-content: space-between; height: 300px; width: 40px; margin-right: 10px;">
'''
for tick in reversed(y_axis_ticks):
chart_html += f'<div style="text-align: left; font-size: 10px;">{tick}</div>'
chart_html += '''
</div>
<div class="chart-content" style="display: flex; align-items: flex-end; justify-content: space-between; height: 300px; width: calc(100% - 50px);">
'''
for record in data:
bar_height = (record['total_amount'] / max_amount * 100) if max_amount > 0 else 0
chart_html += f'''
<div style="width: 10%;
height: {bar_height};
background-color: #dc8add;
text-align: center;
margin: 5px;">
<span style="font-size: 10px; margin-top: 5px;">
{record['user']}
</span>
</div>
'''



return chart_html
