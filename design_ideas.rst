Design Ideas
------------

The ideal Plié would be perfectly decoupled from it's display output, so a drop in replacement of the output format would be possible (ex. qt)

Some version of Model View Controller, Model ViewModel View, or presentation abstraction control


Developer's Notes About This Document
____________________________________

* This is a living document / my scratch pad for reasoning about Plié
* Implementation Details: Like a choose your own adventure of library design 
    * Naming scheme: ID<number><letter>[<.number><letter>] 
    * Stands for Implementation Detail, followed by which detail, and then the option specifier for that implementation detail, followed by optional dependent implementation detail, and the option specifier for that dependent implementation detail. 
        * Ex: ID2a1b: ID2 is the overall architecture of the library, a is the PAC based choice, 1 is __________ question, b is _______ choice
    * Basically question number, followed by answer/choice letter. This is for ease of exploring and referring to different options. 
            
    


Implementation Decisions:
_________________________

Some of these are pending. Some are decided. 

* ID1: Format of UIDFT
    * ID1a: UIDFT is a long string with newlines in it. Offset from top left corner is external to UIDFT. UDD splits the UIDFT on newlines, maintaining the indent from the initial offset. All other formatting is handled in the text of the UIDFT. 
    * ID1b: UIDFT is a list of lines. Offset from top left corner is external to UIDFT. UDD prints one list element per line maintaining the indent from the initial offset. All other formatting is handled in the text of the UIDFT lines. 
    * ID1c: Like ID1a except, UIDFT is an object containing both the internal string and the offset. 
    * ID1d: Like ID1b except, UIDFT is an object containing both the list of lines and the offset. 
* ID2: overall architecture of the library
    * ID2a_: PAC based
    * ID2b: MVC based
    * ID2c: MVP based
* ID2a1: whether AMUC does the draw call
    * ID2a1a: AMUC is a pure function, leaving the draw call up to Control
    * ID2a1b: AMUC is a function with side effects, that side effect is the draw call. 
* ID3: Which way Z-depth goes
    * Note: see usability survey results for people's intuition on the matter
    * ID3a: Lower Z-depth numbers mean shallower and therefore more frontwards
    * ID3b: Higher Z-depth numbers means more on top and therefore more frontwards
* ID4: What draws, individual elements or containers of elements
    * ID4a: Individual elements call a draw function and draw just themselves
        * ID4a1a: Uses a shared universal drawing function 
        * ID4a1b: Uses a drawing function intrinsic to that function's type
    * ID4A: Individual elements return or yield a printable format (UIDFT) to the container, and the container then handles arranging and drawing those all. 
* ID5_: How are the neighbors of the children in TIMTF containers stored?
        * ID5a:  In a datastructure in the abstraction of the abstraction of the parents. 
        * ID5b (chosen 11/6): In a graph based system where the children know their neighbors and are updated on changes. 


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
            * Individual Controllers + Router: Router handles the actual input, then sends it to the correct controller, the controller is model/view specific. This means controllers are specialized, which is simpler. But this also means there needs to be a specialized controller for every model/view. Input only goes one place initially, rather than having input handling be handed off, which seems easier in a way.  
            * Individual Controllers: input goes diretly to the specialized controller. Needs some way of keeping track where the input should go, probably through some method of handing off input to the various specialized controllers.  

.. _ID2a:

PAC Architecture details (ID2a):
    * Follow through of input in a PAC architecture, looking specifically at a menu system. Consider a menu with children of menu elements. Each menu element knows its parent. On a keyboard event, a down arrow for example, the currently active menu item processes that event. Processes can mean: do internally or deactivate itself and then pass the event up to it's parent. The parent receives the event, interprets a down arrow as a way of navigating through the menu, then activates the next menu element in the menu and tells it it is selected. Activates means passing input handling responsibility onto it. 
    * What all this means from a broader architectural standpoint? PAC elements are arranged in a tree like graph. Input is received on the leafs, and propagated towards the root of the tree as needed. 
    * Though this example is with a one dimensional menu, it could just as easily work for a 2D menu like thing, like a character field. All that is required is that the menu (or equivalent) knows the layout of whatever it is representing, which is intrinsic to itself. 
    * How drawing works in PAC: Control registers some event requiring drawing or redrawing. Control gets data from Abstraction (flow of execution briefly enters and then exits from abstraction/model component). Control calls AMUC with data from Abstraction (flow of execution enters Presentation). AMUC converts input to UIDFT and then [see options]:
        * ID2a1a: AMUC returns the UIDFT. Flow of execution returns to Control. Control then calls UDD with UIDFT. 
        * ID2a1b: AMUC calls UDD with UIDFT. 


Current presentation component
______________________________

AMUCs, UDD and UIDFT
* UIDFT: Universal Interoperable Drawing Format of Text
    * A format of text that is basically ready for printing in a terminal. It gets passed to the UDD to do the actual printing. 
* UDD: Universal Dumb Drawer
* AMUC: Adapter/Model to UIDFT Converter


universal dumb drawer 
_____________________

This is specifically for terminal rendering 

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


UIDFT - Universal Interoperable Drawing Format of Text
______________________________________________________

* The specification of how to pass text/data from anything that draws to the universal dumb drawer
* See Implementation Detail 1 (ID1a-d)


