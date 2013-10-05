// flashcard_div = $("#flashcard")
var Flashcard = (function(){
    var $flashcardDiv;
    var strategy_;
    var lastWord_;  // lastWord_ "0x34560x3321

    var logState = function() {
        console.log("last word: ", lastWord_);
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
     * @param 0x1234
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
     * @param vocabulary "0x23120x2233"
     */
    var displayVocabulary = function(vocabulary) {
        lastWord_ = vocabulary;
        logState();
        $flashcardDiv.empty();
        lastWord_.split("").forEach(function(element) {
            $flashcardDiv.append(genHanCharacterDiv(element));
        });
    };

    /**
     * @return "0x23120x2233"
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
