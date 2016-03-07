Plié development todo list
--------------------------

Format:

* [docs] [tests] [implementation] feature
    * [docs] [tests] [implementation] sub-feature


::
    [ ][ ][ ] MultiText

    [ ][ ][ ] Text
        [d][t][i] init
        [ ][ ][ ] update
            [ ][ ][ ] text update
            [ ][ ][ ] bounds update
            [ ][ ][ ] generic update
        [ ][ ][ ] display
            [d][t][i] basic functionality
                [d][t][i] left justify
                [d][t][i] centered
                [d][t][i] right justify
            [ ][ ][ ] speed improvements

    [ ][ ][ ] Renderer
        [ ][t][i] init
        [ ][ ][ ] formulate
            [d][t][i] basic formulate (only one char fill)
            [ ][ ][ ] advanced formulate (works with real text objects)
        [ ][ ][ ] display
        [ ][ ][ ] add_view
        [ ][ ][ ] composite

    [d][ ][ ] View
        [d][ ][i] basic init
        [ ][ ][ ] View repr returns a valid view dict
        [ ][ ][ ] Section repr returns a valid section dict
        [ ]   [ ] Decide whether View should start with an empty list
                  for the body, or a list with one Section already in it.

    [ ][ ][ ] Event handling

    [ ][ ][ ] Docs

    [ ][ ][ ] Other


