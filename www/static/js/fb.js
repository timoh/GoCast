$(document).ready(function(){
  window.fbAsyncInit = function() {
    FB.init({
      appId      : '357093254308731', // App ID
      channelUrl : window.location.href + 'channel', // Channel File
      status     : true, // check login status
      cookie     : true, // enable cookies to allow the server to access the session
      xfbml      : true  // parse XFBML
    });

    // Additional initialization code here
  };

  // Load the SDK Asynchronously
  (function(d){
     var js, id = 'facebook-jssdk'; if (d.getElementById(id)) {return;}
     js = d.createElement('script'); js.id = id; js.async = true;
     js.src = "//connect.facebook.net/en_US/all.js";
     d.getElementsByTagName('head')[0].appendChild(js);
   }(document));


   //add action to login button
   $("#login-button").on("click", function(){
       FB.login(function(response) {
       if (response.authResponse) {
         console.log('Welcome!  Fetching your information.... ');
         FB.api('/me', function(response) {
           console.log('Good to see you, ' + response.name + '.');
           console.log(response)
            //send user info to server
            $.ajax({
              url : "/login",
              type : "POST",
              contentType : "application/json",
              dataType : "json",
              data : JSON.stringify(response),
              success : function(){window.location.replace(window.location.href + "home");},
            });
           //FB.logout(function(response) { console.log('Logged out.');  });
         });
       } else {
         console.log('User cancelled login or did not fully authorize.');
         window.location.replace(window.location.href);
       }
     }, {scope: 'email'});

   });
});