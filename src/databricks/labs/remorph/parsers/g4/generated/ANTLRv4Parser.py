# Generated from src/databricks/labs/remorph/parsers/g4/ANTLRv4Parser.g4 by ANTLR 4.13.1
import sys

from antlr4 import (
    ATN,
    DFA,
    ATNDeserializer,
    NoViableAltException,
    Parser,
    ParserATNSimulator,
    ParserRuleContext,
    ParseTreeVisitor,
    PredictionContextCache,
    RecognitionException,
    Token,
    TokenStream,
)

if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


def serializedATN():
    return [
        4, 1, 61, 617, 2, 0, 7, 0, 2, 1, 7, 1, 2, 2, 7, 2, 2, 3, 7, 3, 2, 4, 7, 4, 2, 5, 7, 5, 2, 6, 7, 6, 2,
        7, 7, 7, 2, 8, 7, 8, 2, 9, 7, 9, 2, 10, 7, 10, 2, 11, 7, 11, 2, 12, 7, 12, 2, 13, 7, 13, 2, 14, 7, 14,
        2, 15, 7, 15, 2, 16, 7, 16, 2, 17, 7, 17, 2, 18, 7, 18, 2, 19, 7, 19, 2, 20, 7, 20, 2, 21, 7, 21, 2,
        22, 7, 22, 2, 23, 7, 23, 2, 24, 7, 24, 2, 25, 7, 25, 2, 26, 7, 26, 2, 27, 7, 27, 2, 28, 7, 28, 2, 29,
        7, 29, 2, 30, 7, 30, 2, 31, 7, 31, 2, 32, 7, 32, 2, 33, 7, 33, 2, 34, 7, 34, 2, 35, 7, 35, 2, 36, 7,
        36, 2, 37, 7, 37, 2, 38, 7, 38, 2, 39, 7, 39, 2, 40, 7, 40, 2, 41, 7, 41, 2, 42, 7, 42, 2, 43, 7, 43,
        2, 44, 7, 44, 2, 45, 7, 45, 2, 46, 7, 46, 2, 47, 7, 47, 2, 48, 7, 48, 2, 49, 7, 49, 2, 50, 7, 50, 2,
        51, 7, 51, 2, 52, 7, 52, 2, 53, 7, 53, 2, 54, 7, 54, 2, 55, 7, 55, 2, 56, 7, 56, 2, 57, 7, 57, 2, 58,
        7, 58, 2, 59, 7, 59, 2, 60, 7, 60, 2, 61, 7, 61, 2, 62, 7, 62, 1, 0, 1, 0, 5, 0, 129, 8, 0, 10, 0, 12,
        0, 132, 9, 0, 1, 0, 1, 0, 5, 0, 136, 8, 0, 10, 0, 12, 0, 139, 9, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 3, 2, 152, 8, 2, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 3, 3, 159, 8, 3, 1, 4,
        1, 4, 1, 4, 1, 4, 5, 4, 165, 8, 4, 10, 4, 12, 4, 168, 9, 4, 1, 4, 1, 4, 1, 5, 1, 5, 1, 5, 1, 5, 1, 6,
        1, 6, 1, 6, 5, 6, 179, 8, 6, 10, 6, 12, 6, 182, 9, 6, 1, 6, 1, 6, 1, 6, 3, 6, 187, 8, 6, 1, 7, 1, 7,
        1, 7, 1, 7, 5, 7, 193, 8, 7, 10, 7, 12, 7, 196, 9, 7, 1, 7, 1, 7, 1, 8, 1, 8, 1, 8, 1, 8, 1, 8, 3, 8,
        205, 8, 8, 1, 9, 1, 9, 3, 9, 209, 8, 9, 1, 9, 1, 9, 1, 10, 1, 10, 3, 10, 215, 8, 10, 1, 10, 1, 10, 1,
        11, 1, 11, 1, 11, 5, 11, 222, 8, 11, 10, 11, 12, 11, 225, 9, 11, 1, 11, 3, 11, 228, 8, 11, 1, 12, 1,
        12, 1, 12, 1, 12, 3, 12, 234, 8, 12, 1, 12, 1, 12, 1, 12, 1, 13, 1, 13, 1, 13, 3, 13, 242, 8, 13, 1,
        14, 1, 14, 5, 14, 246, 8, 14, 10, 14, 12, 14, 249, 9, 14, 1, 14, 1, 14, 1, 15, 1, 15, 5, 15, 255, 8,
        15, 10, 15, 12, 15, 258, 9, 15, 1, 15, 1, 15, 1, 16, 1, 16, 1, 16, 1, 16, 5, 16, 266, 8, 16, 10, 16,
        12, 16, 269, 9, 16, 1, 17, 5, 17, 272, 8, 17, 10, 17, 12, 17, 275, 9, 17, 1, 18, 1, 18, 3, 18, 279, 8,
        18, 1, 19, 3, 19, 282, 8, 19, 1, 19, 1, 19, 3, 19, 286, 8, 19, 1, 19, 3, 19, 289, 8, 19, 1, 19, 3, 19,
        292, 8, 19, 1, 19, 3, 19, 295, 8, 19, 1, 19, 5, 19, 298, 8, 19, 10, 19, 12, 19, 301, 9, 19, 1, 19, 1,
        19, 1, 19, 1, 19, 1, 19, 1, 20, 5, 20, 309, 8, 20, 10, 20, 12, 20, 312, 9, 20, 1, 20, 3, 20, 315, 8,
        20, 1, 21, 1, 21, 1, 21, 1, 21, 1, 22, 1, 22, 1, 22, 1, 23, 1, 23, 3, 23, 326, 8, 23, 1, 24, 1, 24, 1,
        24, 1, 25, 1, 25, 1, 25, 1, 25, 5, 25, 335, 8, 25, 10, 25, 12, 25, 338, 9, 25, 1, 26, 1, 26, 1, 26, 1,
        27, 1, 27, 1, 27, 1, 27, 1, 28, 4, 28, 348, 8, 28, 11, 28, 12, 28, 349, 1, 29, 1, 29, 1, 30, 1, 30, 1,
        31, 1, 31, 1, 31, 5, 31, 359, 8, 31, 10, 31, 12, 31, 362, 9, 31, 1, 32, 1, 32, 1, 32, 3, 32, 367, 8,
        32, 1, 33, 3, 33, 370, 8, 33, 1, 33, 1, 33, 3, 33, 374, 8, 33, 1, 33, 1, 33, 1, 33, 1, 33, 1, 34, 1,
        34, 1, 35, 1, 35, 1, 35, 5, 35, 385, 8, 35, 10, 35, 12, 35, 388, 9, 35, 1, 36, 1, 36, 3, 36, 392, 8,
        36, 1, 36, 3, 36, 395, 8, 36, 1, 37, 4, 37, 398, 8, 37, 11, 37, 12, 37, 399, 1, 37, 3, 37, 403, 8, 37,
        1, 38, 1, 38, 3, 38, 407, 8, 38, 1, 38, 1, 38, 3, 38, 411, 8, 38, 1, 38, 1, 38, 3, 38, 415, 8, 38, 3,
        38, 417, 8, 38, 1, 39, 1, 39, 1, 39, 1, 39, 1, 40, 1, 40, 1, 40, 1, 40, 5, 40, 427, 8, 40, 10, 40, 12,
        40, 430, 9, 40, 1, 41, 1, 41, 1, 41, 1, 41, 1, 41, 1, 41, 3, 41, 438, 8, 41, 1, 42, 1, 42, 3, 42, 442,
        8, 42, 1, 43, 1, 43, 3, 43, 446, 8, 43, 1, 44, 1, 44, 1, 44, 5, 44, 451, 8, 44, 10, 44, 12, 44, 454,
        9, 44, 1, 45, 3, 45, 457, 8, 45, 1, 45, 4, 45, 460, 8, 45, 11, 45, 12, 45, 461, 1, 45, 3, 45, 465, 8,
        45, 1, 46, 1, 46, 1, 46, 3, 46, 470, 8, 46, 1, 46, 1, 46, 1, 46, 3, 46, 475, 8, 46, 1, 46, 1, 46, 1,
        46, 3, 46, 480, 8, 46, 3, 46, 482, 8, 46, 1, 47, 1, 47, 1, 47, 1, 47, 3, 47, 488, 8, 47, 1, 48, 1, 48,
        3, 48, 492, 8, 48, 1, 49, 1, 49, 1, 50, 1, 50, 3, 50, 498, 8, 50, 1, 50, 1, 50, 3, 50, 502, 8, 50, 1,
        50, 1, 50, 3, 50, 506, 8, 50, 3, 50, 508, 8, 50, 1, 51, 1, 51, 1, 51, 1, 51, 1, 51, 1, 51, 3, 51, 516,
        8, 51, 3, 51, 518, 8, 51, 1, 52, 1, 52, 1, 52, 1, 52, 1, 52, 3, 52, 525, 8, 52, 3, 52, 527, 8, 52, 1,
        53, 1, 53, 1, 53, 1, 53, 3, 53, 533, 8, 53, 1, 54, 1, 54, 1, 54, 1, 54, 5, 54, 539, 8, 54, 10, 54, 12,
        54, 542, 9, 54, 1, 54, 1, 54, 1, 55, 1, 55, 3, 55, 548, 8, 55, 1, 55, 1, 55, 3, 55, 552, 8, 55, 1, 55,
        1, 55, 3, 55, 556, 8, 55, 1, 56, 1, 56, 3, 56, 560, 8, 56, 1, 56, 5, 56, 563, 8, 56, 10, 56, 12, 56,
        566, 9, 56, 1, 56, 3, 56, 569, 8, 56, 1, 56, 1, 56, 1, 56, 1, 57, 1, 57, 3, 57, 576, 8, 57, 1, 57, 3,
        57, 579, 8, 57, 1, 58, 1, 58, 1, 58, 1, 58, 1, 59, 1, 59, 3, 59, 587, 8, 59, 1, 59, 1, 59, 3, 59, 591,
        8, 59, 3, 59, 593, 8, 59, 1, 60, 1, 60, 1, 60, 1, 60, 5, 60, 599, 8, 60, 10, 60, 12, 60, 602, 9, 60,
        1, 60, 1, 60, 1, 61, 1, 61, 1, 61, 1, 61, 1, 61, 3, 61, 611, 8, 61, 3, 61, 613, 8, 61, 1, 62, 1, 62,
        1, 62, 0, 0, 63, 0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42,
        44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92,
        94, 96, 98, 100, 102, 104, 106, 108, 110, 112, 114, 116, 118, 120, 122, 124, 0, 3, 2, 0, 16, 16, 20,
        22, 2, 0, 40, 40, 43, 43, 1, 0, 1, 2, 653, 0, 126, 1, 0, 0, 0, 2, 142, 1, 0, 0, 0, 4, 151, 1, 0, 0, 0,
        6, 158, 1, 0, 0, 0, 8, 160, 1, 0, 0, 0, 10, 171, 1, 0, 0, 0, 12, 186, 1, 0, 0, 0, 14, 188, 1, 0, 0, 0,
        16, 204, 1, 0, 0, 0, 18, 206, 1, 0, 0, 0, 20, 212, 1, 0, 0, 0, 22, 218, 1, 0, 0, 0, 24, 229, 1, 0, 0,
        0, 26, 241, 1, 0, 0, 0, 28, 243, 1, 0, 0, 0, 30, 252, 1, 0, 0, 0, 32, 261, 1, 0, 0, 0, 34, 273, 1, 0,
        0, 0, 36, 278, 1, 0, 0, 0, 38, 281, 1, 0, 0, 0, 40, 310, 1, 0, 0, 0, 42, 316, 1, 0, 0, 0, 44, 320, 1,
        0, 0, 0, 46, 325, 1, 0, 0, 0, 48, 327, 1, 0, 0, 0, 50, 330, 1, 0, 0, 0, 52, 339, 1, 0, 0, 0, 54, 342,
        1, 0, 0, 0, 56, 347, 1, 0, 0, 0, 58, 351, 1, 0, 0, 0, 60, 353, 1, 0, 0, 0, 62, 355, 1, 0, 0, 0, 64,
        363, 1, 0, 0, 0, 66, 369, 1, 0, 0, 0, 68, 379, 1, 0, 0, 0, 70, 381, 1, 0, 0, 0, 72, 394, 1, 0, 0, 0,
        74, 402, 1, 0, 0, 0, 76, 416, 1, 0, 0, 0, 78, 418, 1, 0, 0, 0, 80, 422, 1, 0, 0, 0, 82, 437, 1, 0, 0,
        0, 84, 441, 1, 0, 0, 0, 86, 445, 1, 0, 0, 0, 88, 447, 1, 0, 0, 0, 90, 464, 1, 0, 0, 0, 92, 481, 1, 0,
        0, 0, 94, 483, 1, 0, 0, 0, 96, 489, 1, 0, 0, 0, 98, 493, 1, 0, 0, 0, 100, 507, 1, 0, 0, 0, 102, 517,
        1, 0, 0, 0, 104, 526, 1, 0, 0, 0, 106, 532, 1, 0, 0, 0, 108, 534, 1, 0, 0, 0, 110, 555, 1, 0, 0, 0,
        112, 557, 1, 0, 0, 0, 114, 573, 1, 0, 0, 0, 116, 580, 1, 0, 0, 0, 118, 592, 1, 0, 0, 0, 120, 594, 1,
        0, 0, 0, 122, 612, 1, 0, 0, 0, 124, 614, 1, 0, 0, 0, 126, 130, 3, 2, 1, 0, 127, 129, 3, 6, 3, 0, 128,
        127, 1, 0, 0, 0, 129, 132, 1, 0, 0, 0, 130, 128, 1, 0, 0, 0, 130, 131, 1, 0, 0, 0, 131, 133, 1, 0, 0,
        0, 132, 130, 1, 0, 0, 0, 133, 137, 3, 34, 17, 0, 134, 136, 3, 32, 16, 0, 135, 134, 1, 0, 0, 0, 136,
        139, 1, 0, 0, 0, 137, 135, 1, 0, 0, 0, 137, 138, 1, 0, 0, 0, 138, 140, 1, 0, 0, 0, 139, 137, 1, 0, 0,
        0, 140, 141, 5, 0, 0, 1, 141, 1, 1, 0, 0, 0, 142, 143, 3, 4, 2, 0, 143, 144, 3, 124, 62, 0, 144, 145,
        5, 32, 0, 0, 145, 3, 1, 0, 0, 0, 146, 147, 5, 17, 0, 0, 147, 152, 5, 19, 0, 0, 148, 149, 5, 18, 0, 0,
        149, 152, 5, 19, 0, 0, 150, 152, 5, 19, 0, 0, 151, 146, 1, 0, 0, 0, 151, 148, 1, 0, 0, 0, 151, 150, 1,
        0, 0, 0, 152, 5, 1, 0, 0, 0, 153, 159, 3, 8, 4, 0, 154, 159, 3, 14, 7, 0, 155, 159, 3, 18, 9, 0, 156,
        159, 3, 20, 10, 0, 157, 159, 3, 24, 12, 0, 158, 153, 1, 0, 0, 0, 158, 154, 1, 0, 0, 0, 158, 155, 1, 0,
        0, 0, 158, 156, 1, 0, 0, 0, 158, 157, 1, 0, 0, 0, 159, 7, 1, 0, 0, 0, 160, 166, 5, 12, 0, 0, 161, 162,
        3, 10, 5, 0, 162, 163, 5, 32, 0, 0, 163, 165, 1, 0, 0, 0, 164, 161, 1, 0, 0, 0, 165, 168, 1, 0, 0, 0,
        166, 164, 1, 0, 0, 0, 166, 167, 1, 0, 0, 0, 167, 169, 1, 0, 0, 0, 168, 166, 1, 0, 0, 0, 169, 170, 5,
        36, 0, 0, 170, 9, 1, 0, 0, 0, 171, 172, 3, 124, 62, 0, 172, 173, 5, 40, 0, 0, 173, 174, 3, 12, 6, 0,
        174, 11, 1, 0, 0, 0, 175, 180, 3, 124, 62, 0, 176, 177, 5, 48, 0, 0, 177, 179, 3, 124, 62, 0, 178,
        176, 1, 0, 0, 0, 179, 182, 1, 0, 0, 0, 180, 178, 1, 0, 0, 0, 180, 181, 1, 0, 0, 0, 181, 187, 1, 0, 0,
        0, 182, 180, 1, 0, 0, 0, 183, 187, 5, 8, 0, 0, 184, 187, 3, 28, 14, 0, 185, 187, 5, 7, 0, 0, 186, 175,
        1, 0, 0, 0, 186, 183, 1, 0, 0, 0, 186, 184, 1, 0, 0, 0, 186, 185, 1, 0, 0, 0, 187, 13, 1, 0, 0, 0,
        188, 189, 5, 15, 0, 0, 189, 194, 3, 16, 8, 0, 190, 191, 5, 31, 0, 0, 191, 193, 3, 16, 8, 0, 192, 190,
        1, 0, 0, 0, 193, 196, 1, 0, 0, 0, 194, 192, 1, 0, 0, 0, 194, 195, 1, 0, 0, 0, 195, 197, 1, 0, 0, 0,
        196, 194, 1, 0, 0, 0, 197, 198, 5, 32, 0, 0, 198, 15, 1, 0, 0, 0, 199, 200, 3, 124, 62, 0, 200, 201,
        5, 40, 0, 0, 201, 202, 3, 124, 62, 0, 202, 205, 1, 0, 0, 0, 203, 205, 3, 124, 62, 0, 204, 199, 1, 0,
        0, 0, 204, 203, 1, 0, 0, 0, 205, 17, 1, 0, 0, 0, 206, 208, 5, 13, 0, 0, 207, 209, 3, 22, 11, 0, 208,
        207, 1, 0, 0, 0, 208, 209, 1, 0, 0, 0, 209, 210, 1, 0, 0, 0, 210, 211, 5, 36, 0, 0, 211, 19, 1, 0, 0,
        0, 212, 214, 5, 14, 0, 0, 213, 215, 3, 22, 11, 0, 214, 213, 1, 0, 0, 0, 214, 215, 1, 0, 0, 0, 215,
        216, 1, 0, 0, 0, 216, 217, 5, 36, 0, 0, 217, 21, 1, 0, 0, 0, 218, 223, 3, 124, 62, 0, 219, 220, 5, 31,
        0, 0, 220, 222, 3, 124, 62, 0, 221, 219, 1, 0, 0, 0, 222, 225, 1, 0, 0, 0, 223, 221, 1, 0, 0, 0, 223,
        224, 1, 0, 0, 0, 224, 227, 1, 0, 0, 0, 225, 223, 1, 0, 0, 0, 226, 228, 5, 31, 0, 0, 227, 226, 1, 0, 0,
        0, 227, 228, 1, 0, 0, 0, 228, 23, 1, 0, 0, 0, 229, 233, 5, 49, 0, 0, 230, 231, 3, 26, 13, 0, 231, 232,
        5, 30, 0, 0, 232, 234, 1, 0, 0, 0, 233, 230, 1, 0, 0, 0, 233, 234, 1, 0, 0, 0, 234, 235, 1, 0, 0, 0,
        235, 236, 3, 124, 62, 0, 236, 237, 3, 28, 14, 0, 237, 25, 1, 0, 0, 0, 238, 242, 3, 124, 62, 0, 239,
        242, 5, 17, 0, 0, 240, 242, 5, 18, 0, 0, 241, 238, 1, 0, 0, 0, 241, 239, 1, 0, 0, 0, 241, 240, 1, 0,
        0, 0, 242, 27, 1, 0, 0, 0, 243, 247, 5, 11, 0, 0, 244, 246, 5, 60, 0, 0, 245, 244, 1, 0, 0, 0, 246,
        249, 1, 0, 0, 0, 247, 245, 1, 0, 0, 0, 247, 248, 1, 0, 0, 0, 248, 250, 1, 0, 0, 0, 249, 247, 1, 0, 0,
        0, 250, 251, 5, 58, 0, 0, 251, 29, 1, 0, 0, 0, 252, 256, 5, 10, 0, 0, 253, 255, 5, 57, 0, 0, 254, 253,
        1, 0, 0, 0, 255, 258, 1, 0, 0, 0, 256, 254, 1, 0, 0, 0, 256, 257, 1, 0, 0, 0, 257, 259, 1, 0, 0, 0,
        258, 256, 1, 0, 0, 0, 259, 260, 5, 55, 0, 0, 260, 31, 1, 0, 0, 0, 261, 262, 5, 28, 0, 0, 262, 263, 3,
        124, 62, 0, 263, 267, 5, 32, 0, 0, 264, 266, 3, 66, 33, 0, 265, 264, 1, 0, 0, 0, 266, 269, 1, 0, 0, 0,
        267, 265, 1, 0, 0, 0, 267, 268, 1, 0, 0, 0, 268, 33, 1, 0, 0, 0, 269, 267, 1, 0, 0, 0, 270, 272, 3,
        36, 18, 0, 271, 270, 1, 0, 0, 0, 272, 275, 1, 0, 0, 0, 273, 271, 1, 0, 0, 0, 273, 274, 1, 0, 0, 0,
        274, 35, 1, 0, 0, 0, 275, 273, 1, 0, 0, 0, 276, 279, 3, 38, 19, 0, 277, 279, 3, 66, 33, 0, 278, 276,
        1, 0, 0, 0, 278, 277, 1, 0, 0, 0, 279, 37, 1, 0, 0, 0, 280, 282, 3, 56, 28, 0, 281, 280, 1, 0, 0, 0,
        281, 282, 1, 0, 0, 0, 282, 283, 1, 0, 0, 0, 283, 285, 5, 2, 0, 0, 284, 286, 3, 30, 15, 0, 285, 284, 1,
        0, 0, 0, 285, 286, 1, 0, 0, 0, 286, 288, 1, 0, 0, 0, 287, 289, 3, 48, 24, 0, 288, 287, 1, 0, 0, 0,
        288, 289, 1, 0, 0, 0, 289, 291, 1, 0, 0, 0, 290, 292, 3, 50, 25, 0, 291, 290, 1, 0, 0, 0, 291, 292, 1,
        0, 0, 0, 292, 294, 1, 0, 0, 0, 293, 295, 3, 52, 26, 0, 294, 293, 1, 0, 0, 0, 294, 295, 1, 0, 0, 0,
        295, 299, 1, 0, 0, 0, 296, 298, 3, 46, 23, 0, 297, 296, 1, 0, 0, 0, 298, 301, 1, 0, 0, 0, 299, 297, 1,
        0, 0, 0, 299, 300, 1, 0, 0, 0, 300, 302, 1, 0, 0, 0, 301, 299, 1, 0, 0, 0, 302, 303, 5, 29, 0, 0, 303,
        304, 3, 60, 30, 0, 304, 305, 5, 32, 0, 0, 305, 306, 3, 40, 20, 0, 306, 39, 1, 0, 0, 0, 307, 309, 3,
        42, 21, 0, 308, 307, 1, 0, 0, 0, 309, 312, 1, 0, 0, 0, 310, 308, 1, 0, 0, 0, 310, 311, 1, 0, 0, 0,
        311, 314, 1, 0, 0, 0, 312, 310, 1, 0, 0, 0, 313, 315, 3, 44, 22, 0, 314, 313, 1, 0, 0, 0, 314, 315, 1,
        0, 0, 0, 315, 41, 1, 0, 0, 0, 316, 317, 5, 26, 0, 0, 317, 318, 3, 30, 15, 0, 318, 319, 3, 28, 14, 0,
        319, 43, 1, 0, 0, 0, 320, 321, 5, 27, 0, 0, 321, 322, 3, 28, 14, 0, 322, 45, 1, 0, 0, 0, 323, 326, 3,
        8, 4, 0, 324, 326, 3, 54, 27, 0, 325, 323, 1, 0, 0, 0, 325, 324, 1, 0, 0, 0, 326, 47, 1, 0, 0, 0, 327,
        328, 5, 23, 0, 0, 328, 329, 3, 30, 15, 0, 329, 49, 1, 0, 0, 0, 330, 331, 5, 25, 0, 0, 331, 336, 3,
        124, 62, 0, 332, 333, 5, 31, 0, 0, 333, 335, 3, 124, 62, 0, 334, 332, 1, 0, 0, 0, 335, 338, 1, 0, 0,
        0, 336, 334, 1, 0, 0, 0, 336, 337, 1, 0, 0, 0, 337, 51, 1, 0, 0, 0, 338, 336, 1, 0, 0, 0, 339, 340, 5,
        24, 0, 0, 340, 341, 3, 30, 15, 0, 341, 53, 1, 0, 0, 0, 342, 343, 5, 49, 0, 0, 343, 344, 3, 124, 62, 0,
        344, 345, 3, 28, 14, 0, 345, 55, 1, 0, 0, 0, 346, 348, 3, 58, 29, 0, 347, 346, 1, 0, 0, 0, 348, 349,
        1, 0, 0, 0, 349, 347, 1, 0, 0, 0, 349, 350, 1, 0, 0, 0, 350, 57, 1, 0, 0, 0, 351, 352, 7, 0, 0, 0,
        352, 59, 1, 0, 0, 0, 353, 354, 3, 62, 31, 0, 354, 61, 1, 0, 0, 0, 355, 360, 3, 64, 32, 0, 356, 357, 5,
        45, 0, 0, 357, 359, 3, 64, 32, 0, 358, 356, 1, 0, 0, 0, 359, 362, 1, 0, 0, 0, 360, 358, 1, 0, 0, 0,
        360, 361, 1, 0, 0, 0, 361, 63, 1, 0, 0, 0, 362, 360, 1, 0, 0, 0, 363, 366, 3, 90, 45, 0, 364, 365, 5,
        50, 0, 0, 365, 367, 3, 124, 62, 0, 366, 364, 1, 0, 0, 0, 366, 367, 1, 0, 0, 0, 367, 65, 1, 0, 0, 0,
        368, 370, 5, 16, 0, 0, 369, 368, 1, 0, 0, 0, 369, 370, 1, 0, 0, 0, 370, 371, 1, 0, 0, 0, 371, 373, 5,
        1, 0, 0, 372, 374, 3, 8, 4, 0, 373, 372, 1, 0, 0, 0, 373, 374, 1, 0, 0, 0, 374, 375, 1, 0, 0, 0, 375,
        376, 5, 29, 0, 0, 376, 377, 3, 68, 34, 0, 377, 378, 5, 32, 0, 0, 378, 67, 1, 0, 0, 0, 379, 380, 3, 70,
        35, 0, 380, 69, 1, 0, 0, 0, 381, 386, 3, 72, 36, 0, 382, 383, 5, 45, 0, 0, 383, 385, 3, 72, 36, 0,
        384, 382, 1, 0, 0, 0, 385, 388, 1, 0, 0, 0, 386, 384, 1, 0, 0, 0, 386, 387, 1, 0, 0, 0, 387, 71, 1, 0,
        0, 0, 388, 386, 1, 0, 0, 0, 389, 391, 3, 74, 37, 0, 390, 392, 3, 80, 40, 0, 391, 390, 1, 0, 0, 0, 391,
        392, 1, 0, 0, 0, 392, 395, 1, 0, 0, 0, 393, 395, 1, 0, 0, 0, 394, 389, 1, 0, 0, 0, 394, 393, 1, 0, 0,
        0, 395, 73, 1, 0, 0, 0, 396, 398, 3, 76, 38, 0, 397, 396, 1, 0, 0, 0, 398, 399, 1, 0, 0, 0, 399, 397,
        1, 0, 0, 0, 399, 400, 1, 0, 0, 0, 400, 403, 1, 0, 0, 0, 401, 403, 1, 0, 0, 0, 402, 397, 1, 0, 0, 0,
        402, 401, 1, 0, 0, 0, 403, 75, 1, 0, 0, 0, 404, 406, 3, 102, 51, 0, 405, 407, 3, 100, 50, 0, 406, 405,
        1, 0, 0, 0, 406, 407, 1, 0, 0, 0, 407, 417, 1, 0, 0, 0, 408, 410, 3, 78, 39, 0, 409, 411, 3, 100, 50,
        0, 410, 409, 1, 0, 0, 0, 410, 411, 1, 0, 0, 0, 411, 417, 1, 0, 0, 0, 412, 414, 3, 28, 14, 0, 413, 415,
        5, 41, 0, 0, 414, 413, 1, 0, 0, 0, 414, 415, 1, 0, 0, 0, 415, 417, 1, 0, 0, 0, 416, 404, 1, 0, 0, 0,
        416, 408, 1, 0, 0, 0, 416, 412, 1, 0, 0, 0, 417, 77, 1, 0, 0, 0, 418, 419, 5, 33, 0, 0, 419, 420, 3,
        70, 35, 0, 420, 421, 5, 34, 0, 0, 421, 79, 1, 0, 0, 0, 422, 423, 5, 37, 0, 0, 423, 428, 3, 82, 41, 0,
        424, 425, 5, 31, 0, 0, 425, 427, 3, 82, 41, 0, 426, 424, 1, 0, 0, 0, 427, 430, 1, 0, 0, 0, 428, 426,
        1, 0, 0, 0, 428, 429, 1, 0, 0, 0, 429, 81, 1, 0, 0, 0, 430, 428, 1, 0, 0, 0, 431, 432, 3, 84, 42, 0,
        432, 433, 5, 33, 0, 0, 433, 434, 3, 86, 43, 0, 434, 435, 5, 34, 0, 0, 435, 438, 1, 0, 0, 0, 436, 438,
        3, 84, 42, 0, 437, 431, 1, 0, 0, 0, 437, 436, 1, 0, 0, 0, 438, 83, 1, 0, 0, 0, 439, 442, 3, 124, 62,
        0, 440, 442, 5, 28, 0, 0, 441, 439, 1, 0, 0, 0, 441, 440, 1, 0, 0, 0, 442, 85, 1, 0, 0, 0, 443, 446,
        3, 124, 62, 0, 444, 446, 5, 7, 0, 0, 445, 443, 1, 0, 0, 0, 445, 444, 1, 0, 0, 0, 446, 87, 1, 0, 0, 0,
        447, 452, 3, 90, 45, 0, 448, 449, 5, 45, 0, 0, 449, 451, 3, 90, 45, 0, 450, 448, 1, 0, 0, 0, 451, 454,
        1, 0, 0, 0, 452, 450, 1, 0, 0, 0, 452, 453, 1, 0, 0, 0, 453, 89, 1, 0, 0, 0, 454, 452, 1, 0, 0, 0,
        455, 457, 3, 120, 60, 0, 456, 455, 1, 0, 0, 0, 456, 457, 1, 0, 0, 0, 457, 459, 1, 0, 0, 0, 458, 460,
        3, 92, 46, 0, 459, 458, 1, 0, 0, 0, 460, 461, 1, 0, 0, 0, 461, 459, 1, 0, 0, 0, 461, 462, 1, 0, 0, 0,
        462, 465, 1, 0, 0, 0, 463, 465, 1, 0, 0, 0, 464, 456, 1, 0, 0, 0, 464, 463, 1, 0, 0, 0, 465, 91, 1, 0,
        0, 0, 466, 469, 3, 94, 47, 0, 467, 470, 3, 100, 50, 0, 468, 470, 1, 0, 0, 0, 469, 467, 1, 0, 0, 0,
        469, 468, 1, 0, 0, 0, 470, 482, 1, 0, 0, 0, 471, 474, 3, 104, 52, 0, 472, 475, 3, 100, 50, 0, 473,
        475, 1, 0, 0, 0, 474, 472, 1, 0, 0, 0, 474, 473, 1, 0, 0, 0, 475, 482, 1, 0, 0, 0, 476, 482, 3, 96,
        48, 0, 477, 479, 3, 28, 14, 0, 478, 480, 5, 41, 0, 0, 479, 478, 1, 0, 0, 0, 479, 480, 1, 0, 0, 0, 480,
        482, 1, 0, 0, 0, 481, 466, 1, 0, 0, 0, 481, 471, 1, 0, 0, 0, 481, 476, 1, 0, 0, 0, 481, 477, 1, 0, 0,
        0, 482, 93, 1, 0, 0, 0, 483, 484, 3, 124, 62, 0, 484, 487, 7, 1, 0, 0, 485, 488, 3, 104, 52, 0, 486,
        488, 3, 112, 56, 0, 487, 485, 1, 0, 0, 0, 487, 486, 1, 0, 0, 0, 488, 95, 1, 0, 0, 0, 489, 491, 3, 112,
        56, 0, 490, 492, 3, 98, 49, 0, 491, 490, 1, 0, 0, 0, 491, 492, 1, 0, 0, 0, 492, 97, 1, 0, 0, 0, 493,
        494, 3, 100, 50, 0, 494, 99, 1, 0, 0, 0, 495, 497, 5, 41, 0, 0, 496, 498, 5, 41, 0, 0, 497, 496, 1, 0,
        0, 0, 497, 498, 1, 0, 0, 0, 498, 508, 1, 0, 0, 0, 499, 501, 5, 42, 0, 0, 500, 502, 5, 41, 0, 0, 501,
        500, 1, 0, 0, 0, 501, 502, 1, 0, 0, 0, 502, 508, 1, 0, 0, 0, 503, 505, 5, 44, 0, 0, 504, 506, 5, 41,
        0, 0, 505, 504, 1, 0, 0, 0, 505, 506, 1, 0, 0, 0, 506, 508, 1, 0, 0, 0, 507, 495, 1, 0, 0, 0, 507,
        499, 1, 0, 0, 0, 507, 503, 1, 0, 0, 0, 508, 101, 1, 0, 0, 0, 509, 518, 3, 116, 58, 0, 510, 518, 3,
        118, 59, 0, 511, 518, 3, 106, 53, 0, 512, 518, 5, 3, 0, 0, 513, 515, 5, 48, 0, 0, 514, 516, 3, 120,
        60, 0, 515, 514, 1, 0, 0, 0, 515, 516, 1, 0, 0, 0, 516, 518, 1, 0, 0, 0, 517, 509, 1, 0, 0, 0, 517,
        510, 1, 0, 0, 0, 517, 511, 1, 0, 0, 0, 517, 512, 1, 0, 0, 0, 517, 513, 1, 0, 0, 0, 518, 103, 1, 0, 0,
        0, 519, 527, 3, 118, 59, 0, 520, 527, 3, 114, 57, 0, 521, 527, 3, 106, 53, 0, 522, 524, 5, 48, 0, 0,
        523, 525, 3, 120, 60, 0, 524, 523, 1, 0, 0, 0, 524, 525, 1, 0, 0, 0, 525, 527, 1, 0, 0, 0, 526, 519,
        1, 0, 0, 0, 526, 520, 1, 0, 0, 0, 526, 521, 1, 0, 0, 0, 526, 522, 1, 0, 0, 0, 527, 105, 1, 0, 0, 0,
        528, 529, 5, 51, 0, 0, 529, 533, 3, 110, 55, 0, 530, 531, 5, 51, 0, 0, 531, 533, 3, 108, 54, 0, 532,
        528, 1, 0, 0, 0, 532, 530, 1, 0, 0, 0, 533, 107, 1, 0, 0, 0, 534, 535, 5, 33, 0, 0, 535, 540, 3, 110,
        55, 0, 536, 537, 5, 45, 0, 0, 537, 539, 3, 110, 55, 0, 538, 536, 1, 0, 0, 0, 539, 542, 1, 0, 0, 0,
        540, 538, 1, 0, 0, 0, 540, 541, 1, 0, 0, 0, 541, 543, 1, 0, 0, 0, 542, 540, 1, 0, 0, 0, 543, 544, 5,
        34, 0, 0, 544, 109, 1, 0, 0, 0, 545, 547, 5, 1, 0, 0, 546, 548, 3, 120, 60, 0, 547, 546, 1, 0, 0, 0,
        547, 548, 1, 0, 0, 0, 548, 556, 1, 0, 0, 0, 549, 551, 5, 8, 0, 0, 550, 552, 3, 120, 60, 0, 551, 550,
        1, 0, 0, 0, 551, 552, 1, 0, 0, 0, 552, 556, 1, 0, 0, 0, 553, 556, 3, 116, 58, 0, 554, 556, 5, 3, 0, 0,
        555, 545, 1, 0, 0, 0, 555, 549, 1, 0, 0, 0, 555, 553, 1, 0, 0, 0, 555, 554, 1, 0, 0, 0, 556, 111, 1,
        0, 0, 0, 557, 568, 5, 33, 0, 0, 558, 560, 3, 8, 4, 0, 559, 558, 1, 0, 0, 0, 559, 560, 1, 0, 0, 0, 560,
        564, 1, 0, 0, 0, 561, 563, 3, 54, 27, 0, 562, 561, 1, 0, 0, 0, 563, 566, 1, 0, 0, 0, 564, 562, 1, 0,
        0, 0, 564, 565, 1, 0, 0, 0, 565, 567, 1, 0, 0, 0, 566, 564, 1, 0, 0, 0, 567, 569, 5, 29, 0, 0, 568,
        559, 1, 0, 0, 0, 568, 569, 1, 0, 0, 0, 569, 570, 1, 0, 0, 0, 570, 571, 3, 88, 44, 0, 571, 572, 5, 34,
        0, 0, 572, 113, 1, 0, 0, 0, 573, 575, 5, 2, 0, 0, 574, 576, 3, 30, 15, 0, 575, 574, 1, 0, 0, 0, 575,
        576, 1, 0, 0, 0, 576, 578, 1, 0, 0, 0, 577, 579, 3, 120, 60, 0, 578, 577, 1, 0, 0, 0, 578, 579, 1, 0,
        0, 0, 579, 115, 1, 0, 0, 0, 580, 581, 5, 8, 0, 0, 581, 582, 5, 47, 0, 0, 582, 583, 5, 8, 0, 0, 583,
        117, 1, 0, 0, 0, 584, 586, 5, 1, 0, 0, 585, 587, 3, 120, 60, 0, 586, 585, 1, 0, 0, 0, 586, 587, 1, 0,
        0, 0, 587, 593, 1, 0, 0, 0, 588, 590, 5, 8, 0, 0, 589, 591, 3, 120, 60, 0, 590, 589, 1, 0, 0, 0, 590,
        591, 1, 0, 0, 0, 591, 593, 1, 0, 0, 0, 592, 584, 1, 0, 0, 0, 592, 588, 1, 0, 0, 0, 593, 119, 1, 0, 0,
        0, 594, 595, 5, 38, 0, 0, 595, 600, 3, 122, 61, 0, 596, 597, 5, 31, 0, 0, 597, 599, 3, 122, 61, 0,
        598, 596, 1, 0, 0, 0, 599, 602, 1, 0, 0, 0, 600, 598, 1, 0, 0, 0, 600, 601, 1, 0, 0, 0, 601, 603, 1,
        0, 0, 0, 602, 600, 1, 0, 0, 0, 603, 604, 5, 39, 0, 0, 604, 121, 1, 0, 0, 0, 605, 613, 3, 124, 62, 0,
        606, 607, 3, 124, 62, 0, 607, 610, 5, 40, 0, 0, 608, 611, 3, 124, 62, 0, 609, 611, 5, 8, 0, 0, 610,
        608, 1, 0, 0, 0, 610, 609, 1, 0, 0, 0, 611, 613, 1, 0, 0, 0, 612, 605, 1, 0, 0, 0, 612, 606, 1, 0, 0,
        0, 613, 123, 1, 0, 0, 0, 614, 615, 7, 2, 0, 0, 615, 125, 1, 0, 0, 0, 82, 130, 137, 151, 158, 166, 180,
        186, 194, 204, 208, 214, 223, 227, 233, 241, 247, 256, 267, 273, 278, 281, 285, 288, 291, 294, 299,
        310, 314, 325, 336, 349, 360, 366, 369, 373, 386, 391, 394, 399, 402, 406, 410, 414, 416, 428, 437,
        441, 445, 452, 456, 461, 464, 469, 474, 479, 481, 487, 491, 497, 501, 505, 507, 515, 517, 524, 526,
        532, 540, 547, 551, 555, 559, 564, 568, 575, 578, 586, 590, 592, 600, 610, 612,
    ]


