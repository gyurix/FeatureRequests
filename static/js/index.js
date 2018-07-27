model.signup = {};
model.login = {};

function update(form, id) {
    updateSingle(form, id, function () {
        if (form === 'signup') {
            if (id === 'password' && model[form].repeat_password.data().length > 0) {
                updateSingle(form, 'repeat_password')
            } else if (id === 'repeat_password') {
                updateSingle(form, 'password')
            }
        }
        else if (form === 'login') {
            if (id === 'email' && model[form].password.data().length > 0) {
                updateSingle(form, 'password')
            }
        }
    });
}

function login_now() {
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
    });
    return false;
}

function signup_now() {
    msgInfo("Signup", "Signing Up...");
    signupForm = model.signup;
    //Only post captcha field if captcha is enabled
    try {
        signupForm = jQuery.extend(model.signup, {"captcha": grecaptcha.getResponse()});
    }
    catch (ignored) {
    }
    $.post("/api/signup/submit", JSON.parse(JSON.stringify(signupForm)), function (data) {
        if (data.indexOf('\n') !== -1) {
            msgWarn('Success!', data);
            return;
        }
        msgSuccess('Success!', data);
        window.location.href = "/dashboard";
    }).fail(function (error) {
        msgError('Error!', error.responseText);
    });
    return false;
}
