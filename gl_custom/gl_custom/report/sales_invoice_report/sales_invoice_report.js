// Copyright (c) 2025, Aravind and contributors
// For license information, please see license.txt

frappe.query_reports["Sales Invoice Report"] = {
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
			"width": 100
		},
		{
			"fieldname": "company",
			"label": "Company",
			"fieldtype": "Link",
			"options": "Company",
			"width": 100
		}
	],

	onload: function(report) {
		report.page.add_inner_button("My Button", ()=> {
			frappe.msgprint("Button is clicked!")
		}, "Actions")
	}
};
