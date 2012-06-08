jQuery(function($){
	
	/*
	
	MENU / NAVBAR EVENTS
	
	*/
	
		$("#navbar_collapse-button").click(function() {
		    mixpanel.track("Navbar Collapse pressed"); 
		});
	
		$("#navbar_landing_page-button-button").click(function() {
		    mixpanel.track("Navbar Landing page button pressed"); 
		});
	
		$("#navbar_salary-button").click(function() {
		    mixpanel.track("Navbar Salary button pressed"); 
		});
	
		$("#navbar_transactions-button").click(function() {
		    mixpanel.track("Navbar Transactions button pressed"); 
		});
	
		$("#navbar_home-button").click(function() {
		    mixpanel.track("Navbar Home button pressed"); 
		});
	
		$("#navbar_brand-button").click(function() {
		    mixpanel.track("Navbar Brand button pressed"); 
		});
	
	/*
	
	LANDING PAGE EVENTS
	
	*/
	
		$("#get_started_button").click(function() {
		    mixpanel.track("Get Started clicked"); 
		});
	
		$("#build_it-button").click(function() {
		    mixpanel.track("Build it. footer link clicked"); 
		});
	
	/*
	
	BALANCE PAGE EVENTS
	
	*/
	
		$("#balance_amount-field").focus(function() {
		    mixpanel.track("Balance Amount field focused"); 
		});
	
		$("#balance-submit").submit(function() {
		    mixpanel.track("Balance submitted"); 
		});
	
	/*
	
	SALARY PAGE EVENTS
	
	*/
	
		$("#salary_amount-field").focus(function() {
		    mixpanel.track("Salary Amount field focused"); 
		});
	
		$("#salary_date-field").focus(function() {
		    mixpanel.track("Salary Date field focused"); 
		});
	
		$("#salary-submit").submit(function() {
		    mixpanel.track("Salary submitted"); 
		});
	
	/*
	
	TRANSACTIONS PAGE EVENTS
	
	*/
	
		$("#transactions_amount-field").focus(function() {
		    mixpanel.track("Transactions Amount field focused"); 
		});
	
		$("#transactions_date-field").focus(function() {
		    mixpanel.track("Transactions Date field focused"); 
		});
	
		$("#transactions-submit").submit(function() {
		    mixpanel.track("Transactions submitted"); 
		});
	
});