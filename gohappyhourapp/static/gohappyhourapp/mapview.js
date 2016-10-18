   var MapView = MapView || (function() {

     function initializeMap() {

       lat_in = $("meta[name='latitude']").attr('content');
       long_in = $("meta[name='longitude']").attr('content');
       zoom_in = $("meta[name='zoom']").attr('content');
       var zoom

       if (lat_in && long_in) {
         latitude = parseFloat(lat_in)
         longitude = parseFloat(long_in)
       }

       if (zoom_in) {
         zoom = parseFloat(zoom_in)
       } else {
         if (lat_in && long_in) {
           zoom = 12
         } else {
           zoom = 2
         }
       }

       var centerposition = new google.maps.LatLng(latitude, longitude)
       var mapCanvas = document.getElementById('map-canvas');
       var mapOptions = {
         center: centerposition,
         zoom: zoom,
         mapTypeId: google.maps.MapTypeId.ROADMAP,
         mapTypeControl: true,
         overviewMapControl: true,
         zoomControl:true,
       }
       map = new google.maps.Map(mapCanvas, mapOptions)
       google.maps.event.addListener(map, 'idle', move);
       if (!(lat_in && long_in) && navigator.geolocation) {
         browserSupportFlag = true;
         latitude =
           navigator.geolocation.getCurrentPosition(function(position) {
             latitude = position.coords.latitude
             longitude = position.coords.longitude
             var centerposition = new google.maps.LatLng(latitude, longitude)
             map.setCenter(centerposition);
             if (!zoom_in) {
               zoom = 14
             }
             map.setZoom(zoom);

           }, function() {});
       }
       onResize()



     }

     function move(event) {
       var bounds = map.getBounds();
       var offernow = 'anytime'

       var center = map.getCenter();
       latitude = center.lat()
       longitude = center.lng()
       zoom = map.getZoom()

       UrlMaker.setCoordinates(latitude, longitude, zoom)
       SearchBar.setcoordinates(bounds.getNorthEast().lat(), bounds.getSouthWest().lat(), bounds.getSouthWest().lng(), bounds.getNorthEast().lng())
       if (zoom<14){
         var hbins=15
         var mapwidth = parseFloat($('#map-canvas').css('width'));
         var mapheight = parseFloat($('#map-canvas').css('height'));
         var vbins=Math.ceil(hbins*mapheight/mapwidth)
         $.getJSON("/api/locations/distribution", {
           "lat1": bounds.getSouthWest().lat(),
           "lat2": bounds.getNorthEast().lat(),
           "long1": bounds.getSouthWest().lng(),
           "long2": bounds.getNorthEast().lng(),
           "latbins":vbins,
           "longbins":hbins,
           "offernow": offernow,
           "format": "json"
         }, receivedLocationDistributionMap)
       }
       else{
         $.getJSON("/api/locations/search", {
           "lat1": bounds.getSouthWest().lat(),
           "lat2": bounds.getNorthEast().lat(),
           "long1": bounds.getSouthWest().lng(),
           "long2": bounds.getNorthEast().lng(),
           "page_size": 100,
           "offernow": offernow,
           "format": "json"
         }, receivedLocationListMap)
       }
       
     }


     function receivedLocationListMap(data) {

       newlist = [];
       for (i = 0; i < data.results.length; i++) {
         var item = data.results[i]

         newlist.push(printMarkerLocation(item));
         if (i === 100) {
           break;
         }
       }

       DeleteMarkers();
       markers = newlist;
       newlist = []
     }

     function printMarkerLocation(locationData){
         var iconbasepath = "/static/gohappyhourapp/icons/"
         if (locationData.offernow) {
           var iconpath = iconbasepath + 'measle_big_red.png'
         } else {
           var iconpath = iconbasepath + 'measle_big_blue.png'
         }
         var markerIcon = {
              url: iconpath, // url
              scaledSize: new google.maps.Size(14,14), // scaled size
              origin: new google.maps.Point(0,0), // origin
              anchor: new google.maps.Point(7, 7) // anchor
          };
         var marker = new google.maps.Marker({
           position: new google.maps.LatLng(locationData.latitude, locationData.longitude),
           map: map,
           title: locationData.name,
           icon: markerIcon,
           zIndex: 0,
         });

         google.maps.event.addListener(marker, 'click', handleLocationClick(locationData.id));
       return marker
     }

     function receivedLocationDistributionMap(data) {

       newlist = [];
       for (i = 0; i < data.results.length; i++) {
         var item = data.results[i]
         if (item.count==1){          
           newlist.push(printMarkerLocation(item));
         }
         else{
           newlist.push(printMarkerDistribution(item));
         }
         
       }

       DeleteMarkers();
       markers = newlist;
       newlist = []
     }

     function printMarkerDistribution(data){
         var iconbasepath = "/static/gohappyhourapp/icons/"

         var iconpath = iconbasepath + 'bigredcircle.png'

         function CalculateSizeMarker(count){
            var minsize=30;
            var maxsize=80;
            var qfactor=0.02;
            return minsize + (maxsize-minsize)*(Math.atan(qfactor*(count-1)))/(Math.PI/2);

         }

         var size=CalculateSizeMarker(data.count)
         var labelfontsize=size*0.4
         var digits=(data.count + '').length
         var labelwidth=2*labelfontsize*digits

         var markerIcon = {
              url: iconpath, // url
              scaledSize: new google.maps.Size(size,size), // scaled size
              origin: new google.maps.Point(0,0), // origin
              anchor: new google.maps.Point(size/2, size/2) // anchor
          };

         var marker = new MarkerWithLabel({
           position: new google.maps.LatLng(data.latitude, data.longitude),
           raiseOnDrag: true,
           map: map,
           labelContent: data.count + "",
           labelAnchor: new google.maps.Point(labelwidth/2, labelfontsize/2+2),
           title: data.count + " locations",
           icon: markerIcon,
           zIndex: 0,
           labelClass: "distributionmarkerlabel", // the CSS class for the label
           labelStyle: {"font-size": labelfontsize+"px", "width": labelwidth+"px" }
         });

         google.maps.event.addListener(marker, 'click', handleDistributionClick(map.getZoom()+2,data.latitude, data.longitude));

         return marker

     }

     function handleLocationClick(locid) {
       return function(e) {
         SearchBar.openlocation(locid)
       };
     }

     function handleDistributionClick(zoom,latitude,longitude) {
       return function(e) {
         var centerposition = new google.maps.LatLng(latitude, longitude)
         map.setCenter(centerposition);
         map.setZoom(zoom);
       };
     }

     function DeleteMarkers() {
       //Loop through all the markers and remove
       for (var i = 0; i < markers.length; i++) {
         markers[i].setMap(null);
       }
       markers = []
     }

     function initializeSearch() {
       $.get("/static/gohappyhourapp/searchbar.html", function(template, textStatus, jqXhr) {
         $('#positionsearch').html(template)
         SearchBar.init();
         if (map){
           var bounds = map.getBounds();
           if (bounds) {
             SearchBar.setcoordinates(bounds.getNorthEast().lat(), bounds.getSouthWest().lat(), bounds.getSouthWest().lng(), bounds.getNorthEast().lng())
           }
         }

         $(document).mouseup(function(e) {
           var csearch = $("#positionsearch");
           var clogin = $("#positionlogin");

           if (e.target.id != csearch.attr('id') && !csearch.has(e.target).length && e.target.id != clogin.attr('id') && !clogin.has(e.target).length) {
             SearchBar.hideresults()
           }
         });


       });
     }

     function initializeLogin() {
       $.get("/static/gohappyhourapp/login.html", function(template, textStatus, jqXhr) {
         $('#positionlogin').html(template)
         Login.init();
       });
     }

     var waitForFinalEvent = function() {
       var b = {};
       return function(c, d, a) {
         a || (a = "I'm a banana!");
         b[a] && clearTimeout(b[a]);
         b[a] = setTimeout(c, d)
       }
     }();

     function isBreakpoint(alias) {
       $el = $('<div>');
       $el.appendTo($('body'));
       $el.addClass('hidden-' + alias);
       var returnvalue = $el.is(':hidden')
       $el.remove();
       return returnvalue
     }


     function onResize() {
       waitForFinalEvent(function() {
         var size
         if (isBreakpoint('xs')) {
           var mapOptions = {
             streetViewControl: false,
             mapTypeControlOptions: {
               position: google.maps.ControlPosition.RIGHT_BOTTOM,
             },
             panControl:false,
             overviewMapControlOptions: {
               opened: false,
             },
             zoomControlOptions:{
              style:google.maps.ZoomControlStyle.SMALL,
              position:google.maps.ControlPosition.LEFT_BOTTOM,
             }
           }
           size='xs'
         } else {
           var mapOptions = {
             streetViewControl: true,
             mapTypeControlOptions: {
               position: google.maps.ControlPosition.RIGHT_TOP,
             },
             panControl:true,
             overviewMapControlOptions: {
               opened: true,
             },
             zoomControlOptions:{
              style:google.maps.ZoomControlStyle.LARGE,
              position:google.maps.ControlPosition.TOP_LEFT,
             }
           }
           size='other'
         }
          if (size!=prevsize){
            map.setOptions(mapOptions)
            prevsize=size;
          }
          map.setCenter(new google.maps.LatLng(latitude, longitude))

       }, 300, new Date().getTime())
     }



     var markers = []
     var latitude = 40;
     var longitude = 0;
     var selectionmarker = null
     var prevsize = null
     var map = null

     return {
       init: function() {
         var locale = window.navigator.userLanguage || window.navigator.language;
         moment.locale(locale)

         initializeSearch()
         initializeLogin()
         google.maps.event.addDomListener(window, 'load', initializeMap);
         $(window).resize(onResize)

       },

       extraMarker: function(lat, long, name) {
         if (selectionmarker) {
           selectionmarker.setMap(null);
         }

         selectionmarker = new google.maps.Marker({
           position: new google.maps.LatLng(lat, long),
           map: map,
           title: name,
           zIndex: 1,
         });

       },
       extraMarkerReset: function() {
         if (selectionmarker) {
           selectionmarker.setMap(null);
         }
         selectionmarker = null

       },


     }

   })()
   $(document).ready(function() {
     MapView.init();
   });