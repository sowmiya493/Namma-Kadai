import frappe
from frappe.model.document import Document

class ExpenseChart(Document):
    def validate(self):
        data = self.expense_user()
        if data:
            self.user_chart = self.generate_chart(data)
        else:
            self.user_chart = self._generate_empty_chart()

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
        grouped_data = {}
        for record in data:
            if record['expense_type'] not in grouped_data:
                grouped_data[record['expense_type']] = []
            grouped_data[record['expense_type']].append(record)
        chart_html = ''
        for expense_type, records in grouped_data.items():
            max_amount = max(record["total_amount"] for record in records) if records else 0
            if max_amount == 0:
                chart_html += self._generate_empty_chart(expense_type)
            else:
                y_axis_ticks = range(0, int(max_amount) + 1, max(1, int(max_amount // 5)))
                chart_html += self._generate_chart_html(expense_type, records, max_amount, y_axis_ticks)
        return chart_html

    def _generate_empty_chart(self, expense_type=""):
        return f'''
        <div class="chart-container" 
            style="display: flex; 
            flex-direction: column; 
            width: 100%; 
            padding: 4px;
             border: 1px solid purple;
              background-color: #f5f5f5;">
            <h4 style="text-align:
             center; 
             margin-bottom: 10px;">{expense_type} Expenses</h4>
            <div style="text-align: center; 
            font-size: 14px;
            color: #888;">
                No data available for this expense type.
            </div>
        </div>
        '''

    def _generate_chart_html(self, expense_type, data, max_amount, y_axis_ticks):
        """Generate the HTML content for the chart."""
        chart_html = f'''
        <div class="chart-container" 
            style="display: flex;
             flex-direction: column; 
             width: 100%; 
             padding: 4px; 
             border: 1px solid purple; 
             background-color: #f5f5f5;">
            <h4 style="text-align: center; margin-bottom: 10px;">{expense_type} Expenses</h4>
            <div style="display: flex; 
            flex-direction: row;">
                <div class="y-axis" style="display: flex; 
                flex-direction: column;
                justify-content: space-between;
                height: 300px; width: 40px; 
                margin-right: 10px;">
        '''
        for tick in reversed(y_axis_ticks):
            chart_html += f'<div style="text-align: left; font-size: 10px;">{tick}</div>'
        chart_html += '''
                </div>
                <div class="chart-content" style="display: flex; 
                align-items: flex-end;
                justify-content: space-between;
                height: 300px;
                width: calc(100% - 50px);">
        '''
        for record in data:
            bar_height = (record['total_amount'] / max_amount * 100) if max_amount > 0 else 0
            chart_html += f'''
            <div style="width: 10%; 
                        height: {bar_height}%; 
                        background: linear-gradient(0deg, #c061cb 0%, #ffffff 100%);
                        text-align: center; 
                        margin: 5px;">
                <span style="font-size: 10px; 
                margin-top: 5px;">
                    {record['user']}
                </span>
            </div>
            '''
        chart_html += '''
            </div>
        </div>
        <div class="x-axis" style="display: flex; 
        justify-content: space-between;
         margin-top: 10px;
          padding-left: 50px;">
        '''
        for record in data:
            chart_html += f'''
            <div style="text-align: center;
            width: 10%;
            font-size: 10px;">{record['user']}</div>
            '''
        chart_html += '''
        </div>
        </div>
        '''
        return chart_html