class ANTLRv4Parser(Parser):
    grammarFileName = "ANTLRv4Parser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [DFA(ds, i) for i, ds in enumerate(atn.decisionToState)]

    sharedContextCache = PredictionContextCache()

    literalNames = [
        "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>",
        "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>",
        "<INVALID>", "'import'", "'fragment'", "'lexer'", "'parser'", "'grammar'", "'protected'", "'public'",
        "'private'", "'returns'", "'locals'", "'throws'", "'catch'", "'finally'", "'mode'",
    ]

    symbolicNames = [
        "<INVALID>", "TOKEN_REF", "RULE_REF", "LEXER_CHAR_SET", "DOC_COMMENT", "BLOCK_COMMENT",
        "LINE_COMMENT", "INT", "STRING_LITERAL", "UNTERMINATED_STRING_LITERAL", "BEGIN_ARGUMENT",
        "BEGIN_ACTION", "OPTIONS", "TOKENS", "CHANNELS", "IMPORT", "FRAGMENT", "LEXER", "PARSER", "GRAMMAR",
        "PROTECTED", "PUBLIC", "PRIVATE", "RETURNS", "LOCALS", "THROWS", "CATCH", "FINALLY", "MODE", "COLON",
        "COLONCOLON", "COMMA", "SEMI", "LPAREN", "RPAREN", "LBRACE", "RBRACE", "RARROW", "LT", "GT", "ASSIGN",
        "QUESTION", "STAR", "PLUS_ASSIGN", "PLUS", "OR", "DOLLAR", "RANGE", "DOT", "AT", "POUND", "NOT", "ID",
        "WS", "ERRCHAR", "END_ARGUMENT", "UNTERMINATED_ARGUMENT", "ARGUMENT_CONTENT", "END_ACTION",
        "UNTERMINATED_ACTION", "ACTION_CONTENT", "UNTERMINATED_CHAR_SET",
    ]

    RULE_grammarSpec = 0
    RULE_grammarDecl = 1
    RULE_grammarType = 2
    RULE_prequelConstruct = 3
    RULE_optionsSpec = 4
    RULE_option = 5
    RULE_optionValue = 6
    RULE_delegateGrammars = 7
    RULE_delegateGrammar = 8
    RULE_tokensSpec = 9
    RULE_channelsSpec = 10
    RULE_idList = 11
    RULE_action_ = 12
    RULE_actionScopeName = 13
    RULE_actionBlock = 14
    RULE_argActionBlock = 15
    RULE_modeSpec = 16
    RULE_rules = 17
    RULE_ruleSpec = 18
    RULE_parserRuleSpec = 19
    RULE_exceptionGroup = 20
    RULE_exceptionHandler = 21
    RULE_finallyClause = 22
    RULE_rulePrequel = 23
    RULE_ruleReturns = 24
    RULE_throwsSpec = 25
    RULE_localsSpec = 26
    RULE_ruleAction = 27
    RULE_ruleModifiers = 28
    RULE_ruleModifier = 29
    RULE_ruleBlock = 30
    RULE_ruleAltList = 31
    RULE_labeledAlt = 32
    RULE_lexerRuleSpec = 33
    RULE_lexerRuleBlock = 34
    RULE_lexerAltList = 35
    RULE_lexerAlt = 36
    RULE_lexerElements = 37
    RULE_lexerElement = 38
    RULE_lexerBlock = 39
    RULE_lexerCommands = 40
    RULE_lexerCommand = 41
    RULE_lexerCommandName = 42
    RULE_lexerCommandExpr = 43
    RULE_altList = 44
    RULE_alternative = 45
    RULE_element = 46
    RULE_labeledElement = 47
    RULE_ebnf = 48
    RULE_blockSuffix = 49
    RULE_ebnfSuffix = 50
    RULE_lexerAtom = 51
    RULE_atom = 52
    RULE_notSet = 53
    RULE_blockSet = 54
    RULE_setElement = 55
    RULE_block = 56
    RULE_ruleref = 57
    RULE_characterRange = 58
    RULE_terminal = 59
    RULE_elementOptions = 60
    RULE_elementOption = 61
    RULE_identifier = 62

    ruleNames = [
        "grammarSpec", "grammarDecl", "grammarType", "prequelConstruct", "optionsSpec", "option",
        "optionValue", "delegateGrammars", "delegateGrammar", "tokensSpec", "channelsSpec", "idList",
        "action_", "actionScopeName", "actionBlock", "argActionBlock", "modeSpec", "rules", "ruleSpec",
        "parserRuleSpec", "exceptionGroup", "exceptionHandler", "finallyClause", "rulePrequel", "ruleReturns",
        "throwsSpec", "localsSpec", "ruleAction", "ruleModifiers", "ruleModifier", "ruleBlock", "ruleAltList",
        "labeledAlt", "lexerRuleSpec", "lexerRuleBlock", "lexerAltList", "lexerAlt", "lexerElements",
        "lexerElement", "lexerBlock", "lexerCommands", "lexerCommand", "lexerCommandName", "lexerCommandExpr",
        "altList", "alternative", "element", "labeledElement", "ebnf", "blockSuffix", "ebnfSuffix",
        "lexerAtom", "atom", "notSet", "blockSet", "setElement", "block", "ruleref", "characterRange",
        "terminal", "elementOptions", "elementOption", "identifier",
    ]

    EOF = Token.EOF
    TOKEN_REF = 1
    RULE_REF = 2
    LEXER_CHAR_SET = 3
    DOC_COMMENT = 4
    BLOCK_COMMENT = 5
    LINE_COMMENT = 6
    INT = 7
    STRING_LITERAL = 8
    UNTERMINATED_STRING_LITERAL = 9
    BEGIN_ARGUMENT = 10
    BEGIN_ACTION = 11
    OPTIONS = 12
    TOKENS = 13
    CHANNELS = 14
    IMPORT = 15
    FRAGMENT = 16
    LEXER = 17
    PARSER = 18
    GRAMMAR = 19
    PROTECTED = 20
    PUBLIC = 21
    PRIVATE = 22
    RETURNS = 23
    LOCALS = 24
    THROWS = 25
    CATCH = 26
    FINALLY = 27
    MODE = 28
    COLON = 29
    COLONCOLON = 30
    COMMA = 31
    SEMI = 32
    LPAREN = 33
    RPAREN = 34
    LBRACE = 35
    RBRACE = 36
    RARROW = 37
    LT = 38
    GT = 39
    ASSIGN = 40
    QUESTION = 41
    STAR = 42
    PLUS_ASSIGN = 43
    PLUS = 44
    OR = 45
    DOLLAR = 46
    RANGE = 47
    DOT = 48
    AT = 49
    POUND = 50
    NOT = 51
    ID = 52
    WS = 53
    ERRCHAR = 54
    END_ARGUMENT = 55
    UNTERMINATED_ARGUMENT = 56
    ARGUMENT_CONTENT = 57
    END_ACTION = 58
    UNTERMINATED_ACTION = 59
    ACTION_CONTENT = 60
    UNTERMINATED_CHAR_SET = 61

    def __init__(self, input: TokenStream, output: TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None

    class GrammarSpecContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def grammarDecl(self):
            return self.getTypedRuleContext(ANTLRv4Parser.GrammarDeclContext, 0)

        def rules(self):
            return self.getTypedRuleContext(ANTLRv4Parser.RulesContext, 0)

        def EOF(self):
            return self.getToken(ANTLRv4Parser.EOF, 0)

        def prequelConstruct(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(ANTLRv4Parser.PrequelConstructContext)
            else:
                return self.getTypedRuleContext(ANTLRv4Parser.PrequelConstructContext, i)

        def modeSpec(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(ANTLRv4Parser.ModeSpecContext)
            else:
                return self.getTypedRuleContext(ANTLRv4Parser.ModeSpecContext, i)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_grammarSpec

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitGrammarSpec"):
                return visitor.visitGrammarSpec(self)
            else:
                return visitor.visitChildren(self)

    def grammarSpec(self):
        localctx = ANTLRv4Parser.GrammarSpecContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_grammarSpec)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 126
            self.grammarDecl()
            self.state = 130
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while ((_la) & ~0x3F) == 0 and ((1 << _la) & 562949953482752) != 0:
                self.state = 127
                self.prequelConstruct()
                self.state = 132
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 133
            self.rules()
            self.state = 137
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 28:
                self.state = 134
                self.modeSpec()
                self.state = 139
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 140
            self.match(ANTLRv4Parser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class GrammarDeclContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def grammarType(self):
            return self.getTypedRuleContext(ANTLRv4Parser.GrammarTypeContext, 0)

        def identifier(self):
            return self.getTypedRuleContext(ANTLRv4Parser.IdentifierContext, 0)

        def SEMI(self):
            return self.getToken(ANTLRv4Parser.SEMI, 0)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_grammarDecl

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitGrammarDecl"):
                return visitor.visitGrammarDecl(self)
            else:
                return visitor.visitChildren(self)

    def grammarDecl(self):
        localctx = ANTLRv4Parser.GrammarDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_grammarDecl)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 142
            self.grammarType()
            self.state = 143
            self.identifier()
            self.state = 144
            self.match(ANTLRv4Parser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class GrammarTypeContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LEXER(self):
            return self.getToken(ANTLRv4Parser.LEXER, 0)

        def GRAMMAR(self):
            return self.getToken(ANTLRv4Parser.GRAMMAR, 0)

        def PARSER(self):
            return self.getToken(ANTLRv4Parser.PARSER, 0)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_grammarType

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitGrammarType"):
                return visitor.visitGrammarType(self)
            else:
                return visitor.visitChildren(self)

    def grammarType(self):
        localctx = ANTLRv4Parser.GrammarTypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_grammarType)
        try:
            self.state = 151
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [17]:
                self.enterOuterAlt(localctx, 1)
                self.state = 146
                self.match(ANTLRv4Parser.LEXER)
                self.state = 147
                self.match(ANTLRv4Parser.GRAMMAR)
            elif token in [18]:
                self.enterOuterAlt(localctx, 2)
                self.state = 148
                self.match(ANTLRv4Parser.PARSER)
                self.state = 149
                self.match(ANTLRv4Parser.GRAMMAR)
            elif token in [19]:
                self.enterOuterAlt(localctx, 3)
                self.state = 150
                self.match(ANTLRv4Parser.GRAMMAR)
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class PrequelConstructContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def optionsSpec(self):
            return self.getTypedRuleContext(ANTLRv4Parser.OptionsSpecContext, 0)

        def delegateGrammars(self):
            return self.getTypedRuleContext(ANTLRv4Parser.DelegateGrammarsContext, 0)

        def tokensSpec(self):
            return self.getTypedRuleContext(ANTLRv4Parser.TokensSpecContext, 0)

        def channelsSpec(self):
            return self.getTypedRuleContext(ANTLRv4Parser.ChannelsSpecContext, 0)

        def action_(self):
            return self.getTypedRuleContext(ANTLRv4Parser.Action_Context, 0)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_prequelConstruct

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitPrequelConstruct"):
                return visitor.visitPrequelConstruct(self)
            else:
                return visitor.visitChildren(self)

    def prequelConstruct(self):
        localctx = ANTLRv4Parser.PrequelConstructContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_prequelConstruct)
        try:
            self.state = 158
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [12]:
                self.enterOuterAlt(localctx, 1)
                self.state = 153
                self.optionsSpec()
            elif token in [15]:
                self.enterOuterAlt(localctx, 2)
                self.state = 154
                self.delegateGrammars()
            elif token in [13]:
                self.enterOuterAlt(localctx, 3)
                self.state = 155
                self.tokensSpec()
            elif token in [14]:
                self.enterOuterAlt(localctx, 4)
                self.state = 156
                self.channelsSpec()
            elif token in [49]:
                self.enterOuterAlt(localctx, 5)
                self.state = 157
                self.action_()
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class OptionsSpecContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def OPTIONS(self):
            return self.getToken(ANTLRv4Parser.OPTIONS, 0)

        def RBRACE(self):
            return self.getToken(ANTLRv4Parser.RBRACE, 0)

        def option(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(ANTLRv4Parser.OptionContext)
            else:
                return self.getTypedRuleContext(ANTLRv4Parser.OptionContext, i)

        def SEMI(self, i: int = None):
            if i is None:
                return self.getTokens(ANTLRv4Parser.SEMI)
            else:
                return self.getToken(ANTLRv4Parser.SEMI, i)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_optionsSpec

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitOptionsSpec"):
                return visitor.visitOptionsSpec(self)
            else:
                return visitor.visitChildren(self)

    def optionsSpec(self):
        localctx = ANTLRv4Parser.OptionsSpecContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_optionsSpec)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 160
            self.match(ANTLRv4Parser.OPTIONS)
            self.state = 166
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 1 or _la == 2:
                self.state = 161
                self.option()
                self.state = 162
                self.match(ANTLRv4Parser.SEMI)
                self.state = 168
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 169
            self.match(ANTLRv4Parser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class OptionContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self):
            return self.getTypedRuleContext(ANTLRv4Parser.IdentifierContext, 0)

        def ASSIGN(self):
            return self.getToken(ANTLRv4Parser.ASSIGN, 0)

        def optionValue(self):
            return self.getTypedRuleContext(ANTLRv4Parser.OptionValueContext, 0)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_option

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitOption"):
                return visitor.visitOption(self)
            else:
                return visitor.visitChildren(self)

    def option(self):
        localctx = ANTLRv4Parser.OptionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_option)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 171
            self.identifier()
            self.state = 172
            self.match(ANTLRv4Parser.ASSIGN)
            self.state = 173
            self.optionValue()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class OptionValueContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(ANTLRv4Parser.IdentifierContext)
            else:
                return self.getTypedRuleContext(ANTLRv4Parser.IdentifierContext, i)

        def DOT(self, i: int = None):
            if i is None:
                return self.getTokens(ANTLRv4Parser.DOT)
            else:
                return self.getToken(ANTLRv4Parser.DOT, i)

        def STRING_LITERAL(self):
            return self.getToken(ANTLRv4Parser.STRING_LITERAL, 0)

        def actionBlock(self):
            return self.getTypedRuleContext(ANTLRv4Parser.ActionBlockContext, 0)

        def INT(self):
            return self.getToken(ANTLRv4Parser.INT, 0)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_optionValue

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitOptionValue"):
                return visitor.visitOptionValue(self)
            else:
                return visitor.visitChildren(self)

    def optionValue(self):
        localctx = ANTLRv4Parser.OptionValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_optionValue)
        self._la = 0 # Token type
        try:
            self.state = 186
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1, 2]:
                self.enterOuterAlt(localctx, 1)
                self.state = 175
                self.identifier()
                self.state = 180
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la == 48:
                    self.state = 176
                    self.match(ANTLRv4Parser.DOT)
                    self.state = 177
                    self.identifier()
                    self.state = 182
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

            elif token in [8]:
                self.enterOuterAlt(localctx, 2)
                self.state = 183
                self.match(ANTLRv4Parser.STRING_LITERAL)
            elif token in [11]:
                self.enterOuterAlt(localctx, 3)
                self.state = 184
                self.actionBlock()
            elif token in [7]:
                self.enterOuterAlt(localctx, 4)
                self.state = 185
                self.match(ANTLRv4Parser.INT)
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class DelegateGrammarsContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IMPORT(self):
            return self.getToken(ANTLRv4Parser.IMPORT, 0)

        def delegateGrammar(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(ANTLRv4Parser.DelegateGrammarContext)
            else:
                return self.getTypedRuleContext(ANTLRv4Parser.DelegateGrammarContext, i)

        def SEMI(self):
            return self.getToken(ANTLRv4Parser.SEMI, 0)

        def COMMA(self, i: int = None):
            if i is None:
                return self.getTokens(ANTLRv4Parser.COMMA)
            else:
                return self.getToken(ANTLRv4Parser.COMMA, i)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_delegateGrammars

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitDelegateGrammars"):
                return visitor.visitDelegateGrammars(self)
            else:
                return visitor.visitChildren(self)

    def delegateGrammars(self):
        localctx = ANTLRv4Parser.DelegateGrammarsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_delegateGrammars)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 188
            self.match(ANTLRv4Parser.IMPORT)
            self.state = 189
            self.delegateGrammar()
            self.state = 194
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 31:
                self.state = 190
                self.match(ANTLRv4Parser.COMMA)
                self.state = 191
                self.delegateGrammar()
                self.state = 196
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 197
            self.match(ANTLRv4Parser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class DelegateGrammarContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(ANTLRv4Parser.IdentifierContext)
            else:
                return self.getTypedRuleContext(ANTLRv4Parser.IdentifierContext, i)

        def ASSIGN(self):
            return self.getToken(ANTLRv4Parser.ASSIGN, 0)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_delegateGrammar

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitDelegateGrammar"):
                return visitor.visitDelegateGrammar(self)
            else:
                return visitor.visitChildren(self)

    def delegateGrammar(self):
        localctx = ANTLRv4Parser.DelegateGrammarContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_delegateGrammar)
        try:
            self.state = 204
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 8, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 199
                self.identifier()
                self.state = 200
                self.match(ANTLRv4Parser.ASSIGN)
                self.state = 201
                self.identifier()

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 203
                self.identifier()

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class TokensSpecContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TOKENS(self):
            return self.getToken(ANTLRv4Parser.TOKENS, 0)

        def RBRACE(self):
            return self.getToken(ANTLRv4Parser.RBRACE, 0)

        def idList(self):
            return self.getTypedRuleContext(ANTLRv4Parser.IdListContext, 0)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_tokensSpec

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitTokensSpec"):
                return visitor.visitTokensSpec(self)
            else:
                return visitor.visitChildren(self)

    def tokensSpec(self):
        localctx = ANTLRv4Parser.TokensSpecContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_tokensSpec)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 206
            self.match(ANTLRv4Parser.TOKENS)
            self.state = 208
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 1 or _la == 2:
                self.state = 207
                self.idList()

            self.state = 210
            self.match(ANTLRv4Parser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ChannelsSpecContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CHANNELS(self):
            return self.getToken(ANTLRv4Parser.CHANNELS, 0)

        def RBRACE(self):
            return self.getToken(ANTLRv4Parser.RBRACE, 0)

        def idList(self):
            return self.getTypedRuleContext(ANTLRv4Parser.IdListContext, 0)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_channelsSpec

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitChannelsSpec"):
                return visitor.visitChannelsSpec(self)
            else:
                return visitor.visitChildren(self)

    def channelsSpec(self):
        localctx = ANTLRv4Parser.ChannelsSpecContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_channelsSpec)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 212
            self.match(ANTLRv4Parser.CHANNELS)
            self.state = 214
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 1 or _la == 2:
                self.state = 213
                self.idList()

            self.state = 216
            self.match(ANTLRv4Parser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class IdListContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(ANTLRv4Parser.IdentifierContext)
            else:
                return self.getTypedRuleContext(ANTLRv4Parser.IdentifierContext, i)

        def COMMA(self, i: int = None):
            if i is None:
                return self.getTokens(ANTLRv4Parser.COMMA)
            else:
                return self.getToken(ANTLRv4Parser.COMMA, i)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_idList

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitIdList"):
                return visitor.visitIdList(self)
            else:
                return visitor.visitChildren(self)

    def idList(self):
        localctx = ANTLRv4Parser.IdListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_idList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 218
            self.identifier()
            self.state = 223
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input, 11, self._ctx)
            while _alt != 2 and _alt != ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 219
                    self.match(ANTLRv4Parser.COMMA)
                    self.state = 220
                    self.identifier()
                self.state = 225
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input, 11, self._ctx)

            self.state = 227
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 31:
                self.state = 226
                self.match(ANTLRv4Parser.COMMA)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Action_Context(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AT(self):
            return self.getToken(ANTLRv4Parser.AT, 0)

        def identifier(self):
            return self.getTypedRuleContext(ANTLRv4Parser.IdentifierContext, 0)

        def actionBlock(self):
            return self.getTypedRuleContext(ANTLRv4Parser.ActionBlockContext, 0)

        def actionScopeName(self):
            return self.getTypedRuleContext(ANTLRv4Parser.ActionScopeNameContext, 0)

        def COLONCOLON(self):
            return self.getToken(ANTLRv4Parser.COLONCOLON, 0)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_action_

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitAction_"):
                return visitor.visitAction_(self)
            else:
                return visitor.visitChildren(self)

    def action_(self):
        localctx = ANTLRv4Parser.Action_Context(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_action_)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 229
            self.match(ANTLRv4Parser.AT)
            self.state = 233
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 13, self._ctx)
            if la_ == 1:
                self.state = 230
                self.actionScopeName()
                self.state = 231
                self.match(ANTLRv4Parser.COLONCOLON)

            self.state = 235
            self.identifier()
            self.state = 236
            self.actionBlock()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ActionScopeNameContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self):
            return self.getTypedRuleContext(ANTLRv4Parser.IdentifierContext, 0)

        def LEXER(self):
            return self.getToken(ANTLRv4Parser.LEXER, 0)

        def PARSER(self):
            return self.getToken(ANTLRv4Parser.PARSER, 0)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_actionScopeName

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitActionScopeName"):
                return visitor.visitActionScopeName(self)
            else:
                return visitor.visitChildren(self)

    def actionScopeName(self):
        localctx = ANTLRv4Parser.ActionScopeNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_actionScopeName)
        try:
            self.state = 241
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1, 2]:
                self.enterOuterAlt(localctx, 1)
                self.state = 238
                self.identifier()
            elif token in [17]:
                self.enterOuterAlt(localctx, 2)
                self.state = 239
                self.match(ANTLRv4Parser.LEXER)
            elif token in [18]:
                self.enterOuterAlt(localctx, 3)
                self.state = 240
                self.match(ANTLRv4Parser.PARSER)
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ActionBlockContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BEGIN_ACTION(self):
            return self.getToken(ANTLRv4Parser.BEGIN_ACTION, 0)

        def END_ACTION(self):
            return self.getToken(ANTLRv4Parser.END_ACTION, 0)

        def ACTION_CONTENT(self, i: int = None):
            if i is None:
                return self.getTokens(ANTLRv4Parser.ACTION_CONTENT)
            else:
                return self.getToken(ANTLRv4Parser.ACTION_CONTENT, i)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_actionBlock

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitActionBlock"):
                return visitor.visitActionBlock(self)
            else:
                return visitor.visitChildren(self)

    def actionBlock(self):
        localctx = ANTLRv4Parser.ActionBlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_actionBlock)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 243
            self.match(ANTLRv4Parser.BEGIN_ACTION)
            self.state = 247
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 60:
                self.state = 244
                self.match(ANTLRv4Parser.ACTION_CONTENT)
                self.state = 249
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 250
            self.match(ANTLRv4Parser.END_ACTION)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ArgActionBlockContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BEGIN_ARGUMENT(self):
            return self.getToken(ANTLRv4Parser.BEGIN_ARGUMENT, 0)

        def END_ARGUMENT(self):
            return self.getToken(ANTLRv4Parser.END_ARGUMENT, 0)

        def ARGUMENT_CONTENT(self, i: int = None):
            if i is None:
                return self.getTokens(ANTLRv4Parser.ARGUMENT_CONTENT)
            else:
                return self.getToken(ANTLRv4Parser.ARGUMENT_CONTENT, i)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_argActionBlock

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitArgActionBlock"):
                return visitor.visitArgActionBlock(self)
            else:
                return visitor.visitChildren(self)

    def argActionBlock(self):
        localctx = ANTLRv4Parser.ArgActionBlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_argActionBlock)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 252
            self.match(ANTLRv4Parser.BEGIN_ARGUMENT)
            self.state = 256
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 57:
                self.state = 253
                self.match(ANTLRv4Parser.ARGUMENT_CONTENT)
                self.state = 258
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 259
            self.match(ANTLRv4Parser.END_ARGUMENT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ModeSpecContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def MODE(self):
            return self.getToken(ANTLRv4Parser.MODE, 0)

        def identifier(self):
            return self.getTypedRuleContext(ANTLRv4Parser.IdentifierContext, 0)

        def SEMI(self):
            return self.getToken(ANTLRv4Parser.SEMI, 0)

        def lexerRuleSpec(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(ANTLRv4Parser.LexerRuleSpecContext)
            else:
                return self.getTypedRuleContext(ANTLRv4Parser.LexerRuleSpecContext, i)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_modeSpec

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitModeSpec"):
                return visitor.visitModeSpec(self)
            else:
                return visitor.visitChildren(self)

    def modeSpec(self):
        localctx = ANTLRv4Parser.ModeSpecContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_modeSpec)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 261
            self.match(ANTLRv4Parser.MODE)
            self.state = 262
            self.identifier()
            self.state = 263
            self.match(ANTLRv4Parser.SEMI)
            self.state = 267
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 1 or _la == 16:
                self.state = 264
                self.lexerRuleSpec()
                self.state = 269
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class RulesContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ruleSpec(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(ANTLRv4Parser.RuleSpecContext)
            else:
                return self.getTypedRuleContext(ANTLRv4Parser.RuleSpecContext, i)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_rules

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitRules"):
                return visitor.visitRules(self)
            else:
                return visitor.visitChildren(self)

    def rules(self):
        localctx = ANTLRv4Parser.RulesContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_rules)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 273
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while ((_la) & ~0x3F) == 0 and ((1 << _la) & 7405574) != 0:
                self.state = 270
                self.ruleSpec()
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

    class RuleSpecContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def parserRuleSpec(self):
            return self.getTypedRuleContext(ANTLRv4Parser.ParserRuleSpecContext, 0)

        def lexerRuleSpec(self):
            return self.getTypedRuleContext(ANTLRv4Parser.LexerRuleSpecContext, 0)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_ruleSpec

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitRuleSpec"):
                return visitor.visitRuleSpec(self)
            else:
                return visitor.visitChildren(self)

    def ruleSpec(self):
        localctx = ANTLRv4Parser.RuleSpecContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_ruleSpec)
        try:
            self.state = 278
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 19, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 276
                self.parserRuleSpec()

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 277
                self.lexerRuleSpec()

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ParserRuleSpecContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def RULE_REF(self):
            return self.getToken(ANTLRv4Parser.RULE_REF, 0)

        def COLON(self):
            return self.getToken(ANTLRv4Parser.COLON, 0)

        def ruleBlock(self):
            return self.getTypedRuleContext(ANTLRv4Parser.RuleBlockContext, 0)

        def SEMI(self):
            return self.getToken(ANTLRv4Parser.SEMI, 0)

        def exceptionGroup(self):
            return self.getTypedRuleContext(ANTLRv4Parser.ExceptionGroupContext, 0)

        def ruleModifiers(self):
            return self.getTypedRuleContext(ANTLRv4Parser.RuleModifiersContext, 0)

        def argActionBlock(self):
            return self.getTypedRuleContext(ANTLRv4Parser.ArgActionBlockContext, 0)

        def ruleReturns(self):
            return self.getTypedRuleContext(ANTLRv4Parser.RuleReturnsContext, 0)

        def throwsSpec(self):
            return self.getTypedRuleContext(ANTLRv4Parser.ThrowsSpecContext, 0)

        def localsSpec(self):
            return self.getTypedRuleContext(ANTLRv4Parser.LocalsSpecContext, 0)

        def rulePrequel(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(ANTLRv4Parser.RulePrequelContext)
            else:
                return self.getTypedRuleContext(ANTLRv4Parser.RulePrequelContext, i)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_parserRuleSpec

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitParserRuleSpec"):
                return visitor.visitParserRuleSpec(self)
            else:
                return visitor.visitChildren(self)

    def parserRuleSpec(self):
        localctx = ANTLRv4Parser.ParserRuleSpecContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_parserRuleSpec)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 281
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if ((_la) & ~0x3F) == 0 and ((1 << _la) & 7405568) != 0:
                self.state = 280
                self.ruleModifiers()

            self.state = 283
            self.match(ANTLRv4Parser.RULE_REF)
            self.state = 285
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 10:
                self.state = 284
                self.argActionBlock()

            self.state = 288
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 23:
                self.state = 287
                self.ruleReturns()

            self.state = 291
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 25:
                self.state = 290
                self.throwsSpec()

            self.state = 294
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 24:
                self.state = 293
                self.localsSpec()

            self.state = 299
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 12 or _la == 49:
                self.state = 296
                self.rulePrequel()
                self.state = 301
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 302
            self.match(ANTLRv4Parser.COLON)
            self.state = 303
            self.ruleBlock()
            self.state = 304
            self.match(ANTLRv4Parser.SEMI)
            self.state = 305
            self.exceptionGroup()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ExceptionGroupContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def exceptionHandler(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(ANTLRv4Parser.ExceptionHandlerContext)
            else:
                return self.getTypedRuleContext(ANTLRv4Parser.ExceptionHandlerContext, i)

        def finallyClause(self):
            return self.getTypedRuleContext(ANTLRv4Parser.FinallyClauseContext, 0)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_exceptionGroup

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitExceptionGroup"):
                return visitor.visitExceptionGroup(self)
            else:
                return visitor.visitChildren(self)

    def exceptionGroup(self):
        localctx = ANTLRv4Parser.ExceptionGroupContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_exceptionGroup)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 310
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 26:
                self.state = 307
                self.exceptionHandler()
                self.state = 312
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 314
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 27:
                self.state = 313
                self.finallyClause()

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ExceptionHandlerContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CATCH(self):
            return self.getToken(ANTLRv4Parser.CATCH, 0)

        def argActionBlock(self):
            return self.getTypedRuleContext(ANTLRv4Parser.ArgActionBlockContext, 0)

        def actionBlock(self):
            return self.getTypedRuleContext(ANTLRv4Parser.ActionBlockContext, 0)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_exceptionHandler

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitExceptionHandler"):
                return visitor.visitExceptionHandler(self)
            else:
                return visitor.visitChildren(self)

    def exceptionHandler(self):
        localctx = ANTLRv4Parser.ExceptionHandlerContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_exceptionHandler)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 316
            self.match(ANTLRv4Parser.CATCH)
            self.state = 317
            self.argActionBlock()
            self.state = 318
            self.actionBlock()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class FinallyClauseContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FINALLY(self):
            return self.getToken(ANTLRv4Parser.FINALLY, 0)

        def actionBlock(self):
            return self.getTypedRuleContext(ANTLRv4Parser.ActionBlockContext, 0)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_finallyClause

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitFinallyClause"):
                return visitor.visitFinallyClause(self)
            else:
                return visitor.visitChildren(self)

    def finallyClause(self):
        localctx = ANTLRv4Parser.FinallyClauseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_finallyClause)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 320
            self.match(ANTLRv4Parser.FINALLY)
            self.state = 321
            self.actionBlock()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class RulePrequelContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def optionsSpec(self):
            return self.getTypedRuleContext(ANTLRv4Parser.OptionsSpecContext, 0)

        def ruleAction(self):
            return self.getTypedRuleContext(ANTLRv4Parser.RuleActionContext, 0)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_rulePrequel

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitRulePrequel"):
                return visitor.visitRulePrequel(self)
            else:
                return visitor.visitChildren(self)

    def rulePrequel(self):
        localctx = ANTLRv4Parser.RulePrequelContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_rulePrequel)
        try:
            self.state = 325
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [12]:
                self.enterOuterAlt(localctx, 1)
                self.state = 323
                self.optionsSpec()
            elif token in [49]:
                self.enterOuterAlt(localctx, 2)
                self.state = 324
                self.ruleAction()
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class RuleReturnsContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def RETURNS(self):
            return self.getToken(ANTLRv4Parser.RETURNS, 0)

        def argActionBlock(self):
            return self.getTypedRuleContext(ANTLRv4Parser.ArgActionBlockContext, 0)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_ruleReturns

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitRuleReturns"):
                return visitor.visitRuleReturns(self)
            else:
                return visitor.visitChildren(self)

    def ruleReturns(self):
        localctx = ANTLRv4Parser.RuleReturnsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_ruleReturns)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 327
            self.match(ANTLRv4Parser.RETURNS)
            self.state = 328
            self.argActionBlock()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ThrowsSpecContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def THROWS(self):
            return self.getToken(ANTLRv4Parser.THROWS, 0)

        def identifier(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(ANTLRv4Parser.IdentifierContext)
            else:
                return self.getTypedRuleContext(ANTLRv4Parser.IdentifierContext, i)

        def COMMA(self, i: int = None):
            if i is None:
                return self.getTokens(ANTLRv4Parser.COMMA)
            else:
                return self.getToken(ANTLRv4Parser.COMMA, i)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_throwsSpec

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitThrowsSpec"):
                return visitor.visitThrowsSpec(self)
            else:
                return visitor.visitChildren(self)

    def throwsSpec(self):
        localctx = ANTLRv4Parser.ThrowsSpecContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_throwsSpec)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 330
            self.match(ANTLRv4Parser.THROWS)
            self.state = 331
            self.identifier()
            self.state = 336
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 31:
                self.state = 332
                self.match(ANTLRv4Parser.COMMA)
                self.state = 333
                self.identifier()
                self.state = 338
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class LocalsSpecContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LOCALS(self):
            return self.getToken(ANTLRv4Parser.LOCALS, 0)

        def argActionBlock(self):
            return self.getTypedRuleContext(ANTLRv4Parser.ArgActionBlockContext, 0)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_localsSpec

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitLocalsSpec"):
                return visitor.visitLocalsSpec(self)
            else:
                return visitor.visitChildren(self)

    def localsSpec(self):
        localctx = ANTLRv4Parser.LocalsSpecContext(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_localsSpec)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 339
            self.match(ANTLRv4Parser.LOCALS)
            self.state = 340
            self.argActionBlock()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class RuleActionContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AT(self):
            return self.getToken(ANTLRv4Parser.AT, 0)

        def identifier(self):
            return self.getTypedRuleContext(ANTLRv4Parser.IdentifierContext, 0)

        def actionBlock(self):
            return self.getTypedRuleContext(ANTLRv4Parser.ActionBlockContext, 0)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_ruleAction

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitRuleAction"):
                return visitor.visitRuleAction(self)
            else:
                return visitor.visitChildren(self)

    def ruleAction(self):
        localctx = ANTLRv4Parser.RuleActionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 54, self.RULE_ruleAction)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 342
            self.match(ANTLRv4Parser.AT)
            self.state = 343
            self.identifier()
            self.state = 344
            self.actionBlock()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class RuleModifiersContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ruleModifier(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(ANTLRv4Parser.RuleModifierContext)
            else:
                return self.getTypedRuleContext(ANTLRv4Parser.RuleModifierContext, i)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_ruleModifiers

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitRuleModifiers"):
                return visitor.visitRuleModifiers(self)
            else:
                return visitor.visitChildren(self)

    def ruleModifiers(self):
        localctx = ANTLRv4Parser.RuleModifiersContext(self, self._ctx, self.state)
        self.enterRule(localctx, 56, self.RULE_ruleModifiers)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 347
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 346
                self.ruleModifier()
                self.state = 349
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (((_la) & ~0x3F) == 0 and ((1 << _la) & 7405568) != 0):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class RuleModifierContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PUBLIC(self):
            return self.getToken(ANTLRv4Parser.PUBLIC, 0)

        def PRIVATE(self):
            return self.getToken(ANTLRv4Parser.PRIVATE, 0)

        def PROTECTED(self):
            return self.getToken(ANTLRv4Parser.PROTECTED, 0)

        def FRAGMENT(self):
            return self.getToken(ANTLRv4Parser.FRAGMENT, 0)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_ruleModifier

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitRuleModifier"):
                return visitor.visitRuleModifier(self)
            else:
                return visitor.visitChildren(self)

    def ruleModifier(self):
        localctx = ANTLRv4Parser.RuleModifierContext(self, self._ctx, self.state)
        self.enterRule(localctx, 58, self.RULE_ruleModifier)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 351
            _la = self._input.LA(1)
            if not (((_la) & ~0x3F) == 0 and ((1 << _la) & 7405568) != 0):
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

    class RuleBlockContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ruleAltList(self):
            return self.getTypedRuleContext(ANTLRv4Parser.RuleAltListContext, 0)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_ruleBlock

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitRuleBlock"):
                return visitor.visitRuleBlock(self)
            else:
                return visitor.visitChildren(self)

    def ruleBlock(self):
        localctx = ANTLRv4Parser.RuleBlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 60, self.RULE_ruleBlock)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 353
            self.ruleAltList()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class RuleAltListContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def labeledAlt(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(ANTLRv4Parser.LabeledAltContext)
            else:
                return self.getTypedRuleContext(ANTLRv4Parser.LabeledAltContext, i)

        def OR(self, i: int = None):
            if i is None:
                return self.getTokens(ANTLRv4Parser.OR)
            else:
                return self.getToken(ANTLRv4Parser.OR, i)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_ruleAltList

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitRuleAltList"):
                return visitor.visitRuleAltList(self)
            else:
                return visitor.visitChildren(self)

    def ruleAltList(self):
        localctx = ANTLRv4Parser.RuleAltListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 62, self.RULE_ruleAltList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 355
            self.labeledAlt()
            self.state = 360
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 45:
                self.state = 356
                self.match(ANTLRv4Parser.OR)
                self.state = 357
                self.labeledAlt()
                self.state = 362
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class LabeledAltContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def alternative(self):
            return self.getTypedRuleContext(ANTLRv4Parser.AlternativeContext, 0)

        def POUND(self):
            return self.getToken(ANTLRv4Parser.POUND, 0)

        def identifier(self):
            return self.getTypedRuleContext(ANTLRv4Parser.IdentifierContext, 0)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_labeledAlt

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitLabeledAlt"):
                return visitor.visitLabeledAlt(self)
            else:
                return visitor.visitChildren(self)

    def labeledAlt(self):
        localctx = ANTLRv4Parser.LabeledAltContext(self, self._ctx, self.state)
        self.enterRule(localctx, 64, self.RULE_labeledAlt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 363
            self.alternative()
            self.state = 366
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 50:
                self.state = 364
                self.match(ANTLRv4Parser.POUND)
                self.state = 365
                self.identifier()

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class LexerRuleSpecContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TOKEN_REF(self):
            return self.getToken(ANTLRv4Parser.TOKEN_REF, 0)

        def COLON(self):
            return self.getToken(ANTLRv4Parser.COLON, 0)

        def lexerRuleBlock(self):
            return self.getTypedRuleContext(ANTLRv4Parser.LexerRuleBlockContext, 0)

        def SEMI(self):
            return self.getToken(ANTLRv4Parser.SEMI, 0)

        def FRAGMENT(self):
            return self.getToken(ANTLRv4Parser.FRAGMENT, 0)

        def optionsSpec(self):
            return self.getTypedRuleContext(ANTLRv4Parser.OptionsSpecContext, 0)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_lexerRuleSpec

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitLexerRuleSpec"):
                return visitor.visitLexerRuleSpec(self)
            else:
                return visitor.visitChildren(self)

    def lexerRuleSpec(self):
        localctx = ANTLRv4Parser.LexerRuleSpecContext(self, self._ctx, self.state)
        self.enterRule(localctx, 66, self.RULE_lexerRuleSpec)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 369
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 16:
                self.state = 368
                self.match(ANTLRv4Parser.FRAGMENT)

            self.state = 371
            self.match(ANTLRv4Parser.TOKEN_REF)
            self.state = 373
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 12:
                self.state = 372
                self.optionsSpec()

            self.state = 375
            self.match(ANTLRv4Parser.COLON)
            self.state = 376
            self.lexerRuleBlock()
            self.state = 377
            self.match(ANTLRv4Parser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class LexerRuleBlockContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def lexerAltList(self):
            return self.getTypedRuleContext(ANTLRv4Parser.LexerAltListContext, 0)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_lexerRuleBlock

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitLexerRuleBlock"):
                return visitor.visitLexerRuleBlock(self)
            else:
                return visitor.visitChildren(self)

    def lexerRuleBlock(self):
        localctx = ANTLRv4Parser.LexerRuleBlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 68, self.RULE_lexerRuleBlock)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 379
            self.lexerAltList()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class LexerAltListContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def lexerAlt(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(ANTLRv4Parser.LexerAltContext)
            else:
                return self.getTypedRuleContext(ANTLRv4Parser.LexerAltContext, i)

        def OR(self, i: int = None):
            if i is None:
                return self.getTokens(ANTLRv4Parser.OR)
            else:
                return self.getToken(ANTLRv4Parser.OR, i)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_lexerAltList

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitLexerAltList"):
                return visitor.visitLexerAltList(self)
            else:
                return visitor.visitChildren(self)

    def lexerAltList(self):
        localctx = ANTLRv4Parser.LexerAltListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 70, self.RULE_lexerAltList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 381
            self.lexerAlt()
            self.state = 386
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 45:
                self.state = 382
                self.match(ANTLRv4Parser.OR)
                self.state = 383
                self.lexerAlt()
                self.state = 388
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class LexerAltContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def lexerElements(self):
            return self.getTypedRuleContext(ANTLRv4Parser.LexerElementsContext, 0)

        def lexerCommands(self):
            return self.getTypedRuleContext(ANTLRv4Parser.LexerCommandsContext, 0)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_lexerAlt

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitLexerAlt"):
                return visitor.visitLexerAlt(self)
            else:
                return visitor.visitChildren(self)

    def lexerAlt(self):
        localctx = ANTLRv4Parser.LexerAltContext(self, self._ctx, self.state)
        self.enterRule(localctx, 72, self.RULE_lexerAlt)
        self._la = 0 # Token type
        try:
            self.state = 394
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 37, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 389
                self.lexerElements()
                self.state = 391
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 37:
                    self.state = 390
                    self.lexerCommands()

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class LexerElementsContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def lexerElement(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(ANTLRv4Parser.LexerElementContext)
            else:
                return self.getTypedRuleContext(ANTLRv4Parser.LexerElementContext, i)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_lexerElements

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitLexerElements"):
                return visitor.visitLexerElements(self)
            else:
                return visitor.visitChildren(self)

    def lexerElements(self):
        localctx = ANTLRv4Parser.LexerElementsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 74, self.RULE_lexerElements)
        self._la = 0 # Token type
        try:
            self.state = 402
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1, 3, 8, 11, 33, 48, 51]:
                self.enterOuterAlt(localctx, 1)
                self.state = 397
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 396
                    self.lexerElement()
                    self.state = 399
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (((_la) & ~0x3F) == 0 and ((1 << _la) & 2533283380332810) != 0):
                        break

            elif token in [32, 34, 37, 45]:
                self.enterOuterAlt(localctx, 2)

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class LexerElementContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def lexerAtom(self):
            return self.getTypedRuleContext(ANTLRv4Parser.LexerAtomContext, 0)

        def ebnfSuffix(self):
            return self.getTypedRuleContext(ANTLRv4Parser.EbnfSuffixContext, 0)

        def lexerBlock(self):
            return self.getTypedRuleContext(ANTLRv4Parser.LexerBlockContext, 0)

        def actionBlock(self):
            return self.getTypedRuleContext(ANTLRv4Parser.ActionBlockContext, 0)

        def QUESTION(self):
            return self.getToken(ANTLRv4Parser.QUESTION, 0)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_lexerElement

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitLexerElement"):
                return visitor.visitLexerElement(self)
            else:
                return visitor.visitChildren(self)

    def lexerElement(self):
        localctx = ANTLRv4Parser.LexerElementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 76, self.RULE_lexerElement)
        self._la = 0 # Token type
        try:
            self.state = 416
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1, 3, 8, 48, 51]:
                self.enterOuterAlt(localctx, 1)
                self.state = 404
                self.lexerAtom()
                self.state = 406
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if ((_la) & ~0x3F) == 0 and ((1 << _la) & 24189255811072) != 0:
                    self.state = 405
                    self.ebnfSuffix()

            elif token in [33]:
                self.enterOuterAlt(localctx, 2)
                self.state = 408
                self.lexerBlock()
                self.state = 410
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if ((_la) & ~0x3F) == 0 and ((1 << _la) & 24189255811072) != 0:
                    self.state = 409
                    self.ebnfSuffix()

            elif token in [11]:
                self.enterOuterAlt(localctx, 3)
                self.state = 412
                self.actionBlock()
                self.state = 414
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 41:
                    self.state = 413
                    self.match(ANTLRv4Parser.QUESTION)

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class LexerBlockContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAREN(self):
            return self.getToken(ANTLRv4Parser.LPAREN, 0)

        def lexerAltList(self):
            return self.getTypedRuleContext(ANTLRv4Parser.LexerAltListContext, 0)

        def RPAREN(self):
            return self.getToken(ANTLRv4Parser.RPAREN, 0)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_lexerBlock

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitLexerBlock"):
                return visitor.visitLexerBlock(self)
            else:
                return visitor.visitChildren(self)

    def lexerBlock(self):
        localctx = ANTLRv4Parser.LexerBlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 78, self.RULE_lexerBlock)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 418
            self.match(ANTLRv4Parser.LPAREN)
            self.state = 419
            self.lexerAltList()
            self.state = 420
            self.match(ANTLRv4Parser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class LexerCommandsContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def RARROW(self):
            return self.getToken(ANTLRv4Parser.RARROW, 0)

        def lexerCommand(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(ANTLRv4Parser.LexerCommandContext)
            else:
                return self.getTypedRuleContext(ANTLRv4Parser.LexerCommandContext, i)

        def COMMA(self, i: int = None):
            if i is None:
                return self.getTokens(ANTLRv4Parser.COMMA)
            else:
                return self.getToken(ANTLRv4Parser.COMMA, i)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_lexerCommands

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitLexerCommands"):
                return visitor.visitLexerCommands(self)
            else:
                return visitor.visitChildren(self)

    def lexerCommands(self):
        localctx = ANTLRv4Parser.LexerCommandsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 80, self.RULE_lexerCommands)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 422
            self.match(ANTLRv4Parser.RARROW)
            self.state = 423
            self.lexerCommand()
            self.state = 428
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 31:
                self.state = 424
                self.match(ANTLRv4Parser.COMMA)
                self.state = 425
                self.lexerCommand()
                self.state = 430
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class LexerCommandContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def lexerCommandName(self):
            return self.getTypedRuleContext(ANTLRv4Parser.LexerCommandNameContext, 0)

        def LPAREN(self):
            return self.getToken(ANTLRv4Parser.LPAREN, 0)

        def lexerCommandExpr(self):
            return self.getTypedRuleContext(ANTLRv4Parser.LexerCommandExprContext, 0)

        def RPAREN(self):
            return self.getToken(ANTLRv4Parser.RPAREN, 0)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_lexerCommand

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitLexerCommand"):
                return visitor.visitLexerCommand(self)
            else:
                return visitor.visitChildren(self)

    def lexerCommand(self):
        localctx = ANTLRv4Parser.LexerCommandContext(self, self._ctx, self.state)
        self.enterRule(localctx, 82, self.RULE_lexerCommand)
        try:
            self.state = 437
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 45, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 431
                self.lexerCommandName()
                self.state = 432
                self.match(ANTLRv4Parser.LPAREN)
                self.state = 433
                self.lexerCommandExpr()
                self.state = 434
                self.match(ANTLRv4Parser.RPAREN)

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 436
                self.lexerCommandName()

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class LexerCommandNameContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self):
            return self.getTypedRuleContext(ANTLRv4Parser.IdentifierContext, 0)

        def MODE(self):
            return self.getToken(ANTLRv4Parser.MODE, 0)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_lexerCommandName

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitLexerCommandName"):
                return visitor.visitLexerCommandName(self)
            else:
                return visitor.visitChildren(self)

    def lexerCommandName(self):
        localctx = ANTLRv4Parser.LexerCommandNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 84, self.RULE_lexerCommandName)
        try:
            self.state = 441
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1, 2]:
                self.enterOuterAlt(localctx, 1)
                self.state = 439
                self.identifier()
            elif token in [28]:
                self.enterOuterAlt(localctx, 2)
                self.state = 440
                self.match(ANTLRv4Parser.MODE)
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class LexerCommandExprContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self):
            return self.getTypedRuleContext(ANTLRv4Parser.IdentifierContext, 0)

        def INT(self):
            return self.getToken(ANTLRv4Parser.INT, 0)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_lexerCommandExpr

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitLexerCommandExpr"):
                return visitor.visitLexerCommandExpr(self)
            else:
                return visitor.visitChildren(self)

    def lexerCommandExpr(self):
        localctx = ANTLRv4Parser.LexerCommandExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 86, self.RULE_lexerCommandExpr)
        try:
            self.state = 445
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1, 2]:
                self.enterOuterAlt(localctx, 1)
                self.state = 443
                self.identifier()
            elif token in [7]:
                self.enterOuterAlt(localctx, 2)
                self.state = 444
                self.match(ANTLRv4Parser.INT)
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class AltListContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def alternative(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(ANTLRv4Parser.AlternativeContext)
            else:
                return self.getTypedRuleContext(ANTLRv4Parser.AlternativeContext, i)

        def OR(self, i: int = None):
            if i is None:
                return self.getTokens(ANTLRv4Parser.OR)
            else:
                return self.getToken(ANTLRv4Parser.OR, i)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_altList

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitAltList"):
                return visitor.visitAltList(self)
            else:
                return visitor.visitChildren(self)

    def altList(self):
        localctx = ANTLRv4Parser.AltListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 88, self.RULE_altList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 447
            self.alternative()
            self.state = 452
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 45:
                self.state = 448
                self.match(ANTLRv4Parser.OR)
                self.state = 449
                self.alternative()
                self.state = 454
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class AlternativeContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def elementOptions(self):
            return self.getTypedRuleContext(ANTLRv4Parser.ElementOptionsContext, 0)

        def element(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(ANTLRv4Parser.ElementContext)
            else:
                return self.getTypedRuleContext(ANTLRv4Parser.ElementContext, i)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_alternative

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitAlternative"):
                return visitor.visitAlternative(self)
            else:
                return visitor.visitChildren(self)

    def alternative(self):
        localctx = ANTLRv4Parser.AlternativeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 90, self.RULE_alternative)
        self._la = 0 # Token type
        try:
            self.state = 464
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1, 2, 8, 11, 33, 38, 48, 51]:
                self.enterOuterAlt(localctx, 1)
                self.state = 456
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 38:
                    self.state = 455
                    self.elementOptions()

                self.state = 459
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 458
                    self.element()
                    self.state = 461
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (((_la) & ~0x3F) == 0 and ((1 << _la) & 2533283380332806) != 0):
                        break

            elif token in [32, 34, 45, 50]:
                self.enterOuterAlt(localctx, 2)

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ElementContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def labeledElement(self):
            return self.getTypedRuleContext(ANTLRv4Parser.LabeledElementContext, 0)

        def ebnfSuffix(self):
            return self.getTypedRuleContext(ANTLRv4Parser.EbnfSuffixContext, 0)

        def atom(self):
            return self.getTypedRuleContext(ANTLRv4Parser.AtomContext, 0)

        def ebnf(self):
            return self.getTypedRuleContext(ANTLRv4Parser.EbnfContext, 0)

        def actionBlock(self):
            return self.getTypedRuleContext(ANTLRv4Parser.ActionBlockContext, 0)

        def QUESTION(self):
            return self.getToken(ANTLRv4Parser.QUESTION, 0)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_element

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitElement"):
                return visitor.visitElement(self)
            else:
                return visitor.visitChildren(self)

    def element(self):
        localctx = ANTLRv4Parser.ElementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 92, self.RULE_element)
        self._la = 0 # Token type
        try:
            self.state = 481
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 55, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 466
                self.labeledElement()
                self.state = 469
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [41, 42, 44]:
                    self.state = 467
                    self.ebnfSuffix()
                elif token in [1, 2, 8, 11, 32, 33, 34, 45, 48, 50, 51]:
                    pass
                else:
                    raise NoViableAltException(self)

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 471
                self.atom()
                self.state = 474
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [41, 42, 44]:
                    self.state = 472
                    self.ebnfSuffix()
                elif token in [1, 2, 8, 11, 32, 33, 34, 45, 48, 50, 51]:
                    pass
                else:
                    raise NoViableAltException(self)

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 476
                self.ebnf()

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 477
                self.actionBlock()
                self.state = 479
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 41:
                    self.state = 478
                    self.match(ANTLRv4Parser.QUESTION)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class LabeledElementContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self):
            return self.getTypedRuleContext(ANTLRv4Parser.IdentifierContext, 0)

        def ASSIGN(self):
            return self.getToken(ANTLRv4Parser.ASSIGN, 0)

        def PLUS_ASSIGN(self):
            return self.getToken(ANTLRv4Parser.PLUS_ASSIGN, 0)

        def atom(self):
            return self.getTypedRuleContext(ANTLRv4Parser.AtomContext, 0)

        def block(self):
            return self.getTypedRuleContext(ANTLRv4Parser.BlockContext, 0)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_labeledElement

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitLabeledElement"):
                return visitor.visitLabeledElement(self)
            else:
                return visitor.visitChildren(self)

    def labeledElement(self):
        localctx = ANTLRv4Parser.LabeledElementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 94, self.RULE_labeledElement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 483
            self.identifier()
            self.state = 484
            _la = self._input.LA(1)
            if not (_la == 40 or _la == 43):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 487
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1, 2, 8, 48, 51]:
                self.state = 485
                self.atom()
            elif token in [33]:
                self.state = 486
                self.block()
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class EbnfContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def block(self):
            return self.getTypedRuleContext(ANTLRv4Parser.BlockContext, 0)

        def blockSuffix(self):
            return self.getTypedRuleContext(ANTLRv4Parser.BlockSuffixContext, 0)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_ebnf

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitEbnf"):
                return visitor.visitEbnf(self)
            else:
                return visitor.visitChildren(self)

    def ebnf(self):
        localctx = ANTLRv4Parser.EbnfContext(self, self._ctx, self.state)
        self.enterRule(localctx, 96, self.RULE_ebnf)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 489
            self.block()
            self.state = 491
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if ((_la) & ~0x3F) == 0 and ((1 << _la) & 24189255811072) != 0:
                self.state = 490
                self.blockSuffix()

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class BlockSuffixContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ebnfSuffix(self):
            return self.getTypedRuleContext(ANTLRv4Parser.EbnfSuffixContext, 0)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_blockSuffix

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitBlockSuffix"):
                return visitor.visitBlockSuffix(self)
            else:
                return visitor.visitChildren(self)

    def blockSuffix(self):
        localctx = ANTLRv4Parser.BlockSuffixContext(self, self._ctx, self.state)
        self.enterRule(localctx, 98, self.RULE_blockSuffix)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 493
            self.ebnfSuffix()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class EbnfSuffixContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def QUESTION(self, i: int = None):
            if i is None:
                return self.getTokens(ANTLRv4Parser.QUESTION)
            else:
                return self.getToken(ANTLRv4Parser.QUESTION, i)

        def STAR(self):
            return self.getToken(ANTLRv4Parser.STAR, 0)

        def PLUS(self):
            return self.getToken(ANTLRv4Parser.PLUS, 0)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_ebnfSuffix

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitEbnfSuffix"):
                return visitor.visitEbnfSuffix(self)
            else:
                return visitor.visitChildren(self)

    def ebnfSuffix(self):
        localctx = ANTLRv4Parser.EbnfSuffixContext(self, self._ctx, self.state)
        self.enterRule(localctx, 100, self.RULE_ebnfSuffix)
        self._la = 0 # Token type
        try:
            self.state = 507
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [41]:
                self.enterOuterAlt(localctx, 1)
                self.state = 495
                self.match(ANTLRv4Parser.QUESTION)
                self.state = 497
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 41:
                    self.state = 496
                    self.match(ANTLRv4Parser.QUESTION)

            elif token in [42]:
                self.enterOuterAlt(localctx, 2)
                self.state = 499
                self.match(ANTLRv4Parser.STAR)
                self.state = 501
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 41:
                    self.state = 500
                    self.match(ANTLRv4Parser.QUESTION)

            elif token in [44]:
                self.enterOuterAlt(localctx, 3)
                self.state = 503
                self.match(ANTLRv4Parser.PLUS)
                self.state = 505
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 41:
                    self.state = 504
                    self.match(ANTLRv4Parser.QUESTION)

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class LexerAtomContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def characterRange(self):
            return self.getTypedRuleContext(ANTLRv4Parser.CharacterRangeContext, 0)

        def terminal(self):
            return self.getTypedRuleContext(ANTLRv4Parser.TerminalContext, 0)

        def notSet(self):
            return self.getTypedRuleContext(ANTLRv4Parser.NotSetContext, 0)

        def LEXER_CHAR_SET(self):
            return self.getToken(ANTLRv4Parser.LEXER_CHAR_SET, 0)

        def DOT(self):
            return self.getToken(ANTLRv4Parser.DOT, 0)

        def elementOptions(self):
            return self.getTypedRuleContext(ANTLRv4Parser.ElementOptionsContext, 0)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_lexerAtom

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitLexerAtom"):
                return visitor.visitLexerAtom(self)
            else:
                return visitor.visitChildren(self)

    def lexerAtom(self):
        localctx = ANTLRv4Parser.LexerAtomContext(self, self._ctx, self.state)
        self.enterRule(localctx, 102, self.RULE_lexerAtom)
        self._la = 0 # Token type
        try:
            self.state = 517
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 63, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 509
                self.characterRange()

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 510
                self.terminal()

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 511
                self.notSet()

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 512
                self.match(ANTLRv4Parser.LEXER_CHAR_SET)

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 513
                self.match(ANTLRv4Parser.DOT)
                self.state = 515
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 38:
                    self.state = 514
                    self.elementOptions()

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class AtomContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def terminal(self):
            return self.getTypedRuleContext(ANTLRv4Parser.TerminalContext, 0)

        def ruleref(self):
            return self.getTypedRuleContext(ANTLRv4Parser.RulerefContext, 0)

        def notSet(self):
            return self.getTypedRuleContext(ANTLRv4Parser.NotSetContext, 0)

        def DOT(self):
            return self.getToken(ANTLRv4Parser.DOT, 0)

        def elementOptions(self):
            return self.getTypedRuleContext(ANTLRv4Parser.ElementOptionsContext, 0)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_atom

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitAtom"):
                return visitor.visitAtom(self)
            else:
                return visitor.visitChildren(self)

    def atom(self):
        localctx = ANTLRv4Parser.AtomContext(self, self._ctx, self.state)
        self.enterRule(localctx, 104, self.RULE_atom)
        self._la = 0 # Token type
        try:
            self.state = 526
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1, 8]:
                self.enterOuterAlt(localctx, 1)
                self.state = 519
                self.terminal()
            elif token in [2]:
                self.enterOuterAlt(localctx, 2)
                self.state = 520
                self.ruleref()
            elif token in [51]:
                self.enterOuterAlt(localctx, 3)
                self.state = 521
                self.notSet()
            elif token in [48]:
                self.enterOuterAlt(localctx, 4)
                self.state = 522
                self.match(ANTLRv4Parser.DOT)
                self.state = 524
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 38:
                    self.state = 523
                    self.elementOptions()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class NotSetContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NOT(self):
            return self.getToken(ANTLRv4Parser.NOT, 0)

        def setElement(self):
            return self.getTypedRuleContext(ANTLRv4Parser.SetElementContext, 0)

        def blockSet(self):
            return self.getTypedRuleContext(ANTLRv4Parser.BlockSetContext, 0)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_notSet

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitNotSet"):
                return visitor.visitNotSet(self)
            else:
                return visitor.visitChildren(self)

    def notSet(self):
        localctx = ANTLRv4Parser.NotSetContext(self, self._ctx, self.state)
        self.enterRule(localctx, 106, self.RULE_notSet)
        try:
            self.state = 532
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 66, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 528
                self.match(ANTLRv4Parser.NOT)
                self.state = 529
                self.setElement()

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 530
                self.match(ANTLRv4Parser.NOT)
                self.state = 531
                self.blockSet()

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class BlockSetContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAREN(self):
            return self.getToken(ANTLRv4Parser.LPAREN, 0)

        def setElement(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(ANTLRv4Parser.SetElementContext)
            else:
                return self.getTypedRuleContext(ANTLRv4Parser.SetElementContext, i)

        def RPAREN(self):
            return self.getToken(ANTLRv4Parser.RPAREN, 0)

        def OR(self, i: int = None):
            if i is None:
                return self.getTokens(ANTLRv4Parser.OR)
            else:
                return self.getToken(ANTLRv4Parser.OR, i)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_blockSet

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitBlockSet"):
                return visitor.visitBlockSet(self)
            else:
                return visitor.visitChildren(self)

    def blockSet(self):
        localctx = ANTLRv4Parser.BlockSetContext(self, self._ctx, self.state)
        self.enterRule(localctx, 108, self.RULE_blockSet)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 534
            self.match(ANTLRv4Parser.LPAREN)
            self.state = 535
            self.setElement()
            self.state = 540
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 45:
                self.state = 536
                self.match(ANTLRv4Parser.OR)
                self.state = 537
                self.setElement()
                self.state = 542
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 543
            self.match(ANTLRv4Parser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class SetElementContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TOKEN_REF(self):
            return self.getToken(ANTLRv4Parser.TOKEN_REF, 0)

        def elementOptions(self):
            return self.getTypedRuleContext(ANTLRv4Parser.ElementOptionsContext, 0)

        def STRING_LITERAL(self):
            return self.getToken(ANTLRv4Parser.STRING_LITERAL, 0)

        def characterRange(self):
            return self.getTypedRuleContext(ANTLRv4Parser.CharacterRangeContext, 0)

        def LEXER_CHAR_SET(self):
            return self.getToken(ANTLRv4Parser.LEXER_CHAR_SET, 0)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_setElement

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitSetElement"):
                return visitor.visitSetElement(self)
            else:
                return visitor.visitChildren(self)

    def setElement(self):
        localctx = ANTLRv4Parser.SetElementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 110, self.RULE_setElement)
        self._la = 0 # Token type
        try:
            self.state = 555
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 70, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 545
                self.match(ANTLRv4Parser.TOKEN_REF)
                self.state = 547
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 38:
                    self.state = 546
                    self.elementOptions()

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 549
                self.match(ANTLRv4Parser.STRING_LITERAL)
                self.state = 551
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 38:
                    self.state = 550
                    self.elementOptions()

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 553
                self.characterRange()

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 554
                self.match(ANTLRv4Parser.LEXER_CHAR_SET)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class BlockContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAREN(self):
            return self.getToken(ANTLRv4Parser.LPAREN, 0)

        def altList(self):
            return self.getTypedRuleContext(ANTLRv4Parser.AltListContext, 0)

        def RPAREN(self):
            return self.getToken(ANTLRv4Parser.RPAREN, 0)

        def COLON(self):
            return self.getToken(ANTLRv4Parser.COLON, 0)

        def optionsSpec(self):
            return self.getTypedRuleContext(ANTLRv4Parser.OptionsSpecContext, 0)

        def ruleAction(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(ANTLRv4Parser.RuleActionContext)
            else:
                return self.getTypedRuleContext(ANTLRv4Parser.RuleActionContext, i)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_block

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitBlock"):
                return visitor.visitBlock(self)
            else:
                return visitor.visitChildren(self)

    def block(self):
        localctx = ANTLRv4Parser.BlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 112, self.RULE_block)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 557
            self.match(ANTLRv4Parser.LPAREN)
            self.state = 568
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if ((_la) & ~0x3F) == 0 and ((1 << _la) & 562950490296320) != 0:
                self.state = 559
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 12:
                    self.state = 558
                    self.optionsSpec()

                self.state = 564
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la == 49:
                    self.state = 561
                    self.ruleAction()
                    self.state = 566
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 567
                self.match(ANTLRv4Parser.COLON)

            self.state = 570
            self.altList()
            self.state = 571
            self.match(ANTLRv4Parser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class RulerefContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def RULE_REF(self):
            return self.getToken(ANTLRv4Parser.RULE_REF, 0)

        def argActionBlock(self):
            return self.getTypedRuleContext(ANTLRv4Parser.ArgActionBlockContext, 0)

        def elementOptions(self):
            return self.getTypedRuleContext(ANTLRv4Parser.ElementOptionsContext, 0)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_ruleref

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitRuleref"):
                return visitor.visitRuleref(self)
            else:
                return visitor.visitChildren(self)

    def ruleref(self):
        localctx = ANTLRv4Parser.RulerefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 114, self.RULE_ruleref)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 573
            self.match(ANTLRv4Parser.RULE_REF)
            self.state = 575
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 10:
                self.state = 574
                self.argActionBlock()

            self.state = 578
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 38:
                self.state = 577
                self.elementOptions()

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class CharacterRangeContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING_LITERAL(self, i: int = None):
            if i is None:
                return self.getTokens(ANTLRv4Parser.STRING_LITERAL)
            else:
                return self.getToken(ANTLRv4Parser.STRING_LITERAL, i)

        def RANGE(self):
            return self.getToken(ANTLRv4Parser.RANGE, 0)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_characterRange

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitCharacterRange"):
                return visitor.visitCharacterRange(self)
            else:
                return visitor.visitChildren(self)

    def characterRange(self):
        localctx = ANTLRv4Parser.CharacterRangeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 116, self.RULE_characterRange)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 580
            self.match(ANTLRv4Parser.STRING_LITERAL)
            self.state = 581
            self.match(ANTLRv4Parser.RANGE)
            self.state = 582
            self.match(ANTLRv4Parser.STRING_LITERAL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class TerminalContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TOKEN_REF(self):
            return self.getToken(ANTLRv4Parser.TOKEN_REF, 0)

        def elementOptions(self):
            return self.getTypedRuleContext(ANTLRv4Parser.ElementOptionsContext, 0)

        def STRING_LITERAL(self):
            return self.getToken(ANTLRv4Parser.STRING_LITERAL, 0)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_terminal

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitTerminal"):
                return visitor.visitTerminal(self)
            else:
                return visitor.visitChildren(self)

    def terminal(self):
        localctx = ANTLRv4Parser.TerminalContext(self, self._ctx, self.state)
        self.enterRule(localctx, 118, self.RULE_terminal)
        self._la = 0 # Token type
        try:
            self.state = 592
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1]:
                self.enterOuterAlt(localctx, 1)
                self.state = 584
                self.match(ANTLRv4Parser.TOKEN_REF)
                self.state = 586
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 38:
                    self.state = 585
                    self.elementOptions()

            elif token in [8]:
                self.enterOuterAlt(localctx, 2)
                self.state = 588
                self.match(ANTLRv4Parser.STRING_LITERAL)
                self.state = 590
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 38:
                    self.state = 589
                    self.elementOptions()

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ElementOptionsContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LT(self):
            return self.getToken(ANTLRv4Parser.LT, 0)

        def elementOption(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(ANTLRv4Parser.ElementOptionContext)
            else:
                return self.getTypedRuleContext(ANTLRv4Parser.ElementOptionContext, i)

        def GT(self):
            return self.getToken(ANTLRv4Parser.GT, 0)

        def COMMA(self, i: int = None):
            if i is None:
                return self.getTokens(ANTLRv4Parser.COMMA)
            else:
                return self.getToken(ANTLRv4Parser.COMMA, i)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_elementOptions

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitElementOptions"):
                return visitor.visitElementOptions(self)
            else:
                return visitor.visitChildren(self)

    def elementOptions(self):
        localctx = ANTLRv4Parser.ElementOptionsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 120, self.RULE_elementOptions)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 594
            self.match(ANTLRv4Parser.LT)
            self.state = 595
            self.elementOption()
            self.state = 600
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 31:
                self.state = 596
                self.match(ANTLRv4Parser.COMMA)
                self.state = 597
                self.elementOption()
                self.state = 602
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 603
            self.match(ANTLRv4Parser.GT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ElementOptionContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(ANTLRv4Parser.IdentifierContext)
            else:
                return self.getTypedRuleContext(ANTLRv4Parser.IdentifierContext, i)

        def ASSIGN(self):
            return self.getToken(ANTLRv4Parser.ASSIGN, 0)

        def STRING_LITERAL(self):
            return self.getToken(ANTLRv4Parser.STRING_LITERAL, 0)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_elementOption

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitElementOption"):
                return visitor.visitElementOption(self)
            else:
                return visitor.visitChildren(self)

    def elementOption(self):
        localctx = ANTLRv4Parser.ElementOptionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 122, self.RULE_elementOption)
        try:
            self.state = 612
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 81, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 605
                self.identifier()

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 606
                self.identifier()
                self.state = 607
                self.match(ANTLRv4Parser.ASSIGN)
                self.state = 610
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [1, 2]:
                    self.state = 608
                    self.identifier()
                elif token in [8]:
                    self.state = 609
                    self.match(ANTLRv4Parser.STRING_LITERAL)
                else:
                    raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class IdentifierContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def RULE_REF(self):
            return self.getToken(ANTLRv4Parser.RULE_REF, 0)

        def TOKEN_REF(self):
            return self.getToken(ANTLRv4Parser.TOKEN_REF, 0)

        def getRuleIndex(self):
            return ANTLRv4Parser.RULE_identifier

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitIdentifier"):
                return visitor.visitIdentifier(self)
            else:
                return visitor.visitChildren(self)

    def identifier(self):
        localctx = ANTLRv4Parser.IdentifierContext(self, self._ctx, self.state)
        self.enterRule(localctx, 124, self.RULE_identifier)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 614
            _la = self._input.LA(1)
            if not (_la == 1 or _la == 2):
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
