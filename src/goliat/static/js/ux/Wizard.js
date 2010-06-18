Ext.namespace('Ext.ux', 'Ext.ux.layout', 'Ext.ux.Wiz');

/**
 * Licensed under GNU LESSER GENERAL PUBLIC LICENSE Version 3
 *
 * @author Thorsten Suckow-Homberg <ts@siteartwork.de>
 * @url http://www.siteartwork.de/cardlayout
 */

/**
 * @class Ext.ux.layout.CardLayout
 * @extends Ext.layout.CardLayout
 *
 * A specific {@link Ext.layout.CardLayout} that only sets the active item
 * if the 'beforehide'-method of the card to hide did not return false (in this case,
 * components usually won't be hidden).
 * The original implementation of {@link Ext.layout.CardLayout} does not take
 * the return value of the 'beforehide'-method into account.
 *
 * @constructor
 * @param {Object} config The config object
 */
Ext.ux.layout.CardLayout = Ext.extend(Ext.layout.CardLayout, {

    /**
     * Sets the active (visible) item in the layout.
     *
     * If the currently visible item is still visible after calling the 'hide()
     * method on it, this implementation assumes that the 'beforehide'-event returned
     * false, thus not the item was not allowed to be hidden. The active item will then
     * equal to the item that was active, before this method was called.
     *
     * @param {String/Number} item The string component id or numeric index of the item to activate
     */
    setActiveItem : function(item){
        item = this.container.getComponent(item);
        if(this.activeItem != item){
            if(this.activeItem){
                this.activeItem.hide();
            }
            // check if the beforehide method allowed to
            // hide the current item
            if (this.activeItem && !this.activeItem.hidden) {
                return;
            }
            var layout = item.doLayout && (this.layoutOnCardChange || !item.rendered);
            this.activeItem = item;
            item.show();
            this.layout();
            if(layout){
                item.doLayout();
            }
        }
    }

});


/**
 * Licensed under GNU LESSER GENERAL PUBLIC LICENSE Version 3
 *
 * @author Thorsten Suckow-Homberg <ts@siteartwork.de>
 * @url http://www.siteartwork.de/wizardcomponent
 */

/**
 * @class Ext.ux.Wiz
 * @extends Ext.Window
 *
 * A specific {@link Ext.Window} that models a wizard component.
 * A wizard is basically a dialog that guides a user through various steps
 * where he has to fill out form-data.
 * A {@link Ext.ux.Wiz}-component consists typically of a {@link Ext.ux.Wiz.Header}
 * and window-buttons ({@link Ext.Button}) which are linked to the {@link Ext.ux.Wiz.Card}s
 * which themself represent the forms the user has to fill out.
 *
 * In order to switch between the cards in the wizard, you need the {@link Ext.ux.layout.CardLayout},
 * which will check if an active-item can be hidden, before the requested new item will be set to
 * 'active', i.e. shown. This is needed since the wizard may not allow a card to be hidden, if
 * the input entered by the user was not valid. You can get this custom layout at
 * {@link http://www.siteartwork.de/cardlayout}.
 *
 * Note:
 * When data has been collected and teh "onFinish" listener triggers an AJAX-request,
 * you should call the "switchDialogState" method so that the the dialog shows a loadmask.
 * Once the requests finishes, call "switchDialogState" again, specially before any call
 * to the "close" method of this component, otherwise the "closable" property of this
 * instance might prevent a "close" operation for this dialog.
 *
 *
 * @constructor
 * @param {Object} config The config object
 */
