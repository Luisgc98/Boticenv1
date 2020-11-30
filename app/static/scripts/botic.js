var BotIc = {
    bots: [],
    errorShown: false,
    i18nAttrName: 'data-i18n-error',
    msg_html: $("<div class='alert alert-warning' role='alert'> " +
                    "<strong id='msg-text'></strong>" + 
                    "<button type='button' class='close' data-dismiss='alert' aria-label='Close'> " +
                        "<span aria-hidden='true'>&times;</span>"+
                    "</button>"+
                "</div>"),
    show_message: function(message){
        BotIc.clear_messages();
        BotIc.msg_html.find("#msg-text").html(message).show();
        $("#custom_messages").append(BotIc.msg_html);
    },

    clear_messages: function(){
        var msg = BotIc.msg_html.find("#msg-text").text();
        if ('' !== msg || undefined !== msg){
            $("#custom_messages").html("");
        }
    }
}
$(document).ready(function(){
    configureLoader();
    bindValidatesPasswordMatch();
    bindCustomEvents();
    bindBotsRefreshEvent();
    bindTasksRefreshEvent();
    bindPlayTaskEvent();
    bindOnBotClickEvent();
    bindDeleteTaskEvent();
    bindCustomizeConfirmDeleteTaskDialog();
    bindCustomizeScheduleTaskDialog();
    bindScheduleTaskEvent();
    bindScheduleOptionsChangeEvent();
    bindCustomizeTaskDetailsDialog();
});

function cleanBorderClassTo(element){
    if (element.hasClass("border-danger")){
        element.removeClass("border").removeClass("border-danger");
    }
}

function bindValidatesPasswordMatch(){
    $("#password").keyup(function(){
        setTimeout(function(){
            var pass =  $("#password").val();
            var confPass =  $("#conf-password").val();
            if ( pass && confPass ){
                if (pass !== confPass){
                    if (BotIc.errorShown === false){
                        var msg = $("#register-section").attr(BotIc.i18nAttrName);
                        BotIc.show_message(msg);
                        $("#password").addClass("border border-danger");
                        $("#conf-password").addClass("border border-danger");
                        BotIc.errorShown = true;
                    }
                }else{
                    BotIc.clear_messages();
                    BotIc.errorShown = false;
                    cleanBorderClassTo($("#password"));
                    cleanBorderClassTo($("#conf-password"));
                }
            }
        },1000);
    });
    $("#conf-password").keyup(function(){
        setTimeout(function(){
            var pass =  $("#password").val();
            var confPass =  $("#conf-password").val();
            if ( pass && confPass ){
                if (pass !== confPass){
                    if (BotIc.errorShown === false){
                        var msg = $("#register-section").attr(BotIc.i18nAttrName);
                        BotIc.show_message(msg);
                        $("#conf-password").addClass("border border-danger");
                        $("#password").addClass("border border-danger");
                        BotIc.errorShown = true;
                    }
                }else{
                    BotIc.clear_messages();
                    BotIc.errorShown = false;
                    cleanBorderClassTo($("#password"));
                    cleanBorderClassTo($("#conf-password"));
                }
            }
        }, 1000); 
    });
}

