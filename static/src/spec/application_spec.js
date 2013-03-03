describe("Acton app", function() {
  var container;

  beforeEach(function() {
    container = $("#spec_container");
    $("body").append(container);
    window.initializeTemplates();

  });

  afterEach(function() {
    container.remove();
  });

  it("can run jasmine tests.", function() {
    expect(true).toBeTruthy();
  });

  describe("task templates", function() {
    var $incentiveTask;

    beforeEach(function() {
      $("body").append(JST.task(JST.task_json_0));
      expect($("body")).toContain(".task");
      $incentiveTask = $(".task");
    });

    afterEach(function() {
      $incentiveTask.remove();
      $incentiveTask = null;
    });
    
    it("can create a task element.", function() {
      
      expect(JST).toBeDefined();
      expect(JST.task).toBeDefined();

      expect($incentiveTask).toContain(".task-header");
      expect($incentiveTask).toContain(".task-offer");
      expect($incentiveTask).toContain(".task-footer");
      expect($incentiveTask).toContain(".task-actions");
      expect($incentiveTask).toContain(".task-description");
    });

  });

});