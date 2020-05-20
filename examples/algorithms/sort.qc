use liste
use math

und zwar swap mit ls i1 i2
    hjälp ist ls bei i1
    ls bei i1 ist ls bei i2
    ls bei i2 ist hjälp

und zwar bubble_sort mit ls
    len ist länge ls
    swapped ist uzbl
    das holen wir nach solange swapped
        swapped ist not uzbl
        i ist 0
        das holen wir nach solange i < len - 1
            i ist i + 1
            next ist i + 1
            kris? ls bei next < ls bei i
                swap ls i next
                swapped ist uzbl
    ls und fertig

und zwar merge_sort mit ls
    len ist länge ls

    kris? len < 2
        ls und fertig

    len ist (floor (len / 2)) + 1
    left ist merge_sort (ls bis len)
    right ist merge_sort (ls von len)

    merge left right und fertig

und zwar merge mit left right
    sorted ist liste

    das holen wir nach solange (länge left) und (länge right)
        left bei 1 also lf
        right bei 1 also rf
        kris? lf < rf
            push sorted lf
            lösche left 1
        ach kris.
            push sorted rf
            lösche right 1

    das holen wir nach solange (länge left)
        push sorted (left bei 1)
        lösche left 1

    das holen wir nach solange (länge right)
        push sorted (right bei 1)
        lösche right 1

    sorted und fertig
