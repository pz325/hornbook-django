$(document).ready(function(){
    var API_MOST_COMMON_CHARACTER_URL = "api/most_common_character";
    var API_MOST_COMMON_WORD_URL = "api/most_common_word";

    var g_ref_character;
    var g_last_word;

    var gen_han_character_div = function(u_char){
        var han_character_div = $("<div/>", {
                    class: "han_character",
                    text: u_char,
                    style: "cursor: pointer"
        });
        han_character_div.click(function(){
             g_ref_character = $(this).text();
            update_han_characters();
        });
        return han_character_div;
    };

    var display_char = function(u_char) {
        $("#flashcard")
            .empty()
            .append(gen_han_character_div(u_char));
    };

    var display_word = function(u_chars) {
        $("#flashcard").empty();
        $.each(u_chars, function(index, u_char){
            $("#flashcard").append(gen_han_character_div(u_char));
        });
    };

    var get_most_common_character = function() {
        $.get(API_MOST_COMMON_CHARACTER_URL, function(data){
            var data_Obj = $.parseJSON(data);
            console.log("api/most_common_character: " + data_Obj.u_char);

            // update global variables
            g_ref_character = data_Obj.u_char;
            console.log("g_ref_character: " + g_ref_character);

            // update UI
            display_char(g_ref_character);
        });
    };

    var get_most_common_word = function(ref_character, last_word) {
        $.ajax({
            type: "GET",
            url: API_MOST_COMMON_WORD_URL,
            data: "ref_character=" + ref_character + "&last_word=" + last_word,
            success: function(data){
                var data_Obj = $.parseJSON(data);
                console.log('api/most_common_word', data_Obj.u_chars.join(''));

                // update global variables
                var u_chars = data_Obj.u_chars;
                var new_characters = $.grep(u_chars, function(u_char){
                    return (u_char != ref_character);
                });
                if (new_characters.length > 0) {
                    var index = Math.floor((Math.random()*new_characters.length));
                    g_ref_character = new_characters[index];
                }
                else {
                    g_ref_character = ref_character;
                }
                g_last_word = u_chars.join('');
                console.log('g_ref_character: ' + g_ref_character);
                console.log('g_last_word: ' + g_last_word);

                // update UI
                display_word(u_chars);
            }
        });
    }

    var init = function(){
        get_most_common_character();
    };

    var update_han_characters = function(){
        // if num of <div#han_character> of <div#flashcard> is 1
        var num_div_han_characters = $("#flashcard > .han_character").length;
        console.log('num_div_han_characters: ' +  num_div_han_characters);
        if (num_div_han_characters == 1)
        {
            get_most_common_word(g_ref_character, g_last_word);
        }
        else
        {
            display_char(g_ref_character);
        }
    }

    // binding button click event
    $("#button_yes").click(function(){
        update_han_characters();
    });

    $("#button_no").click(function(){
        get_most_common_character();
    });

    // init
    init();
});