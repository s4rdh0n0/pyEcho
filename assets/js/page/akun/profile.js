+ function ($) {
    'use strict';

    $('#formProfile').validate({
        rules: {
            phone: {
                required: true,
            },
            email: {
                required: true,
            }
        },
        messages: {
            phone: {
                required: "Phone tidak boleh kosong.",
            },
            email: {
                required: "Email tidak boleh kosong.",
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
            if (element.parent('.input-group').length) {
                error.insertAfter(element.parent());
            }
            else if (element.prop('type') === 'radio' && element.parent('.radio-inline').length) {
                error.insertAfter(element.parent().parent());
            }
            else if (element.prop('type') === 'checkbox' || element.prop('type') === 'radio') {
                error.appendTo(element.parent().parent());
            }
            else {
                error.insertAfter(element);
            }
        },
        submitHandler: function () {
            $.ajax({
                type: 'POST',
                url: '/akun/profile',
                data: JSON.stringify({
                    email: $('#email').val(),
                    phone: $('#phone').val(),
                }),
                async: true,
                headers: { 'X-XSRFToken': $('input[name="_xsrf"]').val() },
                success: (function (result) {
                    $.notify({
                        title: result.title,
                        message: result.msg,
                    }, {
                        type: result.type,
                        template: '<div data-notify="container" class="col-xs-11 col-sm-3 alert alert-{0}" role="alert">' +
                            '<span data-notify="title">{1}</span>' +
                            '<span data-notify="message">{2}</span>' +
                            '</div>',
                        animate: {
                            enter: 'animated fadeInRight',
                            exit: 'animated fadeOutRight'
                        }
                    });
                }),
                error: (function (XMLHttpRequest, textStatus, errorThrown) {
                    alert("Error: " + errorThrown);
                })
            });
        }
    });

}(jQuery);