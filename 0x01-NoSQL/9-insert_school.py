#!/usr/bin/env python3
''' Module for insert a new document '''


def insert_school(mongo_collection, **kwargs):
    ''' insert a new collection '''
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id