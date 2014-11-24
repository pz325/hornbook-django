$(document).ready(function() {

/// Study elements
    var $panel = $("#learning_panel");
    var $txtRecapList_ = $("#recap #recap_list");
    var $progressBarLearning_ = $('#progressBarLearning');
    var studyList_ = [];
    var studyIndex_ = 0;
    var graspedList_ = [];
    var recapList_ = [];
    
    var clickCallback_ = null;
    var currentMode_ = '';

    var showPanel = function(toShow) {
        if (toShow) $panel.removeClass("hide");
        else $panel.addClass("hide");
    }

    /**
     * @param index
     * @param total
     */
    var updateProgressBar = function(index, total) {
        if (total === 0)
        {
            $progressBarLearning_.css({"width": "0%"});
            $progressBarLearning_.text("");
        }
        else
        {
            var percentage = Math.round((index+1)/total*100).toString() + "%";
            var t = (index+1).toString() + "/" + total.toString();
            $progressBarLearning_.css({"width": percentage});
            $progressBarLearning_.text(t);
        }
    }

    var resetUI = function() {
        showPanel(false);
        $txtRecapList_.text("");
        updateProgressBar(0, 0);       
        studyList_ = [];
        studyIndex_ = 0;
        graspedList_ = [];
        recapList_ = [];

        clickCallback_ = null;
        currentMode_ = '';

        Flashcard.displayVocabulary("");
    };

    /**
     *
     */
    var initUI = function() {
        showPanel(true);
        console.log('Study list: ', studyList_);
        // bind flashcard strategy
        Flashcard.setHanCharacterDivClickCallback(clickCallback_);
        // display the first character
        Flashcard.displayVocabulary(studyList_[studyIndex_]);
        // set learning progress bar to 0%
        updateProgressBar(0, studyList_.length);
    };


/// ======== study new ========

    /*
     * Flashcard click callback in StudyNew mode
     *     save the current vocabulary to graspedList_ (as a holder)
     *     pop one element from studyList_
     *     if studyList_ is empty, swap studyList_ and graspedList_
     *     shuffle studyList_
     */
    var studyNewClickCallback = function() {
        studyIndex_++;
        if (studyIndex_ === studyList_.length)
        {
            studyList_ = Util.shuffle(studyList_);
            studyIndex_ = 0;
        }
        Flashcard.displayVocabulary(studyList_[studyIndex_]);
        updateProgressBar(studyIndex_, studyList_.length);
    };

    /*
     * Init elements for the study new mode
     */ 
    var initStudyNew = function() {
        resetUI();

        studyList_ = [];
        var today_study = $("#input_today_study").val().trim();
        if (today_study.length > 0)
            studyList_ = studyList_.concat(today_study.split(" "));
        console.log("User adds new:", studyList_);
        clickCallback_ = studyNewClickCallback;        
        currentMode_ = "StudyNew";

        // get 3 of most common 500
        console.log('Add 3 of most 500', $("#checkbox_add500").is(':checked'));
        if ($("#checkbox_add500").is(':checked'))
        {
            StudyAPI.getNewFrom500(3)
            .done(function(data, textStatus, jqXHR) {
                var new3 = JSON.parse(data);
                console.log('Most 500: ', new3);
                studyList_ = studyList_.concat(new3);
                initUI();
            });
        }
        else
        {// get new studies
            initUI();
        }
    };

    $("#button_add_new").click(function() {
        initStudyNew();
        return false;
    });

    $("#button_save_to_server").click(function() {
        if (currentMode_ === "StudyNew") {
            console.log("new words:", studyList_);
            StudyAPI.saveNewStudy(studyList_.join(" "))
            .done(function(data, textStatus, jqXHR) {
                Util.notifySuccess("New study saved");
            })
            .fail(function(data, textStatus, jqXHR) {
                Util.notifyError("Failed saving new study");
            });
        }
        return false;
    });


/// ======== revise ========    
    /**
     * call getStudyHistoryIntelligent() or getStudyHistoryBetween()
     * @return $.ajax() deferred object
     */
    var getStudyHistory = function() {
        return StudyAPI.getStudyIntelligent();
    };

    /**
     * Flashcard click callback in revise mode
     *     save to graspedList_
     *     update progress UI
     *     if studyList_ is to be empty,
     *         save revising history to server
     *     show next vocabulary
     */
    var reviseClickCallback = function() {
        graspedList_.push(studyList_[studyIndex_]);
        studyIndex_++;
        if (studyIndex_ === studyList_.length)
        {
            saveRevise();
            // go to recap mode
            if (recapList_.length > 0)
                initRecap();
            else
                resetUI();
        }
        else
        {
            Flashcard.displayVocabulary(studyList_[studyIndex_]);
            updateProgressBar(studyIndex_, studyList_.length);
        }
    };

    /**
     * Save revise to server
     * Start Revise mode if ncessary
     */
    var saveRevise = function() {
        var recall_results = {
            "grasped": graspedList_.join(" "),
            "unknown": recapList_.join(" ")
        };
        $.when(
            StudyAPI.update(JSON.stringify(recall_results))
        ).done(function(r1, r2) {
            Util.notifySuccess("Revise saved");
        })
        .fail(function(r1, r2) {
            Util.notifyError("Failed saving revise");
        });
    };

    /*
     * Init elements for the revise mode
     */ 
    var initRevise = function() {
        // get study history
        getStudyHistory()
        .done(function(data, textStatus, jqXHR) {
            resetUI();

            Util.notifySuccess("Study history loaded");
            console.log('history data: ', data);
            studyList_ = JSON.parse(data);
            if (studyList_.length > 0) {
                studyList_ = Util.shuffle(studyList_);
                clickCallback_ = reviseClickCallback;
                currentMode_ = "Revise";

                initUI();
            }
            else {
                Util.notifyError("No learning history available");
            }
        })
        .fail(function(data, textStatus, jqXHR) {
            Util.notifyError("Failed loading the study history");
        });
    };

    $("#button_add_to_recap_list").click(function() {
        if (currentMode_ === 'Revise') {
            recapList_.push(studyList_[studyIndex_]);
            studyIndex_++;
            if (studyIndex_ === studyList_.length) {
                saveRevise();
                // go to recap mode
                if (recapList_.length > 0)
                    initRecap();
                else
                    resetUI();
            } else {
                Flashcard.displayVocabulary(studyList_[studyIndex_]);
                updateProgressBar(studyIndex_, studyList_.length);
                console.log('recap list: ', recapList_);
                console.log('study list: ', studyList_)
                $txtRecapList_.text(recapList_);
            }
        }
        return false;
    });

/// ======== recap ========
    var recapClickCallback = function() {
        studyIndex_++;
        if (studyIndex_ === studyList_.length)
        {
            studyList_ = Util.shuffle(studyList_);
            studyIndex_ = 0;
        }    
        Flashcard.displayVocabulary(studyList_[studyIndex_]);
        updateProgressBar(studyIndex_, studyList_.length);
    };

    var initRecap = function() {
        studyIndex_ = 0;
        studyList_ = recapList_;
        recapList_ = [];
        $txtRecapList_.text("recap mode");
        clickCallback_ = recapClickCallback;
        currentMode_ = "Recap";

        initUI();
        Util.notifySuccess("Switch to Recap mode");
    };

    // initialise
    // bind Flashcard
    Flashcard.init($("#flashcard"));

    // if /study/index.html, initRevise()
    var url = window.location.href;
    console.log(url);
    var suffix = "/study/";
    if (url.indexOf(suffix, url.length - suffix.length) !== -1)
    {
        initRevise();
    }
});