# -*- coding: utf-8 -*-

from a3json_struct import struct


class User(struct.JsonStruct):
    username = struct.CharField()

