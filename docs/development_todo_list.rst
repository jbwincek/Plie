Plié development todo list
--------------------------

Format:

* [docs] [tests] [implementation] feature
    * [docs] [tests] [implementation] sub-feature


::
    * [d][ ][ ] MultiText
    * [d][ ][ ] Text
        * * [d][t][i] init
        * [d][ ][ ] update
            * [d][ ][i] text update
            * [d][ ][i] bounds update
            * [ ][ ][ ] generic update
        * [ ]   [ ] decide how to handle newlines in Text fields (textwrap.wrap drops them by default
        * [ ][ ][ ] display
            * [d][t][i] basic functionality
                * [d][t][i] left justify
                * [d][t][i] centered
                * [d][t][i] right justify
            * [ ][ ][ ] speed improvements
    * [ ][ ][i] Renderer
        * [d][t][i] init
            * [d][ ][ ] handle passed in terminals
        * [d][ ][i] formulate
            * [d][t][i] basic formulate (only one char fill)
            * [d][ ][i] advanced formulate (works with real text objects)
        * [d][ ][i] display
        * [d][ ][i] add_view
            * [ ][ ][ ] inserting of a blank view underneath it if needed
        * [d][ ][i] composite
        * [d][t][i] _extract_bounds_information
            * [ ] decide if bounding boxes can be negative, and what that would mean
        * [ ][ ][ ] handling of view stacks
            * [ ] resolve the issue with ChainMapss not working with nestled layers of
                  ChainMapss
        * [ ][ ][ ] application of styles
            * [ ][ ][ ] border
            * [ ][ ][ ] background
    * [d][ ][ ] View
        * [d][ ][i] basic init
        * [d][ ][i] View repr returns a valid view dict
        * [d][t][i] Section repr returns a valid section dict
        * [ ]   [ ] Decide whether View should start with an empty list
                  for the body, or a list with one Section already in it.
        * [d][t][i] Sections count as False when empty (__bool__)
        * [ ][ ][ ] Write valid view dict specifying grammar
        * [ ]   [ ] Decide whether add_view should be replaced by a property of View.view_stack
        * [ ][ ][ ] instead of needing to call header.view_object.update or body[0].view_object,
                    View's should have sane defaults setup, so one could just do header.update(),
                    or body.update() and have it pick the only one if there's only one or the first
                    one if there's multiple. Maybe make one body element user selectably primary?
   * [ ][ ][ ] Event handling
        * [ ]   [ ] Create mockup
        * [ ]   [ ] continue exploring ways to integrate multiple invent systems -cough- asyncio
    * [ ][ ][ ] Docs
    * [ ][ ][ ] Navigable
        * [ ] Migrate Navigable stuff into the main project directory
        * [ ][ ][ ] Navigable1D
            * [ ] Document init
            * [ ] Document handles_input
            * [ ] Document up
            * [ ] Document down
            * [ ] Think about how select will actually be used in practice, not just in a mockup
            * [ ] Document select
            * [ ] Address inheritance from ABC Navigable
        * [ ][ ][ ] NavigableMenu
            * [ ][ ][ ] handle highlighting and dehighlighting of selected items

    * [ ][ ][ ] Other
        * [x] learn more about ABCs
        * [ ] use that knowledge in the Renderable ABC
        * [ ] update Text and MultiText to subclass Renderable
        * [x] refine view specifying grammar
            * [ ] examine edge cases
            * [x] write mock ups for different layouts
        * [x] Renderer rewrite
        * [ ] ChainMap with sections for defaults and view inheritance
            - (Note: this was formerly ChainMap for views, but ChainMap as it's programmed, doesn't
              support nested dictionaries.
        * [ ] ScrollableText Renderable
        * [ ] navigable base class
        * [ ] use memoryview's for dictionaries with more lazy production
        * [ ] (after 1.0 release) create a view maker, for easy view creation
        * [ ] (after 1.0 release) create a template engine for views


Profiling results:
    * Start 3/18 12.0s
    * Commit 587040e 3/18 0.168s
    * Commit 4ebb27b 3/20 0.467s (but with more functionality than the last)
    * Commit         3/20 0.267s (CellSpace optimizations

