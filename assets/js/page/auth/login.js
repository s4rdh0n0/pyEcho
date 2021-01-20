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
            data: JSON.stringify({ username: $('#username').val(), password: $('#password').val() }),
            headers: { 'X-XSRFToken': $('input[name="_xsrf"]').val() },
            success: (function (result) {
               if (result.status) {
                  window.location.href = result.url;
               } else {
                  $('#password').val('');
                  $.notify({
                     title: '<strong>Perhatian</strong> <br>',
                     message: result.msg,
                     },{
                     type: 'minimalist',
                     template: '<div data-notify="container" class="col-xs-11 col-sm-3 alert alert-{0}" role="alert">' +
                              '<span data-notify="title">{1}</span>' +
                              '<span data-notify="message">{2}</span>' +
                              '</div>',
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