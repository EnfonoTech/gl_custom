# Copyright (c) 2025, Aravind and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import today, getdate


def execute(filters=None):
	columns = [
		{
			"fieldname": "posting_date",
			"label": "Date",
			"fieldtype": "Date",
			"width": 150
		},
		{
			"fieldname": "name",
			"label": "Voucher No",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "cost_center",
			"label": "Branch",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "job_record",
			"label": "Narration",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "grand_total",
			"label": "Amount",
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"fieldname": "outstanding_amount",
			"label": "O/S Amount",
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"fieldname": "running_total",
			"label": "Running Total",
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"fieldname": "age",
			"label": "Ageing",
			"fieldtype": "Integer",
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


	fields = ['name', 'posting_date', 'due_date', 'cost_center', 'grand_total', 'outstanding_amount']

	# Check for custom fields
	meta = frappe.get_meta('Sales Invoice')
	if meta.has_field('custom_job_record'):
		fields.append('custom_job_record')

	if meta.has_field('custom_warehouse_job_record'):
		fields.append('custom_warehouse_job_record')

	invoices = frappe.get_all(
		"Sales Invoice",
		filters=condns,
		fields=fields,
		order_by='posting_date',
		)
	
	if invoices and len(invoices) != 0:
		running_sum = 0

		for idx, invoice in enumerate(invoices):
			running_sum += invoice.outstanding_amount
			invoice['running_total'] = running_sum
			age = (getdate(today()) - getdate(invoice.due_date)).days
			invoice['age'] = age
			if invoice.cost_center:
				branch = invoice.cost_center.split('-')[0].strip()
				invoice['cost_center'] = branch
			if invoice.custom_job_record:
				invoice['job_record'] = invoice.custom_job_record
			elif invoice.custom_warehouse_job_record:
				invoice['job_record'] = invoice.custom_warehouse_job_record

		data += invoices

	return columns, data
