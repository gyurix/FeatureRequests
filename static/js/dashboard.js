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
        title: "Loading...",
        message: "Loading page " + page
    });
    $.get("/page/" + page, function (data) {
        iziToast.success({
            title: 'Success!',
            message: 'Loaded page ' + page
        });
        model.page_title(page);
        model.page_body(data);
    }).fail(function (error) {
        iziToast.error({
            title: 'Error',
            message: error.status + " - " + error.responseText
        });
    });
}

function MainModel() {
    this.page_title = ko.observable("Loading...");
    this.page_body = ko.observable("<h2>Loading...</h2>");
    this.is_rendered = function (page) {
        return this.page_title() === page;
    }
}

const model = new MainModel();

$(document).ready(function () {
    ko.applyBindings(model);
    render_page("requests");
});