/**
 * Copyright (c) 2013.
 *
 * @author Mugur Marculescu
 * @author Sebastian Serrano
 *
 */

// Javascript templates.
function init () {

  // Compile the JS templates.
  JST = {
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

    // DOM is ready and therefore we can compile templates.
    init();

    var App = new AppView();
});
