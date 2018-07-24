model.signup = {};
model.login = {};

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

function login() {
    $.post("/api/login/submit", {
        email: model.login.email.data(),
        password: model.login.password.data()
    }, function (data) {
        if (data.indexOf("admin") !== -1) {
            msgSuccess('Warning!', data);
            return
        }
        msgSuccess('Success!', data);
        window.location.href = "/dashboard";
    }).fail(function (error) {
        msgError('Error!', error.responseText);
    })
}

function signup() {
    msgInfo("Signup", "Signing Up...");
    signupForm = model.signup;
    //Only post captcha field if captcha is enabled
    try {
        signupForm = jQuery.extend(model.signup, {"captcha": grecaptcha.getResponse()});
    }
    catch (ignored) {
    }
    $.post("/api/signup/submit", signupForm, function (data) {
        if (data.indexOf('\n') !== -1) {
            msgWarn('Success!', data);
            return;
        }
        msgSuccess('Success!', data);
        window.location.href = "/dashboard";
    }).fail(function (error) {
        msgError('Error!', error.responseText);
    })
}