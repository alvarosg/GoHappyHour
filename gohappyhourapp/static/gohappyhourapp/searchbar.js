   var SearchBar = SearchBar || (function() {

     function handleLocationClick(locid) {
       return function(e) {
         locationClick(e, locid);
       };
     }

     function handlePlaceClick(placeid) {
       return function(e) {
         placeClick(e, placeid);
       };
     }

     function handleLocationHoverEnter(lat, long, name) {
       return function(e) {
         MapView.extraMarker(lat, long, name)
       };
     }

     function handleLocationHoverLeave() {
       return function(e) {
         MapView.extraMarkerReset()
       };
     }

     function locationClick(event, locid) {
       $.get("/static/gohappyhourapp/locationview.html", function(template, textStatus, jqXhr) {
         $('#containerlocationview').html(template)
         LocationView.init(locid);

       });
     }

     function placeClick(event, placeid) {
       if (Login.token()) {

         $.ajax({
           url: "/api/locations/addgoogleplace",
           type: "post",
           data: {
             "placeid": placeid
           },
           headers: {
             "Authorization": "Token " + Login.token()
           },
           dataType: 'json',
           success: placePosted
         });
       } else {
         window.alert("You must be authenticated to add locations")
       }
     }

     function placePosted(data) {
       $("#placeresults").text("");
       $("#searchresults").text("");
       SearchChanged()
       locationClick(0, data.id)
     }


     function SearchChanged() {
       textsearch = $("#searchbox").val()
       previousplaces = null

       if (textsearch != "" || 2 > 1) {
         searching = true

         var notoffernow = $("#notoffernowcheck").is(":checked")
         var alllocations = $("#alllocationscheck").is(":checked")
         var offernow
         if (alllocations) {
           offernow = 'none'
         } else {
           if (notoffernow) {
             offernow = 'anytime'
           } else {
             offernow = 'yes'
           }
         }

         $.getJSON("/api/locations/search", {
           "lat1": lat1,
           "lat2": lat2,
           "long1": long1,
           "long2": long2,
           "name": textsearch,
           "page_size": 10,
           "offernow": offernow,
           "format": "json"
         }, receivedLocationListSearch)
         $("#searchoptions").addClass("hidden")
         $("#searchoptions").removeClass("show")
       } else {
         emptySearchList()
         searching = false
         $("#searchendresult").text("");
         $("#searchendplace").text("");
       }
     }

     function hideResults() {
       emptySearchList()
       $("#searchendresult").text("");
       $("#searchendplace").text("");
       searching = false
       $("#searchoptions").addClass("show")
       $("#searchoptions").removeClass("hidden")
     }

     function emptySearchBox() {
       $("#searchbox").val("");
       textsearch = ""
       emptySearchList()
       searching = false
       move(0)
       $("#searchbox").focus();
     }

     function emptySearchList() {
       $("#searchresults").text("");
       $("#placeresults").text("");
     }

     function requestPlaces(number, tokennext) {
       nextshowplaces = number
       var requestnum
       if (!previousplaces) {
         requestnum = number
       } else {
         requestnum = number - previousplaces.length
       }

       if (requestnum > 0) {
         if (tokennext) {
           $.getJSON("/api/locations/searchplaces", {
             "minresults": requestnum,
             "tokennext": tokennext,
             "format": "json"
           }, receivedPlaces)
         } else {
           $.getJSON("/api/locations/searchplaces", {
             "lat1": lat1,
             "lat2": lat2,
             "long1": long1,
             "long2": long2,
             "name": textsearch,
             "minresults": requestnum,
             "format": "json"
           }, receivedPlaces)
         }
       } else {
         var data = {}
         data.results = []
         data.count = 0
         data.tokennext = tokennext
         receivedPlaces(data)
       }
     }

     function receivedPlaces(data) {
       if (searching == false) {
         return
       }
       var countprevious = 0
       if (previousplaces) {
         countprevious = previousplaces.length
       }
       var countreceived = data.results.length
       var countavailable = countprevious + countreceived

       var placestoshow = Math.min(nextshowplaces, countavailable);

       var addmanuallyoption = false;
       var seemoreoption = false
       var finaltext = ""
       if (placestoshow > 1) {

         finaltext = 'Displaying ' + placestoshow + ' new places.'
         if ((countavailable - placestoshow) > 0 || data.tokennext) {
           seemoreoption = true
         } else {
           addmanuallyoption = true
         }

       } else if (placestoshow == 1) {
         finaltext = "Displaying 1 new place."
         if ((countavailable - placestoshow) > 0 || data.tokennext) {
           seemoreoption = true
         } else {
           addmanuallyoption = true
         }
       } else {
         //$("#placeresults").text("");
         //return
         addmanuallyoption = true
       }

       if (seemoreoption) {
         finaltext = finaltext + ' See more.'
       } else if (addmanuallyoption) {
         finaltext = finaltext + ' Add another.'
       }

       var datashow = {}
       datashow.finaltext = finaltext
       if (placestoshow > 0) {
         if (countprevious >= placestoshow) {
           datashow.results = previousplaces.slice(0, placestoshow);
           previousplaces = previousplaces.slice(placestoshow);
         } else if (previousplaces) {
           datashow.results = previousplaces.concat(data.results.slice(0, placestoshow - countprevious))
           previousplaces = data.results.slice(placestoshow - countprevious)
         } else {
           datashow.results = data.results.slice(0, placestoshow)
           previousplaces = data.results.slice(placestoshow)
         }
       }


       $('#placeresults').html(Handlebars.compile($("#placebuttonstemplate").html())(datashow));
       if (placestoshow > 0) {
         for (i = 0; i < datashow.results.length; i++) {
           $('#placeresult' + i).on('click', handlePlaceClick(datashow.results[i].placeid));
           $('#placeresult' + i).mouseenter(handleLocationHoverEnter(datashow.results[i].latitude, datashow.results[i].longitude, datashow.results[i].name))
           $('#placeresult' + i).mouseleave(handleLocationHoverLeave());

         }
       }

       if (seemoreoption) {
         $("#placecount").on('click', function() {
           $('#searchresults').text("");
           requestPlaces(RESULTS_PER_SEARCH, data.tokennext)
         });
       } else if (addmanuallyoption) {
         $("#placecount").on('click',addNewLocation );
       }
     }

     function addNewLocation(){
        if (Login.token()){
           $.get("/static/gohappyhourapp/newlocationview.html", function(template, textStatus, jqXhr) {
             $('#containernewlocation').html(template).promise().done(function() {
               NewLocationView.init(latcenter, longcenter);
             });
           });
       }
       else{
        Login.popup(addNewLocation);
       }
     }

     function receivedLocationListSearch(data) {
       emptySearchList()
       if (searching == false) {
         return
       }
       data.countreceived = data.results.length
       if (data.count == 0) {
         data.finaltext = "No Results Found. New Search."
       } else if (data.count == 1) {
         data.finaltext = 'Displaying ' + data.countreceived + ' of ' + data.count + ' results.'
       } else {
         data.finaltext = 'Displaying ' + data.countreceived + ' of ' + data.count + ' results.'
         if (data.next) {
           data.finaltext = data.finaltext + " See more."
         } else if (!data.next && data.countreceived == RESULTS_PER_SEARCH && $("#alllocationscheck").is(":checked")) {
           data.finaltext = data.finaltext + " Find more places."
         }
       }
       $('#searchresults').html(Handlebars.compile($("#locationbuttonstemplate").html())(data));

       for (i = 0; i < data.results.length; i++) {
         $('#searchresult' + i).on('click', handleLocationClick(data.results[i].id));
         $('#searchresult' + i).mouseenter(handleLocationHoverEnter(data.results[i].latitude, data.results[i].longitude, data.results[i].name))
         $('#searchresult' + i).mouseleave(handleLocationHoverLeave());

       }
       if (data.countreceived == 0) {
         $("#resultcount").on('click', emptySearchBox);
       } else if (data.next) {
         $("#resultcount").on('click', function() {
           $.getJSON(data.next, receivedLocationListSearch)
         });

       }


       if ($("#alllocationscheck").is(":checked")) {
         if (data.results.length < RESULTS_PER_SEARCH) {
           requestPlaces(RESULTS_PER_SEARCH - data.results.length, null)
         } else if (!data.next && data.countreceived == RESULTS_PER_SEARCH) {
           $("#resultcount").on('click', function() {
             $('#searchresults').text("");
             requestPlaces(RESULTS_PER_SEARCH, null)
           });
         }
       }
     }
     var RESULTS_PER_SEARCH = 10

     var textsearch = ""
     var lat1, lat2, long1, long2, latcenter, longcenter

     var searching = false

     var previousplaces = null
     var nextshowplaces = 0

     return {
       init: function() {

         $('#searchbox').on('input', SearchChanged);
         $('#searchbox').on('click', SearchChanged);

         /*$(document).mouseup(function(e) {
           var clocation = $("#containernewlocation");
           var clogin = $("#containerlogin");

           if (e.target.id != clocation.attr('id') && !clocation.has(e.target).length && e.target.id != clogin.attr('id') && !clogin.has(e.target).length) {

           }
         });*/

         var locid = $("meta[name='locid']").attr('content');
         if (locid) {
           locationClick(0, locid)
           $("meta[name='locid']").replaceWith("")
         }

         var locoption=$("meta[name='locoption']").attr('content'); 
         if (locoption==="add"){
            setTimeout(addNewLocation, 200);
            $("meta[name='locoption']").replaceWith("")
            } 
       },

       openlocation: function(locid) {
         locationClick(0, locid)
       },

       setcoordinates: function(lat1_in, lat2_in, long1_in, long2_in) {
         lat1 = lat1_in
         lat2 = lat2_in
         long1 = long1_in
         long2 = long2_in
         latcenter = (lat2 + lat1) / 2
         if (long2 > long1) {
           longcenter = (long2 + long1) / 2
         } else {
           longcenter = (long2 + 360 + long1) / 2
           if (longcenter > 180) {
             longcenter = longcenter - 360
           }
         }
       },

       hideresults: function() {
         hideResults()
       }
     }

   })()