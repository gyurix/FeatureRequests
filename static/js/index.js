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

function Entity(data) {
    this.data = ko.observable(data);
    this.error = ko.observableArray([]);
    this.errorLen = ko.computed(function () {
        return this.error().length > 0;
    }, this);
    this.success = ko.observable("");
    this.successLen = ko.computed(function () {
        return this.success().length > 0;
    }, this)
}

function SignupForm() {
    this.username = new Entity("");
    this.email = new Entity("");
    this.password = new Entity("");
    this.repeat_password = new Entity("")
}

function LoginForm() {
    this.email = new Entity("Email");
    this.password = new Entity("Password")
}

const model = new BaseModel();
ko.applyBindings(model);

function update(form, id) {
    if (form === "signup") {
        if (id === 'password' && $("#" + form + "_repeat_password").val().length > 0) {
            updateSingle(form, 'repeat_password');
        } else if (id === 'repeat_password') {
            updateSingle(form, 'password');
        }
    }
    updateSingle(form, id);
}

function updateSingle(form, id) {
    let data = $("#" + form + "_" + id).val();
    $.post("/api/" + form + "/" + id, {value: data}, function (data) {
        model[form][id].success(data);
        model[form][id].error.removeAll();
    }).fail(function (data) {
        model[form][id].success("");
        model[form][id].error(data.responseText.split("\n"));
    });
}

function login() {
    $.post("/api/login/submit", {value: data}, function (data) {
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
    $.post("/api/signup/submit", {value: data}, function (data) {
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