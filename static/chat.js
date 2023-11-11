$(document).ready(function() {
    // This function runs when the DOM is fully loaded and ready to be manipulated.

    $("#send-button").click(function() {
        // This function runs when the "Send" button is clicked.
        console.log("BUTTON CLICKED ");
        var user_input = $("#user-input").val();
        console.log(user_input);
        const chatLog=document.querySelector('#chat-log');
        chatLog.textContent="";
        if (user_input !== "") {
            // Get the user's input from the input field.
            $.ajax({
                type: "POST",
                url: "/chat",
                data: { user_input: user_input },
                success: function(data) {
                    // Make an AJAX POST request to the /chat route with the user's input.

                    // When the server responds successfully, append the response to the chat log.
                    $("#chat-log").append("<p>" +"QUERY: " +user_input + "</p>"+"<p>" +"RESPONSE: "+ data.response + "</p>");
                }
            });

            // Clear the user's input field.
            $("#user-input").val("");
        }
    });
});