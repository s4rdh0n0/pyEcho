+ function ($) {
    'use strict';



}(jQuery);

/* Initial Table Pegawai */
var tablePegawai = $('#tablePegawai').DataTable({
    'processing': true,
    "serverSide": true,
    "ajax": function (data, callback) {
        $.ajax({
            type: 'POST',
            url: '/administrator/daftarpegawai',
            data: JSON.stringify({
                page: $('#tablePegawai').DataTable().page.info()['page'],
                start: $('#tablePegawai').dataTable().fnSettings()._iDisplayStart,
                limit: $('#tablePegawai').dataTable().fnSettings()._iDisplayLength,
                draw: $('#tablePegawai').dataTable().fnSettings().iDraw,
            }),
            headers: { 'X-XSRFToken': $('input[name="_xsrf"]').val() },
            success: (function (data) {
                // NOTE: print data
                console.log(data)
                
                // NOTE: callback response ajax
                if (data.status){
                    callback(data);
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
        },
        {
            "targets": [1],
            "width": "3%",
            "render": function () {
                return '<i class="fa fa-user-o" aria-hidden="true"></i>';
            },
        },
        {
            "targets": [2],
            "data": 'pegawaiid',
            "className": "dt-center"
        },
        {
            "targets": [3],
            "visible": false,
            "data": 'username'
        },
        {
            "targets": [4],
            "data": 'nama',
            "className": "dt-center"
        },
        {
            "targets": [5],
            "width": "3%",
            "render": function () {
                return '<a id="lihat" class="btn btn-default btn-flat"><i class="fa fa-info-circle" aria-hidden="true"></i></a>';
            }
        }
    ],
    'responsive': true,
    'paging': true,
    'pagingType': 'simple_numbers',
    'lengthChange': false,
    'pageLength': 4,
    'ordering': false,
    'searching': false,
    'info': true
});