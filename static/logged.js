var target, length, num = 0;
var card = '<div class="card" style="width: 20rem;">\
        <div class="layer"></div>\
            <div class="card-block">\
                <h4 class="card-title"></h4>\
                <p class="card-text"></p>\
            </div>\
            <div class="card-block">\
                <div class="delete">Del</div>\
                <div class="edit" data-toggle="modal" data-target="#note">edit</div>\
            </div>\
        </div>';

function save(title, text, layer, id, save_case) {
    args = {
        title: title,
        text:text,
        layer: layer,
        id: id,
        save_case: save_case
    };
    $.get(Flask.url_for('save'), args);
    
}

$(document).ready(function() {
    $.getJSON(Flask.url_for('load'))
    .done(function(data, textStatus, jqXHR) {
        $.each(data, function(index, value) {
            $(".cards").append(card);
            $(".card:last").attr("id", value["id"]);
            $(".card:last h4").html(value["title"]);
            $(".card:last p").html(value["text"]);
            $(".card:last .layer").css({"background-color": value["layer"], "position": "absolute", "opacity": ".2", "top":"0", "left":"0", "width": "100%", "height": "100%"});
            
            length = ((Math.floor(value["text"].length / 23)) * -10) -100;
            $(".card:last .delete,.card:last .edit").css("top", length + "px");
        });
    })
    .fail(function(jqXHR, textStatus, errorThrown) {

        // log error to browser's console
        console.log(errorThrown.toString());
    });
    
    $(".btn-success").click(function() {
        location.href=Flask.url_for("index");
    });
    
    $("#addnote").click(function() {
        $("#noteTitle").val("");
        $("#noteBody").val("");
        $("#add").show(); $("#edit").hide();
    });
    $("#add").click(function() {
        //$(".card").removeClass("new");
        $(".cards").append(card);
        var last = ".card:last";
        $(last).css("opacity", "0").animate({opacity:"1"}, "slow");
        // assign UNIQUE ID to the new card
        while(true) {
            var tmp = num;
            $(".card").each(function() {
            if(tmp == $(this).attr("id")) {
                num++;
                return false;
            }
        });
            if (num == tmp) {
                $(last).attr("id", num);
                break;
            }
        }
        
        
        var title = $("#noteTitle").val();
        var text = $("#noteBody").val();
        //var photo = $("#notePhoto").val();
        //if (photo) {
        //    $("#photo" + num.toString()).prepend('<img class="card-img-top" src=' + photo + ' alt="Card Image">');
        //} else {
        var layer = $("#selected").css("background-color");
        if(layer != "rgb(128, 128, 128)") {
            $(last+" .layer").css({"background-color": layer, "position": "absolute", "opacity": ".2", "top":"0", "left":"0", "width": "100%", "height": "100%"});
        } else {
            var random = Math.floor(Math.random() * 6);
            switch(random) {
                case 0:
                    layer = "yellow";
                    break;
                case 1:
                    layer = "blue";
                    break;
                case 2:
                    layer = "green";
                    break;
                case 3:
                    layer = "red";
                    break;
                case 4:
                    layer = "orange";
                    break;
                case 5:
                    layer = "violet";
                    break;
                case 6:
                    layer = "white";
                    break;
                
            }
            $(last+" .layer").css({"background-color": layer, "position": "absolute", "opacity": ".2", "top":"0", "left":"0", "width": "100%", "height": "100%"});
        }
        //}
        $(last +" h4").html(title);
        $(last +" p").html(text);
        
        save(title, text, layer, num, 1);
        
        length = ((Math.floor(text.length / 23)) * -10) -100;
        
        $(last +" .delete,"+last+" .edit").css("top", length + "px");
        //$(".card").removeClass("new");
    });
    $("main").on("click", ".card", function() {
        if(!$(this).hasClass("selected")) {
            $(".card").removeClass("selected").css("border", "1px solid rgba(0, 0, 0, 0.125)").find(".delete, .edit").hide();
            $(this).css("border", "solid 2px black");
            $(this).addClass("selected");
            $(this).find(".delete, .edit").show();
            
            $("[value=random]").prop("disabled", true);
        } else {
            
            $(this).css("border", "1px solid rgba(0, 0, 0, 0.125)");
            $(this).removeClass("selected");
            $(this).find(".delete, .edit").hide();
            
            $("[value=random]").prop("disabled", false);
        }
    });
    // delete
    $("main").on("click", ".delete", function() {
        var id = $(this).closest(".card").attr("id");
        $(this).closest(".card").animate({opacity: "0"}, "slow", "", function() {
            $(this).remove();
        });
        //$(this).closest(".card").remove();
        save(undefined, undefined, undefined, id, 4);
    });
    // edit
    $("main").on("click", ".edit", function() {
        $("#add").hide(); $("#edit").show();
        target = $(this).closest(".card");
        
        var edit = [target.find("h4").html(), target.find("p").html()];
        $("#noteTitle").val(edit[0]);
        $("#noteBody").val(edit[1]);
        
        //$("#notePhoto").val(photo);
    });
    $("#edit").click(function() {
        target.find("h4").html($("#noteTitle").val());
        target.find("p").html($("#noteBody").val());
        
        length = (Math.floor($("#noteBody").val().length / 23) * 10) -100;
        target.find("delete, edit").css("top", length + "px");
        
        save($("#noteTitle").val(), $("#noteBody").val(), undefined,target.attr("id"), 3);
    });
    
    $(".colors").click(function() {
        if($(".card").hasClass("selected")) {
            var $this = $(this).val(), selected_card = $(".selected").attr("id");
            //"for me": attribute selector below doesn't work for css attributes like border, background, etc.
            $('.selected').css("border", "1px solid rgba(0, 0, 0, 0.125)").end().find(".delete, .edit").hide();
            $('.selected').find(".layer").css("background-color", $this).end().removeClass("selected");
            save(undefined, undefined, $this, selected_card, 2);
        } else {
        
            if($("#selected").html() == "<b>random</b>") {
                $("#selected").html("");
            }
            var selected = $(this).val();
            if(selected == "random") {
                $("#selected").css("backgroundColor", "grey");
                $("#selected").append("<b>random</b>");
            } else {
                $("#selected").css("backgroundColor", selected);
            }
        }
    });
    $(".colors").hover(function() {
        $(this).animate({opacity: "1"}, "fast");
    }, function() {
        $(this).animate({opacity: "0.5"}, "fast");
    });
    
    $(".info").hover(function() {
        $(this).animate({opacity: "1"}, "slow");
        $(this).popover();
    }, function() {
        $(this).animate({opacity: ".8"}, "slow");
    });
});
