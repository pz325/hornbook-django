$(document).ready(function() {
    function getLastWeek() {
        var today = new Date();
        var lastWeek = new Date(today.getTime()-1000*60*60*24*7);
        return lastWeek ;
    }

    function getLastMonth() {
        var today = new Date();
        var lastMonth = new Date(today.getTime()-1000*60*60*24*30);
        return lastMonth ;
    }

    /**
     * deferred
     */
    var getStudyHistory = function() {
        var deferred_obj = $.Deferred();
        var range = $('#select_previous_study option:selected').val();
        console.log('range:', range);

        var today = new Date();
        var end_date = $.datepicker.formatDate('mm/dd/yy', new Date());
        var start_date = null;
        if (range === "last_week") {
            start_date = $.datepicker.formatDate('mm/dd/yy', getLastWeek());
        }
        if (range === "last_month") {
            start_date = $.datepicker.formatDate('mm/dd/yy', getLastMonth());
        }
        //console.log('end_date (today):', end_date);
        //console.log('start_date: ', start_date);
        StudyAPI.getStudyBetween(start_date, end_date)
        .then(function(data, textStatus, jqXHR) {
            deferred_obj.resolve(data, textStatus, jqXHR);
            });                
        return deferred_obj.promise();
    };

    var setVocabularies = function(strategy) {
        var vocabularies = strategy.getAllVocabularies();
        console.log('set vocabularies: ', vocabularies);
        // display all vocabularies
        $(".all_study").text(vocabularies);
        // bind flashcard strategy
        Flashcard.setHanCharacterDivClickCallback(function() {
            Flashcard.displayVocabulary(strategy.getNextVocabulary());
        });
        Flashcard.displayVocabulary(strategy.getNextVocabulary());
    };

    var clearRecap = function() {
        RecapStrategy.clearVocabularies();
    };

    $("#button_add_new").click(function(){
        clearRecap();
        // save today_study
        var today_study = $("#input_today_study").val().trim();
        console.log('today study: ', today_study)
        StudyAPI.saveStudy(today_study)
        .pipe(getStudyHistory)
        .done(function(data, textStatus, jqXHR) {
            // set vocabularies
            console.log('history data: ', data);
            var v = JSON.parse(data);  // v now includes today's study
            StudyStrategy.setVocabularies(v);
            setVocabularies(StudyStrategy);
        });
    });

    $("#button_load_history").click(function() {
        clearRecap();
        getStudyHistory()
        .done(function(data, textStatus, jqXHR) {
            console.log('history data: ', data);
            var v = JSON.parse(data);
            StudyStrategy.setVocabularies(v);
            setVocabularies(StudyStrategy);
        });
    });

    $("#button_add_to_recap_list").click(function() {
        console.log('recap: ', Flashcard.getLastWord());
        RecapStrategy.add(Flashcard.getLastWord());
    });

    $("#button_recap").click(function() {
        setVocabularies(RecapStrategy);
    });

    // initialise
    // bind Flashcard
    Flashcard.init($("#flashcard"));
    // auto load history
    $("#button_load_history").click();
});