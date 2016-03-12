Plié development todo list
--------------------------

Format:

* [docs] [tests] [implementation] feature
    * [docs] [tests] [implementation] sub-feature


::
    [ ][ ][ ] MultiText

    [ ][ ][ ] Text
        [d][t][i] init
        [d][ ][ ] update
            [d][ ][i] text update
            [d][ ][i] bounds update
            [ ][ ][ ] generic update
        [ ]   [ ] decide how to handle newlines in Text fields (textwrap.wrap drops them by default
        [ ][ ][ ] display
            [d][t][i] basic functionality
                [d][t][i] left justify
                [d][t][i] centered
                [d][t][i] right justify
            [ ][ ][ ] speed improvements

    [ ][ ][i] Renderer
        [d][t][i] init
        [d][ ][i] formulate
            [d][t][i] basic formulate (only one char fill)
            [d][ ][i] advanced formulate (works with real text objects)
        [d][ ][i] display
        [d][ ][i] add_view
            [ ][ ][ ] inserting of a blank view underneath it if needed
        [d][ ][i] composite
        [d][t][i] _extract_bounds_information
            [ ] decide if bounding boxes can be negative, and what that would mean

    [d][ ][ ] View
        [d][ ][i] basic init
        [ ][ ][ ] View repr returns a valid view dict
        [ ][ ][ ] Section repr returns a valid section dict
        [ ]   [ ] Decide whether View should start with an empty list
                  for the body, or a list with one Section already in it.
        [d][t][i] Sections count as False when empty (__bool__)
        [ ][ ][ ] Write valid view dict specifying grammar
        [ ]   [ ] Decide whether add_view should be replaced by a property of View.view_stack

    [ ][ ][ ] Event handling
        [ ]   [ ] Create mockup
        [ ]   [ ] continue exploring ways to integrate multiple invent systems -cough- asyncio

    [ ][ ][ ] Docs

    [ ][ ][ ] Other


