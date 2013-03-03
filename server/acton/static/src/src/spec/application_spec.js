describe("Acton app", function() {
  var container;

  beforeEach(function() {
    container = $("#spec_container");
    $("body").append(container);
  });

  afterEach(function() {
    container.remove();
  });

  it("can run jasmine tests.", function() {
    expect(true).toBeTruthy();    
  });

  describe("task templates", function() {
    var $task;

    beforeEach(function() {
      $task = $(JST.task(JST.task_json));    
    });

    afterEach(function() {
      $task.remove();
      $task = null;
    });
    
    it("can create a task element.", function() {
      
      expect(JST).toBeDefined();
      expect(JST.task).toBeDefined();

      expect($task).toContain(".task-header");
      expect($task).toContain(".task-offer");
      expect($task).toContain(".task-footer");
      expect($task).toContain(".task-actions");
      expect($task).toContain(".task-description");
    });

    it("can be attached to body.", function() {
      $("body").append($task);
      expect($("body")).toContain(".task");
    });

  });

});