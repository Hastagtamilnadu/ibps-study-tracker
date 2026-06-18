"""
IBPS Clerk Prelims — Study Data
All 92 topics (T1–T93, T14 skipped) and 186 modules.
Source: Master Study Plan (page_manifest + study_effort_report).
"""

# ── SRS Review Gaps (blocks after module completion) ──────────────────────
REVIEW_GAPS = {
    "VH": [1, 3, 7, 15, 30],   # 5 reviews
    "H":  [3, 7, 15, 30],       # 4 reviews
    "M":  [7, 15, 30],           # 3 reviews
    "L":  [15, 30],              # 2 reviews
}

PRIORITY_LABELS = {
    "VH": ("🟣", "Very High"),
    "H":  ("🔴", "High"),
    "M":  ("🟡", "Medium"),
    "L":  ("🟢", "Low"),
}

# ── Sections ──────────────────────────────────────────────────────────────
SECTIONS = {
    "QA": {"icon": "📗", "name": "Quantitative Aptitude"},
    "RE": {"icon": "📘", "name": "Reasoning Ability"},
    "PS": {"icon": "🟦", "name": "Puzzles & Seating"},
    "DI": {"icon": "📙", "name": "Data Interpretation"},
    "EN": {"icon": "📕", "name": "English Language"},
}

