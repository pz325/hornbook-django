var API_MOST_COMMON_CHARACTER_URL = "/api/most_common_character";
var API_ALL_MOST_COMMON_CHARACTERS_URL = "/api/all_most_common_characters";
var API_MOST_COMMON_WORD_URL = "/api/most_common_word";

// flashcard_div = $("#flashcard")
var Flashcard = (function(){
    var $flashcard_div;
    var strategy_;
    var last_character_;
    var last_word_;

    /**
     * flashcard_div = $("#flashcard")
     * strategy = GradingTest
     */
    var init = function(flashcard_div, strategy){
        $flashcard_div = flashcard_div;
        strategy_ = strategy;
        last_character_ = strategy_.get_next_char();
        last_word_  = "";

        display_char(last_character_);
    };

    var gen_han_character_div = function(u_char){
        var han_character_div = $("<div/>", {
                    class: "han_character",
                    text: u_char,
                    style: "cursor: pointer"
        });
        han_character_div.click(function(){
            ref_character = $(this).text();
            update_han_characters();
        });
        return han_character_div;
    };

    var display_char = function(u_char) {
        $flashcard_div
            .empty()
            .append(gen_han_character_div(u_char));
    };

    var display_word = function(u_chars) {
        $flashcard_div.empty();
        $.each(u_chars, function(index, u_char){
            $flashcard_div.append(gen_han_character_div(u_char));
        });
    };

    var update_han_characters = function(){
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
        display_word: display_word
    };

}) ();
