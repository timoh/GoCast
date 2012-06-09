$(document).ready(function(){
  var fb_dev = '411168845594539',
    fb_prod = '422541527766916',
    host = document.location.host,
    best_key = fb_prod;

  if(host === '127.0.0.1:5000'){
    best_key = fb_dev;
    console.log("Using local api.")
  }

  window.fbAsyncInit = function() {
    FB.init({
      appId      : best_key, // PROD
      channelUrl : "//:"+ window.location.host + '/channel', // Channel File
      status     : true, // check login status
      cookie     : true, // enable cookies to allow the server to access the session
      xfbml      : true  // parse XFBML
    });

    // Additional initialization code here
  };

   

   //add action to login button
   $("#login-button").on("click", function(){
       

    FB.login(function(response) {
       if (response.authResponse) {
         console.log('Welcome!  Fetching your information.... ');
         FB.api('/me', function(response) {
           console.log('Good to see you, ' + response.name + '.');
           //send user info to server
            $.ajax({
              url : window.location.href + "login",
              type : "POST",
              contentType : "application/json",
              dataType : "json",
              data : JSON.stringify(response),
              
            });
         });
       } else {
         console.log('User cancelled login or did not fully authorize.');
       }
     });

   });
});