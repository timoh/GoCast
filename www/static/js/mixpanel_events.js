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
					_gaq.push(['_trackEvent', 'Navbar', 'Button press', 'Collapse']); 
			});
			
			$("#navbar_brand-button").click(function() {
			    mixpanel.track("Navbar Brand button pressed");
			 		_gaq.push(['_trackEvent', 'Navbar', 'Button press', 'Brand']);
			});
	
			$("#navbar_").click(function() {
			    mixpanel.track("Navbar Home / landing page button pressed");
			 		_gaq.push(['_trackEvent', 'Navbar', 'Button press', 'Home / Landing page']);
			});
	
			$("#navbar_balance").click(function() {
			    mixpanel.track("Navbar Setup button pressed"); 
					_gaq.push(['_trackEvent', 'Navbar', 'Button press', 'Balance / Setup']);
			});
	
			$("#navbar_transactions").click(function() {
			    mixpanel.track("Navbar Transactions button pressed"); 
					_gaq.push(['_trackEvent', 'Navbar', 'Button press', 'Transactions']);
			});
	
			$("#navbar_home").click(function() {
			    mixpanel.track("Navbar Results button pressed");
			 		_gaq.push(['_trackEvent', 'Navbar', 'Button press', 'Results / Graph']);
			});
	
		/*
	
		LANDING PAGE EVENTS
	
		*/
	
			$("#get_started_button").click(function() {
			    mixpanel.track("Get Started clicked"); 
					_gaq.push(['_trackEvent', 'Landing Page', 'Button press', 'Get started']);
			});
			
			$("#learn_more-button").click(function() {
			    mixpanel.track("Learn More clicked"); 
					_gaq.push(['_trackEvent', 'Landing Page', 'Button press', 'Learn More']);
			});
	
			$("#build_it-button").click(function() {
			    mixpanel.track("Build it. footer link clicked"); 
					_gaq.push(['_trackEvent', 'Landing Page', 'Button press', 'Build it link']);
			});
	
		/*
	
		BALANCE PAGE EVENTS
	
		*/
	
			$("#balance-amount").focus(function() {
			    mixpanel.track("Balance Amount field focused");
					_gaq.push(['_trackEvent', 'Balance', 'Field focus', 'Balance Amount']);
			});
	
			$("#balance-submit").submit(function() {
			    mixpanel.track("Balance submitted");
					_gaq.push(['_trackEvent', 'Balance', 'Button press', 'Balance Submit']);
			});
	
		/*
	
		TRANSACTIONS PAGE EVENTS
	
		*/
	
			$("#transactions-amount").focus(function() {
			    mixpanel.track("Transactions Amount field focused"); 
					_gaq.push(['_trackEvent', 'Transactions', 'Field focus', 'Transaction Amount']);
			});
	
			$("#transactions-date").focus(function() {
			    mixpanel.track("Transactions Date field focused"); 
					_gaq.push(['_trackEvent', 'Transactions', 'Field focus', 'Transaction Date']);
			});
			
			$("#button-sign").submit(function() {
			    mixpanel.track("Quick add switch sign button pushed"); 
					_gaq.push(['_trackEvent', 'Transactions', 'Quick add', 'Sign']);
			});
			
			$("#button-add_one").submit(function() {
			    mixpanel.track("Quick add button +1 pushed"); 
					_gaq.push(['_trackEvent', 'Transactions', 'Quick add', 'AddOne']);
			});
			
			$("#button-add_five").submit(function() {
			    mixpanel.track("Quick add button +5 pushed"); 
					_gaq.push(['_trackEvent', 'Transactions', 'Quick add', 'AddFive']);
			});
			
			$("#button-add_ten").submit(function() {
			    mixpanel.track("Quick add button +10 pushed");
			 		_gaq.push(['_trackEvent', 'Transactions', 'Quick add', 'AddTen']);
			});
			
			$("#button-add_fifty").submit(function() {
			    mixpanel.track("Quick add button +50 pushed"); 
					_gaq.push(['_trackEvent', 'Transactions', 'Quick add', 'AddFifty']);
			});
			
			$("#transactions-submit").submit(function() {
			    mixpanel.track("Transactions submitted"); 
					_gaq.push(['_trackEvent', 'Transactions', 'Button press', 'Submit']);
			});
	});
});