function bindCustomEvents(){
    $(document).bind("refreshBots",function(ev, data){
        var page = 1;
        if ( data !== undefined ){
            page = data.page;
        }

        $.get("/bots/"+ page,function(data){
            $(".b__bots__data").html($(data).find(".b__bots__data").html());
            $("#bots-pagination").html($(data).find("#bots-pagination").html());
            bindOnBotClickEvent();
            BotIc.bots = [];
        });
    });

    $(document).bind("findBots",function(ev,data){
        var page = 1;
        var q = "";
        if ( data !== undefined ){
            page = data.page;
            q = data.q;
        }

        $.get("/bots/"+ page + "?q="+q,function(data){
            $(".b__bots__data").html($(data).find(".b__bots__data").html());
            $("#bots-pagination").html($(data).find("#bots-pagination").html());
            bindOnBotClickEvent();
            BotIc.bots = [];
        });
    });

    $(document).bind("retrieveTasks",function(ev,data){
        var page = 1;
        var q = "";
        var bot_id;
        if ( data !== undefined ){
            page = data.page;
            q = data.q;
            bot_id = data.bot_id;
        }

        var url = "/tasks/"+page;
        if (q){
            url += "?q="+q;
        }
        if ( bot_id !== undefined && bot_id !== "" ){
            url = '/bot/' + bot_id + '/tasks/'+ page + "?q="+q;
        }
        $.get(url,function(data){
            $("#task-container").html($(data).find("#task-container").html());
            bindPlayTaskEvent();
            bindCustomizeConfirmDeleteTaskDialog();
            bindCustomizeScheduleTaskDialog();
            bindScheduleTaskEvent();
            bindScheduleOptionsChangeEvent();
        });
    });

    $(document).bind("playTask",function(ev,data){
        var jsonData = {
            bots: BotIc.bots
        };
        $.ajax({
            url: "/task/"+data.task_id,
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(jsonData),
            success: function(data){
                BotIc.show_message(data);
            }
        });
    });

    $(document).bind("deleteTask",function(ev,data){
        var bot_id = data.bot_id;
        var url = "/task/"+data.task_id;
        if (bot_id !== undefined && bot_id !== ""){
            url = '/bot/' + bot_id + '/task/' + data.task_id;
        }
        $.ajax({
            url: url,
            type: "PATCH",
            success: function(data){
                BotIc.show_message(data);
                $(".modal-backdrop").remove();
                $("body").removeClass("modal-open");
                $(document).trigger("retrieveTasks", {
                    bot_id: bot_id,
                    q: $("#tasks-search").val(),
                    page: $("#tasks-current-page").text()
                });
            }
        });
    });

    $(document).bind('taskDetails',function(ev,data){
        var taskId = 0;
        if (data){
            taskId = data.taskId;
        }
        $.get("/task/"+ taskId,function(data){
            $("#task-det-cntr").html($(data).find("#task-det-cntr").html());
            bindRefreshScheduleTasksEvent();
            bindDeleteScheduledJob();
            bindTaskExecDetailsRefreshEvent();
            flask_moment_render_all();
        });
    });

    $(document).bind('refreshTaskScheduleDetails',function(ev,data){
        var taskId = 0;
        var page = 1;
        if (data){
            taskId = data.taskId;
            page = data.page;
        }
        $.get("/task/"+ taskId + '/schedules/'+ page,function(data){
            $("#schedules_container").html($(data).find("#schedules_container").html());
            bindDeleteScheduledJob();
        });
    });

    $(document).bind("retrieveExecutionDetails",function(ev, data){
        var page = 1;
        var q = "";
        var task_id;
        if ( data !== undefined ){
            page = data.page;
            q = data.q;
            task_id = data.task_id;
        }
        if (!page){
            page = 1;
        }
        var url = "/tasks/" + task_id + "/executions/" + page;
        if (q){
            url += '?q='+q;
        }

        $.get(url,function(data){
            $("#task-det-cntr").find("tbody").html($(data).find("tbody").html());
            $("#task-det-cntr").find("#exec-details-pagination")
                .html($(data).find("#exec-details-pagination").html());
            flask_moment_render_all();
        });
    });
}

function bindOnBotClickEvent(){
    $("#bots_container").on("click","#select-bot",function(ev){
        BotIc.clear_messages();
        var element = $(ev.target);
        var bot_secret = element.data('bot-secret');
        var is_checked = element.is(':checked');
        if (is_checked){
            if (!BotIc.bots.includes(bot_secret)){
                BotIc.bots.push(bot_secret);
            }
        }else{
            if (BotIc.bots.includes(bot_secret)){
                BotIc.bots.pop(bot_secret);
            }
        }
    });
}

function bindBotsRefreshEvent(){
    $("#btn-bot-refresh").click(function(ev){
        ev.preventDefault();
        $(document).trigger("refreshBots");
    });
}

function bindTasksRefreshEvent(){
    $("#btn-task-refresh").click(function(ev){
        ev.preventDefault();
        var bot_id = $("#bot-id").val();
        var page = $("#tasks-current-page").text();
        $(document).trigger("retrieveTasks", {bot_id: bot_id, page: page});
    });
}

function bindTaskExecDetailsRefreshEvent(){
    $("#btn-task-exec-refresh").click(function(ev){
        ev.preventDefault();
        var task_id = $("#task_id_det").val();
        var page = $("#exec-details-current-page").text();
        $(document).trigger("retrieveExecutionDetails", {task_id: task_id, page: page});
    });
}

function bindPlayTaskEvent(){
    $("body").on("click","#play-task",function(ev){
        ev.preventDefault();
        BotIc.clear_messages();
        bot_secret = $("#bot-secret").val();
        if (bot_secret !== undefined && bot_secret !== ""){
            if (BotIc.bots.indexOf(bot_secret) < 0){
                BotIc.bots.push(bot_secret);
            }
        }
        if(BotIc.bots.length > 0){
            $(document).trigger("playTask",{
                task_id: $(ev.target).data("task-id")
            });
        }else{
            var msg = $(ev.target).attr(BotIc.i18nAttrName);
            if (msg === undefined){
                msg = $(ev.target).parent().attr(BotIc.i18nAttrName);
            }
            BotIc.show_message(msg);
        }
    });
}

function bindDeleteTaskEvent(){
    $("body").on("click","#delete-task",function(ev){
        ev.preventDefault();
        var button = $(ev.target);
        var bot_id = button.data('from-bot');
        BotIc.clear_messages();
        $(document).trigger("deleteTask",{
            task_id: $("#confirm-delete").find("#taskId").val(),
            bot_id: bot_id
        });
    });
}

function bindCustomizeConfirmDeleteTaskDialog(){
    $('#confirm-delete').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget); // Button that triggered the modal
        var taskName = button.data('task-name'); // Extract info from data-* attributes
        var modal = $(this);
        var modal_title = modal.find('.modal-title');
        var base_text = modal_title.data('i18n-text');
        var taskId = button.data('task-id');
        modal.find('#taskId').val(taskId);
        modal.find('.modal-title').text(base_text + " '"+ taskName + "'");
    });
}

function bindCustomizeScheduleTaskDialog(){
    $('#schedule-dialog').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget); // Button that triggered the modal
        var taskName = button.data('task-name'); // Extract info from data-* attributes
        var modal = $(this);
        var modal_title = modal.find('.modal-title');
        var base_text = modal_title.data('i18n-text');
        var taskId = button.data('task-id');
        modal.find('#scheduled_task_id').val(taskId);
        modal.find('#bots_comma_list').val(BotIc.bots.join(','));
        modal.find('.modal-title').text(base_text + " '"+ taskName + "'");
    });
}

function bindCustomizeTaskDetailsDialog(){
    $('#task-details-dialog').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget); // Button that triggered the modal
        var modal = $(this);
        var modal_title = modal.find('.modal-title');
        var base_text = modal_title.data('i18n-text');
        var taskId = button.data('task-id');
        $(document).trigger('taskDetails',{
            taskId: taskId
        });
        modal.find('.modal-title').text(base_text);
        flask_moment_render_all();
    });
}

function configureLoader(){
    $(document).ajaxSend(function(){
        $('#loader').fadeIn(250);
    });
    $(document).ajaxComplete(function(){
        $('#loader').fadeOut(250);
    });
};

function handleTasksPagination(page){
    var bot_id = $("#bot-id").val();
    var task_filter = $("#tasks-search").val();
    if (task_filter !== ""){
        $(document).trigger("retrieveTasks",{
            q: task_filter,
            page: page,
            bot_id: $("#bot-id").val()
        });
    }else{
        $(document).trigger("retrieveTasks", {bot_id: bot_id, page: page});
    }
}

function handleBotsPagination(page){
    var bots_filter = $("#bots-search").val();
    if (bots_filter !== ""){
        $(document).trigger("findBots",{
            q: bots_filter,
            page: page
        });
    }else{
        $(document).trigger("refreshBots", {page: page});
    }
}

function handleTasksExecDetailsSearch(ev){
    if(ev.which === 13){
        var task_id = $("#task_id_det").val();
        $(document).trigger("retrieveExecutionDetails",{
            q: $(ev.target).val(),
            page: 1,
            task_id: task_id
        });
    }
}