Ext.ux.Wiz = Ext.extend(Ext.Window, {

    /**
     * @cfg {Object} An object containing the messages for the {@link Ext.LoadMask}
     * covering the card-panel on request, whereas the property identifies the
     * msg-text to show, and the value is the message text itself. Defaults to
     <pre><code>
{
    default : 'Saving...'
}
     </code></pre>
     *
     * Depending on the contexts the loadMask has to be shown in (using the method
     * showLoadMask of this class), the object can be configure to hold
     * various messages.
<pre><code>
this.loadMaskConfig = {
    default    : 'Saving...',
    validating : 'Please wait, validating input...',
};
// loadMask will be shown, displaying the message 'Please wait, validating input...'
this.showLoadMask(true, 'validating');
     </code></pre>
     */
    loadMaskConfig : {
        'default' : 'Saving...'
    },

    /**
     * @cfg {Number} height The height of the dialog. Defaults to "400".
     */
    height : 400,

    /**
     * @cfg {Number} width The width of the dialog. Defaults to "540".
     */
    width : 540,

    /**
     * @cfg {Boolean} closable Wether the dialog is closable. Defaults to "true".
     * This property will be changed by the "switchDialogState"-method, which will
     * enable/disable controls based on the passed argument. Thus, this config property
     * serves two purposes: Tell the init config to render a "close"-tool, and create a
     * "beforeclose"-listener which will either return true or false, indicating if the
     * dialog may be closed.
     */
    closable : true,

    /**
     * @cfg {Boolean} resizable Wether the dialog is resizable. Defaults to "false".
     */
    resizable : false,

    /**
     * @cfg {Boolean} resizable Wether the dialog is modal. Defaults to "true".
     */
    modal : true,

    /**
     * @cfg {Array} cards A numeric array with the configured {@link Ext.ux.Wiz.Card}s.
     * The index of the cards in the array represent the order in which they get displayed
     * in the wizard (i.e. card at index 0 gets displayed in the first step, card at index 1 gets
     * displayed in the second step and so on).
     */
    cards : null,

    /**
     * @cfg {String} previousButtonText The text to render the previous-button with.
     * Defaults to "&lt; Back" (< Back)
     */
    previousButtonText : '&lt; Previous',

    /**
     * @cfg {String} nextButtonText The text to render the next-button with.
     * Defaults to "Next &gt;" (Next >)
     */
    nextButtonText : 'Next &gt;',

    /**
     * @cfg {String} cancelButtonText The text to render the cancel-button with.
     * Defaults to "Cancel"
     */
    cancelButtonText : 'Cancel',

    /**
     * @cfg {String} finishButtonText The text to render the next-button with when the last
     * step of the wizard is reached. Defaults to "Finish"
     */
    finishButtonText : 'Finish',

    /**
     * @cfg {Object} headerConfig A config-object to use with {@link Ext.ux.Wiz.Header}.
     * If not present, it defaults to an empty object.
     */
    headerConfig : {},

    /**
     * @cfg {Object} cardPanelConfig A config-object to use with {@link Ext.Panel}, which
     * represents the card-panel in this dialog.
     * If not present, it defaults to an empty object
     */
    cardPanelConfig : {},

    /**
     * @param {Ext.Button} The window-button for paging to the previous card.
     * @private
     */
    previousButton : null,

    /**
     * @param {Ext.Button} The window-button for paging to the next card. When the
     * last card is reached, the event fired by and the text rendered to this button
     * will change.
     * @private
     */
    nextButton : null,

    /**
     * @param {Ext.Button} The window-button for canceling the wizard. The event
     * fired by this button will usually close the dialog.
     * @private
     */
    cancelButton : null,

    /**
     * @param {Ex.Panel} The card-panel that holds the various wizard cards
     * ({@link Ext.ux.Wiz.Card}). The card-panel itself uses the custom
     * {@link Ext.ux.layout.CardLayout}, which needs to be accessible by this class.
     * You can get it at {@link http://www.siteartwork.de/cardlayout}.
     * @private
     */
    cardPanel : null,

    /**
     * @param {Number} currentCard The current {@link Ext.ux.Wiz.Card} displayed.
     * Defaults to -1.
     * @private
     */
    currentCard : -1,

    /**
     * @param {Ext.ux.Wiz.Header} The header-panel of the wizard.
     * @private
     */
    headPanel : null,

    /**
     * @param {Number} cardCount Helper for storing the number of cards used
     * by this wizard. Defaults to 0 (inherits "cards.length" later on).
     * @private
     */
    cardCount : 0,

    /**
     * Inits this component with the specified config-properties and automatically
     * creates its components.
     */
    initComponent : function()
    {
        this.initButtons();
        this.initPanels();

        var title = this.title || this.headerConfig.title;
        title     = title || "";

        Ext.apply(this, {
            title     : title,
            layout    : 'border',
            cardCount : this.cards.length,
            buttons   : [
                this.previousButton,
                this.nextButton,
                this.cancelButton
            ],
            items : [
                this.headPanel,
                this.cardPanel
            ]
        });

        this.addEvents(
            /**
             * @event cancel
             * Fires after the cancel-button has been clicked.
             * @param {Ext.ux.Wiz} this
             */
            'cancel',
            /**
             * @event finish
             * Fires after the last card was reached in the wizard and the
             * next/finish-button has been clicked.
             * @param {Ext.ux.Wiz} this
             * @param {Object} data The collected data of the cards, whereas
             * the index is the id of the card and the specific values
             * are objects with key/value pairs in the form formElementName : value
             */
            'finish'
        );

        Ext.ux.Wiz.superclass.initComponent.call(this);
    },

// -------- helper
    /**
     * Returns the form-data of all cards in this wizard. The first index is the
     * id of the card in this wizard,
     * and the values are objects containing key/value pairs in the form of
     * fieldName : fieldValue.
     *
     * @return {Array}
     */
    getWizardData : function()
    {
        var formValues = {};
        var cards = this.cards;
        for (var i = 0, len = cards.length; i < len; i++) {
            if (cards[i].form) {
                formValues[cards[i].id] = cards[i].form.getValues(false);
            } else {
                formValues[cards[i].id] = {};
            }
        }

        return formValues;
    },

    /**
     * Switches the state of this wizard between disabled/enabled.
     * A disabled dialog will have a {@link Ext.LoadMask} covering the card-panel
     * to prevent user input, and the buttons will be rendered disabled/enabled.
     * If the dialog is closable, the close-tool will be masked, too, and the dialog will not
     * be closable by clicking the "close" tool.
     *
     * @param {Boolean} enabled "false" to prevent user input and mask the elements,
     * otherwise true.
     * @param {String} type The type of msg for the {@Ext.LoadMask} covering
     * the cardPanel, as defined in the cfg property "loadMaskConfig"
     */
    switchDialogState : function(enabled, type)
    {
        this.showLoadMask(!enabled, type);

        this.previousButton.setDisabled(!enabled);
        this.nextButton.setDisabled(!enabled);
        this.cancelButton.setDisabled(!enabled);

        var ct = this.tools['close'];

        if (ct) {
            switch (enabled) {
                case true:
                    this.tools['close'].unmask();
                break;

                default:
                    this.tools['close'].mask();
                break;
            }
        }

        this.closable = enabled;
    },

    /**
     * Shows the load mask for this wizard. By default, the cardPanel's body
     * will be masked.
     *
     * @param {Boolean} show true to show the load mask, otherwise false.
     * @param {String} type The type of message for the {@Ext.LoadMask} covering
     * the cardPanel, as defined in the cfg property "loadMaskConfig"
     */
    showLoadMask : function(show, type)
    {
        if (!type) {
            type = 'default';
        }

        if (show) {
            if (this.loadMask == null) {
                this.loadMask = new Ext.LoadMask(this.body);
            }
            this.loadMask.msg = this.loadMaskConfig[type];
            this.loadMask.show();
        } else {
            if (this.loadMask) {
                this.loadMask.hide();
            }
        }
    },


    /**
     * Inits the listener for the various {@link Ext.ux.Wiz.Card}s used
     * by this component.
     */
    initEvents : function()
    {
        Ext.ux.Wiz.superclass.initEvents.call(this);

        this.on('beforeclose', this.onBeforeClose, this);
    },

    /**
     * Creates the head- and the card-panel.
     * Be sure to have the custom {@link Ext.ux.layout.CardLayout} available
     * in order to make the card-panel work as expected by this component
     * ({@link http://www.siteartwork.de/cardlayout}).
     */
    initPanels : function()
    {
        var cards           = this.cards;
        var cardPanelConfig = this.cardPanelConfig;

        Ext.apply(this.headerConfig, {
            steps : cards.length
        });

        this.headPanel = new Ext.ux.Wiz.Header(this.headerConfig);

        Ext.apply(cardPanelConfig, {
            layout : new Ext.ux.layout.CardLayout(),
            items  : cards
        });

        Ext.applyIf(cardPanelConfig, {
            region     : 'center',
            border     : false,
            activeItem : 0
        });

        var cards = this.cards;

        for (var i = 0, len = cards.length; i < len; i++) {
            cards[i].on('show', this.onCardShow, this);
            cards[i].on('hide', this.onCardHide, this);
            cards[i].on('clientvalidation', this.onClientValidation, this);
        }

        this.cardPanel = new Ext.Panel(cardPanelConfig);
    },

    /**
     * Creates the instances for the the window buttons.
     */
    initButtons : function()
    {
        this.previousButton = new Ext.Button({
            text     : this.previousButtonText,
            disabled : true,
            minWidth : 75,
            handler  : this.onPreviousClick,
            scope    : this
        });

        this.nextButton = new Ext.Button({
            text     : this.nextButtonText,
            minWidth : 75,
            handler  : this.onNextClick,
            scope    : this
        });

        this.cancelButton = new Ext.Button({
            text     : this.cancelButtonText,
            handler  : this.onCancelClick,
            scope    : this,
            minWidth : 75
        });
    },

// -------- listeners

    /**
     * Listener for the beforeclose event.
     * This listener will return true or false based on the "closable"
     * property by this component. This property will be changed by the "switchDialogState"
     * method, indicating if there is currently any process running that should prevent
     * this dialog from being closed.
     *
     * @param {Ext.Panel} panel The panel being closed
     *
     * @return {Boolean}
     */
    onBeforeClose : function(panel)
    {
        return this.closable;
    },

    /**
     * By default, the card firing this event monitors user input in a frequent
     * interval and fires the 'clientvalidation'-event along with it. This listener
     * will enable/disable the next/finish-button in accordance with it, based upon
     * the parameter isValid. isValid" will be set by the form validation and depends
     * on the validators you are using for the different input-elemnts in your form.
     * If the card does not contain any forms, this listener will never be called by the
     * card itself.
     *
     * @param {Ext.ux.Wiz.Card} The card that triggered the event.
     * @param {Boolean} isValid "true", if the user input was valid, otherwise
     * "false"
     */
    onClientValidation : function(card, isValid)
    {
        if (!isValid) {
            this.nextButton.setDisabled(true);
        } else {
            this.nextButton.setDisabled(false);
        }
    },

    /**
     * This will render the "next" button as disabled since the bindHandler's delay
     * of the next card to show might be lagging on slower systems
     *
     */
    onCardHide : function(card)
    {
        if (this.cardPanel.layout.activeItem.id === card.id) {
            this.nextButton.setDisabled(true);
        }
    },


    /**
     * Listener for the "show" event of the card that gets shown in the card-panel.
     * Renders the next/previous buttons based on the position of the card in the wizard
     * and updates the head-panel accordingly.
     *
     * @param {Ext.ux.Wiz.Card} The card being shown.
     */
    onCardShow : function(card)
    {
        var parent = card.ownerCt;

        var items = parent.items;

        for (var i = 0, len = items.length; i < len; i++) {
            if (items.get(i).id == card.id) {
                break;
            }
        }

        this.currentCard = i;
        this.headPanel.updateStep(i, card.title);

        if (i == len-1) {
            this.nextButton.setText(this.finishButtonText);
        } else {
            this.nextButton.setText(this.nextButtonText);
        }

        if (card.isValid()) {
            this.nextButton.setDisabled(false);
        }

        if (i == 0) {
            this.previousButton.setDisabled(true);
        } else {
            this.previousButton.setDisabled(false);
        }

    },


    /**
     * Fires the 'cancel'-event. Closes this dialog if the return value of the
     * listeners does not equal to "false".
     */
    onCancelClick : function()
    {
        if (this.fireEvent('cancel', this) !== false) {
            this.close();
        }
    },

    /**
     * Fires the 'finish'-event. Closes this dialog if the return value of the
     * listeners does not equal to "false".
     */
    onFinish : function()
    {
        if (this.fireEvent('finish', this, this.getWizardData()) !== false) {
            this.close();
        }
    },

    /**
     * Listener for the previous-button.
     * Switches to the previous displayed {@link Ext.ux.Wiz.Card}.
     */
    onPreviousClick : function()
    {
        if (this.currentCard > 0) {
            this.cardPanel.getLayout().setActiveItem(this.currentCard - 1);
        }
    },

    /**
     * Listener for the next-button. Switches to the next {@link Ext.ux.Wiz.Card}
     * if the 'beforehide'-method of it did not return false. The functionality
     * for this is implemented in {@link Ext.ux.layout.CardLayout}, which is needed
     * as the layout for the card-panel of this component.
     */
    onNextClick : function()
    {
        if (this.currentCard == this.cardCount-1) {
            this.onFinish();
        } else {
            this.cardPanel.getLayout().setActiveItem(this.currentCard+1);
        }
    }
});



