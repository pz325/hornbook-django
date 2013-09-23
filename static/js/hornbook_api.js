var API_MOST_COMMON_CHARACTER_URL = "/api/most_common_character";
var API_ALL_MOST_COMMON_CHARACTERS_URL = "/api/all_most_common_characters";
var API_MOST_COMMON_WORD_URL = "/api/most_common_word";

var HornbookAPI = (function() {
    var all_most_common_characters = "";
    var index = 0;

    /**
     * Get all most common characters
     * save to all_most_common_characters
     * return the first
     */
    var get_all_most_common_characters = function() {
        $.get(API_ALL_MOST_COMMON_CHARACTERS_URL, function(data) {
            all_most_common_characters = $.parseJSON(data);
            index = 0;
            return all_most_common_characters;
        });
    };

    /**
     * Return the next common character from all_most_common_characters
     */
    var get_next_common_character = function() {
        if (all_most_common_characters === "") {
            get_all_most_common_characters();
        }
        else {
            index += 1;
            if (index == all_most_common_characters.length) {
                index = 0;
            }
        }
        var u_char = all_most_common_characters[index]['u_char'];
        console.log("next character: " + u_char);
        return u_char;
    };

    /**
     * Call HTTP /api/most_common_word
     * Return list of u_chars
     */
    var get_most_common_word = function(character, word) {
        $.ajax({
            type: "GET",
            url: API_MOST_COMMON_WORD_URL,
            data: "ref_character=" + character + "&last_word=" + word,
            success: function(data) {
                var data_Obj = $.parseJSON(data);
                var u_chars = data_Obj.u_chars;
                console.log('api/most_common_word ', u_chars.join(''));
                return u_chars;
            }
        });
    };

    // public interface
    return {
        get_all_most_common_characters: get_all_most_common_characters,
        get_next_common_character: get_next_common_character,
        get_most_common_word: get_most_common_word
    };

})();


var GradingTest = (function(){
    var get_next_char = function(){
        return HornbookAPI.get_next_common_character();
    };

    var get_next_word = function(){
        return "";
    };

    return {
        get_next_char: get_next_char,
        get_next_word: get_next_word
    }
})();