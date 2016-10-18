   var Login = Login || (function() {

     function receivedLoginResult(data) {
       tokenLogin = data.key
       if (data.key) {

         tokenLogin = data.key
         document.getElementById('loginbuttons').setAttribute('style', 'display: none');
         document.getElementById('logininfobox').setAttribute('style', 'display: true');
         $('#modallogin').modal('hide'); 
         $.ajax({
           url: "/api/users/user/",
           type: "get",
           headers: {
             "Authorization": "Token " + Login.token()
           },
           dataType: 'json',
           success: receivedUser,
         });
       } else {
         loggedOut();
       }

     }

     function receivedUser(data){
      
      var fullname=data.first_name+" "+data.last_name;
      username=data.username;
      if (fullname===" "){
        fullname=data.username
        $('#logininfo').text()
      }
      var stringuser="Logged in as "+fullname+" ("+externalLogin+")"
      $('#logininfo').text(stringuser)
     }

     // Google Sign-in (new)
     function onSignInGoogle(googleUser) {

       //window.alert(googleUser.getAuthResponse().access_token)
       var access_token = googleUser.getAuthResponse().access_token
       if (access_token) {
         if (!externalLogin) {
           externalLogin = 'Google'
           externalToken = access_token
           $.ajax({
             url: "/api/users/google/",
             type: "post",
             data: {
               access_token: externalToken
             },
             dataType: 'json',
             success: receivedLoginResult,
             error: receivedLoginResult,
           });
         }
       } else {
         auth2 = gapi.auth2.getAuthInstance();
         auth2.signOut();
       }



     }

     function onSignInFailureGoogle() {

     }



     function initializeGoogleButton() {
       gapi.signin2.render('googlelogin', {
         'scope': 'profile',
         'onsuccess': onSignInGoogle,
         'onfailure': onSignInFailureGoogle,
         'access-type': 'offline',
         'width': 95,
         'height': 25, 
       });

       gapi.signin2.render('googleloginmodal', {
         'scope': 'profile',
         'onsuccess': onSignInGoogle,
         'onfailure': onSignInFailureGoogle,
         'access-type': 'offline',
         'width': 95,
         'height': 25,
       });

     }


     function checkLoginState() {
       FB.getLoginStatus(statusChangeCallback);
     }

     // This is called with the results from from FB.getLoginStatus().
     function statusChangeCallback(response) {
       if (response.status === 'connected') {
         if (!externalLogin) {
           externalLogin = 'Facebook'
           externalToken = response.authResponse.accessToken
           $.ajax({
             url: "/api/users/facebook/",
             type: "post",
             data: {
               "access_token": externalToken
             },
             dataType: 'json',
             success: receivedLoginResult,
             error: receivedLoginResult,
           });
         }

       } else if (response.status === 'not_authorized') {} //Logged into Facebook, but not your app.
       else {} // Not logg into FB

     }

     function initializeFacebookButton() {
       FB.Event.subscribe('auth.statusChange', checkLoginState)
       FB.Event.subscribe('auth.authResponseChange', checkLoginState)
       FB.init({ 
         //appId: '1599812356955227', //Local test
         appId: '1599520313651098', //Open shift test
         //appId: '1593460310923765', //Open shift production
         cookie: true, // enable cookies to allow the server to access 
         xfbml: true, // parse social plugins on this page
         version: 'v2.2', // use version 2.2
         status: true,
       });
     }

     function logOut() {
       if (tokenLogin) {

         $.ajax({
           url: "/api/users/logout/",
           type: "post",
           data: {},
           headers: {
             "Authorization": "Token " + tokenLogin
           },
           dataType: 'json',
           success: loggedOut,
           error: loggedOut
         });
       } else {
         loggedOut()
       }
     }

     function loggedOut() {

       if (externalLogin == 'Google') {
         auth2 = gapi.auth2.getAuthInstance();
         auth2.signOut();
       } else if (externalLogin == 'Facebook') {
         //FB.logout(function(response) {});
       }

       tokenLogin = null
       externalToken = null
       externalLogin = null
       $('#logininfo').text("")
       document.getElementById('loginbuttons').setAttribute('style', 'display: true');
       document.getElementById('logininfobox').setAttribute('style', 'display: none');
     }

     function modalLoginFinished(){
        if (tokenLogin){
            if (logincallback){
              logincallback();
            }
        }
        logincallback = null
     }

     var tokenLogin = null
     var externalToken = null
     var externalLogin = null
     var username = null
     var logincallback = null

     

     return {
       init: function() {

         initializeGoogleButton()        

         document.getElementById('logininfobox').setAttribute('style', 'display: none');
         $('#logout').on('click', logOut);
         $('#fblogin').on('click', checkLoginState);
         $('#fbloginmodal').on('click', checkLoginState);

         initializeFacebookButton()

         $('#modallogin').on('hidden.bs.modal', modalLoginFinished)

       },
       token: function() {
         return tokenLogin
       },

       username: function() {
        if (tokenLogin){
         return username
        }
        else{
          return null
        }
       },

       popup: function(callback_in) {
        if (!tokenLogin){
         $('#modallogin').appendTo("body").modal('show'); 
         logincallback=callback_in
        }
        
      },
     }

   })()