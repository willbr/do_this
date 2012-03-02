#! /usr/bin/env sh

next=~/src/do_this/next.py
todo_folder=~/Dropbox/notes/todo

if [ $# -eq 0 ]
then
    ${next} ${todo_folder}
else
    $EDITOR `${next} --edit ${todo_folder}`
fi

