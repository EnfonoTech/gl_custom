// Copyright (c) 2025, Aravind and contributors
// For license information, please see license.txt

frappe.query_reports["Outstanding Letter"] = {
	"filters": [
		{
			"fieldname": "customer",
			"label": "Customer",
			"fieldtype": "Link",
			"options": "Customer",
			"width": 100
		},
		{
			"fieldname": "from_date",
			"label": "From Date",
			"fieldtype": "Date",
			"width": 100
		},
		{
			"fieldname": "to_date",
			"label": "To Date",
			"fieldtype": "Date",
			"width": 100,
			"default": frappe.datetime.get_today()
		}
	]
};
