/**
 * Copyright (c) 2013.
 *
 * @author Mugur Marculescu
 * @author Sebastian Serrano
 *
 */

// Javascript templates. TODO: move to own file.
function initializeTemplates () {

    JST = {
        task_json_0: {
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
            isToGroup: false,
            isOffer: false,
            sender: "Erin Bajornas",
            recipients: "just you",
            expire: "3h at 7:22pm",
            description: "Wanna get ramen tonight?",
            canForward: false,
            canChange: false,
            tags: ["friend", "food"]
        },

        task: _.template(document.getElementById("task-template").innerText)
    };
}


$(function() {

    initializeTemplates();

    // TESTING: Create a list with template and attach to body.
    $list = $("#main-tasks-list");

    $list.append(JST.task(JST.task_json_1));
    $list.append(JST.task(JST.task_json_0));
    $list.append(JST.task(JST.task_json_3));
    $list.append(JST.task(JST.task_json_2));
});
