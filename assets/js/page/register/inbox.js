+ function ($) {
    'use strict';

    $("#btnFilterBerkas").click(function () {
        $('#tableBerkas').DataTable().ajax.reload(null, false);
    });

    $("#btnResetFilter").click(function () {
        $('#nomorBerkas').val("");
        $('#tahunBerkas').val("");
        $('#tableBerkas').DataTable().ajax.reload(null, false);
    });

    // NOTE:modal messange hide
    $('#modal-messange').on('hide.bs.modal', function () {
        $('#messange-dialog').empty();
    });


    // NOTE: Info Berkas
    $('#tableBerkas tbody').on('click', '#btnInfo', function (event) {
        var selected_row = $(this).parents('tr');
        if (selected_row.hasClass('child')) {
            selected_row = selected_row.prev();
        }

        if (tableBerkas.row(selected_row).data()[0] != "") {
            $('#modal-messange').modal('show');
            $('#messange-dialog').load('/register/inbox/info/registerid=' + tableBerkas.row(selected_row).data()['_id']);
        }

        return false
    });

    // NOTE: New Messange
    $('#tableBerkas tbody').on('click', '#btnNewMessange', function (event) {
        var selected_row = $(this).parents('tr');
        if (selected_row.hasClass('child')) {
            selected_row = selected_row.prev();
        }

        if (tableBerkas.row(selected_row).data()[0] != "") {
            $('#modal-messange').modal('show');
            $('#messange-dialog').load('/register/inbox/registerid=' + tableBerkas.row(selected_row).data()['_id']);
        }

        return false
    });

}(jQuery);

/* Initial Loading */
function run_wait(element) {
    $(element).waitMe({
        effect: 'bounce',
        text: '<b>Sedang proses...</b> <br> harap tunggu',
        bg: 'rgba(255,255,255,0.6)',
        color: '#000'
    });
}


/* Initial Table Berkas */
var tableBerkas = $('#tableBerkas').DataTable({
    'processing': true,
    'serverSide': true,
    'ajax': function (data, callback) {
        $.ajax({
            type: 'POST',
            url: '/register/inbox',
            data: JSON.stringify({
                nomor: $('#nomorBerkas').val(),
                tahun: $('#tahunBerkas').val(),
                page: $('#tableBerkas').DataTable().page.info()['page'],
                start: $('#tableBerkas').dataTable().fnSettings()._iDisplayStart,
                limit: $('#tableBerkas').dataTable().fnSettings()._iDisplayLength,
                draw: $('#tableBerkas').dataTable().fnSettings().iDraw,
            }),
            async: true,
            headers: { 'X-XSRFToken': $('input[name="_xsrf"]').val() },
            success: (function (data) {
                if (typeof (data.data) == "string") {
                    data.data = JSON.parse(data.data)
                    callback(data)
                } else {
                    callback(data)
                }
            }),
            error: (function (XMLHttpRequest, textStatus, errorThrown) {
                alert("Error: " + errorThrown);
            })
        })
    },
    'columns': [
        {
            "targets": [0],
            "visible": false,
            "data": '_id',
        }, {
            "targets": [1],
            "width": "3%",
            "className": "dt-center text-center",
            "render": function (data, type, row, meta) {
                return meta.row + meta.settings._iDisplayStart + 1;
            }
        }, {
            "targets": [2],
            "width": "10%",
            "data": 'nomorberkas',
            "className": "dt-center text-center"
        }, {
            "targets": [3],
            "width": "10%",
            "data": 'tahunberkas',
            "className": "dt-center text-center",
            "render": function (data) {
                return data.toUpperCase();
            }
        }, {
            "targets": [4],
            "width": "10%",
            "data": 'senddate',
            "className": "dt-center text-center",
            "render": function (data) {
                var date = new Date(data.$date);
                var month = date.getUTCMonth() + 1;
                return (date.getUTCDate().toString().length > 1 ? date.getUTCDate() : "0" + date.getUTCDate()) + "/" + (month.toString().length > 1 ? month : "0" + month) + "/" + date.getUTCFullYear() + "  " + (date.getUTCHours().toString().length > 1 ? date.getUTCHours() : "0" + date.getUTCHours()) + ":" + (date.getUTCMinutes().toString().length > 1 ? date.getUTCMinutes() : "0" + date.getUTCMinutes()) + ":" + (date.getUTCSeconds().toString().length > 1 ? date.getUTCSeconds() : "0" + date.getUTCSeconds());
            }
        },{
            "targets": [6],
            "width": "15%",
            "data": 'sendername',
            "className": "dt-center text-center"
        },{
            "targets": [7],
            "width": "26%",
            "data": 'prosedur',
            "className": "dt-center text-center"
        }, {
            "targets": [8],
            "width": "20%",
            "data": 'receivename',
            "className": "dt-center text-center"
        }, {
            "targets": [9],
            "width": "3%",
            "className": "dt-center text-center",
            "render": function (data) {
                return '<a id="btnNewMessange" class="btn btn-primary btn-flat"><i class="fa fa-envelope-o" aria-hidden="true"></i></a>'
            }
        }, {
            "targets": [10],
            "width": "3%",
            "className": "dt-center text-center",
            "render": function (data) {
                return '<a id="btnInfo" class="btn btn-default btn-flat"><i class="fa fa-info-circle" aria-hidden="true"></i></a>'
            }
        }
    ],
    "oLanguage": {
        "sProcessing": "<b>Sedang proses...</b> <br> harap tunggu"
    },
    'responsive': true,
    'paging': true,
    'autoWidth': true,
    'pagingType': 'simple_numbers',
    'lengthChange': false,
    'pageLength': 20,
    'ordering': false,
    'searching': false,
    'info': true
});