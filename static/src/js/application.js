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
    url: '/api/v1/task/',
    
    defaults: function() {
      return {
        description: "no description...",
        can_change: false,
        can_forward: false,
        expire: "2014-03-03T23:28:49",
        is_offer: false,
        bounty: 0,
        is_to_group: false,
        archived: false,
        status: "PE"
      };
    },

    respond : function(accepted){
      $.ajax({
        dataType: "json",
        url: this.id + "respond/",
        data: {
          accepted: accepted
        },
        success: function(data) {
          app.fetchFilteredTasks();
        }
      });
    }
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

    events: {
      "click .task-actions .btn.yes": "handleButtonClick",
      "click .task-actions .btn.no": "handleButtonClick"
    },

    initialize: function() {
      this.listenTo(this.model, 'change', this.render);
      this.listenTo(this.model, 'destroy', this.remove);
    },
    
    render: function() {
      this.$el.html(this.template(this.model.toJSON()));
      return this;
    },

    handleButtonClick : function(e){
      this.model.respond($(e.target).hasClass("yes"));
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
      "keypress .task-input": "create"
    },

    parse: function() {
      var regex_users = this.regex_users.exec(this.input.val());
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
      this.parse_expire.html("Expires in " + this.val_expire + " days.");
      this.parse_bounty.html("$" + this.val_bounty);

      if (!this.val_users) {
        this.$(".task-preview").hide(250);
      } else {
        this.$(".task-preview").show(250);
      }

      if (!this.val_bounty) {
        this.$(".bounty").fadeOut(250);
      } else {
        this.$(".bounty").fadeIn(250);
      }

      if (!this.val_expire) {
        this.$(".expire").fadeOut(250);
      } else {
        this.$(".expire").fadeIn(250);
      }
    },

    create: function(e) {
      if (e.keyCode != 13) return;
      if (this.val_users == '' || this.val_description == '') return;
      
      var data = {
        description: this.val_description,
        users: this.val_users
      };

      if (this.val_expire != '') {
        data['expire'] = this.val_expire;
      }

      if (this.val_bounty != '') {
        data['bounty'] = this.val_bounty;
      }

      var task = new Task(data);
      task.save();
      this.input.val('');

      e.preventDefault();
      this.parse();
      
    }

  });

  App = Backbone.Model.extend({
    defaults: function(){
      return {
        filter: "inbox"
      };
    },

    fetchFilteredTasks : function(){
        Tasks.fetch({data:
        {
          filter: app.get("filter")
        }
      });
    }
  });

  AppView = Backbone.View.extend({
    el: $("#main-content"),

    events: {
      "click #tasks-nav a": "handleFilterChange"
    },

    initialize: function(){
      this.model.on('change', this.render, this);

      this.listenTo(Tasks, 'add', this.addOne);
      this.listenTo(Tasks, 'reset', this.addAll);
      this.listenTo(Tasks, 'all', this.render);
      this.model.fetchFilteredTasks();
      this.create_view = new CreateTaskView();
    },

    render : function(){
      // Update filter nav visuals
      this.$("#tasks-nav li").removeClass("active");
      this.$("#tasks-nav li a[data-filter='" + this.model.get("filter") + "']").parent().addClass("active");
    },

    handleFilterChange : function(e){
      var $a = $(e.currentTarget);
      var filter = $a.data('filter');
      app.set("filter", filter);
      router.navigate("/inbox/" + filter, {trigger:true});
      this.model.fetchFilteredTasks();
    },

    addOne: function(task) {
      var view = new TaskView({model: task});
      $("#main-tasks-list").append(view.render().el);
    },

    addAll: function() {
      if (Tasks.length > 0) {
        $("#main-tasks-list").html("");
      } else {
        $("#main-tasks-list").html("<p class='lead'>There are no tasks in this category.</p>");
      }
      Tasks.each(this.addOne, this);
    }
  });

  AppRouter = Backbone.Router.extend({
    routes: {
      "/inbox/:view_filter": "setViewFilter"
    },

    setViewFilter: function(view_filter) {
      console.log("vf", view_filter);
    }
  });
}


$(function() {

    // DOM is ready and therefore we can compile templates.
    init();

    app = new App();
    appView = new AppView({model: app});
    router = new AppRouter();

    var enablePushState = true;

    // Disable for older browsers
    var pushState = !!(enablePushState && window.history && window.history.pushState);
    Backbone.history.start({ pushState: pushState });

    router.navigate("/inbox/inbox", {trigger: true});
});
