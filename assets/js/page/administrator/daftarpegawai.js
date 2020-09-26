+ function ($) {
    'use strict';

    /* Initial Form Filter */
    $("#formFilter").submit(function (event) {
        event.preventDefault();
        $('#tablePegawai').DataTable().ajax.reload();
    });


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
        submitHandler: function () {
            $.ajax({
                type: 'PUT',
                url: '/administrator/daftarpegawai/pegawai',
                data: JSON.stringify({
                    username: $('#inputUsername').val(),
                }),
                async: false,   
                headers: { 'X-XSRFToken': $('input[name="_xsrf"]').val() },
                success: (function (data) {

                    if (data.status) {
                        $('#userView').load('/administrator/daftarpegawai/pegawai/view/username=' + data.username, function () {

                        });
                    } else {

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
                    }

                }),
                error: (function (XMLHttpRequest, textStatus, errorThrown) {
                    alert("Error: " + errorThrown);
                })
            });
        }

    });

    // NOTE: modal-activation hide
    $('#modal-activation').on('hide.bs.modal', function () {
        tablePegawai.ajax.reload(null, false);
        $('#inputUsername').val("");
        $('#userView').empty();
    });

    // NOTE: modal-role hide
    $('#modal-role').on('hide.bs.modal', function () {
        tablePegawai.ajax.reload(null, false);
        $('#userRole').empty();
    });

    // Role Pegawai
    $('#tablePegawai tbody').on('click', '#btnRolePegawai', function () {
        var selected_row = $(this).parents('tr');
        if (selected_row.hasClass('child')) {
            selected_row = selected_row.prev();
        }

        if (tablePegawai.row(selected_row).data()[0] != "") {
            $('#modal-role').modal('show'); 
            $('#userRole').load('/administrator/daftarpegawai/role/view/userid=' + tablePegawai.row(selected_row).data()['_id'], function () {
                $("#role").select2({
                    placeholder: "Pilih role..",
                    theme: "bootstrap"
                });

                /* Initial Add Role */
                $("#formAddRole").submit(function (event) {
                    event.preventDefault();
                    $.ajax({
                        type: 'PUT',
                        url: '/administrator/daftarpegawai/role/add',
                        data: JSON.stringify({
                            userid: $('input[name=userid]').val(),
                            key: $('#role').val(),
                        }),
                        async: false,   
                        headers: { 'X-XSRFToken': $('input[name="_xsrf"]').val() },
                        success: (function (result) {
                            if (result.status){
                                tableRole.row.add({ "key": result.data.key, "description": result.data.description, "createdate": result.data.createdate}).draw();
                            } else {
                                tableRole.ajax.reload(null, false);
                            }
                        }),
                        error: (function (XMLHttpRequest, textStatus, errorThrown) {
                            alert("Error: " + errorThrown);
                        })
                    });
                });

                // Role Pegawai
                $('#tableRole tbody').on('click', '#btnDeleteRole', function (event) {
                    var selected_row = $(this).parents('tr');
                    if (selected_row.hasClass('child')) {
                        selected_row = selected_row.prev();
                    }

                    if (tableRole.row(selected_row).data()[0] != "") {
                        event.preventDefault();
                        $.ajax({
                            type: 'DELETE',
                            url: '/administrator/daftarpegawai/role/delete',
                            data: JSON.stringify({
                                userid: $('input[name=userid]').val(),
                                key: tableRole.row(selected_row).data()['key']
                            }),
                            async: false,   
                            headers: { 'X-XSRFToken': $('input[name="_xsrf"]').val() },
                            success: (function (data) {
                                if (data.status) {
                                    tableRole.row(selected_row).remove().draw();
                                } else {
                                    tableRole.ajax.reload(null, false);
                                }
                            }),
                            error: (function (XMLHttpRequest, textStatus, errorThrown) {
                                alert("Error: " + errorThrown);
                            })
                        });
                    }
                });

                /* Initial Table Role */
                var tableRole = $('#tableRole').DataTable({
                    'processing': true,
                    'serverSide': true,
                    'ajax': function (data, callback) {
                        $.ajax({
                            type: 'POST',
                            url: '/administrator/daftarpegawai/role',
                            data: JSON.stringify({
                                userid: $('input[name=userid]').val()
                            }),
                            async: true,   
                            headers: { 'X-XSRFToken': $('input[name="_xsrf"]').val() },
                            success: (function (data) {
                                // NOTE: print data
                                console.log(data)

                                // NOTE: callback response ajax
                                callback(data);
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
                            "data": 'key',
                        }, {
                            "targets": [1],
                            "width": "5%",
                            "className": "dt-center text-center",
                            "render": function (data, type, row, meta) {
                                return meta.row + meta.settings._iDisplayStart + 1;
                            }
                        }, {
                            "targets": [2],
                            "width": "70%",
                            "data": 'description',
                            "className": "dt-center text-center",
                        }, {
                            "targets": [3],
                            "width": "20%",
                            "data": 'createdate',
                            "className": "dt-center text-center",
                            "render": function (data) {
                                var date = new Date(data);
                                var month = date.getMonth() + 1;
                                return date.getDate() + "/" + (month.toString().length > 1 ? month : "0" + month) + "/" + date.getFullYear() + "  " + date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds();
                            }
                        }, {
                            "targets": [4],
                            "width": "5%",
                            "className": "dt-center text-center",
                            "render": function () {
                                return '<a id="btnDeleteRole" class="btn btn-danger btn-flat"><i class="fa fa-times" aria-hidden="true"></i></a>';
                            }
                        }
                    ],
                    'responsive': true,
                    'paging': false,
                    'autoWidth': true,
                    'pagingType': 'simple_numbers',
                    'lengthChange': false,
                    'ordering': false,
                    'searching': false,
                    'info': true
                });
            });           
        }
    });

    // Delete Pegawai
    $('#tablePegawai tbody').on('click', '#btnDeletePegawai', function (event) {
        var selected_row = $(this).parents('tr');
        if (selected_row.hasClass('child')) {
            selected_row = selected_row.prev();
        }

        if (tablePegawai.row(selected_row).data()[0] != "") {
            if (confirm('Apakah anda yakin akan menghapus ' + tablePegawai.row(selected_row).data()['nama'] + ' ?')) {
                event.preventDefault();
                $.ajax({
                    type: 'DELETE',
                    url: '/administrator/daftarpegawai/pegawai/delete',
                    data: JSON.stringify({
                        userid: tablePegawai.row(selected_row).data()['_id'],
                    }),
                    async: false,   
                    headers: { 'X-XSRFToken': $('input[name="_xsrf"]').val() },
                    success: (function (data) {
                        if (data.status) {
                            tablePegawai.row(selected_row).remove().draw();
                        } else{
                            tablePegawai.ajax.reload(null, false);
                        }
                    }),
                    error: (function (XMLHttpRequest, textStatus, errorThrown) {
                        alert("Error: " + errorThrown);
                    })
                });
            }
        }
    });

}(jQuery);

/* Initial Loading */
function run_wait(element) {
    $(element).waitMe({
        effect: 'bounce',
        text: 'Harap tunggu...',
        bg: 'rgba(255,255,255,0.6)',
        color: '#000'
    });
}


/* Initial Table Pegawai */
var tablePegawai = $('#tablePegawai').DataTable({
    'processing': true,
    'serverSide': true,
    'ajax': function (data, callback) {
        $.ajax({
            type: 'POST',
            url: '/administrator/daftarpegawai',
            data: JSON.stringify({
                page: $('#tablePegawai').DataTable().page.info()['page'],
                start: $('#tablePegawai').dataTable().fnSettings()._iDisplayStart,
                limit: $('#tablePegawai').dataTable().fnSettings()._iDisplayLength,
                draw: $('#tablePegawai').dataTable().fnSettings().iDraw,
                pegawaiid: $('#inputPegawaiid').val(),
            }),
            async: true,
            headers: { 'X-XSRFToken': $('input[name="_xsrf"]').val() },
            success: (function (data) {
                
                console.log(data);
                
                // NOTE: callback response ajax
                callback(data)
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
        },{
            "targets": [1],
            "width": "5%",
            "className": "dt-center text-center",
            "render": function (data, type, row, meta) {
                return meta.row + meta.settings._iDisplayStart + 1 ;
            }
        },{
            "targets": [2],
            "width": "20%",
            "data": 'pegawaiid',
            "className": "dt-center text-center"
        },{
            "targets": [3],
            "width": "54%",
            "data": 'nama',
            "className": "dt-center text-center"
        },{
            "targets": [4],
            "width": "15%",
            "data": 'createdate',
            "className": "dt-center text-center",
            "render": function (data) {
                var date = new Date(data);
                var month = date.getMonth() + 1;
                return date.getDate() + "/" + (month.toString().length > 1 ? month : "0" + month)  + "/" + date.getFullYear() + "  " + date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds();
            }
        },{
            "targets": [5],
            "width": "3%",
            "render": function () {
                return '<a id="btnDeletePegawai" class="btn btn-danger btn-flat"><i class="fa fa-times" aria-hidden="true"></i></a>';
            }
        },{
            "targets": [6],
            "width": "3%",
            "render": function () {
                return '<a id="btnRolePegawai" class="btn btn-primary btn-flat"><i class="fa fa-universal-access" aria-hidden="true"></i></a>';
            }
        }
    ],
    'responsive': true,
    'paging': true,
    'autoWidth': true,
    'pagingType': 'simple_numbers',
    'lengthChange': false,
    'pageLength': 15,
    'ordering': false,
    'searching': false,
    'info': true
});