$(document).ready(function() {

/// Study elements
    var $txtRecapList_ = $("#recap #recap_list");
    var $progressBarLearning_ = $('#progressBarLearning');
    var studyList_ = [];
    var studyIndex_ = 0;
    var graspedList_ = [];
    var recapList_ = [];
    
    var clickCallback_ = null;
    var currentMode_ = '';

     /**
     * @param ratio 0.2334
     */
    var updateProgress = function(ratio) {
        var percentage = Math.round(ratio * 100).toString() + "%";
        $progressBarLearning_.css({"width": percentage});
    }

    var resetUI = function() {
        $txtRecapList_.text("");
        
        updateProgress(0);       
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
        // set learning progress bar to 0%
        updateProgress(0);
        console.log('Study list: ', studyList_);
        // bind flashcard strategy
        Flashcard.setHanCharacterDivClickCallback(clickCallback_);
        // display the first character
        Flashcard.displayVocabulary(studyList_[studyIndex_]);
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
        updateProgress(studyIndex_/studyList_.length);
        Flashcard.displayVocabulary(studyList_[studyIndex_]);
        if (studyIndex_ === studyList_.length-1) {
            studyList_ = Util.shuffle(studyList_);
            studyIndex_ = 0;
        }
    };

    /*
     * Init elements for the study new mode
     */ 
    var initStudyNew = function() {
        resetUI();

        // get new studies
        var today_study = $("#input_today_study").val().trim();
        console.log("today study: ", today_study);
        studyList_ = today_study.split(" ");

        clickCallback_ = studyNewClickCallback;        
        currentMode_ = "StudyNew";

        initUI();
    };

    $("#button_add_new").click(function() {
        initStudyNew();
        return false;
    });

    $("#button_save_to_server").click(function() {
        if (currentMode_ === "StudyNew") {
            console.log("new words:", studyList_);
            StudyAPI.newStudy(studyList_.join(" "))
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
        updateProgress(studyIndex_/studyList_.length);
        if (studyIndex_ === studyList_.length) {
            saveRevise();
            // go to recap mode
            if (recapList_.length > 0)
                initRecap();
            else
                resetUI();
        } else {
            Flashcard.displayVocabulary(studyList_[studyIndex_]);
        }
    };

    /**
     * Save revise to server
     * Start Revise mode if ncessary
     */
    var saveRevise = function() {
        $.when(
            StudyAPI.reviseStudy(graspedList_.join(" ")),
            StudyAPI.newStudy(recapList_.join(" "))
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

    $("#button_load_history").click(function() {
        initRevise();
        return false;
    });

    $("#button_add_to_recap_list").click(function() {
        if (currentMode_ === 'Revise') {
            recapList_.push(studyList_[studyIndex_]);
            studyIndex_ ++;
            updateProgress(studyIndex_/studyList_.length);
            console.log('recap list: ', recapList_);
            console.log('study list: ', studyList_)
            if (studyIndex_ === studyList_.length) {
                saveRevise();
                // go to recap mode
                if (recapList_.length > 0)
                    initRecap();
                else
                    resetUI();
            } else {
                Flashcard.displayVocabulary(studyList_[studyIndex_]);
                $txtRecapList_.text(recapList_);
            }
        }
        return false;
    });

/// ======== recap ========

    var recapClickCallback = function() {
        studyIndex_++;
        updateProgress(studyIndex_/studyList_.length);
        Flashcard.displayVocabulary(studyList_[studyIndex_]);
        if (studyIndex_ === studyList_.length-1) {
            studyIndex_ = 0;
        }
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

});