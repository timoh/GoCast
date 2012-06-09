/*
	
	THE SCRIPT FOR HANDLING THE QUICK ADD BUTTONS IN ADD TRANSACTIONS VIEW
	
	by Timo H. // 2012 
	
	*** KNOWN BUGS ***
	
	Quick double tap on iPhone zooms (quick adding made more difficult)
	--> TODO

*/

jQuery(function($){
	$(document).ready(function() {

		$('#quick_add-btn_grp').nodoubletapzoom; //this doesn't work at all
		
		/*
		
			SIGN CHANGING (+/-) FOR QUICK ADD BUTTONS
			Button id: #button-sign
			Vars: (bool)sign_positive //keep track of the sign of the buttons
		
		*/
		
		var sign_positive = true;
		
			$('#button-sign').click(function(e){
				e.preventDefault();
				
				/*
				
					TOGGLE SIGN FOR QUICK ADD BUTTONS
					
					Buttons handled:
					
						#button-add_one
						#button-add_five
						#button-add_ten
						#button-add_fifty
				
				*/
				
				if(sign_positive){
					$('#button-add_one').text('-1');
					$('#button-add_five').text('-5');
					$('#button-add_ten').text('-10');
					$('#button-add_fifty').text('-50');
					sign_positive = false;
				} else {
					$('#button-add_one').text('+1');
					$('#button-add_five').text('+5');
					$('#button-add_ten').text('+10');	
					$('#button-add_fifty').text('+50');	
					sign_positive = true;
				}
			});
		
		/*
		
			QUICK ADD or SUBTRACT AMOUNTS
			Button ids:
			
				#button-add_one
				#button-add_five
				#button-add_ten
				
			Vars: 
			
				(float)amount // track the amount field's value
				(float)from_button // stores the value from the quick add button
				
		*/
		
		var amount = 0;
		var from_button;
		
			$('#button-add_one').click(function(e){
				e.preventDefault();
				
					from_button = parseFloat($('#button-add_one').text());
					amount = parseFloat(parseFloat(amount)+parseFloat(from_button));
					$('#amount').val(amount);
				
			});
			
			$('#button-add_five').click(function(e){
				e.preventDefault();
				
					from_button = parseFloat($('#button-add_five').text());
					amount = parseFloat(parseFloat(amount)+parseFloat(from_button));
					$('#amount').val(amount);
				
			});
			
			$('#button-add_ten').click(function(e){
				e.preventDefault();
				
					from_button = parseFloat($('#button-add_ten').text());
					amount = parseFloat(parseFloat(amount)+parseFloat(from_button));
					$('#amount').val(amount);
				
			});
			
			$('#button-add_fifty').click(function(e){
				e.preventDefault();
				
					from_button = parseFloat($('#button-add_fifty').text());
					amount = parseFloat(parseFloat(amount)+parseFloat(from_button));
					$('#amount').val(amount);
				
			});
		
	});
});