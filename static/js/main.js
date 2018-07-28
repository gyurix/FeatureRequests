const csrftoken = $('meta[name=csrf-token]').attr('content');

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        }
    }
});
String.prototype.count = function (c) {
    let result = 0, i = 0;
    for (i; i < this.length; i++) if (this[i] === c) result++;
    return result;
};

const model = new function () {
};

function escape(str) {
    return str.replace(/[\x26<>\x20'"]/g, function (r) {
        return "&#" + r.charCodeAt(0) + ";"
    }).replace(/\n/g, '<br>')
}

function Entity(form, id, d, options) {
    if (d === 'False') {
        d = false
    } else if (d === 'True') {
        d = true
    }
    let self = this;
    this.data = ko.observable(d);
    this.data.subscribe(function (old_value) {
        update(form, id);
    });
    this.error = ko.observableArray([]);
    this.errorLen = ko.computed(function () {
        return this.error().length > 0;
    }, this);
    this.success = ko.observable("");
    this.successLen = ko.computed(function () {
        return this.success().length > 0;
    }, this);
    this.options = ko.observable(options);
    this.optionsKeys = function () {
        return Object.keys(self.options());
    };
    this.optionsValue = function (option) {
        return self.options()[option];
    };
    const data = this.data;
    this.toJSON = function () {
        return data();
    }
}

function msg(mode, title, text) {
    iziToast[mode]({
        title: title,
        titleLineHeight: (text.count('\n') + 1) * 16,
        message: escape(text)
    })
}

function msgSuccess(title = 'Success!', text) {
    msg('success', title, text)
}

function msgError(title = 'Error!', text) {
    msg('error', title, text)
}

function msgWarn(title = 'Warning!', text) {
    msg('warning', title, text)
}

function msgInfo(title, text) {
    iziToast.info({
        title: title,
        titleLineHeight: (text.count('\n') + 1) * 16,
        message: escape(text)
    });
}

function confirm(title, callback) {
    const confirmModal =
        $('<div class="modal fade" tabindex="-1" role="dialog" aria-hidden="true">' +
            '<div class="modal-dialog modal-md">' +
            '<div class="modal-content">' +
            '<div class="modal-header">' +
            '<h4 class="modal-title">' + escape(title) + '</h4>' +
            '<button class="close" data-dismiss="modal">' +
            '<span aria-hidden="true">×</span>' +
            '</button>' +
            '</div>' +
            '<div class="modal-footer">' +
            '<a href="#" class="btn btn-outline-danger" data-dismiss="modal">No</a>' +
            '<a href="#" id="okButton" class="btn btn-success">Yes</a>' +
            '</div></div></div></div>');

    confirmModal.find('#okButton').click(function () {
        callback();
        confirmModal.modal('hide');
    });
    confirmModal.modal('show');
}

function updateSingle(form, id, after = null, editPrefix = '') {
    let value = model[form][id].data();
    if (value === undefined)
        return;
    $.post("/api/" + form + editPrefix + "/" + id, {value: value}, function (data) {
        model[form][id].success(data);
        model[form][id].error.removeAll();
    }).fail(function (data) {
        model[form][id].success("");
        model[form][id].error(data.responseText.split("\n"));
    }).done(after)
}

function update(form, id) {
    updateSingle(form, id);
}

$(document).ready(function () {
    ko.applyBindings(model);
    $(".dtpick").datepicker({dateFormat: 'yy-mm-dd'});
});