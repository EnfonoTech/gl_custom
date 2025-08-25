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
		
		total_under30 = 0
		total_under60 = 0
		total_under90 = 0
		total_under120 = 0
		total_under150 = 0
		total_under180 = 0
		total_from180 = 0

		for idx, invoice in enumerate(invoices):
			running_sum += invoice.outstanding_amount
			invoice['running_total'] = running_sum
			age = (getdate(today()) - getdate(invoice.due_date)).days
			invoice['age'] = age
			if age < 30:
				total_under30 += invoice.outstanding_amount
			elif 30 <= age < 60:
				total_under60 += invoice.outstanding_amount
			elif 60 <= age < 90:
				total_under90 += invoice.outstanding_amount
			elif 90 <= age < 120:
				total_under120 += invoice.outstanding_amount
			elif 120 <= age < 150:
				total_under150 += invoice.outstanding_amount
			elif 150 <= age < 180:
				total_under180 += invoice.outstanding_amount
			elif age >= 180:
				total_from180 += invoice.outstanding_amount
			
			if invoice.cost_center:
				branch = invoice.cost_center.split('-')[0].strip()
				invoice['cost_center'] = branch
			if invoice.custom_job_record:
				invoice['job_record'] = invoice.custom_job_record
			elif invoice.custom_warehouse_job_record:
				invoice['job_record'] = invoice.custom_warehouse_job_record

			if idx == len(invoices)-1:
				invoice['age_group'] = {
					"total_under30": total_under30,
					"total_under60": total_under60,
					"total_under90": total_under90,
					"total_under120": total_under120,
					"total_under150": total_under150,
					"total_under180": total_under180,
					"total_from180": total_from180,
				}

		data += invoices

	return columns, data
