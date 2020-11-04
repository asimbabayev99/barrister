$(document).ready(function() {
    $(".chat-menu-toggle").on("click",function() {
        $(".animation-chat-container").hide(300)
    });
    $(".message-with-btn").on("click",function() {
        $(".animation-chat-container").show()
    })
})