$(document).ready(function () {
	
	//scrolls down away from address bar to make a more webapp like feel on iPhone
	window.addEventListener("load", function() { window.scrollTo(0, 1); });
	
	$('#recurring-group').hide();
	var recurring = false;
	
	
	$('#recurring-checkbox').click(function(e){
		if (recurring == false){
			$('#recurring-group').slideDown('slow');
			recurring = true;
		} else if (recurring == true){
			$('#recurring-group').slideUp('slow');
			$('#recurrence-amount').val(''); //empty recurrence-amount
			recurring = false;
		} else {
			console.warn('Logic error in recurring checkbox jQuery!');
		}
	});
	
	
	function update_navbar(){
		//handles navbar highlighting
		var a_id = document.location.pathname.replace("/", "navbar_");
		$("ul.nav > li").removeClass("active");
		$("a#"+a_id).parent().addClass("active");
	}


	$(function() {
		//add jQueryUI datepicker for every .datefield
        $( ".datefield" ).datepicker({
          showOn: "focus",
          defaultDate: +0
        });
				$(".datefield").datepicker('setDate', new Date());
    });

	update_navbar();
});