+ function ($) {
    'use strict';

    $("#tmplpasswordlama").on("change", function () {
        $(this).is(":checked") ? $("#passwordlama").attr("type", "text") : $("#passwordlama").attr("type", "password");
    });

    $("#tmplpasswordbaru").on("change", function () {
        $(this).is(":checked") ? $("#passwordbaru").attr("type", "text") : $("#passwordbaru").attr("type", "password");
    });

    $("#tmplulangpasswordbaru").on("change", function () {
        $(this).is(":checked") ? $("#ulangpasswordbaru").attr("type", "text") : $("#ulangpasswordbaru").attr("type", "password");
    });
}(jQuery);