function handleExecDetailsPagination(page){
    var task_id = $("#task_id_det").val();
    $(document).trigger("retrieveExecutionDetails", {
        page: page,
        task_id: task_id
    });
}

function handleTasksSearch(ev){
    if(ev.which === 13){
        $(document).trigger("retrieveTasks",{
            q: $(ev.target).val(),
            page: 1,
            bot_id: $("#bot-id").val()
        });
    }
}

function handleBotsSearch(ev){
    if(ev.which === 13){
        $(document).trigger("findBots",{
            q: $(ev.target).val(),
            page: 1
        });
    }
}

function bindScheduleTaskEvent(){
    $("#schedule-btn").click(function(ev){
        var bot_id = $("#bot-id").val();
        var message = $(ev.target).data('i18n-error-text');
        if ((bot_id === undefined || bot_id === '') 
            && BotIc.bots.length === 0){
            alert(message);
            ev.preventDefault();
            return;
        }else{
            console.log("pass to main function");
        }
    });
}

function toggleElement(element, show){
    if (element){
        if (show){
            element.removeClass('hidden');
        }else{
            element.addClass('hidden');
        }
    }
}

function bindScheduleOptionsChangeEvent(){
    $("#periodicity-container").on('click', 'input',function(ev){
        var option_value = $(this).val();
        var on_day_elmnt = $("#on_day_cntr");
        var on_month_elmnt = $("#on_month_cntr");
        var at_hour_elmnt = $("#at_hour_cntr");
        switch(option_value){
            case 'MINUTE':
                toggleElement(on_day_elmnt,false);
                toggleElement(on_month_elmnt,false);
                toggleElement(at_hour_elmnt,false);
                break;
            case 'HOUR':
                toggleElement(on_day_elmnt,false);
                toggleElement(on_month_elmnt,false);
                toggleElement(at_hour_elmnt,false);
                break;
            case 'DAY':
                toggleElement(on_day_elmnt,false);
                toggleElement(on_month_elmnt,false);
                toggleElement(at_hour_elmnt,true);
                break;
            case 'WEEK':
                toggleElement(on_day_elmnt,false);
                toggleElement(on_month_elmnt,false);
                toggleElement(at_hour_elmnt,true);
                break;
            case 'MONTHLY':
                toggleElement(on_day_elmnt,true);
                toggleElement(on_month_elmnt,false);
                toggleElement(at_hour_elmnt,true);
                break;
            case 'YEARLY':
                toggleElement(on_day_elmnt,true);
                toggleElement(on_month_elmnt,true);
                toggleElement(at_hour_elmnt,true);
                break;
        }
    });
}

function bindDeleteScheduledJob(){
    $("#schedules_container").on('click',"#del-sch-task",function(ev){
        ev.preventDefault();
        var job_sch_id = $(ev.target).data('sch-id');
        var task_id = $(ev.target).data('task-id');
        var page = $("#sch_tasks-current-page").text();
        var url = "/schedules/"+job_sch_id;
        $.ajax({
            url: url,
            type: "PATCH",
            success: function(data){
                BotIc.show_message(data);
                $(".modal-backdrop").remove();
                $("body").removeClass("modal-open");
                $(document).trigger("refreshTaskScheduleDetails", {taskId: task_id, page: page});
                var count = $("#div_task_sch_"+ task_id).find("div").text();
                if (count){
                    count = parseInt(count);
                    count = count - 1;
                }
                if (count <= 0){
                    $("#div_task_sch_"+ task_id).find("div").addClass('hidden');
                }else{
                    $("#div_task_sch_"+ task_id).find("div").text(count);
                }
            }
        });
    });
}

function bindRefreshScheduleTasksEvent(){
    $("#btn-sch-task-refresh").click(function(ev){
        var page = $("#sch_tasks-current-page").text();
        ev.preventDefault();
        var task_id = $(ev.target).data('task-id');
        if (!page){
            page = 1;
        }
        $(document).trigger("refreshTaskScheduleDetails", {taskId: task_id, page: page});
    });
}