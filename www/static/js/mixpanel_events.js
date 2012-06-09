/*

	EVENTS FOR MIXPANEL (gocast.herokuapp.com)

	by Timo H. / updated June 6th 2012

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
			    mixpanel.track("Navbar Home / landing page button pressed"); 
			});
	
			$("#navbar_balance").click(function() {
			    mixpanel.track("Navbar Setup button pressed"); 
			});
	
			$("#navbar_transactions").click(function() {
			    mixpanel.track("Navbar Transactions button pressed"); 
			});
	
			$("#navbar_home").click(function() {
			    mixpanel.track("Navbar Results button pressed"); 
			});
	
		/*
	
		LANDING PAGE EVENTS
	
		*/
	
			$("#get_started_button").click(function() {
			    mixpanel.track("Get Started clicked"); 
			});
			
			$("#learn_more-button").click(function() {
			    mixpanel.track("Learn More clicked"); 
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
	
		TRANSACTIONS PAGE EVENTS
	
		*/
	
			$("#transactions-amount").focus(function() {
			    mixpanel.track("Transactions Amount field focused"); 
			});
	
			$("#transactions-date").focus(function() {
			    mixpanel.track("Transactions Date field focused"); 
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
			
			$("#transactions-submit").submit(function() {
			    mixpanel.track("Transactions submitted"); 
			});
	});
});