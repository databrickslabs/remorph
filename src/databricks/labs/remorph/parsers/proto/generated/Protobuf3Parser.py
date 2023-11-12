# Generated from src/databricks/labs/remorph/parsers/proto/Protobuf3.g4 by ANTLR 4.13.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys

if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


def serializedATN():
    return [
        4, 1, 60, 496, 2, 0, 7, 0, 2, 1, 7, 1, 2, 2, 7, 2, 2, 3, 7, 3, 2, 4, 7, 4, 2, 5, 7, 5, 2, 6, 7,
        6, 2, 7, 7, 7, 2, 8, 7, 8, 2, 9, 7, 9, 2, 10, 7, 10, 2, 11, 7, 11, 2, 12, 7, 12, 2, 13, 7, 13,
        2, 14, 7, 14, 2, 15, 7, 15, 2, 16, 7, 16, 2, 17, 7, 17, 2, 18, 7, 18, 2, 19, 7, 19, 2, 20,
        7, 20, 2, 21, 7, 21, 2, 22, 7, 22, 2, 23, 7, 23, 2, 24, 7, 24, 2, 25, 7, 25, 2, 26, 7, 26,
        2, 27, 7, 27, 2, 28, 7, 28, 2, 29, 7, 29, 2, 30, 7, 30, 2, 31, 7, 31, 2, 32, 7, 32, 2, 33,
        7, 33, 2, 34, 7, 34, 2, 35, 7, 35, 2, 36, 7, 36, 2, 37, 7, 37, 2, 38, 7, 38, 2, 39, 7, 39,
        2, 40, 7, 40, 2, 41, 7, 41, 2, 42, 7, 42, 2, 43, 7, 43, 2, 44, 7, 44, 2, 45, 7, 45, 2, 46,
        7, 46, 2, 47, 7, 47, 2, 48, 7, 48, 2, 49, 7, 49, 2, 50, 7, 50, 2, 51, 7, 51, 2, 52, 7, 52,
        1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 5, 0, 113, 8, 0, 10, 0, 12, 0, 116, 9, 0, 1, 0, 1, 0, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 3, 2, 127, 8, 2, 1, 2, 1, 2, 1, 2, 1, 3, 1, 3, 1, 3, 1,
        3, 1, 4, 1, 4, 1, 4, 1, 4, 1, 4, 1, 4, 1, 5, 1, 5, 1, 5, 1, 5, 1, 5, 1, 5, 3, 5, 148, 8, 5, 3,
        5, 150, 8, 5, 1, 6, 1, 6, 1, 7, 3, 7, 155, 8, 7, 1, 7, 1, 7, 1, 7, 1, 7, 1, 7, 1, 7, 1, 7, 1,
        7, 3, 7, 165, 8, 7, 1, 7, 1, 7, 1, 8, 1, 8, 1, 8, 5, 8, 172, 8, 8, 10, 8, 12, 8, 175, 9, 8,
        1, 9, 1, 9, 1, 9, 1, 9, 1, 10, 1, 10, 1, 11, 1, 11, 1, 11, 1, 11, 1, 11, 1, 11, 5, 11, 189,
        8, 11, 10, 11, 12, 11, 192, 9, 11, 1, 11, 1, 11, 1, 12, 1, 12, 1, 12, 1, 12, 1, 12, 1, 12,
        1, 12, 1, 12, 3, 12, 204, 8, 12, 1, 12, 1, 12, 1, 13, 1, 13, 1, 13, 1, 13, 1, 13, 1, 13,
        1, 13, 1, 13, 1, 13, 1, 13, 1, 13, 1, 13, 1, 13, 3, 13, 221, 8, 13, 1, 13, 1, 13, 1, 14,
        1, 14, 1, 15, 1, 15, 1, 15, 1, 15, 1, 15, 1, 15, 1, 15, 1, 15, 1, 15, 1, 15, 1, 15, 1, 15,
        1, 15, 1, 15, 1, 15, 1, 15, 1, 15, 3, 15, 244, 8, 15, 1, 16, 1, 16, 1, 16, 3, 16, 249, 8,
        16, 1, 16, 1, 16, 1, 17, 1, 17, 1, 17, 5, 17, 256, 8, 17, 10, 17, 12, 17, 259, 9, 17, 1,
        18, 1, 18, 1, 18, 1, 18, 3, 18, 265, 8, 18, 3, 18, 267, 8, 18, 1, 19, 1, 19, 1, 19, 5, 19,
        272, 8, 19, 10, 19, 12, 19, 275, 9, 19, 1, 20, 1, 20, 1, 20, 1, 20, 3, 20, 281, 8, 20,
        1, 21, 1, 21, 1, 21, 1, 21, 1, 22, 1, 22, 5, 22, 289, 8, 22, 10, 22, 12, 22, 292, 9, 22,
        1, 22, 1, 22, 1, 23, 1, 23, 1, 23, 3, 23, 299, 8, 23, 1, 24, 1, 24, 1, 24, 3, 24, 304, 8,
        24, 1, 24, 1, 24, 3, 24, 308, 8, 24, 1, 24, 1, 24, 1, 25, 1, 25, 1, 25, 1, 25, 5, 25, 316,
        8, 25, 10, 25, 12, 25, 319, 9, 25, 1, 25, 1, 25, 1, 26, 1, 26, 1, 26, 1, 26, 1, 27, 1, 27,
        1, 27, 1, 27, 1, 28, 1, 28, 5, 28, 333, 8, 28, 10, 28, 12, 28, 336, 9, 28, 1, 28, 1, 28,
        1, 29, 1, 29, 1, 29, 1, 29, 1, 29, 1, 29, 1, 29, 1, 29, 1, 29, 3, 29, 349, 8, 29, 1, 30,
        1, 30, 1, 30, 1, 30, 1, 30, 5, 30, 356, 8, 30, 10, 30, 12, 30, 359, 9, 30, 1, 30, 1, 30,
        1, 31, 1, 31, 1, 31, 1, 31, 5, 31, 367, 8, 31, 10, 31, 12, 31, 370, 9, 31, 1, 31, 1, 31,
        1, 32, 1, 32, 1, 32, 3, 32, 377, 8, 32, 1, 33, 1, 33, 1, 33, 1, 33, 3, 33, 383, 8, 33, 1,
        33, 1, 33, 1, 33, 1, 33, 1, 33, 3, 33, 390, 8, 33, 1, 33, 1, 33, 1, 33, 1, 33, 1, 33, 5,
        33, 397, 8, 33, 10, 33, 12, 33, 400, 9, 33, 1, 33, 1, 33, 3, 33, 404, 8, 33, 1, 34, 1,
        34, 3, 34, 408, 8, 34, 1, 34, 1, 34, 3, 34, 412, 8, 34, 1, 34, 1, 34, 1, 34, 1, 34, 3, 34,
        418, 8, 34, 1, 35, 1, 35, 1, 35, 1, 35, 1, 35, 5, 35, 425, 8, 35, 10, 35, 12, 35, 428,
        9, 35, 1, 35, 1, 35, 1, 36, 1, 36, 1, 37, 1, 37, 3, 37, 436, 8, 37, 1, 38, 1, 38, 1, 38,
        5, 38, 441, 8, 38, 10, 38, 12, 38, 444, 9, 38, 1, 39, 1, 39, 1, 40, 1, 40, 1, 41, 1, 41,
        1, 42, 1, 42, 1, 43, 1, 43, 1, 44, 1, 44, 1, 45, 1, 45, 1, 46, 3, 46, 461, 8, 46, 1, 46,
        1, 46, 1, 46, 5, 46, 466, 8, 46, 10, 46, 12, 46, 469, 9, 46, 1, 46, 1, 46, 1, 47, 3, 47,
        474, 8, 47, 1, 47, 1, 47, 1, 47, 5, 47, 479, 8, 47, 10, 47, 12, 47, 482, 9, 47, 1, 47,
        1, 47, 1, 48, 1, 48, 1, 49, 1, 49, 1, 50, 1, 50, 1, 51, 1, 51, 1, 52, 1, 52, 1, 52, 0, 0,
        53, 0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42,
        44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86,
        88, 90, 92, 94, 96, 98, 100, 102, 104, 0, 7, 1, 0, 36, 37, 1, 0, 3, 4, 1, 0, 7, 8, 1, 0,
        11, 22, 1, 0, 51, 52, 2, 0, 36, 37, 53, 53, 2, 0, 1, 35, 54, 54, 521, 0, 106, 1, 0, 0, 0,
        2, 119, 1, 0, 0, 0, 4, 124, 1, 0, 0, 0, 6, 131, 1, 0, 0, 0, 8, 135, 1, 0, 0, 0, 10, 149, 1,
        0, 0, 0, 12, 151, 1, 0, 0, 0, 14, 154, 1, 0, 0, 0, 16, 168, 1, 0, 0, 0, 18, 176, 1, 0, 0,
        0, 20, 180, 1, 0, 0, 0, 22, 182, 1, 0, 0, 0, 24, 195, 1, 0, 0, 0, 26, 207, 1, 0, 0, 0, 28,
        224, 1, 0, 0, 0, 30, 243, 1, 0, 0, 0, 32, 245, 1, 0, 0, 0, 34, 252, 1, 0, 0, 0, 36, 260,
        1, 0, 0, 0, 38, 268, 1, 0, 0, 0, 40, 280, 1, 0, 0, 0, 42, 282, 1, 0, 0, 0, 44, 286, 1, 0,
        0, 0, 46, 298, 1, 0, 0, 0, 48, 300, 1, 0, 0, 0, 50, 311, 1, 0, 0, 0, 52, 322, 1, 0, 0, 0,
        54, 326, 1, 0, 0, 0, 56, 330, 1, 0, 0, 0, 58, 348, 1, 0, 0, 0, 60, 350, 1, 0, 0, 0, 62, 362,
        1, 0, 0, 0, 64, 376, 1, 0, 0, 0, 66, 378, 1, 0, 0, 0, 68, 417, 1, 0, 0, 0, 70, 419, 1, 0,
        0, 0, 72, 431, 1, 0, 0, 0, 74, 435, 1, 0, 0, 0, 76, 437, 1, 0, 0, 0, 78, 445, 1, 0, 0, 0,
        80, 447, 1, 0, 0, 0, 82, 449, 1, 0, 0, 0, 84, 451, 1, 0, 0, 0, 86, 453, 1, 0, 0, 0, 88, 455,
        1, 0, 0, 0, 90, 457, 1, 0, 0, 0, 92, 460, 1, 0, 0, 0, 94, 473, 1, 0, 0, 0, 96, 485, 1, 0,
        0, 0, 98, 487, 1, 0, 0, 0, 100, 489, 1, 0, 0, 0, 102, 491, 1, 0, 0, 0, 104, 493, 1, 0, 0,
        0, 106, 114, 3, 2, 1, 0, 107, 113, 3, 4, 2, 0, 108, 113, 3, 6, 3, 0, 109, 113, 3, 8, 4,
        0, 110, 113, 3, 40, 20, 0, 111, 113, 3, 72, 36, 0, 112, 107, 1, 0, 0, 0, 112, 108, 1,
        0, 0, 0, 112, 109, 1, 0, 0, 0, 112, 110, 1, 0, 0, 0, 112, 111, 1, 0, 0, 0, 113, 116, 1,
        0, 0, 0, 114, 112, 1, 0, 0, 0, 114, 115, 1, 0, 0, 0, 115, 117, 1, 0, 0, 0, 116, 114, 1,
        0, 0, 0, 117, 118, 5, 0, 0, 1, 118, 1, 1, 0, 0, 0, 119, 120, 5, 1, 0, 0, 120, 121, 5, 39,
        0, 0, 121, 122, 7, 0, 0, 0, 122, 123, 5, 38, 0, 0, 123, 3, 1, 0, 0, 0, 124, 126, 5, 2, 0,
        0, 125, 127, 7, 1, 0, 0, 126, 125, 1, 0, 0, 0, 126, 127, 1, 0, 0, 0, 127, 128, 1, 0, 0,
        0, 128, 129, 3, 98, 49, 0, 129, 130, 5, 38, 0, 0, 130, 5, 1, 0, 0, 0, 131, 132, 5, 5, 0,
        0, 132, 133, 3, 76, 38, 0, 133, 134, 5, 38, 0, 0, 134, 7, 1, 0, 0, 0, 135, 136, 5, 6, 0,
        0, 136, 137, 3, 10, 5, 0, 137, 138, 5, 39, 0, 0, 138, 139, 3, 68, 34, 0, 139, 140, 5,
        38, 0, 0, 140, 9, 1, 0, 0, 0, 141, 150, 3, 76, 38, 0, 142, 143, 5, 40, 0, 0, 143, 144,
        3, 76, 38, 0, 144, 147, 5, 41, 0, 0, 145, 146, 5, 48, 0, 0, 146, 148, 3, 76, 38, 0, 147,
        145, 1, 0, 0, 0, 147, 148, 1, 0, 0, 0, 148, 150, 1, 0, 0, 0, 149, 141, 1, 0, 0, 0, 149,
        142, 1, 0, 0, 0, 150, 11, 1, 0, 0, 0, 151, 152, 7, 2, 0, 0, 152, 13, 1, 0, 0, 0, 153, 155,
        3, 12, 6, 0, 154, 153, 1, 0, 0, 0, 154, 155, 1, 0, 0, 0, 155, 156, 1, 0, 0, 0, 156, 157,
        3, 30, 15, 0, 157, 158, 3, 82, 41, 0, 158, 159, 5, 39, 0, 0, 159, 164, 3, 20, 10, 0, 160,
        161, 5, 42, 0, 0, 161, 162, 3, 16, 8, 0, 162, 163, 5, 43, 0, 0, 163, 165, 1, 0, 0, 0, 164,
        160, 1, 0, 0, 0, 164, 165, 1, 0, 0, 0, 165, 166, 1, 0, 0, 0, 166, 167, 5, 38, 0, 0, 167,
        15, 1, 0, 0, 0, 168, 173, 3, 18, 9, 0, 169, 170, 5, 49, 0, 0, 170, 172, 3, 18, 9, 0, 171,
        169, 1, 0, 0, 0, 172, 175, 1, 0, 0, 0, 173, 171, 1, 0, 0, 0, 173, 174, 1, 0, 0, 0, 174,
        17, 1, 0, 0, 0, 175, 173, 1, 0, 0, 0, 176, 177, 3, 10, 5, 0, 177, 178, 5, 39, 0, 0, 178,
        179, 3, 68, 34, 0, 179, 19, 1, 0, 0, 0, 180, 181, 3, 96, 48, 0, 181, 21, 1, 0, 0, 0, 182,
        183, 5, 9, 0, 0, 183, 184, 3, 84, 42, 0, 184, 190, 5, 44, 0, 0, 185, 189, 3, 8, 4, 0, 186,
        189, 3, 24, 12, 0, 187, 189, 3, 72, 36, 0, 188, 185, 1, 0, 0, 0, 188, 186, 1, 0, 0, 0,
        188, 187, 1, 0, 0, 0, 189, 192, 1, 0, 0, 0, 190, 188, 1, 0, 0, 0, 190, 191, 1, 0, 0, 0,
        191, 193, 1, 0, 0, 0, 192, 190, 1, 0, 0, 0, 193, 194, 5, 45, 0, 0, 194, 23, 1, 0, 0, 0,
        195, 196, 3, 30, 15, 0, 196, 197, 3, 82, 41, 0, 197, 198, 5, 39, 0, 0, 198, 203, 3, 20,
        10, 0, 199, 200, 5, 42, 0, 0, 200, 201, 3, 16, 8, 0, 201, 202, 5, 43, 0, 0, 202, 204,
        1, 0, 0, 0, 203, 199, 1, 0, 0, 0, 203, 204, 1, 0, 0, 0, 204, 205, 1, 0, 0, 0, 205, 206,
        5, 38, 0, 0, 206, 25, 1, 0, 0, 0, 207, 208, 5, 10, 0, 0, 208, 209, 5, 46, 0, 0, 209, 210,
        3, 28, 14, 0, 210, 211, 5, 49, 0, 0, 211, 212, 3, 30, 15, 0, 212, 213, 5, 47, 0, 0, 213,
        214, 3, 86, 43, 0, 214, 215, 5, 39, 0, 0, 215, 220, 3, 20, 10, 0, 216, 217, 5, 42, 0,
        0, 217, 218, 3, 16, 8, 0, 218, 219, 5, 43, 0, 0, 219, 221, 1, 0, 0, 0, 220, 216, 1, 0,
        0, 0, 220, 221, 1, 0, 0, 0, 221, 222, 1, 0, 0, 0, 222, 223, 5, 38, 0, 0, 223, 27, 1, 0,
        0, 0, 224, 225, 7, 3, 0, 0, 225, 29, 1, 0, 0, 0, 226, 244, 5, 23, 0, 0, 227, 244, 5, 24,
        0, 0, 228, 244, 5, 11, 0, 0, 229, 244, 5, 12, 0, 0, 230, 244, 5, 13, 0, 0, 231, 244, 5,
        14, 0, 0, 232, 244, 5, 15, 0, 0, 233, 244, 5, 16, 0, 0, 234, 244, 5, 17, 0, 0, 235, 244,
        5, 18, 0, 0, 236, 244, 5, 19, 0, 0, 237, 244, 5, 20, 0, 0, 238, 244, 5, 21, 0, 0, 239,
        244, 5, 22, 0, 0, 240, 244, 5, 25, 0, 0, 241, 244, 3, 92, 46, 0, 242, 244, 3, 94, 47,
        0, 243, 226, 1, 0, 0, 0, 243, 227, 1, 0, 0, 0, 243, 228, 1, 0, 0, 0, 243, 229, 1, 0, 0,
        0, 243, 230, 1, 0, 0, 0, 243, 231, 1, 0, 0, 0, 243, 232, 1, 0, 0, 0, 243, 233, 1, 0, 0,
        0, 243, 234, 1, 0, 0, 0, 243, 235, 1, 0, 0, 0, 243, 236, 1, 0, 0, 0, 243, 237, 1, 0, 0,
        0, 243, 238, 1, 0, 0, 0, 243, 239, 1, 0, 0, 0, 243, 240, 1, 0, 0, 0, 243, 241, 1, 0, 0,
        0, 243, 242, 1, 0, 0, 0, 244, 31, 1, 0, 0, 0, 245, 248, 5, 26, 0, 0, 246, 249, 3, 34, 17,
        0, 247, 249, 3, 38, 19, 0, 248, 246, 1, 0, 0, 0, 248, 247, 1, 0, 0, 0, 249, 250, 1, 0,
        0, 0, 250, 251, 5, 38, 0, 0, 251, 33, 1, 0, 0, 0, 252, 257, 3, 36, 18, 0, 253, 254, 5,
        49, 0, 0, 254, 256, 3, 36, 18, 0, 255, 253, 1, 0, 0, 0, 256, 259, 1, 0, 0, 0, 257, 255,
        1, 0, 0, 0, 257, 258, 1, 0, 0, 0, 258, 35, 1, 0, 0, 0, 259, 257, 1, 0, 0, 0, 260, 266, 3,
        96, 48, 0, 261, 264, 5, 27, 0, 0, 262, 265, 3, 96, 48, 0, 263, 265, 5, 28, 0, 0, 264,
        262, 1, 0, 0, 0, 264, 263, 1, 0, 0, 0, 265, 267, 1, 0, 0, 0, 266, 261, 1, 0, 0, 0, 266,
        267, 1, 0, 0, 0, 267, 37, 1, 0, 0, 0, 268, 273, 3, 98, 49, 0, 269, 270, 5, 49, 0, 0, 270,
        272, 3, 98, 49, 0, 271, 269, 1, 0, 0, 0, 272, 275, 1, 0, 0, 0, 273, 271, 1, 0, 0, 0, 273,
        274, 1, 0, 0, 0, 274, 39, 1, 0, 0, 0, 275, 273, 1, 0, 0, 0, 276, 281, 3, 54, 27, 0, 277,
        281, 3, 42, 21, 0, 278, 281, 3, 60, 30, 0, 279, 281, 3, 62, 31, 0, 280, 276, 1, 0, 0,
        0, 280, 277, 1, 0, 0, 0, 280, 278, 1, 0, 0, 0, 280, 279, 1, 0, 0, 0, 281, 41, 1, 0, 0, 0,
        282, 283, 5, 29, 0, 0, 283, 284, 3, 80, 40, 0, 284, 285, 3, 44, 22, 0, 285, 43, 1, 0,
        0, 0, 286, 290, 5, 44, 0, 0, 287, 289, 3, 46, 23, 0, 288, 287, 1, 0, 0, 0, 289, 292, 1,
        0, 0, 0, 290, 288, 1, 0, 0, 0, 290, 291, 1, 0, 0, 0, 291, 293, 1, 0, 0, 0, 292, 290, 1,
        0, 0, 0, 293, 294, 5, 45, 0, 0, 294, 45, 1, 0, 0, 0, 295, 299, 3, 8, 4, 0, 296, 299, 3,
        48, 24, 0, 297, 299, 3, 72, 36, 0, 298, 295, 1, 0, 0, 0, 298, 296, 1, 0, 0, 0, 298, 297,
        1, 0, 0, 0, 299, 47, 1, 0, 0, 0, 300, 301, 3, 74, 37, 0, 301, 303, 5, 39, 0, 0, 302, 304,
        5, 52, 0, 0, 303, 302, 1, 0, 0, 0, 303, 304, 1, 0, 0, 0, 304, 305, 1, 0, 0, 0, 305, 307,
        3, 96, 48, 0, 306, 308, 3, 50, 25, 0, 307, 306, 1, 0, 0, 0, 307, 308, 1, 0, 0, 0, 308,
        309, 1, 0, 0, 0, 309, 310, 5, 38, 0, 0, 310, 49, 1, 0, 0, 0, 311, 312, 5, 42, 0, 0, 312,
        317, 3, 52, 26, 0, 313, 314, 5, 49, 0, 0, 314, 316, 3, 52, 26, 0, 315, 313, 1, 0, 0, 0,
        316, 319, 1, 0, 0, 0, 317, 315, 1, 0, 0, 0, 317, 318, 1, 0, 0, 0, 318, 320, 1, 0, 0, 0,
        319, 317, 1, 0, 0, 0, 320, 321, 5, 43, 0, 0, 321, 51, 1, 0, 0, 0, 322, 323, 3, 10, 5, 0,
        323, 324, 5, 39, 0, 0, 324, 325, 3, 68, 34, 0, 325, 53, 1, 0, 0, 0, 326, 327, 5, 30, 0,
        0, 327, 328, 3, 78, 39, 0, 328, 329, 3, 56, 28, 0, 329, 55, 1, 0, 0, 0, 330, 334, 5, 44,
        0, 0, 331, 333, 3, 58, 29, 0, 332, 331, 1, 0, 0, 0, 333, 336, 1, 0, 0, 0, 334, 332, 1,
        0, 0, 0, 334, 335, 1, 0, 0, 0, 335, 337, 1, 0, 0, 0, 336, 334, 1, 0, 0, 0, 337, 338, 5,
        45, 0, 0, 338, 57, 1, 0, 0, 0, 339, 349, 3, 14, 7, 0, 340, 349, 3, 42, 21, 0, 341, 349,
        3, 54, 27, 0, 342, 349, 3, 60, 30, 0, 343, 349, 3, 8, 4, 0, 344, 349, 3, 22, 11, 0, 345,
        349, 3, 26, 13, 0, 346, 349, 3, 32, 16, 0, 347, 349, 3, 72, 36, 0, 348, 339, 1, 0, 0,
        0, 348, 340, 1, 0, 0, 0, 348, 341, 1, 0, 0, 0, 348, 342, 1, 0, 0, 0, 348, 343, 1, 0, 0,
        0, 348, 344, 1, 0, 0, 0, 348, 345, 1, 0, 0, 0, 348, 346, 1, 0, 0, 0, 348, 347, 1, 0, 0,
        0, 349, 59, 1, 0, 0, 0, 350, 351, 5, 32, 0, 0, 351, 352, 3, 92, 46, 0, 352, 357, 5, 44,
        0, 0, 353, 356, 3, 14, 7, 0, 354, 356, 3, 72, 36, 0, 355, 353, 1, 0, 0, 0, 355, 354, 1,
        0, 0, 0, 356, 359, 1, 0, 0, 0, 357, 355, 1, 0, 0, 0, 357, 358, 1, 0, 0, 0, 358, 360, 1,
        0, 0, 0, 359, 357, 1, 0, 0, 0, 360, 361, 5, 45, 0, 0, 361, 61, 1, 0, 0, 0, 362, 363, 5,
        31, 0, 0, 363, 364, 3, 88, 44, 0, 364, 368, 5, 44, 0, 0, 365, 367, 3, 64, 32, 0, 366,
        365, 1, 0, 0, 0, 367, 370, 1, 0, 0, 0, 368, 366, 1, 0, 0, 0, 368, 369, 1, 0, 0, 0, 369,
        371, 1, 0, 0, 0, 370, 368, 1, 0, 0, 0, 371, 372, 5, 45, 0, 0, 372, 63, 1, 0, 0, 0, 373,
        377, 3, 8, 4, 0, 374, 377, 3, 66, 33, 0, 375, 377, 3, 72, 36, 0, 376, 373, 1, 0, 0, 0,
        376, 374, 1, 0, 0, 0, 376, 375, 1, 0, 0, 0, 377, 65, 1, 0, 0, 0, 378, 379, 5, 33, 0, 0,
        379, 380, 3, 90, 45, 0, 380, 382, 5, 40, 0, 0, 381, 383, 5, 34, 0, 0, 382, 381, 1, 0,
        0, 0, 382, 383, 1, 0, 0, 0, 383, 384, 1, 0, 0, 0, 384, 385, 3, 92, 46, 0, 385, 386, 5,
        41, 0, 0, 386, 387, 5, 35, 0, 0, 387, 389, 5, 40, 0, 0, 388, 390, 5, 34, 0, 0, 389, 388,
        1, 0, 0, 0, 389, 390, 1, 0, 0, 0, 390, 391, 1, 0, 0, 0, 391, 392, 3, 92, 46, 0, 392, 403,
        5, 41, 0, 0, 393, 398, 5, 44, 0, 0, 394, 397, 3, 8, 4, 0, 395, 397, 3, 72, 36, 0, 396,
        394, 1, 0, 0, 0, 396, 395, 1, 0, 0, 0, 397, 400, 1, 0, 0, 0, 398, 396, 1, 0, 0, 0, 398,
        399, 1, 0, 0, 0, 399, 401, 1, 0, 0, 0, 400, 398, 1, 0, 0, 0, 401, 404, 5, 45, 0, 0, 402,
        404, 5, 38, 0, 0, 403, 393, 1, 0, 0, 0, 403, 402, 1, 0, 0, 0, 404, 67, 1, 0, 0, 0, 405,
        418, 3, 76, 38, 0, 406, 408, 7, 4, 0, 0, 407, 406, 1, 0, 0, 0, 407, 408, 1, 0, 0, 0, 408,
        409, 1, 0, 0, 0, 409, 418, 3, 96, 48, 0, 410, 412, 7, 4, 0, 0, 411, 410, 1, 0, 0, 0, 411,
        412, 1, 0, 0, 0, 412, 413, 1, 0, 0, 0, 413, 418, 3, 102, 51, 0, 414, 418, 3, 98, 49, 0,
        415, 418, 3, 100, 50, 0, 416, 418, 3, 70, 35, 0, 417, 405, 1, 0, 0, 0, 417, 407, 1, 0,
        0, 0, 417, 411, 1, 0, 0, 0, 417, 414, 1, 0, 0, 0, 417, 415, 1, 0, 0, 0, 417, 416, 1, 0,
        0, 0, 418, 69, 1, 0, 0, 0, 419, 426, 5, 44, 0, 0, 420, 421, 3, 74, 37, 0, 421, 422, 5,
        50, 0, 0, 422, 423, 3, 68, 34, 0, 423, 425, 1, 0, 0, 0, 424, 420, 1, 0, 0, 0, 425, 428,
        1, 0, 0, 0, 426, 424, 1, 0, 0, 0, 426, 427, 1, 0, 0, 0, 427, 429, 1, 0, 0, 0, 428, 426,
        1, 0, 0, 0, 429, 430, 5, 45, 0, 0, 430, 71, 1, 0, 0, 0, 431, 432, 5, 38, 0, 0, 432, 73,
        1, 0, 0, 0, 433, 436, 5, 57, 0, 0, 434, 436, 3, 104, 52, 0, 435, 433, 1, 0, 0, 0, 435,
        434, 1, 0, 0, 0, 436, 75, 1, 0, 0, 0, 437, 442, 3, 74, 37, 0, 438, 439, 5, 48, 0, 0, 439,
        441, 3, 74, 37, 0, 440, 438, 1, 0, 0, 0, 441, 444, 1, 0, 0, 0, 442, 440, 1, 0, 0, 0, 442,
        443, 1, 0, 0, 0, 443, 77, 1, 0, 0, 0, 444, 442, 1, 0, 0, 0, 445, 446, 3, 74, 37, 0, 446,
        79, 1, 0, 0, 0, 447, 448, 3, 74, 37, 0, 448, 81, 1, 0, 0, 0, 449, 450, 3, 74, 37, 0, 450,
        83, 1, 0, 0, 0, 451, 452, 3, 74, 37, 0, 452, 85, 1, 0, 0, 0, 453, 454, 3, 74, 37, 0, 454,
        87, 1, 0, 0, 0, 455, 456, 3, 74, 37, 0, 456, 89, 1, 0, 0, 0, 457, 458, 3, 74, 37, 0, 458,
        91, 1, 0, 0, 0, 459, 461, 5, 48, 0, 0, 460, 459, 1, 0, 0, 0, 460, 461, 1, 0, 0, 0, 461,
        467, 1, 0, 0, 0, 462, 463, 3, 74, 37, 0, 463, 464, 5, 48, 0, 0, 464, 466, 1, 0, 0, 0, 465,
        462, 1, 0, 0, 0, 466, 469, 1, 0, 0, 0, 467, 465, 1, 0, 0, 0, 467, 468, 1, 0, 0, 0, 468,
        470, 1, 0, 0, 0, 469, 467, 1, 0, 0, 0, 470, 471, 3, 78, 39, 0, 471, 93, 1, 0, 0, 0, 472,
        474, 5, 48, 0, 0, 473, 472, 1, 0, 0, 0, 473, 474, 1, 0, 0, 0, 474, 480, 1, 0, 0, 0, 475,
        476, 3, 74, 37, 0, 476, 477, 5, 48, 0, 0, 477, 479, 1, 0, 0, 0, 478, 475, 1, 0, 0, 0, 479,
        482, 1, 0, 0, 0, 480, 478, 1, 0, 0, 0, 480, 481, 1, 0, 0, 0, 481, 483, 1, 0, 0, 0, 482,
        480, 1, 0, 0, 0, 483, 484, 3, 80, 40, 0, 484, 95, 1, 0, 0, 0, 485, 486, 5, 56, 0, 0, 486,
        97, 1, 0, 0, 0, 487, 488, 7, 5, 0, 0, 488, 99, 1, 0, 0, 0, 489, 490, 5, 54, 0, 0, 490, 101,
        1, 0, 0, 0, 491, 492, 5, 55, 0, 0, 492, 103, 1, 0, 0, 0, 493, 494, 7, 6, 0, 0, 494, 105,
        1, 0, 0, 0, 45, 112, 114, 126, 147, 149, 154, 164, 173, 188, 190, 203, 220, 243, 248,
        257, 264, 266, 273, 280, 290, 298, 303, 307, 317, 334, 348, 355, 357, 368, 376,
        382, 389, 396, 398, 403, 407, 411, 417, 426, 435, 442, 460, 467, 473, 480
    ]