# ── Topics ────────────────────────────────────────────────────────────────
# (id, name, section, priority, pdf_filename, total_pages)
_RAW_TOPICS = [
    # ── 📗 Quantitative Aptitude ──
    ("T1",  "Number System & Simplification",       "QA", "VH", "Number System, Simplification.pdf",           31),
    ("T2",  "Number Series",                         "QA", "H",  "Number Series.pdf",                          26),
    ("T3",  "Quadratic Equations / Inequality",      "QA", "M",  "Inequality.pdf",                             41),
    ("T4",  "Percentage",                            "QA", "H",  "Percentage.pdf",                             22),
    ("T5",  "Ratio, Proportion & Partnership",       "QA", "M",  "Ratio & Proportion and Partnership.pdf",     28),
    ("T6",  "Average & Ages",                        "QA", "M",  "Average and Ages.pdf",                       25),
    ("T7",  "Profit & Loss",                         "QA", "H",  "Profit and Loss.pdf",                        33),
    ("T8",  "Simple & Compound Interest",            "QA", "M",  "Simple Interest and Compound Interest.pdf",  26),
    ("T9",  "Time & Work + Pipe & Cistern",          "QA", "M",  "Time and Work & Pipe and Cistern.pdf",       41),
    ("T10", "Speed, Time & Distance",                "QA", "M",  "Speed, Time and Distance.pdf",               35),
    ("T11", "Boat & Stream",                         "QA", "L",  "Boat and Stream.pdf",                        22),
    ("T12", "Mixture & Alligation",                  "QA", "L",  "Mixture & Alligation.pdf",                   21),
    ("T13", "Mensuration",                           "QA", "L",  "Mensuration.pdf",                            33),
    ("T15", "Data Sufficiency (QA)",                 "QA", "L",  "Data Sufficiency.pdf",                       35),
    ("T16", "Permutation, Combination & Probability","QA", "L",  "Permutation, Combination and Probability.pdf",23),
    # ── 📘 Reasoning Ability ──
    ("T17", "Alpha-Numeric Series",                  "RE", "H",  "Reasoning_Part1_2.pdf",                      22),
    ("T18", "Order & Ranking",                       "RE", "M",  "Reasoning_Part1_2.pdf",                      12),
    ("T19", "Direction & Distance",                  "RE", "M",  "Reasoning_Part1_2.pdf",                      12),
    ("T20", "Word Formation",                        "RE", "L",  "Reasoning_Part1_2.pdf",                      11),
    ("T21", "Coding-Decoding",                       "RE", "H",  "Reasoning_Part1_2.pdf",                      30),
    ("T22", "Inequality (Reasoning)",                "RE", "H",  "Reasoning_Part1_2.pdf",                      19),
    ("T23", "Blood Relation",                        "RE", "H",  "Reasoning_Part1_2.pdf",                      26),
    ("T24", "Syllogism",                             "RE", "VH", "Reasoning_Part1_2.pdf",                      37),
    ("T25", "Input-Output",                          "RE", "M",  "Reasoning_Part1_2.pdf",                      28),
    ("T26", "Seating Arrangement (concept)",         "RE", "VH", "Linear Seating Arrangement.pdf",             15),
    ("T27", "Puzzles (concept)",                     "RE", "VH", "Floor Based Puzzle.pdf",                     14),
    ("T28", "Data Sufficiency (Reasoning)",          "RE", "L",  "Reasoning_Part1_2.pdf",                      39),
    ("T29", "Direction, Figure & Distance",          "RE", "L",  "Reasoning_Part1_2.pdf",                       6),
    ("T30", "Decision Making",                       "RE", "L",  "Reasoning_Part1_2.pdf",                       6),
    ("T31", "Cause & Effect",                        "RE", "L",  "Reasoning_Part1_2.pdf",                      17),
    ("T32", "Course of Action",                      "RE", "L",  "Reasoning_Part1_2.pdf",                      26),
    ("T33", "Statements & Assumptions",              "RE", "L",  "Reasoning_Part1_2.pdf",                      19),
    ("T34", "Strength of Arguments",                 "RE", "L",  "Reasoning_Part1_2.pdf",                      17),
    ("T35", "Statements & Conclusions",              "RE", "L",  "Reasoning_Part1_2.pdf",                      18),
    ("T36", "Inference",                             "RE", "L",  "Reasoning_Part1_2.pdf",                      28),
    # ── 🟦 Puzzles & Seating ──
    ("T37", "Linear Seating Arrangement",            "PS", "VH", "Linear Seating Arrangement.pdf",             44),
    ("T38", "Circular Seating Arrangement",          "PS", "VH", "Circular Seating Arrangement.pdf",           44),
    ("T39", "Rectangular Seating",                   "PS", "H",  "RectangularSquare Seating Arrangement.pdf",  25),
    ("T40", "Floor-Based Puzzle",                    "PS", "VH", "Floor Based Puzzle.pdf",                     42),
    ("T41", "Box-Based Puzzle",                      "PS", "VH", "Box Based Puzzle.pdf",                       28),
    ("T42", "Blood Relation Puzzle",                 "PS", "VH", "Blood Relation Based Puzzle.pdf",            33),
    ("T43", "Day / Month / Year Puzzle",             "PS", "VH", "DayMonthYear Based Puzzle.pdf",              33),
    ("T44", "Categorized Puzzle",                    "PS", "VH", "Categorized Based Puzzle.pdf",               43),
    ("T45", "Comparison Puzzle",                     "PS", "H",  "Comparison Based Puzzle.pdf",                14),
    ("T46", "Direction Puzzle",                      "PS", "H",  "Direction Based Puzzle.pdf",                 25),
    ("T47", "Figure Puzzle",                         "PS", "M",  "Figure Based Puzzle.pdf",                    20),
    ("T48", "Mixed / Advanced Puzzle",               "PS", "VH", "PART B.pdf",                                44),
    ("T49", "Practice Sets 1–8 (timed)",             "PS", "VH", "15_Practice_Sets.pdf",                       60),
    ("T50", "Practice Sets 9–15 (timed)",            "PS", "VH", "15_Practice_Sets.pdf",                       55),
    # ── 📙 Data Interpretation ──
    ("T51", "Introduction to DI",                    "DI", "M",  "Introduction to Data Interpretation.pdf",    20),
    ("T52", "Table DI",                              "DI", "VH", "Table DI.pdf",                              124),
    ("T53", "Bar Graph DI",                          "DI", "VH", "Bar Graph.pdf",                              85),
    ("T54", "Line Graph DI",                         "DI", "VH", "Line Graph.pdf",                             78),
    ("T55", "Pie Chart DI",                          "DI", "VH", "Pie Graph.pdf",                              70),
    ("T56", "Caselet DI",                            "DI", "VH", "Caselet DI.pdf",                            129),
    ("T57", "Arithmetic DI",                         "DI", "VH", "Arithmetic DI.pdf",                          89),
    ("T58", "Mixed Graph DI",                        "DI", "H",  "Mixed Graph.pdf",                           111),
    ("T59", "New Pattern DI",                        "DI", "M",  "New Pattern DI.pdf",                         21),
    ("T60", "Radar / Web Chart",                     "DI", "L",  "Radar Graph DI.pdf",                         29),
    # ── 📕 English Language ──
    ("T61", "Subject-Verb Agreement",                "EN", "L",  "Subject Verb Agreement.pdf",                   8),
    ("T62", "Tenses",                                "EN", "L",  "Tenses.pdf",                                  13),
    ("T63", "Noun",                                  "EN", "L",  "Noun.pdf",                                    18),
    ("T64", "Pronoun",                               "EN", "L",  "Pronoun.pdf",                                  9),
    ("T65", "Verb",                                  "EN", "L",  "Verb.pdf",                                     7),
    ("T66", "Preposition",                           "EN", "L",  "Preposition.pdf",                             13),
    ("T67", "Articles",                              "EN", "L",  "Articles.pdf",                                  8),
    ("T68", "Adjectives",                            "EN", "L",  "Adjectives.pdf",                              11),
    ("T69", "Adverb",                                "EN", "L",  "Adverb.pdf",                                   6),
    ("T70", "Conjunction",                           "EN", "L",  "Conjunction.pdf",                               8),
    ("T71", "Conditional Sentences",                 "EN", "L",  "Conditional Sentences.pdf",                     5),
    ("T72", "Active & Passive Voice",                "EN", "L",  "Voices.pdf",                                    6),
    ("T73", "Direct & Indirect Speech",              "EN", "L",  "Narrations.pdf",                                6),
    ("T74", "Error Detection & Correction",          "EN", "H",  "Error Correction.pdf",                         23),
    ("T75", "Sentence Improvement",                  "EN", "H",  "Sentence Improvement.pdf",                     16),
    ("T76", "Fillers",                               "EN", "H",  "Fillers.pdf",                                  23),
    ("T77", "Cloze Test",                            "EN", "H",  "Cloze Test.pdf",                               30),
    ("T78", "Reading Comprehension",                 "EN", "VH", "Reading Comprehension.pdf",                    67),
    ("T79", "Para Jumbles / Sentence Rearrangement", "EN", "H",  "Sentence Rearrangement.pdf",                   32),
    ("T80", "Para Completion",                       "EN", "L",  "Paragraph Completion.pdf",                     17),
    ("T81", "Word Rearrangement",                    "EN", "L",  "Word Rearrangement.pdf",                       11),
    ("T82", "Sentence Starters",                     "EN", "L",  "Starters.pdf",                                  9),
    ("T83", "Sentence Connectors",                   "EN", "L",  "Sentence Connector.pdf",                        8),
    ("T84", "Collocations",                          "EN", "L",  "Collocations.pdf",                             22),
    ("T85", "Column-Based Questions",                "EN", "L",  "Column Based.pdf",                             22),
    ("T86", "Coherent Paragraph",                    "EN", "L",  "Coherent Paragraph.pdf",                        7),
    ("T87", "Paragraph-Based Questions",             "EN", "L",  "Paragraph Based Questions.pdf",                 5),
    ("T88", "Inferences",                            "EN", "L",  "Inferences.pdf",                               17),
    ("T89", "Spelling Errors",                       "EN", "L",  "Spelling Errors.pdf",                           7),
    ("T90", "Phrasal Verbs",                         "EN", "L",  "Phrasal Verb.pdf",                              5),
    ("T91", "Word List / Vocabulary",                "EN", "M",  "Wordlist.pdf",                                  14),
    ("T92", "How to Improve Vocabulary",             "EN", "L",  "How to improve Vocabulary A Brief Discussion.pdf", 19),
    ("T93", "Miscellaneous English",                 "EN", "M",  "Miscellaneous.pdf",                             27),
]

TOPICS = {
    t[0]: {"name": t[1], "section": t[2], "priority": t[3], "pdf": t[4], "pages": t[5]}
    for t in _RAW_TOPICS
}

# ── Modules ───────────────────────────────────────────────────────────────
# (module_id, topic_id, page_start, page_end, section_label)
_RAW_MODULES = [
    # ── 📗 QA (32 modules) ──
    ("T1-M1",  "T1",  1, 16, None), ("T1-M2",  "T1",  17, 31, None),
    ("T2-M1",  "T2",  1, 13, None), ("T2-M2",  "T2",  14, 26, None),
    ("T3-M1",  "T3",  1, 14, None), ("T3-M2",  "T3",  15, 28, None), ("T3-M3",  "T3",  29, 41, None),
    ("T4-M1",  "T4",  1, 11, None), ("T4-M2",  "T4",  12, 22, None),
    ("T5-M1",  "T5",  1, 14, None), ("T5-M2",  "T5",  15, 28, None),
    ("T6-M1",  "T6",  1, 13, None), ("T6-M2",  "T6",  14, 25, None),
    ("T7-M1",  "T7",  1, 17, None), ("T7-M2",  "T7",  18, 33, None),
    ("T8-M1",  "T8",  1, 13, None), ("T8-M2",  "T8",  14, 26, None),
    ("T9-M1",  "T9",  1, 14, None), ("T9-M2",  "T9",  15, 28, None), ("T9-M3",  "T9",  29, 41, None),
    ("T10-M1", "T10", 1, 18, None), ("T10-M2", "T10", 19, 35, None),
    ("T11-M1", "T11", 1, 11, None), ("T11-M2", "T11", 12, 22, None),
    ("T12-M1", "T12", 1, 11, None), ("T12-M2", "T12", 12, 21, None),
    ("T13-M1", "T13", 1, 17, None), ("T13-M2", "T13", 18, 33, None),
    ("T15-M1", "T15", 1, 18, None), ("T15-M2", "T15", 19, 35, None),
    ("T16-M1", "T16", 1, 12, None), ("T16-M2", "T16", 13, 23, None),
    # ── 📘 Reasoning (28 modules) ──
    ("T17-M1", "T17",   1,  11, None), ("T17-M2", "T17",  12,  22, None),
    ("T18-M1", "T18",  23,  34, None),
    ("T19-M1", "T19",  35,  46, None),
    ("T20-M1", "T20",  47,  57, None),
    ("T21-M1", "T21",  58,  72, None), ("T21-M2", "T21",  73,  87, None),
    ("T22-M1", "T22",  88, 106, None),
    ("T23-M1", "T23", 107, 119, None), ("T23-M2", "T23", 120, 132, None),
    ("T24-M1", "T24", 133, 151, None), ("T24-M2", "T24", 152, 169, None),
    ("T25-M1", "T25", 170, 183, None), ("T25-M2", "T25", 184, 197, None),
    ("T26-M1", "T26",   1,  15, None),
    ("T27-M1", "T27",   1,  14, None),
    ("T28-M1", "T28", 306, 325, None), ("T28-M2", "T28", 326, 344, None),
    ("T29-M1", "T29", 345, 350, None),
    ("T30-M1", "T30", 351, 356, None),
    ("T31-M1", "T31", 357, 373, None),
    ("T32-M1", "T32", 374, 386, None), ("T32-M2", "T32", 387, 399, None),
    ("T33-M1", "T33", 400, 418, None),
    ("T34-M1", "T34", 419, 435, None),
    ("T35-M1", "T35", 436, 453, None),
    ("T36-M1", "T36", 454, 467, None), ("T36-M2", "T36", 468, 481, None),
    # ── 🟦 Puzzles & Seating (33 modules) ──
    ("T37-M1", "T37",  1, 15, None), ("T37-M2", "T37", 16, 30, None), ("T37-M3", "T37", 31, 44, None),
    ("T38-M1", "T38",  1, 15, None), ("T38-M2", "T38", 16, 30, None), ("T38-M3", "T38", 31, 44, None),
    ("T39-M1", "T39",  1, 13, None), ("T39-M2", "T39", 14, 25, None),
    ("T40-M1", "T40",  1, 14, None), ("T40-M2", "T40", 15, 28, None), ("T40-M3", "T40", 29, 42, None),
    ("T41-M1", "T41",  1, 14, None), ("T41-M2", "T41", 15, 28, None),
    ("T42-M1", "T42",  1, 17, None), ("T42-M2", "T42", 18, 33, None),
    ("T43-M1", "T43",  1, 17, None), ("T43-M2", "T43", 18, 33, None),
    ("T44-M1", "T44",  1, 15, None), ("T44-M2", "T44", 16, 30, None), ("T44-M3", "T44", 31, 43, None),
    ("T45-M1", "T45",  1, 14, None),
    ("T46-M1", "T46",  1, 13, None), ("T46-M2", "T46", 14, 25, None),
    ("T47-M1", "T47",  1, 20, None),
    ("T48-M1", "T48",  1, 15, None), ("T48-M2", "T48", 16, 30, None), ("T48-M3", "T48", 31, 44, None),
    ("T49-M1", "T49",  1, 20, None), ("T49-M2", "T49", 21, 40, None), ("T49-M3", "T49", 41, 60, None),
    ("T50-M1", "T50", 61, 79, None), ("T50-M2", "T50", 80, 98, None), ("T50-M3", "T50", 99,115, None),
    # ── 📙 Data Interpretation (50 modules) ──
    ("T51-M1",    "T51",   1,  20, None),
    # T52 — Table DI (mega: 4 sections, 9 modules)
    ("T52-SA-M1", "T52",   1,  16, "A: Basic Tables"),
    ("T52-SA-M2", "T52",  17,  31, "A: Basic Tables"),
    ("T52-SB-M1", "T52",  32,  43, "B: Advanced Tables"),
    ("T52-SB-M2", "T52",  44,  54, "B: Advanced Tables"),
    ("T52-SC-M1", "T52",  55,  66, "C: Mixed Tables"),
    ("T52-SC-M2", "T52",  67,  77, "C: Mixed Tables"),
    ("T52-SD-M1", "T52",  78,  93, "D: Exam-Level Sets"),
    ("T52-SD-M2", "T52",  94, 109, "D: Exam-Level Sets"),
    ("T52-SD-M3", "T52", 110, 124, "D: Exam-Level Sets"),
    # T53 — Bar Graph (5 modules)
    ("T53-M1", "T53",  1, 17, None), ("T53-M2", "T53", 18, 34, None),
    ("T53-M3", "T53", 35, 51, None), ("T53-M4", "T53", 52, 68, None), ("T53-M5", "T53", 69, 85, None),
    # T54 — Line Graph (5 modules)
    ("T54-M1", "T54",  1, 16, None), ("T54-M2", "T54", 17, 32, None),
    ("T54-M3", "T54", 33, 48, None), ("T54-M4", "T54", 49, 64, None), ("T54-M5", "T54", 65, 78, None),
    # T55 — Pie Chart (5 modules)
    ("T55-M1", "T55",  1, 14, None), ("T55-M2", "T55", 15, 28, None),
    ("T55-M3", "T55", 29, 42, None), ("T55-M4", "T55", 43, 56, None), ("T55-M5", "T55", 57, 70, None),
    # T56 — Caselet DI (mega: 3 sections, 8 modules)
    ("T56-SA-M1", "T56",   1,  18, "A: Basic Caselets"),
    ("T56-SA-M2", "T56",  19,  36, "A: Basic Caselets"),
    ("T56-SA-M3", "T56",  37,  53, "A: Basic Caselets"),
    ("T56-SB-M1", "T56",  54,  67, "B: Multi-variable Caselets"),
    ("T56-SB-M2", "T56",  68,  81, "B: Multi-variable Caselets"),
    ("T56-SC-M1", "T56",  82,  97, "C: Exam-Level Caselets"),
    ("T56-SC-M2", "T56",  98, 113, "C: Exam-Level Caselets"),
    ("T56-SC-M3", "T56", 114, 129, "C: Exam-Level Caselets"),
    # T57 — Arithmetic DI (6 modules)
    ("T57-M1", "T57",  1, 15, None), ("T57-M2", "T57", 16, 30, None),
    ("T57-M3", "T57", 31, 45, None), ("T57-M4", "T57", 46, 60, None),
    ("T57-M5", "T57", 61, 75, None), ("T57-M6", "T57", 76, 89, None),
    # T58 — Mixed Graph DI (mega: 3 sections, 7 modules)
    ("T58-SA-M1", "T58",  1,  13, "A: Intro & Solved Examples"),
    ("T58-SB-M1", "T58", 14,  31, "B: Combined Chart Practice"),
    ("T58-SB-M2", "T58", 32,  49, "B: Combined Chart Practice"),
    ("T58-SB-M3", "T58", 50,  66, "B: Combined Chart Practice"),
    ("T58-SC-M1", "T58", 67,  81, "C: Mains PYQ & Exam-Level"),
    ("T58-SC-M2", "T58", 82,  96, "C: Mains PYQ & Exam-Level"),
    ("T58-SC-M3", "T58", 97, 111, "C: Mains PYQ & Exam-Level"),
    # T59 — New Pattern DI (2 modules)
    ("T59-M1", "T59",  1, 11, None), ("T59-M2", "T59", 12, 21, None),
    # T60 — Radar / Web Chart (2 modules)
    ("T60-M1", "T60",  1, 15, None), ("T60-M2", "T60", 16, 29, None),
    # ── 📕 English Language (43 modules) ──
    ("T61-M1", "T61",  1,  8, None),
    ("T62-M1", "T62",  1, 13, None),
    ("T63-M1", "T63",  1, 18, None),
    ("T64-M1", "T64",  1,  9, None),
    ("T65-M1", "T65",  1,  7, None),
    ("T66-M1", "T66",  1, 13, None),
    ("T67-M1", "T67",  1,  8, None),
    ("T68-M1", "T68",  1, 11, None),
    ("T69-M1", "T69",  1,  6, None),
    ("T70-M1", "T70",  1,  8, None),
    ("T71-M1", "T71",  1,  5, None),
    ("T72-M1", "T72",  1,  6, None),
    ("T73-M1", "T73",  1,  6, None),
    ("T74-M1", "T74",  1, 12, None), ("T74-M2", "T74", 13, 23, None),
    ("T75-M1", "T75",  1, 16, None),
    ("T76-M1", "T76",  1, 12, None), ("T76-M2", "T76", 13, 23, None),
    ("T77-M1", "T77",  1, 15, None), ("T77-M2", "T77", 16, 30, None),
    ("T78-M1", "T78",  1, 17, None), ("T78-M2", "T78", 18, 34, None),
    ("T78-M3", "T78", 35, 51, None), ("T78-M4", "T78", 52, 67, None),
    ("T79-M1", "T79",  1, 16, None), ("T79-M2", "T79", 17, 32, None),
    ("T80-M1", "T80",  1, 17, None),
    ("T81-M1", "T81",  1, 11, None),
    ("T82-M1", "T82",  1,  9, None),
    ("T83-M1", "T83",  1,  8, None),
    ("T84-M1", "T84",  1, 11, None), ("T84-M2", "T84", 12, 22, None),
    ("T85-M1", "T85",  1, 11, None), ("T85-M2", "T85", 12, 22, None),
    ("T86-M1", "T86",  1,  7, None),
    ("T87-M1", "T87",  1,  5, None),
    ("T88-M1", "T88",  1, 17, None),
    ("T89-M1", "T89",  1,  7, None),
    ("T90-M1", "T90",  1,  5, None),
    ("T91-M1", "T91",  1, 14, None),
    ("T92-M1", "T92",  1, 19, None),
    ("T93-M1", "T93",  1, 14, None), ("T93-M2", "T93", 15, 27, None),
]

