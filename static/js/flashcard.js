// flashcard_div = $("#flashcard")
var Flashcard = (function(){
    var $flashcardDiv;
    var lastWord_;  // lastWord_ "0x34560x3321
    var hanCharacterDivClickCallback_;
    var hanCharacterDivs_ = [];

    var logState = function() {
        console.log("last word: ", lastWord_);
    };

    /**
     * flashcardDiv = $("#flashcard")
     */
    var init = function(flashcardDiv, hanCharacterDivClickCallback){
        $flashcardDiv = flashcardDiv;
        hanCharacterDivs_ = [];
        hanCharacterDivClickCallback_ = hanCharacterDivClickCallback;
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
        hanCharacterDivs_.push(hanCharacterDiv);
        return hanCharacterDiv;
    };

    /**
     * @param vocabulary "0x23120x2233"
     */
    var displayVocabulary = function(vocabulary) {
        lastWord_ = vocabulary;
        logState();

        $flashcardDiv.fadeOut('slow', function() {
            $flashcardDiv.empty();
            lastWord_.split("").forEach(function(element) {
                genHanCharacterDiv(element)
                .appendTo($flashcardDiv)
            });
            $flashcardDiv.fadeIn('fast');
        });
    };

    var setHanCharacterDivClickCallback = function(hanCharacterDivClickCallback) {
        hanCharacterDivClickCallback_ = hanCharacterDivClickCallback;
        hanCharacterDivs_.forEach(function(element) {
            element.click(hanCharacterDivClickCallback_);
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
        getLastWord: getLastWord,
        setHanCharacterDivClickCallback: setHanCharacterDivClickCallback
    };
}) ();
