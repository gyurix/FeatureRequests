const csrftoken = $('meta[name=csrf-token]').attr('content');

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        }
    }
});

const model = new function () {
};

function escape(str) {
    return str.replace(/[\x26<>'"]/g, function (r) {
        return "&#" + r.charCodeAt(0) + ";"
    }).replace("\n", "<br><br>")
}

function Entity(form, id, d) {
    this.data = ko.observable(d);
    this.data.subscribe(function (value) {
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
    const data = this.data;
    this.toJSON = function () {
        return data();
    }
}

function msgSuccess(title, text) {
    iziToast.success({
        title: title,
        message: escape(text.replace("\n", "<br>"))
    });
}

function msgError(title, text) {
    iziToast.error({
        title: title,
        message: escape(text)
    });
}

function msgInfo(title, text) {
    iziToast.info({
        title: title,
        message: escape(text)
    });
}

function updateSingle(form, id) {
    $.post("/api/" + form + "/" + id, {value: model[form][id].data()}, function (data) {
        model[form][id].success(data);
        model[form][id].error.removeAll();
    }).fail(function (data) {
        model[form][id].success("");
        model[form][id].error(data.responseText.split("\n"));
    });
}

function update(form, id) {
    updateSingle(form, id);
}

$(document).ready(function () {
    ko.applyBindings(model);
});