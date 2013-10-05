$(document).ready(function(){
    Flashcard.init($("#flashcard"), StudyStrategy);

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
        console.log('end_date (today):', end_date);
        console.log('start_date: ', start_date);
        StudyAPI.getStudyBetween(start_date, end_date)
        .then(function(data, textStatus, jqXHR) {
            deferred_obj.resolve(data, textStatus, jqXHR);
            });                
        return deferred_obj.promise();
    };

    var setVocabularies = function(vocabularies) {
        console.log('set vocabularies: ', vocabularies);
        // TODO: display all vocabularies
        // update StudyStrategy and Flashcard
        StudyStrategy.setVocabularies(vocabularies);
        Flashcard.displayVocabulary(StudyStrategy.getNextVocabulary());
    };

    $("#button_save_study").click(function(){
        var today_study = $("#input_today_study").val();
        StudyAPI.saveStudy(today_study)
        .pipe(getStudyHistory)
        .done(function(data, textStatus, jqXHR) {
            // set vocabularies
            console.log(data);
            var v = JSON.parse(data);
            today_study.split(' ').forEach(function(element) {
                v.push(element);
            });
            setVocabularies(v);
        });
    });
}); 