/**
 * Licensed under GNU LESSER GENERAL PUBLIC LICENSE Version 3
 *
 * @author Thorsten Suckow-Homberg <ts@siteartwork.de>
 * @url http://www.siteartwork.de/wizardcomponent
 */

/**
 * @class Ext.ux.Wiz.Card
 * @extends Ext.FormPanel
 *
 * A specific {@link Ext.FormPanel} that can be used as a card in a
 * {@link Ext.ux.Wiz}-component. An instance of this card does only work properly
 * if used in a panel that uses a {@see Ext.layout.CardLayout}-layout.
 *
 * @constructor
 * @param {Object} config The config object
 */
Ext.ux.Wiz.Card = Ext.extend(Ext.FormPanel, {

    /**
     * @cfg {Boolean} header "True" to create the header element. Defaults to
     * "false". See {@link Ext.form.FormPanel#header}
     */
    header : false,

    /**
     * @cfg {Strting} hideMode Hidemode of this component. Defaults to "offsets".
     * See {@link Ext.form.FormPanel#hideMode}
     */
    hideMode : 'display',

    initComponent : function()
    {
        this.addEvents(
            /**
             * @event beforecardhide
             * If you want to add additional checks to your card which cannot be easily done
             * using default validators of input-fields (or using the monitorValid-config option),
             * add your specific listeners to this event.
             * This event gets only fired if the activeItem of the ownerCt-component equals to
             * this instance of {@see Ext.ux.Wiz.Card}. This is needed since a card layout usually
             * hides it's items right after rendering them, involving the beforehide-event.
             * If those checks would be attached to the normal beforehide-event, the card-layout
             * would never be able to hide this component after rendering it, depending on the
             * listeners return value.
             *
             * @param {Ext.ux.Wiz.Card} card The card that triggered the event
             */
            'beforecardhide'
        );


        Ext.ux.Wiz.Card.superclass.initComponent.call(this);

    },

// -------- helper
    isValid : function()
    {
        if (this.monitorValid) {
            return this.bindHandler();
        }

        return true;
    },

// -------- overrides

    /**
     * Overrides parent implementation since we allow to add any element
     * in this component which must not be neccessarily be a form-element.
     * So before a call to "isValid()" is about to be made, this implementation
     * checks first if the specific item sitting in this component has a method "isValid" - if it
     * does not exists, it will be added on the fly.
     */
    bindHandler : function()
    {
        this.form.items.each(function(f){
            if(!f.isValid){
                f.isValid = Ext.emptyFn;
            }
        });

        Ext.ux.Wiz.Card.superclass.bindHandler.call(this);
    },

    /**
     * Overrides parent implementation. This is needed because in case
     * this method uses "monitorValid=true", the method "startMonitoring" must
     * not be called, until the "show"-event of this card fires.
     */
    initEvents : function()
    {
        var old = this.monitorValid;
        this.monitorValid = false;
        Ext.ux.Wiz.Card.superclass.initEvents.call(this);
        this.monitorValid = old;

        this.on('beforehide',     this.bubbleBeforeHideEvent, this);

        this.on('beforecardhide', this.isValid,    this);
        this.on('show',           this.onCardShow, this);
        this.on('hide',           this.onCardHide, this);
    },

// -------- listener
    /**
     * Checks wether the beforecardhide-event may be triggered.
     */
    bubbleBeforeHideEvent : function()
    {
        var ly         = this.ownerCt.layout;
        var activeItem = ly.activeItem;

        if (activeItem && activeItem.id === this.id) {
            return this.fireEvent('beforecardhide', this);
        }

        return true;
    },

    /**
     * Stops monitoring the form elements in this component when the
     * 'hide'-event gets fired.
     */
    onCardHide : function()
    {
        if (this.monitorValid) {
            this.stopMonitoring();
        }
    },

    /**
     * Starts monitoring the form elements in this component when the
     * 'show'-event gets fired.
     */
    onCardShow : function()
    {
        if (this.monitorValid) {
            this.startMonitoring();
        }
    }

});



