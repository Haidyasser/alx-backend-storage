#!/usr/bin/env python3
''' Module for function list_all '''


def list_all(mongo_collection):
    ''' Lists all documents in a collection '''
    return list(mongo_collection.find())