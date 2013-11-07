trovebox-syncer
===============

A simple one-way photo synchronization tool, which "syncs" all images from a Trovebox account. It will download all raw (original) images and then create symlinks to those originals, based on date (date the photo was taken), and also create "collections" with symlinks for all tags and albums.

Setup needed
------------
* install Trovebox' Python lib (``pip install trovebox``) 
* create OAuth tokens for this application
* configure ``~/.config/trovebox/default`` (with OAuth tokens)
* modify paths in ``__init__`` below (or improve script :-)
