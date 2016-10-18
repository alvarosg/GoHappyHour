   var NewLocationView = NewLocationView || (function() {


     function submitLocation() {
       var name = $("#newlocationname").val()
       var latitude = $("#newlocationlatitude").val()
       var longitude = $("#newlocationlongitude").val()
       var address = $("#newlocationaddress").val()
       var country = $("#newlocationcountry").val()
       var postcode = $("#newlocationpostcode").val()
       var phonenumber = $("#newlocationphonenumber").val()
       var website = $("#newlocationwebsite").val()

       var missing = ""
       if (!name) {
         missing += "Name "
       }
       if (!latitude) {
         missing += "Latitude "
       }
       if (!longitude) {
         missing += "Longitude "
       }

       if (missing) {
         window.alert('Missing the following fields: ' + missing)
         return
       } else {
         var data = {
           "name": name,
           "longitude": longitude,
           "latitude": latitude,
           "address": address,
           "country": country,
           "postcode": postcode,
           "phonenumber": phonenumber,
           "website": website
         }
         $.ajax({
           url: "/api/locations/",
           type: "post",
           data: data,
           headers: {
             "Authorization": "Token " + Login.token()
           },
           dataType: 'json',
           success: locationPosted,
           error: locationNotPosted
         });

       }
     }

     function locationPosted(data) {
       var locid = data.id
       var picture = $("#newlocationpicture").val()

       if (picture) {
         file = document.getElementById("newlocationpicture").files[0]
         var xhr = new XMLHttpRequest();
         var fd = new FormData();
         fd.append('picture', file);
         xhr.open('post', "/api/locations/" + locid + "/pictures/upload", true);
         xhr.setRequestHeader("Authorization", "Token " + Login.token());
         xhr.onreadystatechange = picturePosted
         xhr.send(fd);

       }
       $('#modalnewlocationview').modal('hide');
       SearchBar.openlocation(data.id)

     }

     function locationNotPosted(data) {
       window.alert('Error posting: are you still logged in? Are the coordinates valid?')
     }

     function picturePosted(data) {
       console.log(data)
       LocationView.update()
     }

     function pictureNotPosted(data) {
       window.alert('Error posting the image')
     }

     function initializeMap() {
       resizeMap()
       var mapCanvas = document.getElementById("map-newlocation-canvas");
       var mapOptions = {
         center: new google.maps.LatLng(latcenter, longcenter),
         zoom: 15,
         mapTypeId: google.maps.MapTypeId.ROADMAP
       }

       mapNewLocation = new google.maps.Map(mapCanvas, mapOptions)

       markerNewLocation = new google.maps.Marker({
         position: new google.maps.LatLng(latcenter, longcenter),
         map: mapNewLocation,
       });

       $('#newlocationlatitude').val(latcenter);
       $('#newlocationlongitude').val(longcenter);

       google.maps.event.addListener(mapNewLocation, 'click', changeMarker);
       resizeMap()
       setTimeout(resizeMap, 1500);
       

     }

     function changeMarker(event) {
       latcenter = event.latLng.lat();
       longcenter = event.latLng.lng();
       markerNewLocation.setPosition(event.latLng)
       $('#newlocationlatitude').val(latcenter);
       $('#newlocationlongitude').val(longcenter);
     }

     function changedCoordinates() {
       latcenter = $('#newlocationlatitude').val()
       longcenter = $('#newlocationlongitude').val()
       var latlong = new google.maps.LatLng(latcenter, longcenter)
       markerNewLocation.setPosition(latlong)
       mapNewLocation.setCenter(latlong)
     }

     function resizeMap() {
       mapwidth = $('#map-newlocation-canvas').css('width');
       mapheight = mapwidth
       $('#map-newlocation-canvas').css('height', mapheight)

       if (mapNewLocation){
          mapNewLocation.setCenter(new google.maps.LatLng(latcenter,longcenter))
       }
     };

     var latcenter, longcenter
     var markerNewLocation=null
     var mapNewLocation=null
     return {
       init: function(latcenter_in, longcenter_in) {
         latcenter = latcenter_in
         longcenter = longcenter_in
         console.log("NewOfferViewInit")

         $(window).resize(resizeMap)

         $("#submitlocationbutton").on('click', submitLocation);
         $('#newlocationlongitude').on('input', changedCoordinates);
         $('#newlocationlatitude').on('input', changedCoordinates);

         setTimeout(initializeMap, 1000);

         $('#modalnewlocationview').appendTo("body").modal('show');

         $("#newlocationpicture").fileinput({
          //allowedFileExtensions : ['jpg', 'png','gif'],
          dropZoneEnabled: true,
          allowedFileTypes: ['image'],
          showUpload: false,
          });

         $('#modalnewlocationview').on('hidden.bs.modal', function(){UrlMaker.setAddLocation(false)})
         UrlMaker.setAddLocation(true)
         
       }
     }

   })()
   console.log("LocationView")