MODULES = {
    m[0]: {"topic": m[1], "start": m[2], "end": m[3], "label": m[4]}
    for m in _RAW_MODULES
}

# ── Topic Introduction Sequence (S01–S92) ─────────────────────────────────
# Order: priority-interleaved across sections.
# First modules of each topic introduced in this order.
# Remaining modules filled via breadth-first queue (see build_study_queue).
TOPIC_SEQUENCE = [
    # Phase 1: QA Foundations
    "T1", "T4", "T5", "T6", "T7", "T8",
    # Phase 2: English Grammar Basics (light breather)
    "T61", "T62", "T63", "T64", "T65", "T66", "T67",
    # Phase 3: More QA + Reasoning intro
    "T2", "T3", "T9", "T10", "T17", "T21", "T22", "T23",
    # Phase 4: More English Grammar
    "T68", "T69", "T70", "T71", "T72", "T73", "T74",
    # Phase 5: Key Reasoning + English skills
    "T24", "T26", "T27", "T25", "T18", "T19", "T75", "T76",
    # Phase 6: Puzzles VH + English H
    "T37", "T38", "T40", "T41", "T42", "T43", "T44", "T48", "T77", "T78",
    # Phase 7: DI Core + misc H
    "T51", "T52", "T53", "T54", "T55", "T56", "T57", "T58", "T79", "T39",
    # Phase 8: Remaining Puzzles + DI + M English
    "T45", "T46", "T49", "T50", "T59", "T47", "T91", "T93",
    # Phase 9: Remaining L QA/Reasoning
    "T11", "T12", "T13", "T15", "T16", "T20", "T80", "T81", "T82", "T83", "T84", "T85",
    # Phase 10: Final L topics
    "T28", "T29", "T30", "T31", "T32", "T33", "T34", "T35", "T36", "T60",
    "T86", "T87", "T88", "T89", "T90", "T92",
]

