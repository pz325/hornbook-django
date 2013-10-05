// flashcard_div = $("#flashcard")
var Flashcard = (function(){
    var $flashcardDiv;
    var strategy_;
    var lastWord_ = [];  // lastWord_ [{u_char: 0x3456}, {u_char: 0x3321}]

    var logState = function() {
        var w = "";
        if (lastWord_.length > 0) {
            lastWord_.forEach(function(element){
                w += element["u_char"];
            });
        }
        else {
            w = "not set";
        }
        console.log("last word: ", w);
    };

    /**
     * flashcardDiv = $("#flashcard")
     * strategy = GradingTest
     */
    var init = function(flashcardDiv, strategy){
        $flashcardDiv = flashcardDiv;
        strategy_ = strategy;

        strategy_.init()
        .done(function() {
            lastWord_ = strategy_.getNextVocabulary();
            if (lastWord_) {
                logState();
                displayVocabulary(lastWord_);
            }
        });
    };

    /**
     * @param u_char
     */
    var genHanCharacterDiv = function(u_char){
        var hanCharacterDiv = $("<div/>", {
                    class: "han_character",
                    text: u_char,
                    style: "cursor: pointer"
        });
        return hanCharacterDiv;
    };

    /**
     * @param vocabulary [{u_char: 0x2312}, {u_char: 0x2233}]
     */
    var displayVocabulary = function(vocabulary) {
        lastWord_ = vocabulary;
        logState();
        $flashcardDiv.empty();
        lastWord_.forEach(function(element) {
            $flashcardDiv.append(genHanCharacterDiv(element["u_char"]));
        });
    };

    /**
     * @return [{u_char: 0x2312}, {u_char: 0x2233}]
     */
    var getLastWord = function() {
        return lastWord_;
    };

    // public interface
    return {
        init: init,
        displayVocabulary: displayVocabulary,
        getLastWord: getLastWord
    };
}) ();
