$(document).ready(function () {
	
	window.addEventListener("load", function() { window.scrollTo(0, 1); });
	
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
    });

	update_navbar();
});