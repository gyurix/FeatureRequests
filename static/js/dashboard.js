const pages = {
    requests: function () {
        this.id = ko.observable('');
        this.title = ko.observable('Title');
        this.desc = ko.observable('Description');
        this.client = ko.observable(0);
        this.priority = ko.observable(0);
        this.date = ko.observable('20180101');
        this.area = ko.observable(0);
        this.poster = ko.observable(0);
        this.created = ko.observable('20180101');
    },
    roles: function () {
        this.id = ko.observable(0);
        this.name = ko.observable('');
        this.enabled = ko.observable(false);
        this.view = ko.observable(false);
        this.add = ko.observable(false);
        this.edit = ko.observable(false);
        this.admin = ko.observable(false);
    },
    users: function () {
        this.id = ko.observable(0);
        this.name = ko.observable('');
        this.email = ko.observable('');
        this.role = ko.observable(0);
    },
    production: function () {
        this.id = ko.observable(0);
        this.name = ko.observable('');
    },
    clients: function () {
        this.id = ko.observable(0);
        this.name = ko.observable('');
    }
};

function update(form, id) {
    if (form === 'requests' && id === 'client') {
        msgInfo('Info', 'Update - ' + form + ' - ' + id);
        updateSingle(form, id, function () {
            msgInfo('Updating', 'Updating priorities... ' + model[form].client.data());
            $.get('/api/clients/priorities/' + model[form].client.data(), function (data) {
                let priorities = model[form].priority.options;
                priorities.removeAll();
                len = data.length;
                for (let i = 0; i < len; ++i) {
                    priorities.push(data[i]);
                }
                msgSuccess('Done', 'Updated priorities to ' + JSON.stringify(data));
            }).fail(function (data) {
                msgError('Error', data.responseText);
            });
        })
    }
}


function htmlBodyHeightUpdate() {
    const height1 = $('.nav').height() + 50;
    const height2 = $('.main').height();
    const height3 = $(window).height();
    if (height2 > height3) {
        $('html').height(Math.max(height1, height3, height2) + 10);
        $('body').height(Math.max(height1, height3, height2) + 10);
    }
    else {
        $('html').height(Math.max(height1, height3, height2));
        $('body').height(Math.max(height1, height3, height2));
    }
}

function render_page(page) {
    load_page(page, false);
}

function add() {
    setTimeout(function () {
        let elementName = model.page_title();
        elementName = elementName.charAt(elementName.length - 1) === 's' ? elementName.substr(0, elementName.length - 1) : elementName;
        elementName[0] = elementName[0].toUpperCase();
        let page = model.page();
        $.post('/api/' + page + '/submit', JSON.parse(JSON.stringify(model[page])), function (data) {
            let item = JSON.parse(data);
            $('#modal').modal('hide');
            let model_item = new pages[page]();
            model[page + 'Names']().forEach(k => {
                model_item[k](item[k]);
            });
            model[page + 'Data'].push(model_item);
            msgSuccess('Added!', 'Added ' + elementName + ' #' + item['id'] + ' - ' + item['name']);
        }).fail(function (error) {
            msgError('Error!', error.responseText);
        });
    }, 1);
    return false;
}

function load_fields() {
    Object.keys(pages).forEach(page => {
        model[page] = {};
        model[page + 'Data'] = ko.observableArray([]);
        model[page + 'Names'] = ko.observableArray(Object.keys(new pages[page]()));
        load_page(page);
    });
}

function load_page(page) {
    $.get('/api/' + page, function (data) {
        let items = JSON.parse(data);
        model[page + 'Data'].removeAll();
        items.forEach(item => {
            let model_item = new pages[page]();
            model[page + 'Names']().forEach(k => {
                model_item[k](item[k]);
            });
            model[page + 'Data'].push(model_item);
        });
    }).fail(function (error) {
        msgError('Error on loading ' + page + ' data', error.status + ' - ' + JSON.stringify(error.responseText));
    });
}

function show_page(page) {
    model.page(page);
    model.page_title(page[0].toUpperCase() + page.substr(1));
}

function logout() {
    msgInfo('Logout', 'Logging out...');
    $.get('/api/logout', function (msg) {
        msgSuccess('Logged out', msg);
        window.location.href = '/dashboard';
    }).fail(function (error) {
        msgError('Error on logging out', error.status + ' - ' + error.responseText);
    })
}

model.page_title = ko.observable('Loading...');
model.page = ko.observable('requests');
model.items = function () {
    return model[model.page() + 'Data'];
};
model.itemNames = function () {
    return model[model.page() + 'Names'];
};
model.removeItem = function (item) {
    const items = model.items();
    const index = items.indexOf(item);
    if (index > -1) {
        $.get('/api/' + model.page() + '/remove/' + item.id(), function (data) {
            items.splice(index, 1);
        }).fail(function (error) {
            msgError('Error!', error.responseText);
        });
    }
};
model.isRendered = function (page) {
    return model.page() === page;
};
model.getRoleName = function (id) {
    roles = model.rolesData();
    let len = roles.length;
    for (let i = 0; i < len; ++i) {
        if (roles[i].id() === id) {
            return roles[i].name();
        }
    }
    return 'Unknown role (' + id + ')';
};

load_fields();

$(document).ready(function () {
    show_page('users');
});