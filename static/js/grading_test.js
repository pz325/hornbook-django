$(document).ready(function(){
    
    var list_ = new VocabularyList();

    var initGradingTest = function() {
        // load 500 common
        HornbookAPI.getAllMostCommonCharacters()
        .done(function(data) {
            Util.notifySuccess("Test data loaded");
            list_.set(data, false);
            Flashcard.displayVocabulary(list_.get());
        })
        .fail(function(data) {
            Util.notifyError("Failed loading test data");
        });
    };


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

    /*
     * binding button click event
     * add as grasped to database
     */
    $("#button_yes").click(function() {
        StudyAPI.addGrasped(list_.get())
        .done(function(){
            Util.notifySuccess("Grasped added");
            Flashcard.displayVocabulary(list_.getNext());
        })
        .fail(function(){
            Util.notifyError("Failed adding grasped");
        });
    });
    
    $("#button_no").click(function() { 
        Flashcard.displayVocabulary(list_.getNext()); 
    });


    // initialise
    // bind Flashcard
    Flashcard.init($("#flashcard"));
    initGradingTest();
});