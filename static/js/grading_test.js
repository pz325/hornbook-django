$(document).ready(function(){
    Flashcard.init($("#flashcard"), GradingTestStrategy);

    var nextVocabulary = function() {
        var vocabulary = GradingTestStrategy.getNextVocabulary();
        console.log("vocabulary to display: ", vocabulary);
        Flashcard.displayVocabulary(vocabulary);
    };

    /**
     * @vocabulary [{u_char: u0x2345}, {u_char: u0x1234}, ...]
     */
    var addToUserVocabulary = function(vocabulary) {
        var request = $.ajax({
            url: "/user_vocabularies/add_to_user_vocabulary/",
            contentType: "application/json; charset=UTF-8",
            data: {
                "vocabulary": vocabulary,
            }
        });
    }

    // binding button click event
    $("#button_yes").click(function() {
        var vocabulary = Flashcard.getLastWord();
        addToUserVocabulary(vocabulary);
        nextVocabulary(); 
    });
    
    $("#button_no").click(function() { 
        nextVocabulary(); 
    });
});