// flashcard_div = $("#flashcard")
var Flashcard = (function(){
    var $flashcardDiv;
    var strategy_;
    var lastWord_;  // lastWord_ "0x34560x3321
    var hanCharacterDivClickCallback_;

    var logState = function() {
        console.log("last word: ", lastWord_);
    };

    /**
     * flashcardDiv = $("#flashcard")
     * strategy = GradingTest
     */
    var init = function(flashcardDiv, strategy, hanCharacterDivClickCallback){
        $flashcardDiv = flashcardDiv;
        strategy_ = strategy;
        hanCharacterDivClickCallback_ = hanCharacterDivClickCallback;
        strategy_.init()
        .done(function() {
            displayVocabulary(strategy_.getNextVocabulary());
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
        if (hanCharacterDivClickCallback_) {
            hanCharacterDiv.click(hanCharacterDivClickCallback_);
        }
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