AMUC - Pure Function Views / Presenters
_______________________________________

* Takes a particular input from a model and then converts that to UIDFT for drawing with the UDD
* Where awareness of screen size is
* could be called Abstraction/Model to UIDFT Converter or AMUC for short

Models / Abstractions
_____________________

* Where the actual data is held

Abstraction Storage Format
__________________________
    
* Design considerations:
    * The idea of an interoperable format that the abstraction outputs seems good

TextBase - An object, with text and styles associated with it. 
    * Styles like background, text color, italic, bold
TextContainer - Is one or more of the following a TextBase or a TextContainer
    * Can hold multiple text objects and containers as needed.
    * Used for creating a bit of text with varied styles in it. 

* choices for the name of the the class of all the things that make up the library
    * widget - overused and annoying, but also seems to be the universal
    * corps - (pronounced kawr) french for body, plays off of Plié as a ballet term
    * pas - (pronounced pah) french for step
    * dispositif - 
    * irality
    * bitoniau(x) - french for little thingy 

Bounds, Offset and Z-Depth Information
_____________________________

    * Held in the abstraction. In PAC element knows and keeps track of its own bounds and offset. It is a policy to respect your bounds, offset and Z-Depth, but not enforced by any mechanism(1). Z-depth is recorded as 0 being the front most (zero depth) and higher numbers are farther back
        (1) This is to allow things to draw outside of their bounds if needed, like in the case of a drop down menu which overlays over the stuff when it pops out. 


Menu Container
______________

* An interactive menu
* Knows the order of the children
* Children are menu elements
* Menu Elements are a bit of text that can handle interactivity, including processing basic input. Like up down arrows, or left right, or enter/back. This allows it to do a little bit of processing. Maybe that means activating whatever the menu element signifies or handing off control to something outside of its scope. 
    * what happens when something is outside of its scope:
        * The menu element defocuses itself, then sends an event (using an atomic message queue) to its parent (the menu container), the menu container receives the event and then processes it. 
        * concrete example: A menu element in a menu of vertically stacked menu elements gets a down arrow. Menu element A defocuses, sends event to parent, parent sees event from menu element A, processes the down arrow as a command to activate and give focus to menu element B. Container sends event to menu element B telling it this. Menu element B processes the event, and then sets up the input handling (gains focus).
* Menu Element base class
    * could handle the basic processing functionality. The actual processing function should be a simple case switch function which delegates out to other functions to actually act on the input given. This way subclasses can override those functions. 
        * Concrete example: the processor detects a down arrow and then calls handle_down_arrow(), that way subclasses can write their own handle_down_arrow(). 


Text Fields
___________

* Places to put text
* Called label in Kivy


Scrollable container
____________________

* It makes whatever is inside of it scrollable (just a neat idea for now)


Tileable Interactive Monoline Text Fields - TIMTF
_________________________________________________

Contains a bit of text with optional styling for editing, only one of each style type per TIMTF

* In abstraction: a bit of text, where it goes, how big the field is, cursor location and what styles should be applied to it
* In control: process input
    * normal letter keys and numbers split on cursor location, then join the left, key and right parts back together
    * arrow keys
        * left and right change decrement or increment the cursor location
            * if cursor decrements below zero, then the PAC element defocuses, and pases the event to parent (so parent can tell the TIMTF to the left that it is now active and its cursor position is on the far right)
            * The converse applies for if the cursor increments past the bounds
        * up and down causes defocus, and passing of the event up to the parent

Tileable Interactive Text Field Container
_________________________________________

* Needs to handle the case where the left most decrements from the left most column and then can't go any farther
* needs to handle the converse for the right most
* needs to handle line splitting/wrapping
    * How is TIMTFs extending over the newline at the end handled.
        * If presentation happened at the container level rather than individual level, then each TIMTF could properly format its own output, and then the container could handle the line wrapping if needed. This would mean TIMTFs wouldn't need to know where they go specifically, instead the container would have to sort that out based on the order and content of all the TIMTFs 
* needs to handle moving between TIMTFs 
* needs to handle TIMTFs changing length and then shifting over the TIMTFs after it

.. _ID5:

Thoughts about children - there seem like two ways to store data about the TITF children of the container:

.. _ID5a:

* In a data structure in the abstraction of the parents. (ID5a)

.. _ID5b:

* In a graph based system where the children know their neighbors and are updated on changes. I like this option better. It potentially descreases coupling. (ID5b)
        
.. _ID5b1: 

* How can the container efficiently iterate over all the children.
        
.. _ID5b1a: 
        
    * One way to is for container control to pull the neighbor out of the TIMTF, and then use that to go to the next TIMTF. This increases coupling because it depends on a consistent storage method for neighbors (stops interchanging of other things in the place of TIMTFs). 
        
.. _ID5b1b: 

    * Another way could be to have a get_neighbor(direction) method in the TIMTF. This gives a consistent interface, which allows interoperablity. This also seems slightly less pythonic, since it uses a getter (and perhaps a setter). One wonders then if there should be an instance property. But that seems weird, since ostensibly it would be an instance property of the control. 
        
.. _ID5b1c: 

    * Another way could be to have a message receiving or an event receiving procedure in the control of the TIMTF through which all exterior communication would happen. Through this protocol the parent TITF container would communicate with the child TIMTF. 
    


