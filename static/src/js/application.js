/**
 * Copyright (c) 2013.
 *
 * @author Mugur Marculescu
 * @author Sebastian Serrano
 *
 */

// Javascript templates. TODO: move to own file.
function init () {

  // Compile the JS templates.
  JST = {
    task_json_0: {
        isForwarded: false,
        isToGroup: true,
        isOffer: true,
        offer_amount: "$825",
        sender: "Sebastian (Devsar)",
        recipients: "you and 2 others",
        expire: "2 weeks",
        description: "We need a new logo for PyCON.",
        canForward: true,
        canChange: true,
        tags: ["pycon", "work"]
    },

    task_json_1: {
        isForwarded: true,
        isToGroup: false,
        isOffer: false,
        sender: "Sebastian (Devsar)",
        recipients: "you",
        expire: "1 week",
        description: "PyCON 2013 Banner. Can you make sure the printer has all the artwork and answer any other questions they might have?",
        canForward: true,
        canChange: true,
        tags: ["pycon", "work"]
    },

    task_json_2: {
        isForwarded: false,
        isToGroup: false,
        isOffer: false,
        sender: "Sebastian Serrano",
        recipients: "just you",
        expire: "3 days",
        description: "Enough work, let's meet up this weekend!",
        canForward: true,
        canChange: true,
        tags: ["friend"]
    },

    task_json_3: {
        isForwarded: false,
        isToGroup: false,
        isOffer: false,
        sender: "Erin Bajornas",
        recipients: "just you",
        expire: "7:22pm",
        description: "Wanna get ramen tonight?",
        canForward: false,
        canChange: false,
        tags: ["friend", "food"]
    },

    task: _.template(document.getElementById("task-template").innerText)
  };

  Task = Backbone.Model.extend({

  });

  TaskList = Backbone.Collection.extend({
    model: Task,

    url: '/api/v1/task?format=json',

    parse: function(response) {
      return response.objects;
    }
  });

  Tasks = new TaskList();

  TaskView = Backbone.View.extend({

    template: JST.task,

    initialize: function() {
      this.listenTo(this.model, 'change', this.render);
      this.listenTo(this.model, 'destroy', this.remove);
    },
    
    render: function() {
      this.$el.html(this.template(this.model.toJSON()));
      return this;
    }

  });

  CreateTaskView = Backbone.View.extend({
    el: $('#create-task-container'),
    template: JST.task,
    regex_users: /((\+\w[\w\d\-\@]+),?)*/,
    regex_blocks: /(\+\w[\w\d\-\@]+,)* ([^|]+)(|.*)?/,
    regex_expire: /expire:([\d]+)/,
    regex_bounty: /bounty:([\d]+)/,

    initialize: function() {
      console.log("CreateView created");
      this.input = $(".task-input", this.el);
      this.parse_recipients =  $(".recipients", this.el);
      this.parse_description =  $(".description", this.el);
      this.parse_expire =  $(".expire", this.el);
      this.parse_bounty =  $(".bounty", this.el);
      this.val_description = '';
      this.val_users = '';
      this.val_expire = '';
      this.val_bounty = '';
    },

    events: {
      "keyup .task-input": "parse",
    },

    parse: function() {
      var regex_users = this.regex_users.exec(this.input.val())
      var regex_description = this.regex_blocks.exec(this.input.val());
      var regex_expire = this.regex_expire.exec(this.input.val());
      var regex_bounty = this.regex_bounty.exec(this.input.val());

      this.val_description = '';
      this.val_users = '';
      this.val_expire = '';
      this.val_bounty = '';

      if (regex_users[0]) {
        this.val_users = regex_users[0].split(',');
      }
      if (regex_description) {
        this.val_description = regex_description[2];
      }

      if (regex_expire) {
        this.val_expire = regex_expire[1];
        this.val_description = this.val_description.replace(regex_expire[0], '');
      }

      if (regex_bounty) {
        this.val_bounty = regex_bounty[1];
        this.val_description = this.val_description.replace(regex_bounty[0], '');
      }

      this.parse_recipients.html(this.val_users);
      this.parse_description.html(this.val_description);
      this.parse_expire.html(this.val_expire);
      this.parse_bounty.html(this.val_bounty);
    },

    render: function() {
      this.$el.html(this.template(this.model.toJSON()));
      return this;
    }

  });

  AppView = Backbone.View.extend({
    el: $("main-content"),

    initialize: function(){
      this.listenTo(Tasks, 'add', this.addOne);
      this.listenTo(Tasks, 'reset', this.addAll);
      this.listenTo(Tasks, 'all', this.render);
      Tasks.fetch();
      this.create_view = new CreateTaskView()
    },

    addOne: function(task) {
      var view = new TaskView({model: task});
      $("#main-tasks-list").append(view.render().el);
    },

    addAll: function() {
      Tasks.each(this.addOne, this);
    }
  });
}


$(function() {

    init();

    var App = new AppView();
});
