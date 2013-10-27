$(document).ready(function(){
    var nextVocabulary = function() {
        var vocabulary = GradingTestStrategy.getNextVocabulary();
        console.log("vocabulary to display: ", vocabulary);
        Flashcard.displayVocabulary(vocabulary);
    };

    /**
     * @vocabulary "u0x2345u0x1234"
     */
    var addToUserVocabulary = function(vocabulary) {
        var request = $.ajax({
            type: "POST",
            url: "/user_vocabularies/add_to_user_vocabulary/",
            data: {
                "vocabulary": vocabulary,
            }
        });
    }

    // binding button click event
    $("#button_yes").click(function() {
        var vocabulary = Flashcard.getLastWord();
        console.log('vocabulary to save: ', vocabulary);
        addToUserVocabulary(vocabulary);
        nextVocabulary(); 
    });
    
    $("#button_no").click(function() { 
        nextVocabulary(); 
    });

    // initialise page
    GradingTestStrategy.init()
    .done(function() {
        console.log("GradingTestStrategy initialised: ");
        Flashcard.init($("#flashcard"));
        Flashcard.setHanCharacterDivClickCallback(function() {
            Flashcard.displayVocabulary(GradingTestStrategy.getNextVocabulary());
        });
        Flashcard.displayVocabulary(GradingTestStrategy.getNextVocabulary());
    });
});