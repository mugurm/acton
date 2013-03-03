/**
 * Copyright (c) 2013.
 *
 * @author Mugur Marculescu
 * @author Sebastian Serrano
 *
 */

// Javascript templates. TODO: move to own file.
JST = {
    task_json: {
        offer_amount: "$825",
        sender: "Sebastian Serrano",
        recipients: "you and 2 others",
        expire: "2 weeks",
        description: "We need a new logo for PyCON"
    },

    task: _.template(
        '<div class="task offer">\n' +
            '<div class="task-header">\n' +
                '<div class="task-offer">\n' +
                    '<span class="task-offer-badge">Incentive</span>\n' +
                    '<span class="task-offer-amount"><strong><%= offer_amount %></strong></span>\n' +
                '</div>\n' +
            '</div>\n' +
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

    // TODO: replace body with #main_task_list when that exist.
    $body = $("body");
    $t1 = $(JST.task(JST.task_json));
    $body.append($t1);
});
