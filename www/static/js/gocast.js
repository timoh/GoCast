$(document).ready(function () {
	function update_navbar(){
		//handles navbar highlighting
		var a_id = document.location.pathname.replace("/", "navbar_");
		$("ul.nav > li").removeClass("active");
		$("a#"+a_id).parent().addClass("active");
	}

	update_navbar();
});