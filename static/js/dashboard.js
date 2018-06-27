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