require.config({
    baseUrl: "/static/js/prettify"
});

require(["prettify"], 
	function() {
	        prettyPrint()
	        console.log("prettify is loaded")

});
