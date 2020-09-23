+ function ($) {
    'use strict';

    
    /* Initial Form Activation */
    $('#formActivation').validate({
        rules: {
            username: {
                required: true,
            }
        },
        messages: {
            username: {
                required: 'Username tidak boleh kosong.',
            }
        },
        errorElement: "small",
        highlight: function (element, errorClass, validClass) {
            var elem = $(element);
            elem.closest('.form-group').addClass('has-error');
        },
        unhighlight: function (element, errorClass, validClass) {
            var elem = $(element);
            elem.closest('.form-group').removeClass('has-error');
        }, errorPlacement: function (error, element) {
            error.insertAfter('.input-group'); //So i putted it after the .form-group so it will not include to your append/prepend group.
        },
        submitHandler: function (form) {
            $.ajax({
                type: 'POST',
                url: '/administrator/activationuser',
                data: JSON.stringify({
                    username: $('#username').val(),
                }),
                headers: { 'X-XSRFToken': $('input[name="_xsrf"]').val() },
                success: (function (data) {

                    if (data.status){
                        $('#userkkp').load('/administrator/activationuser/username=' + data.username);
                    }else{
                        $.notify({
                            title: '<strong><i class="fa fa-info-circle" aria-hidden="true"></i> Info</strong> <br>',
                            message: data.msg,
                        }, {
                            type: data.type,
                            animate: {
                                enter: 'animated fadeInRight',
                                exit: 'animated fadeOutRight'
                            }
                        });

                        $('#userkkp').empty();
                    }

                }),
                error: (function (XMLHttpRequest, textStatus, errorThrown) {
                    alert("Error: " + errorThrown);
                })
            });
        }

        
    });

}(jQuery);
