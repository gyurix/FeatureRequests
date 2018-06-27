var csrftoken = $('meta[name=csrf-token]').attr('content');

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        }
    }
});

function BaseModel() {
    this.signup = new SignupForm();
    this.login = new LoginForm();
}

function Entity(form, id, data) {
    this.data = ko.observable(data);
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

    this.toJSON = function () {
        return data();
    }
}

function SignupForm() {
}

function LoginForm() {
}

const model = new BaseModel();

function update(form, id) {
    if (form === "signup") {
        if (id === 'password' && model[form].repeat_password.data().length > 0) {
            updateSingle(form, 'repeat_password');
        } else if (id === 'repeat_password') {
            updateSingle(form, 'password');
        }
    }
    updateSingle(form, id);
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

function login() {
    $.post("/api/login/submit", {value: model[form][id].data}, function (data) {
        iziToast.success({
            title: 'Success!',
            message: data
        });
    }).fail(function (error) {
        iziToast.error({
            title: 'Error!',
            message: error.responseText
        });
    })
}

function signup() {
    iziToast.info({
        message: "Signing up..."
    });
    $.post("/api/signup/submit", {value: JSON.stringify(model.signup)}, function (data) {
        iziToast.success({
            title: 'Success!',
            message: data
        });
        $.get("/dashboard", function (data) {
            ko.cleanNode();
            $("#contentBody").innerHTML = data;
        });
    }).fail(function (error) {
        iziToast.error({
            title: 'Error!',
            message: error.responseText
        });
    })
}

$(document).ready(function () {
    ko.applyBindings(model);
});