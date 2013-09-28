var API_MOST_COMMON_CHARACTER_URL = "/api/most_common_character";
var API_ALL_MOST_COMMON_CHARACTERS_URL = "/api/all_most_common_characters";
var API_MOST_COMMON_WORD_URL = "/api/most_common_word";

/**
 *
 */
var HornbookAPI = (function() {
    var all_most_common_characters;

    /**
     * Call HTTP GET /api/all_most_common_characters
     * an local cache kept
     */
    var get_all_most_common_characters = function() {
        var deferred_obj = $.Deferred();  
        if (!all_most_common_characters) {
            $.ajax({
                type: "GET",
                url: API_ALL_MOST_COMMON_CHARACTERS_URL
            })
            .done(function(resp) {
                all_most_common_characters = $.parseJSON(resp);
                deferred_obj.resolve(all_most_common_characters);
            });
        }
        else {
            deferred_obj.resolve(all_most_common_characters);
        }
        return deferred_obj.promise();
    };

    /**
     * HTTP GET /api/most_common_word
     */
    var get_most_common_word = function(character, word) {
        return $.ajax({
            type: "GET",
            url: API_MOST_COMMON_WORD_URL,
            data: "ref_character=" + character + "&last_word=" + word
        });
    };

    /**
     * HTTP GET /api/most_common_character
     */
    var get_most_common_character = function() {
        return $.ajax({
            type: "GET",
            url: API_MOST_COMMON_CHARACTER_URL
        });
    }

    // public interface
    return {
        get_all_most_common_characters: get_all_most_common_characters,
        get_most_common_word: get_most_common_word,
        get_most_common_character: get_most_common_character
    };
})();


var GradingTest = (function() {
    var all_most_common_characters_;
    var index_;

    var init = function() {
        index_ = 0;
        var deferred_obj = $.Deferred();
        if (!all_most_common_characters_)
        {
            $.when(HornbookAPI.get_all_most_common_characters())
            .done(function(data) {
                all_most_common_characters_ = data;
                deferred_obj.resolve();        
            });    
        }
        else {
            deferred_obj.resolve();
        }
        return deferred_obj.promise();
    };

    var get_next_char = function() {
        var u_char = all_most_common_characters_[index_]["u_char"];
        index_ += 1;
        if (index_ >= all_most_common_characters_.length) {
            index_ = 0;
        }
        return u_char;
    };

    var get_next_word = function(){
        return "";
    };

    return {
        init: init,
        get_next_char: get_next_char,
        get_next_word: get_next_word
    };
})();