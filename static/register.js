$(document).ready(function() {
    $("#register").click(function(event) {
        if (!$("#username").val()) {
            $(".alert-danger").html("<div><strong>provide your username!</strong></div>");
            $("#username").css("border", "1px red solid");
            $(".alert-danger").css("display", "block");
            return false;
        }
        else
            $("#username").css("border", "2px green solid");

        if (!$("#password").val()) {
            $(".alert-danger").html("<div><strong>provide your password!</strong></div>");
            $("#password").css("border", "1px red solid");
            $(".alert-danger").css({display:"block", "opacity":"0"}).animate({opacity: "1"}, "slow");
            return false;
        }
        else
            $("#password").css("border", "2px green solid");
            
        if (!$("#confirm").val()) {
            $(".alert-danger").html("<div><strong>confirm your password!</strong></div>");
            $("#confirm").css("border", "1px red solid");
            $(".alert-danger").css({display:"block", "opacity":"0"}).animate({opacity: "1"}, "slow");
            return false;
        }
        else
            $("#confirm").css("border", "2px green solid");
            
        if ($("#password").val() != $("#confirm").val()) {
            $(".alert-danger").html("<div><strong>passwords do not match!</strong></div>");
            $("#confirm").css("border", "1px red solid");
            $(".alert-danger").css({display:"block", "opacity":"0"}).animate({opacity: "1"}, "slow");
            return false;
        }
        
    });
});

