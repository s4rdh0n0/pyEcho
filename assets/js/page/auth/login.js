+ function ($) {
   'use strict';

   $('#signin').validate({
      rules: {
         username: {
            required: true
         },
         password: {
            required: true
         },
      }, messages: {
            username: {
               required: 'Username tidak boleh kosong.'
            },
            password: {
               required: 'Password tidak boleh kosong.'
            },
      },
      errorElement: "small",
      highlight: function (element, errorClass, validClass) {
         $(element).parents(".has-feedback").addClass("has-error").removeClass("has-success");
      },
      unhighlight: function (element, errorClass, validClass) {
         $(element).parents(".has-feedback").removeClass("has-error");
      },
      submitHandler: function () {
         $.ajax({
            type: 'POST',
            url: '/login',
            contentType: "application/json",
            data: JSON.stringify({ username: $('#username').val(), password: $('#password').val() }),
            headers: { 'X-XSRFToken': $('input[name="_xsrf"]').val() },
            success: (function (result) {
               if (result.status) {
                  window.location.href = result.url;
               } else {
                  $('#password').val('');
                  $.notify({
                     title: '<strong>Warning!</strong> <br>',
                     message: result.msg,
                     },{
                     type: result.type,
                     animate: {
                        enter: 'animated fadeInRight',
                        exit: 'animated fadeOutRight'
                     }
                  });
               }
            }),
            error: (function (XMLHttpRequest, textStatus, errorThrown) {
               $.notify({
                  title: '<strong>Error!</strong> <br>',
                  message: errorThrown,
                  },{
                  type: "danger",
                  animate: {
                     enter: 'animated fadeInRight',
                     exit: 'animated fadeOutRight'
                  }
               });
            })
         });
      },
   });

}(jQuery);