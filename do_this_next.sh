#! /usr/bin/env sh

next=~/src/do_this/next.py
todo_folder=~/Dropbox/notes/todo

if [ $# -eq 0 ]
then
    ${next} ${todo_folder}
else
    case $1 in
        edit)
            $EDITOR `${next} --edit ${todo_folder}`
            ;;
        edit-last)
            $EDITOR `${next} --edit --last ${todo_folder}`
            ;;
        last)
            ${next} --last ${todo_folder}
            ;;
        *)
            echo Unknown command: $1
            ;;
    esac
fi