/**
 * Licensed under GNU LESSER GENERAL PUBLIC LICENSE Version 3
 *
 * @author Thorsten Suckow-Homberg <ts@siteartwork.de>
 * @url http://www.siteartwork.de/wizardcomponent
 */

/**
 * @class Ext.ux.Wiz.Header
 * @extends Ext.BoxComponent
 *
 * A specific {@link Ext.BoxComponent} that can be used to show the current process in an
 * {@link Ext.ux.Wiz}.
 *
 * An instance of this class is usually being created by {@link Ext.ux.Wiz#initPanels} using the
 * {@link Ext.ux.Wiz#headerConfig}-object.
 *
 * @private
 * @constructor
 * @param {Object} config The config object
 */
Ext.ux.Wiz.Header = Ext.extend(Ext.BoxComponent, {

    /**
     * @cfg {Number} height The height of this component. Defaults to "55".
     */
    height : 55,

    /**
     * @cfg {String} region The Region of this component. Since a {@link Ext.ux.Wiz}
     * usually uses a {@link Ext.layout.BorderLayout}, this property defaults to
     * "north". If you want to change this property, you should also change the appropriate
     * css-classes that are used for this component.
     */
    region : 'north',

    /**
     * @cfg {String} title The title that gets rendered in the head of the component. This
     * should be a text describing the purpose of the wizard.
     */
    title : 'Wizard',

    /**
     * @cfg {Number} steps The overall number of steps the user has to go through
     * to finish the wizard.
     */
    steps : 0,

    /**
     * @cfg {String} stepText The text in the header indicating the current process in the wizard.
     * (defaults to "Step {0} of {1}: {2}").
     * {0} is replaced with the index (+1) of the current card, {1} is replaced by the
     * total number of cards in the wizard and {2} is replaced with the title-property of the
     * {@link Ext.ux.Wiz.Card}
     * @type String
     */
    stepText : "Step {0} of {1}: {2}",

    /**
     * @cfg {Object} autoEl The element markup used to render this component.
     */
    autoEl : {
        tag : 'div',
        cls      : 'ext-ux-wiz-Header',
        children : [{
            tag      : 'div',
            cls      : 'ext-ux-wiz-Header-title'
        }, {
            tag  : 'div',
            children : [{
                tag : 'div',
                cls : 'ext-ux-wiz-Header-step'
            }, {
                tag : 'div',
                cls : 'ext-ux-wiz-Header-stepIndicator-container'
            }]
        }]
    },

    /**
     * @param {Ext.Element}
     */
    titleEl : null,

    /**
     * @param {Ext.Element}
     */
    stepEl  : null,

    /**
     * @param {Ext.Element}
     */
    imageContainer : null,

    /**
     * @param {Array}
     */
    indicators : null,

    /**
     * @param {Ext.Template}
     */
    stepTemplate : null,

    /**
     * @param {Number} lastActiveStep Stores the index of the last active card that
     * was shown-
     */
    lastActiveStep : -1,

// -------- helper
    /**
     * Gets called by  {@link Ext.ux.Wiz#onCardShow()} and updates the header
     * with the approppriate information, such as the progress of the wizard
     * (i.e. which card is being shown etc.)
     *
     * @param {Number} currentStep The index of the card currently shown in
     * the wizard
     * @param {String} title The title-property of the {@link Ext.ux.Wiz.Card}
     *
     * @private
     */
    updateStep : function(currentStep, title)
    {
        var html = this.stepTemplate.apply({
            0 : currentStep+1,
            1 : this.steps,
            2 : title
        });

        this.stepEl.update(html);

        if (this.lastActiveStep != -1) {
            this.indicators[this.lastActiveStep].removeClass('ext-ux-wiz-Header-stepIndicator-active');
        }

        this.indicators[currentStep].addClass('ext-ux-wiz-Header-stepIndicator-active');

        this.lastActiveStep = currentStep;
    },


// -------- listener
    /**
     * Overrides parent implementation to render this component properly.
     */
    onRender : function(ct, position)
    {
        Ext.ux.Wiz.Header.superclass.onRender.call(this, ct, position);

        this.indicators   = [];
        this.stepTemplate = new Ext.Template(this.stepText);
        this.stepTemplate.compile();

        var el = this.el.dom.firstChild;
        var ns = el.nextSibling;

        this.titleEl        = new Ext.Element(el);
        this.stepEl         = new Ext.Element(ns.firstChild);
        this.imageContainer = new Ext.Element(ns.lastChild);

        this.titleEl.update(this.title);

        var image = null;
        for (var i = 0, len = this.steps; i < len; i++) {
            image = document.createElement('div');
            image.innerHTML = "&#160;";
            image.className = 'ext-ux-wiz-Header-stepIndicator';
            this.indicators[i] = new Ext.Element(image);
            this.imageContainer.appendChild(image);
        }
    }
});

