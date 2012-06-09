/*

	EVENTS FOR MIXPANEL (gocast.herokuapp.com)

	by Timo H. / 2012

*/

jQuery(function($){
	$(document).ready(function() {
		
		/*
	
		MENU / NAVBAR EVENTS
	
		*/
	
			$("#navbar_collapse-button").click(function() {
			    mixpanel.track("Navbar Collapse pressed"); 
			});
			
			$("#navbar_brand-button").click(function() {
			    mixpanel.track("Navbar Brand button pressed"); 
			});
	
			$("#navbar_").click(function() {
			    mixpanel.track("Navbar Landing page button pressed"); 
			});
	
			$("#navbar_balance").click(function() {
			    mixpanel.track("Navbar Salary button pressed"); 
			});
	
			$("#navbar_salary").click(function() {
			    mixpanel.track("Navbar Salary button pressed"); 
			});
	
			$("#navbar_transactions").click(function() {
			    mixpanel.track("Navbar Transactions button pressed"); 
			});
	
			$("#navbar_home").click(function() {
			    mixpanel.track("Navbar Home button pressed"); 
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
	
			$("#balance-amount").focus(function() {
			    mixpanel.track("Balance Amount field focused"); 
			});
	
			$("#balance-submit").submit(function() {
			    mixpanel.track("Balance submitted"); 
			});
	
		/*
	
		SALARY PAGE EVENTS
	
		*/
	
			$("#salary-amount").focus(function() {
			    mixpanel.track("Salary Amount field focused"); 
			});
	
			$("#salary-date").focus(function() {
			    mixpanel.track("Salary Date field focused"); 
			});
	
			$("#salary-submit").submit(function() {
			    mixpanel.track("Salary submitted"); 
			});
	
		/*
	
		TRANSACTIONS PAGE EVENTS
	
		*/
	
			$("#transactions-amount").focus(function() {
			    mixpanel.track("Transactions Amount field focused"); 
			});
	
			$("#transactions-date").focus(function() {
			    mixpanel.track("Transactions Date field focused"); 
			});
	
			$("#transactions-submit").submit(function() {
			    mixpanel.track("Transactions submitted"); 
			});
			
			$("#button-sign").submit(function() {
			    mixpanel.track("Quick add switch sign button pushed"); 
			});
			
			$("#button-add_one").submit(function() {
			    mixpanel.track("Quick add button +1 pushed"); 
			});
			
			$("#button-add_five").submit(function() {
			    mixpanel.track("Quick add button +5 pushed"); 
			});
			
			$("#button-add_ten").submit(function() {
			    mixpanel.track("Quick add button +10 pushed"); 
			});
			
			$("#button-add_fifty").submit(function() {
			    mixpanel.track("Quick add button +50 pushed"); 
			});
	});
});