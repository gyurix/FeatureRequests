const pages = {
    requests: function () {
        this.id = ko.observable('');
        this.title = ko.observable('Title');
        this.desc = ko.observable('Description');
        this.client = ko.observable(0);
        this.priority = ko.observable(0);
        this.date = ko.observable('20180101');
        this.production = ko.observable(0);
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
    productions: function () {
        this.id = ko.observable(0);
        this.name = ko.observable('');
    },
    clients: function () {
        this.id = ko.observable(0);
        this.name = ko.observable('');
    }
};

function updatePriorities() {
    $.get('/api/clients/priorities/' + (model.editor.isActive() ? model.editor.item().id() + '/' : '')
        + model.requests.client.data(), function (data) {
        msgInfo('Priorities', data);
        model.requests.priority.options(JSON.parse(data));
    }).fail(function (data) {
        msgError('Error', data.responseText);
    });
}

function update(form, id) {
    let editPrefix = model.editor.isActive() ? '/edit/' + model.editor.item().id() : '';
    if (form === 'requests' && id === 'client') {
        updateSingle(form, id, updatePriorities, editPrefix);
    }
    else {
        updateSingle(form, id, null, editPrefix);
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
        let page = model.page();
        $.post('/api/' + page + '/submit', JSON.parse(JSON.stringify(model[page])), function (data) {
            let item = JSON.parse(data);
            $('#add-item-modal').modal('hide');
            let model_item = new pages[page]();
            model[page + 'Names']().forEach(k => {
                model_item[k](item[k]);
            });
            model[page + 'Data'].push(model_item);
            if (page === 'requests') {
                data = model.requestsData();
                let len = data.length;
                let id = item.id;
                let client = item.client;
                let priority = item.priority;
                for (let i = 0; i < len; ++i) {
                    d = data[i];
                    if (d.id() !== id && d.client() === client && d.priority() >= priority) {
                        d.priority(parseInt(d.priority()) + 1);
                    }
                }
                updatePriorities();
            }
        }).fail(function (error) {
            msgError('Error!', error.responseText);
        });
    }, 1);
    return false;
}

function edit() {
    setTimeout(function () {
        let page = model.page();
        $.post('/api/' + page + '/edit/' + model.editor.item().id() + '/submit', JSON.parse(JSON.stringify(model[page])), function (data) {
            let item = JSON.parse(data);
            $('#edit-item-modal').modal('hide');
            let old_item = model.editor.item();
            model.editor.item(undefined);
            model.items().splice(model.findItem(old_item.id()), 1);
            let model_item = new pages[page]();
            model[page + 'Names']().forEach(k => {
                model_item[k](item[k]);
            });
            if (page === 'requests') {
                data = model.requestsData();
                let len = data.length;
                let client = item.client;
                let oldclient = old_item.client();
                let oldpriority = old_item.priority();
                let priority = item.priority;
                for (let i = 0; i < len; ++i) {
                    d = data[i];
                    if (d.client() === oldclient && d.priority() > oldpriority) {
                        d.priority(parseInt(d.priority()) - 1);
                    }
                }
                for (let i = 0; i < len; ++i) {
                    d = data[i];
                    if (d.client() === client && d.priority() >= priority) {
                        d.priority(parseInt(d.priority()) + 1);
                    }
                }
                updatePriorities();
            }
            model.items().push(model_item);
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
model.findItem = function (id) {
    items = model.items();
    len = items.length;
    for (let i = 0; i < len; ++i) {
        if (items[i].id() === id) {
            return i;
        }
    }
    return -1;
};
model.itemNames = function () {
    return model[model.page() + 'Names'];
};
model.removeItem = function (item) {
    confirm('Remove ' + model.getNameOrId(item) + '?', function () {
        const items = model.items();
        const index = items.indexOf(item);
        if (index > -1) {
            $.get('/api/' + model.page() + '/remove/' + item.id(), function (data) {
                items.splice(index, 1);
                if (model.page() === 'requests') {
                    data = model.requestsData();
                    let len = data.length;
                    let id = item.id;
                    let client = item.client;
                    let priority = item.priority;
                    for (let i = 0; i < len; ++i) {
                        d = data[i];
                        if (d.client() === client && d.priority() >= priority) {
                            d.priority(parseInt(d.priority()) - 1);
                        }
                    }
                }
            }).fail(function (error) {
                msgError('Error!', error.responseText);
            });
        }
    });
};

model.editItem = function edit(item) {
    let page = model.page();
    model[page + "Names"]().forEach(k => {
        msgInfo('Info', page + ' - ' + k);
        try {
            model[page][k].data(item[k]());
            model[page][k].error.removeAll();
            model[page][k].success('');
        }
        catch (e) {
        }
    });
    /*$.post('/api/' + page + '/edit/' + item().id(), function (data) {
        data.foreach((k, v) => {
            model[page][k].data(v.data);
            model[page][k].success().removeAll();
            model[page][k].error().removeAll();
        });
    });*/
    model.editor.item(item);
};

model.isRendered = function (page) {
    return model.page() === page;
};
model.getName = function (field, id) {
    if (field === 'poster') {
        field = 'user';
    }
    data = model[field + 'sData']();
    let len = data.length;
    for (let i = 0; i < len; ++i) {
        if (data[i].id() === id) {
            return data[i].name();
        }
    }
    return 'Unknown ' + field + ' (' + id + ')';
};
model.getNameOrId = function (item) {
    if (item === undefined)
        return '';
    try {
        item = item()
    }
    catch (e) {
    }
    let name = '#' + item.id();
    try {
        name = item.name();
    }
    catch (e) {
    }
    let page = model.page();
    page = page.substr(0, page.length - 1);
    return page[0].toUpperCase() + page.substr(1) + ' ' + name;
};
model.editor = {
    item: ko.observable(),
    title: function () {
        if (this.item() === undefined)
            return '';
        return 'Edit ' + model.getNameOrId(this.item);
    },
    footer: function () {
        if (this.item() === undefined)
            return '';
        return 'Finish editing ' + model.getNameOrId(this.item);
    },
    isActive: function () {
        return this.item() !== undefined;
    }
};

load_fields();

$(document).ready(function () {
    show_page('requests');
});