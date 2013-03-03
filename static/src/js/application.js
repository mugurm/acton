/**
 * Copyright (c) 2013.
 *
 * @author Mugur Marculescu
 * @author Sebastian Serrano
 *
 */

// Javascript templates. TODO: move to own file.
JST = {
    task_json_0: {
        isOffer: true,
        offer_amount: "$825",
        sender: "Sebastian (Devsar)",
        recipients: "you and 2 others",
        expire: "2 weeks",
        description: "We need a new logo for PyCON.",
        canForward: true,
        canChange: true
    },

    task_json_1: {
        isOffer: false,
        sender: "Sebastian (Devsar)",
        recipients: "you",
        expire: "1 week",
        description: "PyCON 2013 Banner. Can you make sure the printer has all the artwork and answer any other questions they might have?",
        canForward: true,
        canChange: true
    },

    task_json_2: {
        isOffer: false,
        sender: "Sebastian Serrano",
        recipients: "just you",
        expire: "3 days",
        description: "Enough work, let's meet up this weekend!",
        canForward: true,
        canChange: true
    },

    task_json_3: {
         isOffer: false,
        sender: "Erin Bajornas",
        recipients: "just you",
        expire: "3h at 7:22pm",
        description: "Wanna get ramen tonight?",
        canForward: false,
        canChange: false
    },

    task: _.template(
        '<div class="task <% if(isOffer) { print("offer"); } %>">\n' +
            '<% if( isOffer ) { %>' +
            '<div class="task-header">\n' +
                '<div class="task-offer">\n' +
                    '<span class="task-offer-badge">Incentive</span>\n' +
                    '<span class="task-offer-amount"><strong><%= offer_amount %></strong></span>\n' +
                '</div>\n' +
            '</div>\n' +
            '<% } %>' +
            '<div class="task-info">\n' +
                '<span class="task-sender"><%= sender %></span> to \n' +
                '<span class="task-recipients"><%= recipients %><i class="icon-user"></i></span>\n' +
                '<span class="task-expire pull-right"><%= expire %></span>\n' +
            '</div>\n' +
            '<blockquote class="task-description">\n' +
                '<p><%= description %></p>\n' +
            '</blockquote>\n' +
            '<div class="task-footer clearfix">\n' +
                '<span class="task-tags">\n' +
                    '<span class="label label-important">pycon</span>\n' +
                    '<span class="label label-important">work</span>\n' +
                '</span>\n' +
                '<span class="task-actions pull-right">\n' +
                    '<div class="btn-group">\n' +
                        '<button class="btn btn-mini">Forward <i class="icon-forward"></i></button>\n' +
                    '</div>\n' +
                    '<div class="btn-group">\n' +
                      '<button class="btn btn-mini">Change <i class="icon-pencil"></i></button>\n' +
                      '<button class="btn btn-mini btn-danger">No</button>\n' +
                      '<button class="btn btn-mini btn-success">Yes</button>\n' +
                    '</div>\n' +
                '</span>\n' +
            '</div>\n' +
        '</div>\n'
    )
};


$(function() {

    // TESTING: Create a list with template and attach to body.
    $list = $("#main-tasks-list");
    $t0 = $(JST.task(JST.task_json_0));
    $t1 = $(JST.task(JST.task_json_1));
    $t2 = $(JST.task(JST.task_json_2));
    $t3 = $(JST.task(JST.task_json_3));
    $list.append($t1);
    $list.append($t0);
    $list.append($t3);
    $list.append($t2);
});
