   var UrlMaker = UrlMaker || (function() {

     
     var latitude = null;
     var longitude = null;
     var zoom = null;
     var locid = null;
     var offerid = null;
     var addoffer = null;
     var addlocation = null;

     function updateUrl(){
        var url="/"
        var title="Go-HappyHour.com"
        if (locid){
          url=url+"locations/"+locid+"/"
        
          if (offerid){
            url=url+"offers/"+offerid+"/"
          }
          else if (addoffer){
            url=url+"offers/add"
          }
        }
        else if (addlocation){
          url=url+"locations/add"
        }
        if (latitude && longitude && zoom){
          url=url+"?lat="+latitude+"&long="+longitude+"&zoom="+zoom
        }
        window.history.pushState(null, "Go-HappyHour.com", url);
     }



     return {
       setCoordinates: function(lat_in,long_in,zoom_in) {
          latitude=lat_in
          longitude=long_in
          zoom=zoom_in
          updateUrl()

       },

       setLocation: function(locid_in){
          locid=locid_in
          updateUrl()
       },

       setAddLocation: function(addlocation_in){
          addlocation=addlocation_in
          updateUrl()
       },

       setOffer: function(offerid_in){
          offerid=offerid_in
          updateUrl()
       },

       setAddOffer: function(addoffer_in){
          addoffer=addoffer_in
          updateUrl()
       },
     }

   })()