class Protobuf3Parser(Parser):
    grammarFileName = "Protobuf3.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [DFA(ds, i) for i, ds in enumerate(atn.decisionToState)]

    sharedContextCache = PredictionContextCache()

    literalNames = ["<INVALID>", "'syntax'", "'import'", "'weak'", "'public'",
                    "'package'", "'option'", "'optional'", "'repeated'",
                    "'oneof'", "'map'", "'int32'", "'int64'", "'uint32'",
                    "'uint64'", "'sint32'", "'sint64'", "'fixed32'", "'fixed64'",
                    "'sfixed32'", "'sfixed64'", "'bool'", "'string'", "'double'",
                    "'float'", "'bytes'", "'reserved'", "'to'", "'max'",
                    "'enum'", "'message'", "'service'", "'extend'", "'rpc'",
                    "'stream'", "'returns'", "'\"proto3\"'", "''proto3''",
                    "';'", "'='", "'('", "')'", "'['", "']'", "'{'", "'}'",
                    "'<'", "'>'", "'.'", "','", "':'", "'+'", "'-'"]

    symbolicNames = ["<INVALID>", "SYNTAX", "IMPORT", "WEAK", "PUBLIC",
                     "PACKAGE", "OPTION", "OPTIONAL", "REPEATED", "ONEOF",
                     "MAP", "INT32", "INT64", "UINT32", "UINT64", "SINT32",
                     "SINT64", "FIXED32", "FIXED64", "SFIXED32", "SFIXED64",
                     "BOOL", "STRING", "DOUBLE", "FLOAT", "BYTES", "RESERVED",
                     "TO", "MAX", "ENUM", "MESSAGE", "SERVICE", "EXTEND",
                     "RPC", "STREAM", "RETURNS", "PROTO3_LIT_SINGLE", "PROTO3_LIT_DOBULE",
                     "SEMI", "EQ", "LP", "RP", "LB", "RB", "LC", "RC",
                     "LT", "GT", "DOT", "COMMA", "COLON", "PLUS", "MINUS",
                     "STR_LIT", "BOOL_LIT", "FLOAT_LIT", "INT_LIT", "IDENTIFIER",
                     "WS", "LINE_COMMENT", "COMMENT"]

    RULE_proto = 0
    RULE_syntax = 1
    RULE_importStatement = 2
    RULE_packageStatement = 3
    RULE_optionStatement = 4
    RULE_optionName = 5
    RULE_fieldLabel = 6
    RULE_field = 7
    RULE_fieldOptions = 8
    RULE_fieldOption = 9
    RULE_fieldNumber = 10
    RULE_oneof = 11
    RULE_oneofField = 12
    RULE_mapField = 13
    RULE_keyType = 14
    RULE_type_ = 15
    RULE_reserved = 16
    RULE_ranges = 17
    RULE_range_ = 18
    RULE_reservedFieldNames = 19
    RULE_topLevelDef = 20
    RULE_enumDef = 21
    RULE_enumBody = 22
    RULE_enumElement = 23
    RULE_enumField = 24
    RULE_enumValueOptions = 25
    RULE_enumValueOption = 26
    RULE_messageDef = 27
    RULE_messageBody = 28
    RULE_messageElement = 29
    RULE_extendDef = 30
    RULE_serviceDef = 31
    RULE_serviceElement = 32
    RULE_rpc = 33
    RULE_constant = 34
    RULE_blockLit = 35
    RULE_emptyStatement_ = 36
    RULE_ident = 37
    RULE_fullIdent = 38
    RULE_messageName = 39
    RULE_enumName = 40
    RULE_fieldName = 41
    RULE_oneofName = 42
    RULE_mapName = 43
    RULE_serviceName = 44
    RULE_rpcName = 45
    RULE_messageType = 46
    RULE_enumType = 47
    RULE_intLit = 48
    RULE_strLit = 49
    RULE_boolLit = 50
    RULE_floatLit = 51
    RULE_keywords = 52

    ruleNames = ["proto", "syntax", "importStatement", "packageStatement",
                 "optionStatement", "optionName", "fieldLabel", "field",
                 "fieldOptions", "fieldOption", "fieldNumber", "oneof",
                 "oneofField", "mapField", "keyType", "type_", "reserved",
                 "ranges", "range_", "reservedFieldNames", "topLevelDef",
                 "enumDef", "enumBody", "enumElement", "enumField", "enumValueOptions",
                 "enumValueOption", "messageDef", "messageBody", "messageElement",
                 "extendDef", "serviceDef", "serviceElement", "rpc", "constant",
                 "blockLit", "emptyStatement_", "ident", "fullIdent",
                 "messageName", "enumName", "fieldName", "oneofName",
                 "mapName", "serviceName", "rpcName", "messageType", "enumType",
                 "intLit", "strLit", "boolLit", "floatLit", "keywords"]

    EOF = Token.EOF
    SYNTAX = 1
    IMPORT = 2
    WEAK = 3
    PUBLIC = 4
    PACKAGE = 5
    OPTION = 6
    OPTIONAL = 7
    REPEATED = 8
    ONEOF = 9
    MAP = 10
    INT32 = 11
    INT64 = 12
    UINT32 = 13
    UINT64 = 14
    SINT32 = 15
    SINT64 = 16
    FIXED32 = 17
    FIXED64 = 18
    SFIXED32 = 19
    SFIXED64 = 20
    BOOL = 21
    STRING = 22
    DOUBLE = 23
    FLOAT = 24
    BYTES = 25
    RESERVED = 26
    TO = 27
    MAX = 28
    ENUM = 29
    MESSAGE = 30
    SERVICE = 31
    EXTEND = 32
    RPC = 33
    STREAM = 34
    RETURNS = 35
    PROTO3_LIT_SINGLE = 36
    PROTO3_LIT_DOBULE = 37
    SEMI = 38
    EQ = 39
    LP = 40
    RP = 41
    LB = 42
    RB = 43
    LC = 44
    RC = 45
    LT = 46
    GT = 47
    DOT = 48
    COMMA = 49
    COLON = 50
    PLUS = 51
    MINUS = 52
    STR_LIT = 53
    BOOL_LIT = 54
    FLOAT_LIT = 55
    INT_LIT = 56
    IDENTIFIER = 57
    WS = 58
    LINE_COMMENT = 59
    COMMENT = 60

    def __init__(self, input: TokenStream, output: TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None

    class ProtoContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def syntax(self):
            return self.getTypedRuleContext(Protobuf3Parser.SyntaxContext, 0)

        def EOF(self):
            return self.getToken(Protobuf3Parser.EOF, 0)

        def importStatement(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(Protobuf3Parser.ImportStatementContext)
            else:
                return self.getTypedRuleContext(Protobuf3Parser.ImportStatementContext, i)

        def packageStatement(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(Protobuf3Parser.PackageStatementContext)
            else:
                return self.getTypedRuleContext(Protobuf3Parser.PackageStatementContext, i)

        def optionStatement(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(Protobuf3Parser.OptionStatementContext)
            else:
                return self.getTypedRuleContext(Protobuf3Parser.OptionStatementContext, i)

        def topLevelDef(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(Protobuf3Parser.TopLevelDefContext)
            else:
                return self.getTypedRuleContext(Protobuf3Parser.TopLevelDefContext, i)

        def emptyStatement_(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(Protobuf3Parser.EmptyStatement_Context)
            else:
                return self.getTypedRuleContext(Protobuf3Parser.EmptyStatement_Context, i)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_proto

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitProto"):
                return visitor.visitProto(self)
            else:
                return visitor.visitChildren(self)

    def proto(self):

        localctx = Protobuf3Parser.ProtoContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_proto)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 106
            self.syntax()
            self.state = 114
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 282930970724) != 0):
                self.state = 112
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [2]:
                    self.state = 107
                    self.importStatement()
                    pass
                elif token in [5]:
                    self.state = 108
                    self.packageStatement()
                    pass
                elif token in [6]:
                    self.state = 109
                    self.optionStatement()
                    pass
                elif token in [29, 30, 31, 32]:
                    self.state = 110
                    self.topLevelDef()
                    pass
                elif token in [38]:
                    self.state = 111
                    self.emptyStatement_()
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 116
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 117
            self.match(Protobuf3Parser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class SyntaxContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SYNTAX(self):
            return self.getToken(Protobuf3Parser.SYNTAX, 0)

        def EQ(self):
            return self.getToken(Protobuf3Parser.EQ, 0)

        def SEMI(self):
            return self.getToken(Protobuf3Parser.SEMI, 0)

        def PROTO3_LIT_SINGLE(self):
            return self.getToken(Protobuf3Parser.PROTO3_LIT_SINGLE, 0)

        def PROTO3_LIT_DOBULE(self):
            return self.getToken(Protobuf3Parser.PROTO3_LIT_DOBULE, 0)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_syntax

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitSyntax"):
                return visitor.visitSyntax(self)
            else:
                return visitor.visitChildren(self)

    def syntax(self):

        localctx = Protobuf3Parser.SyntaxContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_syntax)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 119
            self.match(Protobuf3Parser.SYNTAX)
            self.state = 120
            self.match(Protobuf3Parser.EQ)
            self.state = 121
            _la = self._input.LA(1)
            if not (_la == 36 or _la == 37):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 122
            self.match(Protobuf3Parser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ImportStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IMPORT(self):
            return self.getToken(Protobuf3Parser.IMPORT, 0)

        def strLit(self):
            return self.getTypedRuleContext(Protobuf3Parser.StrLitContext, 0)

        def SEMI(self):
            return self.getToken(Protobuf3Parser.SEMI, 0)

        def WEAK(self):
            return self.getToken(Protobuf3Parser.WEAK, 0)

        def PUBLIC(self):
            return self.getToken(Protobuf3Parser.PUBLIC, 0)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_importStatement

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitImportStatement"):
                return visitor.visitImportStatement(self)
            else:
                return visitor.visitChildren(self)

    def importStatement(self):

        localctx = Protobuf3Parser.ImportStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_importStatement)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 124
            self.match(Protobuf3Parser.IMPORT)
            self.state = 126
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 3 or _la == 4:
                self.state = 125
                _la = self._input.LA(1)
                if not (_la == 3 or _la == 4):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()

            self.state = 128
            self.strLit()
            self.state = 129
            self.match(Protobuf3Parser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class PackageStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PACKAGE(self):
            return self.getToken(Protobuf3Parser.PACKAGE, 0)

        def fullIdent(self):
            return self.getTypedRuleContext(Protobuf3Parser.FullIdentContext, 0)

        def SEMI(self):
            return self.getToken(Protobuf3Parser.SEMI, 0)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_packageStatement

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitPackageStatement"):
                return visitor.visitPackageStatement(self)
            else:
                return visitor.visitChildren(self)

    def packageStatement(self):

        localctx = Protobuf3Parser.PackageStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_packageStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 131
            self.match(Protobuf3Parser.PACKAGE)
            self.state = 132
            self.fullIdent()
            self.state = 133
            self.match(Protobuf3Parser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class OptionStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def OPTION(self):
            return self.getToken(Protobuf3Parser.OPTION, 0)

        def optionName(self):
            return self.getTypedRuleContext(Protobuf3Parser.OptionNameContext, 0)

        def EQ(self):
            return self.getToken(Protobuf3Parser.EQ, 0)

        def constant(self):
            return self.getTypedRuleContext(Protobuf3Parser.ConstantContext, 0)

        def SEMI(self):
            return self.getToken(Protobuf3Parser.SEMI, 0)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_optionStatement

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitOptionStatement"):
                return visitor.visitOptionStatement(self)
            else:
                return visitor.visitChildren(self)

    def optionStatement(self):

        localctx = Protobuf3Parser.OptionStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_optionStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 135
            self.match(Protobuf3Parser.OPTION)
            self.state = 136
            self.optionName()
            self.state = 137
            self.match(Protobuf3Parser.EQ)
            self.state = 138
            self.constant()
            self.state = 139
            self.match(Protobuf3Parser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class OptionNameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def fullIdent(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(Protobuf3Parser.FullIdentContext)
            else:
                return self.getTypedRuleContext(Protobuf3Parser.FullIdentContext, i)

        def LP(self):
            return self.getToken(Protobuf3Parser.LP, 0)

        def RP(self):
            return self.getToken(Protobuf3Parser.RP, 0)

        def DOT(self):
            return self.getToken(Protobuf3Parser.DOT, 0)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_optionName

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitOptionName"):
                return visitor.visitOptionName(self)
            else:
                return visitor.visitChildren(self)

    def optionName(self):

        localctx = Protobuf3Parser.OptionNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_optionName)
        self._la = 0  # Token type
        try:
            self.state = 149
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
                         27, 28, 29, 30, 31, 32, 33, 34, 35, 54, 57]:
                self.enterOuterAlt(localctx, 1)
                self.state = 141
                self.fullIdent()
                pass
            elif token in [40]:
                self.enterOuterAlt(localctx, 2)
                self.state = 142
                self.match(Protobuf3Parser.LP)
                self.state = 143
                self.fullIdent()
                self.state = 144
                self.match(Protobuf3Parser.RP)
                self.state = 147
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 48:
                    self.state = 145
                    self.match(Protobuf3Parser.DOT)
                    self.state = 146
                    self.fullIdent()

                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class FieldLabelContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def OPTIONAL(self):
            return self.getToken(Protobuf3Parser.OPTIONAL, 0)

        def REPEATED(self):
            return self.getToken(Protobuf3Parser.REPEATED, 0)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_fieldLabel

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitFieldLabel"):
                return visitor.visitFieldLabel(self)
            else:
                return visitor.visitChildren(self)

    def fieldLabel(self):

        localctx = Protobuf3Parser.FieldLabelContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_fieldLabel)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 151
            _la = self._input.LA(1)
            if not (_la == 7 or _la == 8):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class FieldContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def type_(self):
            return self.getTypedRuleContext(Protobuf3Parser.Type_Context, 0)

        def fieldName(self):
            return self.getTypedRuleContext(Protobuf3Parser.FieldNameContext, 0)

        def EQ(self):
            return self.getToken(Protobuf3Parser.EQ, 0)

        def fieldNumber(self):
            return self.getTypedRuleContext(Protobuf3Parser.FieldNumberContext, 0)

        def SEMI(self):
            return self.getToken(Protobuf3Parser.SEMI, 0)

        def fieldLabel(self):
            return self.getTypedRuleContext(Protobuf3Parser.FieldLabelContext, 0)

        def LB(self):
            return self.getToken(Protobuf3Parser.LB, 0)

        def fieldOptions(self):
            return self.getTypedRuleContext(Protobuf3Parser.FieldOptionsContext, 0)

        def RB(self):
            return self.getToken(Protobuf3Parser.RB, 0)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_field

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitField"):
                return visitor.visitField(self)
            else:
                return visitor.visitChildren(self)

    def field(self):

        localctx = Protobuf3Parser.FieldContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_field)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 154
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 5, self._ctx)
            if la_ == 1:
                self.state = 153
                self.fieldLabel()

            self.state = 156
            self.type_()
            self.state = 157
            self.fieldName()
            self.state = 158
            self.match(Protobuf3Parser.EQ)
            self.state = 159
            self.fieldNumber()
            self.state = 164
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 42:
                self.state = 160
                self.match(Protobuf3Parser.LB)
                self.state = 161
                self.fieldOptions()
                self.state = 162
                self.match(Protobuf3Parser.RB)

            self.state = 166
            self.match(Protobuf3Parser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class FieldOptionsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def fieldOption(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(Protobuf3Parser.FieldOptionContext)
            else:
                return self.getTypedRuleContext(Protobuf3Parser.FieldOptionContext, i)

        def COMMA(self, i: int = None):
            if i is None:
                return self.getTokens(Protobuf3Parser.COMMA)
            else:
                return self.getToken(Protobuf3Parser.COMMA, i)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_fieldOptions

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitFieldOptions"):
                return visitor.visitFieldOptions(self)
            else:
                return visitor.visitChildren(self)

    def fieldOptions(self):

        localctx = Protobuf3Parser.FieldOptionsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_fieldOptions)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 168
            self.fieldOption()
            self.state = 173
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 49:
                self.state = 169
                self.match(Protobuf3Parser.COMMA)
                self.state = 170
                self.fieldOption()
                self.state = 175
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class FieldOptionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def optionName(self):
            return self.getTypedRuleContext(Protobuf3Parser.OptionNameContext, 0)

        def EQ(self):
            return self.getToken(Protobuf3Parser.EQ, 0)

        def constant(self):
            return self.getTypedRuleContext(Protobuf3Parser.ConstantContext, 0)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_fieldOption

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitFieldOption"):
                return visitor.visitFieldOption(self)
            else:
                return visitor.visitChildren(self)

    def fieldOption(self):

        localctx = Protobuf3Parser.FieldOptionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_fieldOption)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 176
            self.optionName()
            self.state = 177
            self.match(Protobuf3Parser.EQ)
            self.state = 178
            self.constant()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class FieldNumberContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def intLit(self):
            return self.getTypedRuleContext(Protobuf3Parser.IntLitContext, 0)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_fieldNumber

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitFieldNumber"):
                return visitor.visitFieldNumber(self)
            else:
                return visitor.visitChildren(self)

    def fieldNumber(self):

        localctx = Protobuf3Parser.FieldNumberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_fieldNumber)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 180
            self.intLit()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class OneofContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ONEOF(self):
            return self.getToken(Protobuf3Parser.ONEOF, 0)

        def oneofName(self):
            return self.getTypedRuleContext(Protobuf3Parser.OneofNameContext, 0)

        def LC(self):
            return self.getToken(Protobuf3Parser.LC, 0)

        def RC(self):
            return self.getToken(Protobuf3Parser.RC, 0)

        def optionStatement(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(Protobuf3Parser.OptionStatementContext)
            else:
                return self.getTypedRuleContext(Protobuf3Parser.OptionStatementContext, i)

        def oneofField(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(Protobuf3Parser.OneofFieldContext)
            else:
                return self.getTypedRuleContext(Protobuf3Parser.OneofFieldContext, i)

        def emptyStatement_(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(Protobuf3Parser.EmptyStatement_Context)
            else:
                return self.getTypedRuleContext(Protobuf3Parser.EmptyStatement_Context, i)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_oneof

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitOneof"):
                return visitor.visitOneof(self)
            else:
                return visitor.visitChildren(self)

    def oneof(self):

        localctx = Protobuf3Parser.OneofContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_oneof)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 182
            self.match(Protobuf3Parser.ONEOF)
            self.state = 183
            self.oneofName()
            self.state = 184
            self.match(Protobuf3Parser.LC)
            self.state = 190
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 162411405159432190) != 0):
                self.state = 188
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input, 8, self._ctx)
                if la_ == 1:
                    self.state = 185
                    self.optionStatement()
                    pass

                elif la_ == 2:
                    self.state = 186
                    self.oneofField()
                    pass

                elif la_ == 3:
                    self.state = 187
                    self.emptyStatement_()
                    pass

                self.state = 192
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 193
            self.match(Protobuf3Parser.RC)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class OneofFieldContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def type_(self):
            return self.getTypedRuleContext(Protobuf3Parser.Type_Context, 0)

        def fieldName(self):
            return self.getTypedRuleContext(Protobuf3Parser.FieldNameContext, 0)

        def EQ(self):
            return self.getToken(Protobuf3Parser.EQ, 0)

        def fieldNumber(self):
            return self.getTypedRuleContext(Protobuf3Parser.FieldNumberContext, 0)

        def SEMI(self):
            return self.getToken(Protobuf3Parser.SEMI, 0)

        def LB(self):
            return self.getToken(Protobuf3Parser.LB, 0)

        def fieldOptions(self):
            return self.getTypedRuleContext(Protobuf3Parser.FieldOptionsContext, 0)

        def RB(self):
            return self.getToken(Protobuf3Parser.RB, 0)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_oneofField

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitOneofField"):
                return visitor.visitOneofField(self)
            else:
                return visitor.visitChildren(self)

    def oneofField(self):

        localctx = Protobuf3Parser.OneofFieldContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_oneofField)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 195
            self.type_()
            self.state = 196
            self.fieldName()
            self.state = 197
            self.match(Protobuf3Parser.EQ)
            self.state = 198
            self.fieldNumber()
            self.state = 203
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 42:
                self.state = 199
                self.match(Protobuf3Parser.LB)
                self.state = 200
                self.fieldOptions()
                self.state = 201
                self.match(Protobuf3Parser.RB)

            self.state = 205
            self.match(Protobuf3Parser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class MapFieldContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def MAP(self):
            return self.getToken(Protobuf3Parser.MAP, 0)

        def LT(self):
            return self.getToken(Protobuf3Parser.LT, 0)

        def keyType(self):
            return self.getTypedRuleContext(Protobuf3Parser.KeyTypeContext, 0)

        def COMMA(self):
            return self.getToken(Protobuf3Parser.COMMA, 0)

        def type_(self):
            return self.getTypedRuleContext(Protobuf3Parser.Type_Context, 0)

        def GT(self):
            return self.getToken(Protobuf3Parser.GT, 0)

        def mapName(self):
            return self.getTypedRuleContext(Protobuf3Parser.MapNameContext, 0)

        def EQ(self):
            return self.getToken(Protobuf3Parser.EQ, 0)

        def fieldNumber(self):
            return self.getTypedRuleContext(Protobuf3Parser.FieldNumberContext, 0)

        def SEMI(self):
            return self.getToken(Protobuf3Parser.SEMI, 0)

        def LB(self):
            return self.getToken(Protobuf3Parser.LB, 0)

        def fieldOptions(self):
            return self.getTypedRuleContext(Protobuf3Parser.FieldOptionsContext, 0)

        def RB(self):
            return self.getToken(Protobuf3Parser.RB, 0)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_mapField

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitMapField"):
                return visitor.visitMapField(self)
            else:
                return visitor.visitChildren(self)

    def mapField(self):

        localctx = Protobuf3Parser.MapFieldContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_mapField)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 207
            self.match(Protobuf3Parser.MAP)
            self.state = 208
            self.match(Protobuf3Parser.LT)
            self.state = 209
            self.keyType()
            self.state = 210
            self.match(Protobuf3Parser.COMMA)
            self.state = 211
            self.type_()
            self.state = 212
            self.match(Protobuf3Parser.GT)
            self.state = 213
            self.mapName()
            self.state = 214
            self.match(Protobuf3Parser.EQ)
            self.state = 215
            self.fieldNumber()
            self.state = 220
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 42:
                self.state = 216
                self.match(Protobuf3Parser.LB)
                self.state = 217
                self.fieldOptions()
                self.state = 218
                self.match(Protobuf3Parser.RB)

            self.state = 222
            self.match(Protobuf3Parser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class KeyTypeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT32(self):
            return self.getToken(Protobuf3Parser.INT32, 0)

        def INT64(self):
            return self.getToken(Protobuf3Parser.INT64, 0)

        def UINT32(self):
            return self.getToken(Protobuf3Parser.UINT32, 0)

        def UINT64(self):
            return self.getToken(Protobuf3Parser.UINT64, 0)

        def SINT32(self):
            return self.getToken(Protobuf3Parser.SINT32, 0)

        def SINT64(self):
            return self.getToken(Protobuf3Parser.SINT64, 0)

        def FIXED32(self):
            return self.getToken(Protobuf3Parser.FIXED32, 0)

        def FIXED64(self):
            return self.getToken(Protobuf3Parser.FIXED64, 0)

        def SFIXED32(self):
            return self.getToken(Protobuf3Parser.SFIXED32, 0)

        def SFIXED64(self):
            return self.getToken(Protobuf3Parser.SFIXED64, 0)

        def BOOL(self):
            return self.getToken(Protobuf3Parser.BOOL, 0)

        def STRING(self):
            return self.getToken(Protobuf3Parser.STRING, 0)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_keyType

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitKeyType"):
                return visitor.visitKeyType(self)
            else:
                return visitor.visitChildren(self)

    def keyType(self):

        localctx = Protobuf3Parser.KeyTypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_keyType)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 224
            _la = self._input.LA(1)
            if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 8386560) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Type_Context(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DOUBLE(self):
            return self.getToken(Protobuf3Parser.DOUBLE, 0)

        def FLOAT(self):
            return self.getToken(Protobuf3Parser.FLOAT, 0)

        def INT32(self):
            return self.getToken(Protobuf3Parser.INT32, 0)

        def INT64(self):
            return self.getToken(Protobuf3Parser.INT64, 0)

        def UINT32(self):
            return self.getToken(Protobuf3Parser.UINT32, 0)

        def UINT64(self):
            return self.getToken(Protobuf3Parser.UINT64, 0)

        def SINT32(self):
            return self.getToken(Protobuf3Parser.SINT32, 0)

        def SINT64(self):
            return self.getToken(Protobuf3Parser.SINT64, 0)

        def FIXED32(self):
            return self.getToken(Protobuf3Parser.FIXED32, 0)

        def FIXED64(self):
            return self.getToken(Protobuf3Parser.FIXED64, 0)

        def SFIXED32(self):
            return self.getToken(Protobuf3Parser.SFIXED32, 0)

        def SFIXED64(self):
            return self.getToken(Protobuf3Parser.SFIXED64, 0)

        def BOOL(self):
            return self.getToken(Protobuf3Parser.BOOL, 0)

        def STRING(self):
            return self.getToken(Protobuf3Parser.STRING, 0)

        def BYTES(self):
            return self.getToken(Protobuf3Parser.BYTES, 0)

        def messageType(self):
            return self.getTypedRuleContext(Protobuf3Parser.MessageTypeContext, 0)

        def enumType(self):
            return self.getTypedRuleContext(Protobuf3Parser.EnumTypeContext, 0)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_type_

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitType_"):
                return visitor.visitType_(self)
            else:
                return visitor.visitChildren(self)

    def type_(self):

        localctx = Protobuf3Parser.Type_Context(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_type_)
        try:
            self.state = 243
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 12, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 226
                self.match(Protobuf3Parser.DOUBLE)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 227
                self.match(Protobuf3Parser.FLOAT)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 228
                self.match(Protobuf3Parser.INT32)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 229
                self.match(Protobuf3Parser.INT64)
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 230
                self.match(Protobuf3Parser.UINT32)
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 231
                self.match(Protobuf3Parser.UINT64)
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 232
                self.match(Protobuf3Parser.SINT32)
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 233
                self.match(Protobuf3Parser.SINT64)
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 234
                self.match(Protobuf3Parser.FIXED32)
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 235
                self.match(Protobuf3Parser.FIXED64)
                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 236
                self.match(Protobuf3Parser.SFIXED32)
                pass

            elif la_ == 12:
                self.enterOuterAlt(localctx, 12)
                self.state = 237
                self.match(Protobuf3Parser.SFIXED64)
                pass

            elif la_ == 13:
                self.enterOuterAlt(localctx, 13)
                self.state = 238
                self.match(Protobuf3Parser.BOOL)
                pass

            elif la_ == 14:
                self.enterOuterAlt(localctx, 14)
                self.state = 239
                self.match(Protobuf3Parser.STRING)
                pass

            elif la_ == 15:
                self.enterOuterAlt(localctx, 15)
                self.state = 240
                self.match(Protobuf3Parser.BYTES)
                pass

            elif la_ == 16:
                self.enterOuterAlt(localctx, 16)
                self.state = 241
                self.messageType()
                pass

            elif la_ == 17:
                self.enterOuterAlt(localctx, 17)
                self.state = 242
                self.enumType()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ReservedContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def RESERVED(self):
            return self.getToken(Protobuf3Parser.RESERVED, 0)

        def SEMI(self):
            return self.getToken(Protobuf3Parser.SEMI, 0)

        def ranges(self):
            return self.getTypedRuleContext(Protobuf3Parser.RangesContext, 0)

        def reservedFieldNames(self):
            return self.getTypedRuleContext(Protobuf3Parser.ReservedFieldNamesContext, 0)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_reserved

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitReserved"):
                return visitor.visitReserved(self)
            else:
                return visitor.visitChildren(self)

    def reserved(self):

        localctx = Protobuf3Parser.ReservedContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_reserved)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 245
            self.match(Protobuf3Parser.RESERVED)
            self.state = 248
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [56]:
                self.state = 246
                self.ranges()
                pass
            elif token in [36, 37, 53]:
                self.state = 247
                self.reservedFieldNames()
                pass
            else:
                raise NoViableAltException(self)

            self.state = 250
            self.match(Protobuf3Parser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class RangesContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def range_(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(Protobuf3Parser.Range_Context)
            else:
                return self.getTypedRuleContext(Protobuf3Parser.Range_Context, i)

        def COMMA(self, i: int = None):
            if i is None:
                return self.getTokens(Protobuf3Parser.COMMA)
            else:
                return self.getToken(Protobuf3Parser.COMMA, i)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_ranges

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitRanges"):
                return visitor.visitRanges(self)
            else:
                return visitor.visitChildren(self)

    def ranges(self):

        localctx = Protobuf3Parser.RangesContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_ranges)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 252
            self.range_()
            self.state = 257
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 49:
                self.state = 253
                self.match(Protobuf3Parser.COMMA)
                self.state = 254
                self.range_()
                self.state = 259
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Range_Context(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def intLit(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(Protobuf3Parser.IntLitContext)
            else:
                return self.getTypedRuleContext(Protobuf3Parser.IntLitContext, i)

        def TO(self):
            return self.getToken(Protobuf3Parser.TO, 0)

        def MAX(self):
            return self.getToken(Protobuf3Parser.MAX, 0)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_range_

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitRange_"):
                return visitor.visitRange_(self)
            else:
                return visitor.visitChildren(self)

    def range_(self):

        localctx = Protobuf3Parser.Range_Context(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_range_)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 260
            self.intLit()
            self.state = 266
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 27:
                self.state = 261
                self.match(Protobuf3Parser.TO)
                self.state = 264
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [56]:
                    self.state = 262
                    self.intLit()
                    pass
                elif token in [28]:
                    self.state = 263
                    self.match(Protobuf3Parser.MAX)
                    pass
                else:
                    raise NoViableAltException(self)



        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ReservedFieldNamesContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def strLit(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(Protobuf3Parser.StrLitContext)
            else:
                return self.getTypedRuleContext(Protobuf3Parser.StrLitContext, i)

        def COMMA(self, i: int = None):
            if i is None:
                return self.getTokens(Protobuf3Parser.COMMA)
            else:
                return self.getToken(Protobuf3Parser.COMMA, i)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_reservedFieldNames

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitReservedFieldNames"):
                return visitor.visitReservedFieldNames(self)
            else:
                return visitor.visitChildren(self)

    def reservedFieldNames(self):

        localctx = Protobuf3Parser.ReservedFieldNamesContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_reservedFieldNames)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 268
            self.strLit()
            self.state = 273
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 49:
                self.state = 269
                self.match(Protobuf3Parser.COMMA)
                self.state = 270
                self.strLit()
                self.state = 275
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class TopLevelDefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def messageDef(self):
            return self.getTypedRuleContext(Protobuf3Parser.MessageDefContext, 0)

        def enumDef(self):
            return self.getTypedRuleContext(Protobuf3Parser.EnumDefContext, 0)

        def extendDef(self):
            return self.getTypedRuleContext(Protobuf3Parser.ExtendDefContext, 0)

        def serviceDef(self):
            return self.getTypedRuleContext(Protobuf3Parser.ServiceDefContext, 0)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_topLevelDef

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitTopLevelDef"):
                return visitor.visitTopLevelDef(self)
            else:
                return visitor.visitChildren(self)

    def topLevelDef(self):

        localctx = Protobuf3Parser.TopLevelDefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_topLevelDef)
        try:
            self.state = 280
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [30]:
                self.enterOuterAlt(localctx, 1)
                self.state = 276
                self.messageDef()
                pass
            elif token in [29]:
                self.enterOuterAlt(localctx, 2)
                self.state = 277
                self.enumDef()
                pass
            elif token in [32]:
                self.enterOuterAlt(localctx, 3)
                self.state = 278
                self.extendDef()
                pass
            elif token in [31]:
                self.enterOuterAlt(localctx, 4)
                self.state = 279
                self.serviceDef()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class EnumDefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ENUM(self):
            return self.getToken(Protobuf3Parser.ENUM, 0)

        def enumName(self):
            return self.getTypedRuleContext(Protobuf3Parser.EnumNameContext, 0)

        def enumBody(self):
            return self.getTypedRuleContext(Protobuf3Parser.EnumBodyContext, 0)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_enumDef

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitEnumDef"):
                return visitor.visitEnumDef(self)
            else:
                return visitor.visitChildren(self)

    def enumDef(self):

        localctx = Protobuf3Parser.EnumDefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_enumDef)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 282
            self.match(Protobuf3Parser.ENUM)
            self.state = 283
            self.enumName()
            self.state = 284
            self.enumBody()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class EnumBodyContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LC(self):
            return self.getToken(Protobuf3Parser.LC, 0)

        def RC(self):
            return self.getToken(Protobuf3Parser.RC, 0)

        def enumElement(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(Protobuf3Parser.EnumElementContext)
            else:
                return self.getTypedRuleContext(Protobuf3Parser.EnumElementContext, i)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_enumBody

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitEnumBody"):
                return visitor.visitEnumBody(self)
            else:
                return visitor.visitChildren(self)

    def enumBody(self):

        localctx = Protobuf3Parser.EnumBodyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_enumBody)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 286
            self.match(Protobuf3Parser.LC)
            self.state = 290
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 162129930182721534) != 0):
                self.state = 287
                self.enumElement()
                self.state = 292
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 293
            self.match(Protobuf3Parser.RC)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class EnumElementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def optionStatement(self):
            return self.getTypedRuleContext(Protobuf3Parser.OptionStatementContext, 0)

        def enumField(self):
            return self.getTypedRuleContext(Protobuf3Parser.EnumFieldContext, 0)

        def emptyStatement_(self):
            return self.getTypedRuleContext(Protobuf3Parser.EmptyStatement_Context, 0)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_enumElement

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitEnumElement"):
                return visitor.visitEnumElement(self)
            else:
                return visitor.visitChildren(self)

    def enumElement(self):

        localctx = Protobuf3Parser.EnumElementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_enumElement)
        try:
            self.state = 298
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 20, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 295
                self.optionStatement()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 296
                self.enumField()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 297
                self.emptyStatement_()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class EnumFieldContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ident(self):
            return self.getTypedRuleContext(Protobuf3Parser.IdentContext, 0)

        def EQ(self):
            return self.getToken(Protobuf3Parser.EQ, 0)

        def intLit(self):
            return self.getTypedRuleContext(Protobuf3Parser.IntLitContext, 0)

        def SEMI(self):
            return self.getToken(Protobuf3Parser.SEMI, 0)

        def MINUS(self):
            return self.getToken(Protobuf3Parser.MINUS, 0)

        def enumValueOptions(self):
            return self.getTypedRuleContext(Protobuf3Parser.EnumValueOptionsContext, 0)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_enumField

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitEnumField"):
                return visitor.visitEnumField(self)
            else:
                return visitor.visitChildren(self)

    def enumField(self):

        localctx = Protobuf3Parser.EnumFieldContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_enumField)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 300
            self.ident()
            self.state = 301
            self.match(Protobuf3Parser.EQ)
            self.state = 303
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 52:
                self.state = 302
                self.match(Protobuf3Parser.MINUS)

            self.state = 305
            self.intLit()
            self.state = 307
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 42:
                self.state = 306
                self.enumValueOptions()

            self.state = 309
            self.match(Protobuf3Parser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class EnumValueOptionsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LB(self):
            return self.getToken(Protobuf3Parser.LB, 0)

        def enumValueOption(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(Protobuf3Parser.EnumValueOptionContext)
            else:
                return self.getTypedRuleContext(Protobuf3Parser.EnumValueOptionContext, i)

        def RB(self):
            return self.getToken(Protobuf3Parser.RB, 0)

        def COMMA(self, i: int = None):
            if i is None:
                return self.getTokens(Protobuf3Parser.COMMA)
            else:
                return self.getToken(Protobuf3Parser.COMMA, i)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_enumValueOptions

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitEnumValueOptions"):
                return visitor.visitEnumValueOptions(self)
            else:
                return visitor.visitChildren(self)

    def enumValueOptions(self):

        localctx = Protobuf3Parser.EnumValueOptionsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_enumValueOptions)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 311
            self.match(Protobuf3Parser.LB)
            self.state = 312
            self.enumValueOption()
            self.state = 317
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 49:
                self.state = 313
                self.match(Protobuf3Parser.COMMA)
                self.state = 314
                self.enumValueOption()
                self.state = 319
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 320
            self.match(Protobuf3Parser.RB)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class EnumValueOptionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def optionName(self):
            return self.getTypedRuleContext(Protobuf3Parser.OptionNameContext, 0)

        def EQ(self):
            return self.getToken(Protobuf3Parser.EQ, 0)

        def constant(self):
            return self.getTypedRuleContext(Protobuf3Parser.ConstantContext, 0)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_enumValueOption

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitEnumValueOption"):
                return visitor.visitEnumValueOption(self)
            else:
                return visitor.visitChildren(self)

    def enumValueOption(self):

        localctx = Protobuf3Parser.EnumValueOptionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_enumValueOption)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 322
            self.optionName()
            self.state = 323
            self.match(Protobuf3Parser.EQ)
            self.state = 324
            self.constant()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class MessageDefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def MESSAGE(self):
            return self.getToken(Protobuf3Parser.MESSAGE, 0)

        def messageName(self):
            return self.getTypedRuleContext(Protobuf3Parser.MessageNameContext, 0)

        def messageBody(self):
            return self.getTypedRuleContext(Protobuf3Parser.MessageBodyContext, 0)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_messageDef

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitMessageDef"):
                return visitor.visitMessageDef(self)
            else:
                return visitor.visitChildren(self)

    def messageDef(self):

        localctx = Protobuf3Parser.MessageDefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 54, self.RULE_messageDef)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 326
            self.match(Protobuf3Parser.MESSAGE)
            self.state = 327
            self.messageName()
            self.state = 328
            self.messageBody()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class MessageBodyContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LC(self):
            return self.getToken(Protobuf3Parser.LC, 0)

        def RC(self):
            return self.getToken(Protobuf3Parser.RC, 0)

        def messageElement(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(Protobuf3Parser.MessageElementContext)
            else:
                return self.getTypedRuleContext(Protobuf3Parser.MessageElementContext, i)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_messageBody

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitMessageBody"):
                return visitor.visitMessageBody(self)
            else:
                return visitor.visitChildren(self)

    def messageBody(self):

        localctx = Protobuf3Parser.MessageBodyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 56, self.RULE_messageBody)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 330
            self.match(Protobuf3Parser.LC)
            self.state = 334
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 162411405159432190) != 0):
                self.state = 331
                self.messageElement()
                self.state = 336
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 337
            self.match(Protobuf3Parser.RC)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class MessageElementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def field(self):
            return self.getTypedRuleContext(Protobuf3Parser.FieldContext, 0)

        def enumDef(self):
            return self.getTypedRuleContext(Protobuf3Parser.EnumDefContext, 0)

        def messageDef(self):
            return self.getTypedRuleContext(Protobuf3Parser.MessageDefContext, 0)

        def extendDef(self):
            return self.getTypedRuleContext(Protobuf3Parser.ExtendDefContext, 0)

        def optionStatement(self):
            return self.getTypedRuleContext(Protobuf3Parser.OptionStatementContext, 0)

        def oneof(self):
            return self.getTypedRuleContext(Protobuf3Parser.OneofContext, 0)

        def mapField(self):
            return self.getTypedRuleContext(Protobuf3Parser.MapFieldContext, 0)

        def reserved(self):
            return self.getTypedRuleContext(Protobuf3Parser.ReservedContext, 0)

        def emptyStatement_(self):
            return self.getTypedRuleContext(Protobuf3Parser.EmptyStatement_Context, 0)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_messageElement

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitMessageElement"):
                return visitor.visitMessageElement(self)
            else:
                return visitor.visitChildren(self)

    def messageElement(self):

        localctx = Protobuf3Parser.MessageElementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 58, self.RULE_messageElement)
        try:
            self.state = 348
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 25, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 339
                self.field()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 340
                self.enumDef()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 341
                self.messageDef()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 342
                self.extendDef()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 343
                self.optionStatement()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 344
                self.oneof()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 345
                self.mapField()
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 346
                self.reserved()
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 347
                self.emptyStatement_()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ExtendDefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EXTEND(self):
            return self.getToken(Protobuf3Parser.EXTEND, 0)

        def messageType(self):
            return self.getTypedRuleContext(Protobuf3Parser.MessageTypeContext, 0)

        def LC(self):
            return self.getToken(Protobuf3Parser.LC, 0)

        def RC(self):
            return self.getToken(Protobuf3Parser.RC, 0)

        def field(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(Protobuf3Parser.FieldContext)
            else:
                return self.getTypedRuleContext(Protobuf3Parser.FieldContext, i)

        def emptyStatement_(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(Protobuf3Parser.EmptyStatement_Context)
            else:
                return self.getTypedRuleContext(Protobuf3Parser.EmptyStatement_Context, i)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_extendDef

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitExtendDef"):
                return visitor.visitExtendDef(self)
            else:
                return visitor.visitChildren(self)

    def extendDef(self):

        localctx = Protobuf3Parser.ExtendDefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 60, self.RULE_extendDef)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 350
            self.match(Protobuf3Parser.EXTEND)
            self.state = 351
            self.messageType()
            self.state = 352
            self.match(Protobuf3Parser.LC)
            self.state = 357
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 162411405159432190) != 0):
                self.state = 355
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
                             26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 48, 54, 57]:
                    self.state = 353
                    self.field()
                    pass
                elif token in [38]:
                    self.state = 354
                    self.emptyStatement_()
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 359
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 360
            self.match(Protobuf3Parser.RC)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ServiceDefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SERVICE(self):
            return self.getToken(Protobuf3Parser.SERVICE, 0)

        def serviceName(self):
            return self.getTypedRuleContext(Protobuf3Parser.ServiceNameContext, 0)

        def LC(self):
            return self.getToken(Protobuf3Parser.LC, 0)

        def RC(self):
            return self.getToken(Protobuf3Parser.RC, 0)

        def serviceElement(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(Protobuf3Parser.ServiceElementContext)
            else:
                return self.getTypedRuleContext(Protobuf3Parser.ServiceElementContext, i)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_serviceDef

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitServiceDef"):
                return visitor.visitServiceDef(self)
            else:
                return visitor.visitChildren(self)

    def serviceDef(self):

        localctx = Protobuf3Parser.ServiceDefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 62, self.RULE_serviceDef)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 362
            self.match(Protobuf3Parser.SERVICE)
            self.state = 363
            self.serviceName()
            self.state = 364
            self.match(Protobuf3Parser.LC)
            self.state = 368
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 283467841600) != 0):
                self.state = 365
                self.serviceElement()
                self.state = 370
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 371
            self.match(Protobuf3Parser.RC)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ServiceElementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def optionStatement(self):
            return self.getTypedRuleContext(Protobuf3Parser.OptionStatementContext, 0)

        def rpc(self):
            return self.getTypedRuleContext(Protobuf3Parser.RpcContext, 0)

        def emptyStatement_(self):
            return self.getTypedRuleContext(Protobuf3Parser.EmptyStatement_Context, 0)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_serviceElement

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitServiceElement"):
                return visitor.visitServiceElement(self)
            else:
                return visitor.visitChildren(self)

    def serviceElement(self):

        localctx = Protobuf3Parser.ServiceElementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 64, self.RULE_serviceElement)
        try:
            self.state = 376
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [6]:
                self.enterOuterAlt(localctx, 1)
                self.state = 373
                self.optionStatement()
                pass
            elif token in [33]:
                self.enterOuterAlt(localctx, 2)
                self.state = 374
                self.rpc()
                pass
            elif token in [38]:
                self.enterOuterAlt(localctx, 3)
                self.state = 375
                self.emptyStatement_()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class RpcContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def RPC(self):
            return self.getToken(Protobuf3Parser.RPC, 0)

        def rpcName(self):
            return self.getTypedRuleContext(Protobuf3Parser.RpcNameContext, 0)

        def LP(self, i: int = None):
            if i is None:
                return self.getTokens(Protobuf3Parser.LP)
            else:
                return self.getToken(Protobuf3Parser.LP, i)

        def messageType(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(Protobuf3Parser.MessageTypeContext)
            else:
                return self.getTypedRuleContext(Protobuf3Parser.MessageTypeContext, i)

        def RP(self, i: int = None):
            if i is None:
                return self.getTokens(Protobuf3Parser.RP)
            else:
                return self.getToken(Protobuf3Parser.RP, i)

        def RETURNS(self):
            return self.getToken(Protobuf3Parser.RETURNS, 0)

        def LC(self):
            return self.getToken(Protobuf3Parser.LC, 0)

        def RC(self):
            return self.getToken(Protobuf3Parser.RC, 0)

        def SEMI(self):
            return self.getToken(Protobuf3Parser.SEMI, 0)

        def STREAM(self, i: int = None):
            if i is None:
                return self.getTokens(Protobuf3Parser.STREAM)
            else:
                return self.getToken(Protobuf3Parser.STREAM, i)

        def optionStatement(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(Protobuf3Parser.OptionStatementContext)
            else:
                return self.getTypedRuleContext(Protobuf3Parser.OptionStatementContext, i)

        def emptyStatement_(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(Protobuf3Parser.EmptyStatement_Context)
            else:
                return self.getTypedRuleContext(Protobuf3Parser.EmptyStatement_Context, i)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_rpc

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitRpc"):
                return visitor.visitRpc(self)
            else:
                return visitor.visitChildren(self)

    def rpc(self):

        localctx = Protobuf3Parser.RpcContext(self, self._ctx, self.state)
        self.enterRule(localctx, 66, self.RULE_rpc)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 378
            self.match(Protobuf3Parser.RPC)
            self.state = 379
            self.rpcName()
            self.state = 380
            self.match(Protobuf3Parser.LP)
            self.state = 382
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 30, self._ctx)
            if la_ == 1:
                self.state = 381
                self.match(Protobuf3Parser.STREAM)

            self.state = 384
            self.messageType()
            self.state = 385
            self.match(Protobuf3Parser.RP)
            self.state = 386
            self.match(Protobuf3Parser.RETURNS)
            self.state = 387
            self.match(Protobuf3Parser.LP)
            self.state = 389
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 31, self._ctx)
            if la_ == 1:
                self.state = 388
                self.match(Protobuf3Parser.STREAM)

            self.state = 391
            self.messageType()
            self.state = 392
            self.match(Protobuf3Parser.RP)
            self.state = 403
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [44]:
                self.state = 393
                self.match(Protobuf3Parser.LC)
                self.state = 398
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la == 6 or _la == 38:
                    self.state = 396
                    self._errHandler.sync(self)
                    token = self._input.LA(1)
                    if token in [6]:
                        self.state = 394
                        self.optionStatement()
                        pass
                    elif token in [38]:
                        self.state = 395
                        self.emptyStatement_()
                        pass
                    else:
                        raise NoViableAltException(self)

                    self.state = 400
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 401
                self.match(Protobuf3Parser.RC)
                pass
            elif token in [38]:
                self.state = 402
                self.match(Protobuf3Parser.SEMI)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ConstantContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def fullIdent(self):
            return self.getTypedRuleContext(Protobuf3Parser.FullIdentContext, 0)

        def intLit(self):
            return self.getTypedRuleContext(Protobuf3Parser.IntLitContext, 0)

        def MINUS(self):
            return self.getToken(Protobuf3Parser.MINUS, 0)

        def PLUS(self):
            return self.getToken(Protobuf3Parser.PLUS, 0)

        def floatLit(self):
            return self.getTypedRuleContext(Protobuf3Parser.FloatLitContext, 0)

        def strLit(self):
            return self.getTypedRuleContext(Protobuf3Parser.StrLitContext, 0)

        def boolLit(self):
            return self.getTypedRuleContext(Protobuf3Parser.BoolLitContext, 0)

        def blockLit(self):
            return self.getTypedRuleContext(Protobuf3Parser.BlockLitContext, 0)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_constant

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitConstant"):
                return visitor.visitConstant(self)
            else:
                return visitor.visitChildren(self)

    def constant(self):

        localctx = Protobuf3Parser.ConstantContext(self, self._ctx, self.state)
        self.enterRule(localctx, 68, self.RULE_constant)
        self._la = 0  # Token type
        try:
            self.state = 417
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 37, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 405
                self.fullIdent()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 407
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 51 or _la == 52:
                    self.state = 406
                    _la = self._input.LA(1)
                    if not (_la == 51 or _la == 52):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()

                self.state = 409
                self.intLit()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 411
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 51 or _la == 52:
                    self.state = 410
                    _la = self._input.LA(1)
                    if not (_la == 51 or _la == 52):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()

                self.state = 413
                self.floatLit()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 414
                self.strLit()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 415
                self.boolLit()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 416
                self.blockLit()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class BlockLitContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LC(self):
            return self.getToken(Protobuf3Parser.LC, 0)

        def RC(self):
            return self.getToken(Protobuf3Parser.RC, 0)

        def ident(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(Protobuf3Parser.IdentContext)
            else:
                return self.getTypedRuleContext(Protobuf3Parser.IdentContext, i)

        def COLON(self, i: int = None):
            if i is None:
                return self.getTokens(Protobuf3Parser.COLON)
            else:
                return self.getToken(Protobuf3Parser.COLON, i)

        def constant(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(Protobuf3Parser.ConstantContext)
            else:
                return self.getTypedRuleContext(Protobuf3Parser.ConstantContext, i)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_blockLit

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitBlockLit"):
                return visitor.visitBlockLit(self)
            else:
                return visitor.visitChildren(self)

    def blockLit(self):

        localctx = Protobuf3Parser.BlockLitContext(self, self._ctx, self.state)
        self.enterRule(localctx, 70, self.RULE_blockLit)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 419
            self.match(Protobuf3Parser.LC)
            self.state = 426
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 162129655304814590) != 0):
                self.state = 420
                self.ident()
                self.state = 421
                self.match(Protobuf3Parser.COLON)
                self.state = 422
                self.constant()
                self.state = 428
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 429
            self.match(Protobuf3Parser.RC)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class EmptyStatement_Context(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SEMI(self):
            return self.getToken(Protobuf3Parser.SEMI, 0)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_emptyStatement_

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitEmptyStatement_"):
                return visitor.visitEmptyStatement_(self)
            else:
                return visitor.visitChildren(self)

    def emptyStatement_(self):

        localctx = Protobuf3Parser.EmptyStatement_Context(self, self._ctx, self.state)
        self.enterRule(localctx, 72, self.RULE_emptyStatement_)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 431
            self.match(Protobuf3Parser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class IdentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(Protobuf3Parser.IDENTIFIER, 0)

        def keywords(self):
            return self.getTypedRuleContext(Protobuf3Parser.KeywordsContext, 0)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_ident

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitIdent"):
                return visitor.visitIdent(self)
            else:
                return visitor.visitChildren(self)

    def ident(self):

        localctx = Protobuf3Parser.IdentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 74, self.RULE_ident)
        try:
            self.state = 435
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [57]:
                self.enterOuterAlt(localctx, 1)
                self.state = 433
                self.match(Protobuf3Parser.IDENTIFIER)
                pass
            elif token in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
                           26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 54]:
                self.enterOuterAlt(localctx, 2)
                self.state = 434
                self.keywords()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class FullIdentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ident(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(Protobuf3Parser.IdentContext)
            else:
                return self.getTypedRuleContext(Protobuf3Parser.IdentContext, i)

        def DOT(self, i: int = None):
            if i is None:
                return self.getTokens(Protobuf3Parser.DOT)
            else:
                return self.getToken(Protobuf3Parser.DOT, i)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_fullIdent

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitFullIdent"):
                return visitor.visitFullIdent(self)
            else:
                return visitor.visitChildren(self)

    def fullIdent(self):

        localctx = Protobuf3Parser.FullIdentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 76, self.RULE_fullIdent)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 437
            self.ident()
            self.state = 442
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 48:
                self.state = 438
                self.match(Protobuf3Parser.DOT)
                self.state = 439
                self.ident()
                self.state = 444
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class MessageNameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ident(self):
            return self.getTypedRuleContext(Protobuf3Parser.IdentContext, 0)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_messageName

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitMessageName"):
                return visitor.visitMessageName(self)
            else:
                return visitor.visitChildren(self)

    def messageName(self):

        localctx = Protobuf3Parser.MessageNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 78, self.RULE_messageName)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 445
            self.ident()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class EnumNameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ident(self):
            return self.getTypedRuleContext(Protobuf3Parser.IdentContext, 0)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_enumName

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitEnumName"):
                return visitor.visitEnumName(self)
            else:
                return visitor.visitChildren(self)

    def enumName(self):

        localctx = Protobuf3Parser.EnumNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 80, self.RULE_enumName)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 447
            self.ident()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class FieldNameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ident(self):
            return self.getTypedRuleContext(Protobuf3Parser.IdentContext, 0)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_fieldName

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitFieldName"):
                return visitor.visitFieldName(self)
            else:
                return visitor.visitChildren(self)

    def fieldName(self):

        localctx = Protobuf3Parser.FieldNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 82, self.RULE_fieldName)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 449
            self.ident()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class OneofNameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ident(self):
            return self.getTypedRuleContext(Protobuf3Parser.IdentContext, 0)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_oneofName

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitOneofName"):
                return visitor.visitOneofName(self)
            else:
                return visitor.visitChildren(self)

    def oneofName(self):

        localctx = Protobuf3Parser.OneofNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 84, self.RULE_oneofName)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 451
            self.ident()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class MapNameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ident(self):
            return self.getTypedRuleContext(Protobuf3Parser.IdentContext, 0)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_mapName

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitMapName"):
                return visitor.visitMapName(self)
            else:
                return visitor.visitChildren(self)

    def mapName(self):

        localctx = Protobuf3Parser.MapNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 86, self.RULE_mapName)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 453
            self.ident()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ServiceNameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ident(self):
            return self.getTypedRuleContext(Protobuf3Parser.IdentContext, 0)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_serviceName

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitServiceName"):
                return visitor.visitServiceName(self)
            else:
                return visitor.visitChildren(self)

    def serviceName(self):

        localctx = Protobuf3Parser.ServiceNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 88, self.RULE_serviceName)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 455
            self.ident()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class RpcNameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ident(self):
            return self.getTypedRuleContext(Protobuf3Parser.IdentContext, 0)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_rpcName

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitRpcName"):
                return visitor.visitRpcName(self)
            else:
                return visitor.visitChildren(self)

    def rpcName(self):

        localctx = Protobuf3Parser.RpcNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 90, self.RULE_rpcName)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 457
            self.ident()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class MessageTypeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def messageName(self):
            return self.getTypedRuleContext(Protobuf3Parser.MessageNameContext, 0)

        def DOT(self, i: int = None):
            if i is None:
                return self.getTokens(Protobuf3Parser.DOT)
            else:
                return self.getToken(Protobuf3Parser.DOT, i)

        def ident(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(Protobuf3Parser.IdentContext)
            else:
                return self.getTypedRuleContext(Protobuf3Parser.IdentContext, i)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_messageType

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitMessageType"):
                return visitor.visitMessageType(self)
            else:
                return visitor.visitChildren(self)

    def messageType(self):

        localctx = Protobuf3Parser.MessageTypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 92, self.RULE_messageType)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 460
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 48:
                self.state = 459
                self.match(Protobuf3Parser.DOT)

            self.state = 467
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input, 42, self._ctx)
            while _alt != 2 and _alt != ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 462
                    self.ident()
                    self.state = 463
                    self.match(Protobuf3Parser.DOT)
                self.state = 469
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input, 42, self._ctx)

            self.state = 470
            self.messageName()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class EnumTypeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def enumName(self):
            return self.getTypedRuleContext(Protobuf3Parser.EnumNameContext, 0)

        def DOT(self, i: int = None):
            if i is None:
                return self.getTokens(Protobuf3Parser.DOT)
            else:
                return self.getToken(Protobuf3Parser.DOT, i)

        def ident(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(Protobuf3Parser.IdentContext)
            else:
                return self.getTypedRuleContext(Protobuf3Parser.IdentContext, i)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_enumType

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitEnumType"):
                return visitor.visitEnumType(self)
            else:
                return visitor.visitChildren(self)

    def enumType(self):

        localctx = Protobuf3Parser.EnumTypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 94, self.RULE_enumType)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 473
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 48:
                self.state = 472
                self.match(Protobuf3Parser.DOT)

            self.state = 480
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input, 44, self._ctx)
            while _alt != 2 and _alt != ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 475
                    self.ident()
                    self.state = 476
                    self.match(Protobuf3Parser.DOT)
                self.state = 482
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input, 44, self._ctx)

            self.state = 483
            self.enumName()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class IntLitContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT_LIT(self):
            return self.getToken(Protobuf3Parser.INT_LIT, 0)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_intLit

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitIntLit"):
                return visitor.visitIntLit(self)
            else:
                return visitor.visitChildren(self)

    def intLit(self):

        localctx = Protobuf3Parser.IntLitContext(self, self._ctx, self.state)
        self.enterRule(localctx, 96, self.RULE_intLit)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 485
            self.match(Protobuf3Parser.INT_LIT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class StrLitContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STR_LIT(self):
            return self.getToken(Protobuf3Parser.STR_LIT, 0)

        def PROTO3_LIT_SINGLE(self):
            return self.getToken(Protobuf3Parser.PROTO3_LIT_SINGLE, 0)

        def PROTO3_LIT_DOBULE(self):
            return self.getToken(Protobuf3Parser.PROTO3_LIT_DOBULE, 0)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_strLit

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitStrLit"):
                return visitor.visitStrLit(self)
            else:
                return visitor.visitChildren(self)

    def strLit(self):

        localctx = Protobuf3Parser.StrLitContext(self, self._ctx, self.state)
        self.enterRule(localctx, 98, self.RULE_strLit)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 487
            _la = self._input.LA(1)
            if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 9007405413171200) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class BoolLitContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BOOL_LIT(self):
            return self.getToken(Protobuf3Parser.BOOL_LIT, 0)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_boolLit

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitBoolLit"):
                return visitor.visitBoolLit(self)
            else:
                return visitor.visitChildren(self)

    def boolLit(self):

        localctx = Protobuf3Parser.BoolLitContext(self, self._ctx, self.state)
        self.enterRule(localctx, 100, self.RULE_boolLit)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 489
            self.match(Protobuf3Parser.BOOL_LIT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class FloatLitContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FLOAT_LIT(self):
            return self.getToken(Protobuf3Parser.FLOAT_LIT, 0)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_floatLit

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitFloatLit"):
                return visitor.visitFloatLit(self)
            else:
                return visitor.visitChildren(self)

    def floatLit(self):

        localctx = Protobuf3Parser.FloatLitContext(self, self._ctx, self.state)
        self.enterRule(localctx, 102, self.RULE_floatLit)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 491
            self.match(Protobuf3Parser.FLOAT_LIT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class KeywordsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SYNTAX(self):
            return self.getToken(Protobuf3Parser.SYNTAX, 0)

        def IMPORT(self):
            return self.getToken(Protobuf3Parser.IMPORT, 0)

        def WEAK(self):
            return self.getToken(Protobuf3Parser.WEAK, 0)

        def PUBLIC(self):
            return self.getToken(Protobuf3Parser.PUBLIC, 0)

        def PACKAGE(self):
            return self.getToken(Protobuf3Parser.PACKAGE, 0)

        def OPTION(self):
            return self.getToken(Protobuf3Parser.OPTION, 0)

        def OPTIONAL(self):
            return self.getToken(Protobuf3Parser.OPTIONAL, 0)

        def REPEATED(self):
            return self.getToken(Protobuf3Parser.REPEATED, 0)

        def ONEOF(self):
            return self.getToken(Protobuf3Parser.ONEOF, 0)

        def MAP(self):
            return self.getToken(Protobuf3Parser.MAP, 0)

        def INT32(self):
            return self.getToken(Protobuf3Parser.INT32, 0)

        def INT64(self):
            return self.getToken(Protobuf3Parser.INT64, 0)

        def UINT32(self):
            return self.getToken(Protobuf3Parser.UINT32, 0)

        def UINT64(self):
            return self.getToken(Protobuf3Parser.UINT64, 0)

        def SINT32(self):
            return self.getToken(Protobuf3Parser.SINT32, 0)

        def SINT64(self):
            return self.getToken(Protobuf3Parser.SINT64, 0)

        def FIXED32(self):
            return self.getToken(Protobuf3Parser.FIXED32, 0)

        def FIXED64(self):
            return self.getToken(Protobuf3Parser.FIXED64, 0)

        def SFIXED32(self):
            return self.getToken(Protobuf3Parser.SFIXED32, 0)

        def SFIXED64(self):
            return self.getToken(Protobuf3Parser.SFIXED64, 0)

        def BOOL(self):
            return self.getToken(Protobuf3Parser.BOOL, 0)

        def STRING(self):
            return self.getToken(Protobuf3Parser.STRING, 0)

        def DOUBLE(self):
            return self.getToken(Protobuf3Parser.DOUBLE, 0)

        def FLOAT(self):
            return self.getToken(Protobuf3Parser.FLOAT, 0)

        def BYTES(self):
            return self.getToken(Protobuf3Parser.BYTES, 0)

        def RESERVED(self):
            return self.getToken(Protobuf3Parser.RESERVED, 0)

        def TO(self):
            return self.getToken(Protobuf3Parser.TO, 0)

        def MAX(self):
            return self.getToken(Protobuf3Parser.MAX, 0)

        def ENUM(self):
            return self.getToken(Protobuf3Parser.ENUM, 0)

        def MESSAGE(self):
            return self.getToken(Protobuf3Parser.MESSAGE, 0)

        def SERVICE(self):
            return self.getToken(Protobuf3Parser.SERVICE, 0)

        def EXTEND(self):
            return self.getToken(Protobuf3Parser.EXTEND, 0)

        def RPC(self):
            return self.getToken(Protobuf3Parser.RPC, 0)

        def STREAM(self):
            return self.getToken(Protobuf3Parser.STREAM, 0)

        def RETURNS(self):
            return self.getToken(Protobuf3Parser.RETURNS, 0)

        def BOOL_LIT(self):
            return self.getToken(Protobuf3Parser.BOOL_LIT, 0)

        def getRuleIndex(self):
            return Protobuf3Parser.RULE_keywords

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitKeywords"):
                return visitor.visitKeywords(self)
            else:
                return visitor.visitChildren(self)

    def keywords(self):

        localctx = Protobuf3Parser.KeywordsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 104, self.RULE_keywords)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 493
            _la = self._input.LA(1)
            if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 18014467228958718) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx
