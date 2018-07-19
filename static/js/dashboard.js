function Request() {
    this.id = ko.observale(0);
    this.title = ko.observale("Title");
    this.desc = ko.observale("Description");
    this.client = ko.observale(0);
    this.priority = ko.observale(0);
    this.date = ko.observale("20180101");
    this.area = ko.observale(0);
    this.poster = ko.observale(0);
    this.created = ko.observale("20180101")
}

function Role() {
    this.id = ko.observable(0);
    this.name = ko.observable("");
    this.enabled = ko.observable(false);
    this.view = ko.observable(false);
    this.add = ko.observable(false);
    this.edit = ko.observable(false);
    this.admin = ko.observable(false);
}

function Client() {
    this.id = ko.observable(0);
    this.name = ko.observable("");
}

function Production() {
    this.id = ko.observable(0);
    this.name = ko.observable("")
}

function User() {
    this.id = ko.observable(0);
    this.name = ko.observable("");
    this.email = ko.observable("");
    this.password = ko.observable("");
    this.role = ko.observable(0);
}

function htmlbodyHeightUpdate() {
    const height3 = $(window).height();
    const height1 = $('.nav').height() + 50;
    const height2 = $('.main').height();
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
    iziToast.info({
        title: "Loading data...",
        message: "Loading page " + page
    });
    $.get("/api/" + page, function (data) {
        iziToast.success({
            title: 'Success!',
            message: 'Loaded data ' + data
        });
        model.items.removeAll();
        items = JSON.parse(data);
        items.forEach(item => {
            const mItem = {};
            Object.keys(item).forEach(k => {
                mItem[k] = ko.observable(item[k]);
            });
            model.items.push(mItem);
        });
        model.page_title(page[0].toUpperCase() + page.substr(1));
    }).fail(function (error) {
        iziToast.error({
            title: 'Error on loading ' + page + " data",
            message: error.status + " - " + JSON.stringify(error.responseText)
        });
    });
}

function logout() {
    iziToast.info({
        title: "Log Out",
        message: "Logging out..."
    });
    $.get("/api/logout", function (msg) {
        alert("Logout");
        iziToast.success({
            title: 'Logged Out',
            message: msg
        });
    }).fail(function (error) {
        iziToast.error({
            title: 'Error on logging out',
            message: error.status + " - " + JSON.stringify(error.responseText)
        });
    })
}

function MainModel() {
    const self = this;
    this.page_title = ko.observable("Loading...");
    this.test = ko.observable("Test succeed");
    this.page_body = ko.observable("<h2>Loading...</h2>");
    this.items = ko.observableArray([]);
    this.hasItems = function () {
        return this.items().length > 0;
    };
    this.hasNoItems = function () {
        return this.items().length === 0;
    };
    this.itemNames = function () {
        if (this.items().length > 0) {
            keys = Object.keys(this.items()[0]);
            return keys;
        }
        return {};
    };

    self.removeItem = function (item) {
        const index = self.items.indexOf(item);
        if (index > -1) {
            self.items.splice(index, 1);
        }
    };

    this.is_rendered = function (page) {
        return this.page_title() === page;
    }
}

const model = new MainModel();

$(document).ready(function () {
    ko.applyBindings(model);
    render_page("users");
});