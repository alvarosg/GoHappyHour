   var LocationView = LocationView || (function() {

     function initializeMap() {
       resizeMap()
       var mapCanvas = document.getElementById("map-location-canvas");
       var mapOptions = {
         center: new google.maps.LatLng(data.latitude, data.longitude),
         zoom: 15,
         mapTypeId: google.maps.MapTypeId.ROADMAP
       }

       mapLocation = new google.maps.Map(mapCanvas, mapOptions)

       marker = new google.maps.Marker({
         position: new google.maps.LatLng(data.latitude, data.longitude),
         map: mapLocation,
         title: data.name,
       });
     }



     function receivedLocation(data_in) {
       data = data_in
       
       $('#locationdiv').html(Handlebars.compile($("#locationtemplate").html())(data));
       for (i = 0; i < data.offers.length; i++) {
         $('#offerbutton' + i).on('click', handleOfferClick(data.offers[i].id));
       }
       $("#addofferbutton").on('click', addNewOffer);
       $("#picturesbutton").on('click', showPictures);
       $('#modallocationview').appendTo("body").modal('show');
      
       setTimeout(initializeMap, 1000);

       var offerid = $("meta[name='offerid']").attr('content');
       if (offerid) {
         offerClick(0, offerid)
         $("meta[name='offerid']").replaceWith("")
       }

       var offeroption = $("meta[name='offeroption']").attr('content');
       if (offeroption === "add") {
         addNewOffer()
         $("meta[name='offeroption']").replaceWith("")
       }

     }

     function handleOfferClick(offerid) {
       return function(e) {
         offerClick(e, offerid);
       };
     }

     function offerClick(e, offerid) {


       $.get("/static/gohappyhourapp/offerview.html", function(template, textStatus, jqXhr) {
         $('#containerofferview').html(template)
         OfferView.init(locid, offerid);
       });
     }

     function addNewOffer() {
       if (Login.token()){
         $.get("/static/gohappyhourapp/newofferview.html", function(template, textStatus, jqXhr) {
           $('#containernewoffer').html(template)
           NewOfferView.init(locid);
         });
       }
       else{
        Login.popup(addNewOffer);
       }

     }

     function showPictures() {
       $.get("/api/locations/"+data.id+"/externalpictures", function(data_in) {
         $('#containerlocationimage').html(Handlebars.compile($("#picturescarouseltemplate").html())(data_in)).promise();
       });

     }

     function resizeMap() {
       mapwidth = $('#map-location-canvas').css('width');
       mapheight = mapwidth
       $('#map-location-canvas').css('height', mapheight)

       if (mapLocation){
          mapLocation.setCenter(new google.maps.LatLng(data.latitude, data.longitude))
       }
     };

     var data = null
     var mapLocation = null
     var marker = null
     var locid
     return {
       init: function(locid_in) {

         locid = locid_in;
         $.getJSON("/api/locations/" + locid + "/detail", {
           "format": "json"
         }, receivedLocation)

         $(window).resize(resizeMap)


         

         $('#modallocationview').on('hidden.bs.modal', function(){UrlMaker.setLocation(null)})
         UrlMaker.setLocation(locid)
         


       },
       update: function() {
         $.getJSON("/api/locations/" + locid + "/detail", {
           "format": "json"
         }, receivedLocation)
       }
     }

   })()