# ── Helper Functions ──────────────────────────────────────────────────────

def _module_sort_key(module_id):
    """Sort key for ordering modules within a topic.
    T1-M1 → (0, '', 1), T52-SA-M1 → (0, 'SA', 1)
    """
    parts = module_id.split("-")
    # Find section code and module number
    section = ""
    mod_num = 0
    for p in parts[1:]:
        if p.startswith("S") and len(p) == 2 and p[1].isalpha():
            section = p
        elif p.startswith("M") and p[1:].isdigit():
            mod_num = int(p[1:])
    return (0, section, mod_num)


def get_topic_modules(topic_id):
    """Get all module IDs for a topic, sorted in study order."""
    mods = [mid for mid, m in MODULES.items() if m["topic"] == topic_id]
    mods.sort(key=_module_sort_key)
    return mods


def build_study_queue():
    """Build the full 186-module study queue.
    Round 1: first module of each topic (in TOPIC_SEQUENCE order).
    Round 2: second module of topics that have ≥2 modules.
    Round N: Nth module, continuing until all 186 are queued.
    """
    topic_mods = {tid: get_topic_modules(tid) for tid in TOPIC_SEQUENCE}
    max_mods = max(len(mods) for mods in topic_mods.values())

    queue = []
    for round_idx in range(max_mods):
        for tid in TOPIC_SEQUENCE:
            mods = topic_mods[tid]
            if round_idx < len(mods):
                queue.append(mods[round_idx])
    return queue


def get_topic_status(topic_id, completed_set):
    """Compute topic status from completed modules.
    Returns: 'Not Started', 'In Progress', or 'Completed'
    """
    mods = get_topic_modules(topic_id)
    done = sum(1 for m in mods if m in completed_set)
    if done == 0:
        return "Not Started"
    elif done < len(mods):
        return "In Progress"
    return "Completed"


# Pre-compute the study queue (module-level constant)
STUDY_QUEUE = build_study_queue()

TOTAL_MODULES = len(MODULES)  # 186
TOTAL_TOPICS = len(TOPICS)    # 92
TOTAL_PAGES = sum(t["pages"] for t in TOPICS.values())  # 2609
