$(document).ready(function(){
    Flashcard.init($("#flashcard"), GradingTestStrategy);

    var next_char = function() {
        var u_char = GradingTest.get_next_char();
        console.log("char to display: ", u_char);
        Flashcard.display_char(u_char);
    };

    var add_to_user_vocabulary = function(u_char) {
        var request = $.ajax({
            type: "POST",
            url: "/user_vocabularies/add_to_user_vocabulary/",
            data: {
                "vocabulary": u_char,
            }
        });
    }

    // binding button click event
    $("#button_yes").click(function() {
        var u_char = Flashcard.get_ref_character();
        add_to_user_vocabulary(u_char);
        next_char(); 
    });
    
    $("#button_no").click(function() { 
        next_char(); 
    });
});