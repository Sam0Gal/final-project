$(document).ready(function() {
    if($(".message").html() == "username already exists." || $(".message").html() == "Invalid username or password")
        $(".messages").css({"border-left": "red 5px solid", "display": "block"}).animate({opacity: "1"}, 2000);
    
    else if($(".message").html() == "You have successfully registerd!") {
        $(".messages").css({"border-left": "green 5px solid", "background-color": "aquamarine", "display": "block"}).animate({opacity: "1"}, 2000);
        $(".messages").animate({opacity: "0"}, 5000, function() {
            $(this).remove();
        });
    
    }
    
})