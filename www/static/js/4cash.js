$(document).ready(function () {
	function update_navbar(){
		//handles navbar highlighting
		var a_id = document.location.pathname.replace("/", "navbar_");
		$("ul.nav > li").removeClass("active");
		$("a#"+a_id).parent().addClass("active");
	}

	$(function() {
		//add jQueryUI datepicker for every .datefield
        $( ".datefield" ).datepicker({
          showOn: "button",
          buttonImage: "/static/img/calendar.gif",
          buttonImageOnly: true,
          defaultDate: +0
        });
    });

	update_navbar();
});