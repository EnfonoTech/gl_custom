# Copyright (c) 2025, Aravind and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import today

def execute(filters=None):
	# frappe.errprint(filters)
	columns = [
		{
			"fieldname": "transaction",
			"label": "Transaction",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "custom_awb_mbl",
			"label": "AWB/MBL No",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "custom_remarks_custom",
			"label": "Remarks",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname":"posting_date",
			"label": "Invoice Date",
			"fieldtype": "Date",
			"width": 120
		},
		{
			"fieldname": "name",
			"label": "Invoice No",
			"fieldtype": "Data",
			"width": 180
		},
		{
			"fieldname": "grand_total",
			"label": "Total",
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"fieldname": "payments",
			"label": "Payments",
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"fieldname": "balance",
			"label": "Balance",
			"fieldtype": "Currency",
			"width": 150
		},
	]

	condns = {
		'docstatus': 1
	}
	data = []
	if filters:
		if filters.customer:
			condns['customer'] = filters.customer
		if filters.from_date and filters.to_date:
			condns["posting_date"] = ["between", [filters.from_date, filters.to_date]]
		elif filters.from_date and not filters.to_date:
			condns["posting_date"] = [">=", filters.from_date]
		elif filters.to_date and not filters.from_date:
			condns["posting_date"] = ["<=", filters.from_date]
		# if filters.customer and filters.from_date:
		# 	result = frappe.db.sql("""
		# 		SELECT SUM(debit) - SUM(credit) AS opening_balance
		# 		FROM `tabGL Entry`
		# 		WHERE party_type = 'Customer'
		# 		AND party = %s
		# 		AND posting_date < %s
		# 		AND is_cancelled = 0
		# 	""", (filters.customer, filters.from_date), as_dict=True)
		# 	opening_balance = result[0].opening_balance or 0

		# 	data.append({
		# 		"posting_date": "",
		# 		"transaction": "Opening Balance",
		# 		"grand_total": None,
		# 		"payments": None,
		# 		"balance": opening_balance
		# 	})

	fields = ['name', 'posting_date', 'grand_total', 'outstanding_amount']
	
	# Check for custom fields
	meta = frappe.get_meta('Sales Invoice')
	if meta.has_field('custom_awb_mbl'):
		fields.append('custom_awb_mbl')

	if meta.has_field('custom_remarks_custom'):
		fields.append('custom_remarks_custom')

	invoices = frappe.get_all(
		"Sales Invoice",
		filters=condns,
		fields=fields,
		order_by='posting_date',
		)
	
	if invoices and len(invoices) != 0:
		running_sum = 0

		for invoice in invoices:
			running_sum += invoice.outstanding_amount
			invoice['transaction'] = "Debit Note"
			invoice['payments'] = invoice.grand_total - invoice.outstanding_amount
			invoice['balance'] = running_sum

		data += invoices

		# total_grand = sum(row.grand_total for row in data)
		# total_payments = sum(row.payments for row in data)
		# total_outstanding = sum(row.outstanding_amount for row in data)
		
		# Add custom balance row
		data.append({
			"transaction": f"Balance Due (As of {today()})",
			"grand_total": None,
			"payments": None,
			"balance": invoices[-1].balance
		})

		return columns, data
