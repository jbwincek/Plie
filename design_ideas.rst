Design Ideas
------------

The ideal Plié would be perfectly decoupled from it's display output, so a drop in replacement of the output format would be possible (ex. qt)

Some version of Model View Controller, Model ViewModel View, or presentation abstraction control


Developers Notes About This Document
____________________________________

    * ID<number><letter> stands for Implementation Detail, followed by which detail, and then the multiple options for that implementation detail. This is for ease of exploring and referring to different options.
    * This is a living document / my scratch pad for reasoning about Plié

universal dumb drawer
_____________________

    * draws UIDFT to the screen
    * be as basic / dumb as possible
        * cleverness should happen in Views / Presenters if at all
    * takes UIDFT and some offset from the top left corner and then draws the text there
        * indentation: split the UIDFT on newlines, and instead of just printing new lines, move the drawing cursor down one line and back to the X offset. This is slight cleverness, but the rule is explicit, and then it lets views/presenters do cleverness like unindent or reindent if they want to. The UDD doesn't have to worry about that.
    * possible alternative implementations:
        * split on newlines in UIDFT input (ID1a)
            * complexity in parsing newlines (that's minor though),
        * UIDFT is a list of lines (ID1b)
            * would newline for each line, but would allow UIDFT to newline midline if needed, I can't think of why that would be needed though.
            * introduces complexity in making UIDFT not just a basically printable string


Universal Interoperable Drawing Format of Text
______________________________________________

    * The specification of how to pass text/data from anything that draws to the universal dumb drawer
    * possible alternative implementations
        * ID1a: UDD splits newlines in the corpus of UIDFT
        * ID1b: UIDFT is a list of lines

Pure Function Views / Presenters
________________________________

    * Takes a particular input from a model and then converts that to UIDFT for drawing with the UDD
    * Where awareness of screen size is
    * could be called Abstraction/Model to UIDFT Converter or AMUC for short

Models / Abstractions
_____________________

    * Where the actual data is held

Library Architecture
____________________

    * Does a model know which view/presenter draws it? A question about the coupling between models/abstractions and views/presenters.
        * In Presentation Abstraction Control (PAC), control would take the abstraction and then pass that to the presentation (view/presenter -- AMUC) to then be drawn. Which means the abstraction/model wouldn't need to know about view/presenter at all.
        * In Model View Controller (MVC), control would tell the model to update the view, so then the model would need know about the view/presenter.
        * In Model View presenter (MVP), the presenter would get the model and then pass that onto the presenter, so the model doesn't know about the view
    * How is input handled?
        * In PAC, the control takes in the input, and then does with it as it sees fit (whether that is update the abstraction/model then presenter/view, or just update the presenter/view). But it is not quite that simple; PAC is hierarchical. So there is a tree of elements. Input events get passed to the control of the leaf PAC element, then if needed they can propagate up the tree (and then down a branch if needed).
        * In MVC, the controller takes in the input and then uses it through the model. This means the way of handling input is coupled with the controller. I can't tell if there's coupling of input handling and the view or model though. Since although the controller takes in all the events, how are those events specified? Like where are they routed from / how does the controller know what they mean. Because the controller has to convert input into commands for the the model or view. It seems like there would need to be three distinct layer objects, one at each layer, for each object in the program. Object in the program means, like a widget. What I mean is layer objects are like the object is represented in the view, model and controller
        * In MVP, the view takes in the input and routes it to the presenter/controller. This means the way of handling input are coupled with the view, but that also means the input handling is decoupled from the presenter/controller. This also necessitates an interface between the view and the presenter/controller which would have to be specified. Because there's an interface between the view and the presenter/controller testing the presenter/controller logic is easier, since one can mock the input over the interface
    * A tale of three layers - each architecture choice has its own pluses and minuses, trade offs and characteristics. In this section we look at how it seems like for many of these options each drawable object or widget or whatever it would be called needs three seperate parts. Although each of these parts do something different —— abstraction/model, control/controller, and view/presenter. —— it is a question in my mind whether these three parts are needed for every object, or if in some architectural choices some parts can be used for all objects or shared between some objects. 
        * Presenter - Abstraction - Control:
            * Because of it's heirarchical system, each PAC element needs a presenter, abstraction and controller
        * Model - View - Controller: 
            * The controller handles input, and then passes events off to models through an interface, which then triggers events in the View. This seems like there is an option for a centralized Controller, let's explore these options:
                * Centralized Controller: handle everything in one place, would require updating for each model or view that's added that needs some new way of being interacted with, general purpose so less duplication, but general purpose also means more complicated. Input only goes one place initially, rather than having input handling be handed off, which seems easier in a way. 
                * Individual Controllers + Router: Router handles the actual input, then sends it to the correct controller, the controller is model/view specific. This means controllers are specialized, which is simplier. But this also means there needs to be a specialized controller for every model/view. Input only goes one place initially, rather than having input handling be handed off, which seems easier in a way.  
                * Individual Controllers: input goes diretly to the specialized controller. Needs some way of keeping track where the input should go, probably through some method of handing off input to the various specialized controllers.  




