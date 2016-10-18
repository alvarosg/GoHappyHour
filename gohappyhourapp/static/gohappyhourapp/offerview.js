   var OfferView = OfferView || (function() {

 
     function handleVoteClick(vote) {
       return function(e) {
         voteClick(e, vote);
       };
     }

     function voteClick(e, vote) {
       if (!Login.token()) {
         Login.popup(handleVoteClick(vote))
         return
       }
       data = {}
       data.value = vote
       $.ajax({
         url: "/api/locations/" + locid + "/offers/" + offerid + "/votes/",
         type: "post",
         data: data,
         headers: {
           "Authorization": "Token " + Login.token()
         },
         dataType: 'json',
         success: votePosted,
         error: voteNotPosted
       });

     }

     function votePosted() {
       OfferView.update()
     }

     function voteNotPosted() {

     }
     
     function commentClick(e) {
       if (!Login.token()) {
         Login.popup(commentClick)
         return
       }
       data = {}
       data.comment = $("#offernewcomment").val()
       $.ajax({
         url: "/api/locations/" + locid + "/offers/" + offerid + "/comments/",
         type: "post",
         data: data,
         headers: {
           "Authorization": "Token " + Login.token()
         },
         dataType: 'json',
         success: commentPosted,
         error: commentNotPosted
       });

     }

     function commentPosted() {
       OfferView.update()
     }

     function commentNotPosted() {

     }
     

     function receivedOffer(data_in) {
       data = data_in
       data.plusvotes = ((data.votes) + (data.score)) / 2
       data.minusvotes = -((data.score) - (data.votes)) / 2
       data.editable = (Login.username()===data.owner)

       $('#offerdiv').html(Handlebars.compile($("#offertemplate").html())(data)).promise().done(showComments);
       $("#offerplusvotes").on('click', handleVoteClick(1));
       $("#offerminusvotes").on('click', handleVoteClick(-1));
       $("#offerdelete").on('click', deleteOffer);
       $("#offersendcomment").on('click', commentClick);
       $('#modalofferview').appendTo("body").modal('show'); 

     }

     function deleteOffer(){
      $.ajax({
         url: "/api/locations/" + locid + "/offers/" + offerid + "/",
         type: "delete",
         data: data,
         headers: {
           "Authorization": "Token " + Login.token()
         },
         dataType: 'json',
         success: offerDeleted,
         error: offerDeleted,
       });
     }

     function offerDeleted(){
       $('#modalnofferview').modal('hide');
       LocationView.update()
     }

     function showComments(e){
      $.getJSON("/api/locations/" + locid + "/offers/" + offerid + "/comments", {
           "format": "json"
         }, receivedComments)
     }

     function receivedComments(data){
      $('#offercomments').html(Handlebars.compile($("#commentstemplate").html())(data));
     }

     var data = null
     var locid = null
     var offerid = null
     return {
       init: function(locid_in, offerid_in) {

         locid = locid_in;
         offerid = offerid_in;
         $.getJSON("/api/locations/" + locid + "/offers/" + offerid + "/detail", {
           "format": "json"
         }, receivedOffer)

         $('#modalofferview').on('hidden.bs.modal', function(){UrlMaker.setOffer(null)})
         UrlMaker.setOffer(offerid)
       },
       update: function() {
         $.getJSON("/api/locations/" + locid + "/offers/" + offerid + "/detail", {
           "format": "json"
         }, receivedOffer)
       },
     }
})() 
console.log("OfferView")