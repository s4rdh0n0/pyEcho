+ function ($) {
    'use strict';

    /* Initial Form Filter */
    $("#formFilter").submit(function (event) {
        event.preventDefault();
        $('#tablePegawai').DataTable().ajax.reload();
    });

    $("#btnResetFilter").click(function (event) {
        $('#inputPegawaiid').val("")
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
                type: 'PUT',
                url: '/administrator/daftarpegawai/pegawai',
                data: JSON.stringify({
                    username: $('#inputUsername').val(),
                }),
                async: false,   
                headers: { 'X-XSRFToken': $('input[name="_xsrf"]').val() },
                beforeSend: function () {
                    $('#userView').empty();
                },
                success: (function (data) {

                    if (data.status) {
                        $('#userView').load('/administrator/daftarpegawai/pegawai/view/username=' + data.username);
                    } else {
                        $('#modal-activation').modal('hide');
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
    });

    // NOTE: modal-activation show
    $('#modal-activation').on('show.bs.modal', function () {
        $('#inputUsername').val("");
        $('#userView').empty();
    });

    // NOTE: modal-role hide
    $('#modal-role').on('hide.bs.modal', function () {
        // tablePegawai.ajax.reload(null, false);
        $('#userRole').empty();
    });

    // Role Pegawai
    $('#tablePegawai tbody').on('click', '#btnRolePegawai', function () {
        var selected_row = $(this).parents('tr');
        if (selected_row.hasClass('child')) {
            selected_row = selected_row.prev();
        }

        if (tablePegawai.row(selected_row).data()[0] != "") { 
            $('#userRole').load('/administrator/daftarpegawai/role/view/userid=' + tablePegawai.row(selected_row).data()['_id'], function () {

                $("#typeRole").select2({
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
                            key: $('#typeRole').val(),
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
                            headers: { 'X-XSRFToken': $('input[name="_xsrf"]').val() },
                            success: (function (data) {
                                // NOTE: print data
                                // console.log(data)

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
                            "data": 'startdate',
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
                                return '<a id="btnDeleteRole" class="btn btn-danger btn-flat"><i class="fa fa-trash" aria-hidden="true"></i></a>';
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
            $('#modal-role').modal('show');
        }
    });

    // Delete Pegawai
    $('#tablePegawai tbody').on('click', '#btnDeAndActivation', function (event) {
        var selected_row = $(this).parents('tr');
        if (selected_row.hasClass('child')) {
            selected_row = selected_row.prev();
        }
        
        if (tablePegawai.row(selected_row).data()[0] != "") {    
            var answer = window.confirm(tablePegawai.row(selected_row).data()['nama'].toUpperCase() + " AKAN DINONAKTIFKAN.....?" );
            if (answer) {
                $.ajax({
                    type: 'PUT',
                    url: '/administrator/daftarpegawai/pegawai/status',
                    data: JSON.stringify({
                        userid: tablePegawai.row(selected_row).data()['_id'],
                    }),
                    async: true,
                    headers: { 'X-XSRFToken': $('input[name="_xsrf"]').val() },
                    error: (function (XMLHttpRequest, textStatus, errorThrown) {
                        alert("Error: " + errorThrown);
                    })
                });

                tablePegawai.ajax.reload();
            }
        }
    });

    
    $('#tablePegawai').on('processing', function (e, processing) {
        e.preventDefault();
        $('#tablePegawai').off('edit');
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
                if (data.status){
                    // NOTE: callback response ajax
                    callback(data)
                }
            }),
            error: (function (XMLHttpRequest, textStatus, errorThrown) {
                alert("Error: " + errorThrown);
            })
        })
    }, 'createdRow': function (row, data, dataIndex) {
        if (data['actived']) {
            $(row).removeClass('strikeout');
        }else{
            $(row).addClass('strikeout');
        }
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
            "width": "51%",
            "data": 'nama',
            "className": "dt-center text-center",
            "render": function (data) {
                return data.toUpperCase();
            }
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
            "data": 'actived',
            "className": "dt-center text-center",
            "render": function (data) {
                if (data) {
                    return '<a id="btnRolePegawai" class="btn btn-primary btn-flat"><i class="fa fa-pencil-square-o" aria-hidden="true"></i></a>'
                }else{
                    return ''
                }
            }
        }, {
            "targets": [6],
            "width": "3%",
            "className": "dt-center text-center",
            "render": function (data, type, row) {
                if (row.actived){
                    return '<a id="btnDeAndActivation" class="btn btn-danger btn-flat btn-small"><i class="fa fa-window-close" aria-hidden="true"></i></a>'
                }else{
                    return ''
                }
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