// flashcard_div = $("#flashcard")
var Flashcard = (function(){
    var $flashcard_div;
    var strategy_;
    var ref_character_;
    var last_word_ = [];  // last_word_ is an array of u_chars

    var log_state = function() {
        console.log("ref character: ", ref_character_, "last word: ", last_word_);
    };

    /**
     * flashcard_div = $("#flashcard")
     * strategy = GradingTest
     */
    var init = function(flashcard_div, strategy){
        $flashcard_div = flashcard_div;
        strategy_ = strategy;

        $.when(strategy_.init())
        .done(function() {
            ref_character_ = strategy_.get_next_char();
            last_word_ = [];
            last_word_.push(ref_character_);
            log_state();
            display_char(ref_character_);
        });
    };

    var gen_han_character_div = function(u_char){
        var han_character_div = $("<div/>", {
                    class: "han_character",
                    text: u_char,
                    style: "cursor: pointer"
        });
        han_character_div.click(function(){
            ref_character_ = $(this).text();
            log_state();
        });
        return han_character_div;
    };

    var display_char = function(u_char) {
        ref_character_ = u_char;
        last_word_ = [];
        last_word_.push(ref_character_);
        log_state();
        $flashcard_div
            .empty()
            .append(gen_han_character_div(u_char));
    };

    var display_word = function(u_chars) {
        last_word_ = u_chars;
        log_state();
        $flashcard_div.empty();
        $.each(last_word_, function(index, u_char){
            $flashcard_div.append(gen_han_character_div(u_char));
        });
    };

    var get_ref_character = function() {
        return ref_character_;
    };

    var get_last_word = function() {
        return last_word_;
    };

    var update_han_characters = function() {
        // if num of <div#han_character> of <div#flashcard> is 1
        var num_div_han_characters = $("#flashcard > .han_character").length;
        console.log('num_div_han_characters: ' +  num_div_han_characters);
        if (num_div_han_characters == 1)
        {
            get_most_common_word(ref_character, last_word);
        }
        else
        {
            display_char(ref_character);
        }
    };

    // public interface
    return {
        init: init,
        display_char: display_char,
        display_word: display_word,
        get_ref_character: get_ref_character,
        get_last_word: get_last_word
    };

}) ();
