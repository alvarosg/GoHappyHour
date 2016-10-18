   var NewOfferView = NewOfferView || (function() {


     var data = null
     var loc_id
     var timerangesnum

     function addTimeRange() {
       var data = {
         ind: timerangesnum
       }
       $('#newoffertimestable').append(Handlebars.compile($("#newtimerangetemplate").html())(data));
       $('#newofferstarttime_'+timerangesnum).datetimepicker({
              format: "HH:mm",
              locale: 'en',
              showClear: true,
              showClose: true,
              /*widgetPositioning: {
                horizontal: 'auto',
                vertical: 'bottom',
             },*/
         });
       $('#newofferendtime_'+timerangesnum).datetimepicker({
              format: "HH:mm",
              locale: 'en',
              showClear: true,
              showClose: true,
              /*widgetPositioning: {
                horizontal: 'auto',
                vertical: 'bottom',
             },*/
         });
       timerangesnum += 1

     }

     function removeTimgeRange() {
       if (timerangesnum > 1) {
         $('#newofferrow_' + (timerangesnum - 1)).remove();
         timerangesnum -= 1
       }
     }

     function submitOffer() {
       var name = $("#newoffername").val()
       var description = $("#newofferdescription").val()
       var picture = $("#newofferpicture").val()
       var expirationdate = $("#newofferexpirationdate").val()

       var missing = ""
       if (!name) {
         missing += "Name "
       }
       if (!description && !picture) {
         missing += "Description or Picture"
       }

       var timestart0 = $("#newofferstarttime_0").val()
       var timeend0 = $("#newofferendtime_0").val()

       if (!timestart0) {
         missing += "Start Time "
       }
       if (!timeend0) {
         missing += "End Time "
       }
       var weekday = false
       for (i = 0; i < 7; i++) {
         if ($("#newoffercheck" + i + "_0").is(":checked")) {
           weekday = true
           break;
         }
       }
       if (!weekday) {
         missing += "Weekday "
       }

       if (missing) {
         window.alert('Missing the following fields: ' + missing)
         return
       } else {
         var data = {
           "name": name,
           "description": description,
         }
         if (expirationdate) {
           data.date_expire = expirationdate
         }
         $.ajax({
           url: "/api/locations/" + locid + "/offers/",
           type: "post",
           data: data,
           headers: {
             "Authorization": "Token " + Login.token()
           },
           dataType: 'json',
           success: offerPosted,
           error: offerNotPosted
         });

       }
     }

     function offerPosted(data) {
       var offerid = data.id


       //Posting the time ranges
       for (i = 0; i < timerangesnum; i++) {
         var timestart = $("#newofferstarttime_" + i).val()
         var timeend = $("#newofferendtime_" + i).val()
         var weekday = false
         var weekdays = ""
         for (j = 0; j < 7; j++) {
           if ($("#newoffercheck" + j + "_" + i).is(":checked")) {
             weekday = true
             weekdays += "1"
           } else {
             weekdays += "0"
           }
         }
         if (timestart && timeend && weekday) {
           $.ajax({
             url: "/api/locations/" + locid + "/offers/" + offerid + "/timeranges/",
             type: "post",
             data: {
               "weekdays": weekdays,
               "time_start": timestart,
               "time_end": timeend,
             },
             headers: {
               "Authorization": "Token " + Login.token()
             },
             dataType: 'json',
             error: timerangeNotPosted,
             success: timerangePosted
           });
         }
       }

       var picture = $("#newofferpicture").val()

       if (picture) {
         file=document.getElementById("newofferpicture").files[0]
         var xhr = new XMLHttpRequest();
         var fd = new FormData();
         fd.append('picture', file);
         xhr.open('post', "/api/locations/" + locid + "/offers/" + offerid + "/pictures/upload", true);
         xhr.setRequestHeader("Authorization", "Token " + Login.token());
         xhr.onreadystatechange = picturePosted 
         xhr.send(fd);

       }
       $('#modalnewofferview').modal('hide');
       LocationView.update()

     }

     function offerNotPosted(data) {
       window.alert('Error posting: are you still logged in?')
     }

     function timerangePosted(data) {
       //LocationView.update()
     }

     function timerangeNotPosted(data) {
       window.alert('Error in one of the timeranges')
     }

     function picturePosted(data) {
       LocationView.update()
     }

     function pictureNotPosted(data) {
       window.alert('Error posting the image')
     }



     return {
       init: function(locid_in) {
         locid = locid_in

         timerangesnum = 0
         addTimeRange();
         

         $("#newofferaddtimerangebutton").on('click', addTimeRange);
         $("#newofferremovetimerangebutton").on('click', removeTimgeRange);
         $("#submitofferbutton").on('click', submitOffer);
         /*
         $('#expirationdate').datepicker({
              format: "yyyy-mm-dd",
              container: "#textnewoffer"
          });
         */
         $('#newofferexpirationdate').datetimepicker({
              format: "YYYY-MM-DD",
              locale: moment.locale(),
              showClear: true,
              showClose: true,
              /*widgetPositioning: {
                horizontal: 'auto',
                vertical: 'bottom',
             },*/
         });
         $("#newofferpicture").fileinput({
          //allowedFileExtensions : ['jpg', 'png','gif'],
          dropZoneEnabled: true,
          allowedFileTypes: ['image'],
          showUpload: false,
          });

         $('#modalnewofferview').appendTo("body").modal('show');
         $('#modalnewofferview').on('hidden.bs.modal', function(){UrlMaker.setAddOffer(false)})
         UrlMaker.setAddOffer(true)

       }
     }

   })()