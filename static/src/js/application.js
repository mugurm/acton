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

  AppView = Backbone.View.extend({
    el: $("main-content"),

    initialize: function(){
      this.listenTo(Tasks, 'add', this.addOne);
      this.listenTo(Tasks, 'reset', this.addAll);
      this.listenTo(Tasks, 'all', this.render);
      Tasks.fetch();
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
