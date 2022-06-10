#!/usr/bin/env python

# Players skill assumed to be all 7s
              #DF, WG, PM, PS, SC
base_skills = [ 7,  7,  7,  7,  7]
# Taken from hattrickportal.pro
# Starting skill 7, 17y0d, solid trainer, 10 assistants, stamina 10, intensity 100
# will deviate a lot when calculating for long training periods
#                  7  8   9  10  11  12  13  14  15  16  17   18   19   20
training_table = [[0, 5, 10, 15, 22, 30, 39, 49, 60, 74, 90, 111, 141, 201], #Defending
                  [0, 3,  6,  9, 13, 18, 23, 29, 36, 43, 52,  77,  95, 126], #Crossing
                  [0, 4,  8, 13, 19, 25, 33, 42, 51, 63, 77,  93, 116, 154], #Playmaking
                  [0, 4,  8, 12, 18, 24, 31, 39, 48, 59, 71,  86, 107, 139], #Short passes
                  [0, 4,  9, 14, 20, 26, 34, 43, 53, 65, 80,  97, 121, 163]] #Scoring

TRAINING_DEFENDING  = 0
TRAINING_CROSSING   = 1
TRAINING_PLAYMAKING = 2
TRAINING_PASSING    = 3
TRAINING_SCORING    = 4

contribution = [ #  DF,   PM,   WG,   PA,   SC
                [                           # Wingback Def
                 [1.00,    0,    0,    0,    0],  # Side def
                 [0.43,    0,    0,    0,    0],  # Cen def
                 [   0, 0.10,    0,    0,    0],  # Midfield
                 [   0,    0, 0.45,    0,    0],  # Side Atk
                 [   0,    0,    0,    0,    0]], # Cen Atk
                [                           # Wingback
                 [0.92,    0,    0,    0,    0],  # Side def
                 [0.38,    0,    0,    0,    0],  # Cen def
                 [   0, 0.15,    0,    0,    0],  # Midfield
                 [   0,    0, 0.59,    0,    0],  # Side Atk
                 [   0,    0,    0,    0,    0]], # Cen Atk
                [                           # Wingback tm
                 [0.75,    0,    0,    0,    0],  # Side def
                 [0.70,    0,    0,    0,    0],  # Cen def
                 [   0, 0.20,    0,    0,    0],  # Midfield
                 [   0,    0, 0.35,    0,    0],  # Side Atk
                 [   0,    0,    0,    0,    0]], # Cen Atk
                [                           # Wingback off
                 [0.74,    0,    0,    0,    0],  # Side def
                 [0.35,    0,    0,    0,    0],  # Cen def
                 [   0, 0.20,    0,    0,    0],  # Midfield
                 [   0,    0, 0.69,    0,    0],  # Side Atk
                 [   0,    0,    0,    0,    0]], # Cen Atk
                 #  DF,   PM,   WG,   PA,   SC
                [                           # Defender (L/R)
                 [0.52,    0,    0,    0,    0],  # Side def
                 [1.00,    0,    0,    0,    0],  # Cen def
                 [   0, 0.25,    0,    0,    0],  # Midfield
                 [   0,    0,    0,    0,    0],  # Side Atk
                 [   0,    0,    0,    0,    0]], # Cen Atk
                [                           # Defender tw
                 [0.81,    0,    0,    0,    0],  # Side def
                 [0.67,    0,    0,    0,    0],  # Cen def
                 [   0, 0.15,    0,    0,    0],  # Midfield
                 [   0,    0, 0.26,    0,    0],  # Side Atk
                 [   0,    0,    0,    0,    0]], # Cen Atk
                [                           # Defender off (L/R)
                 [0.40,    0,    0,    0,    0],  # Side def
                 [0.73,    0,    0,    0,    0],  # Cen def
                 [   0, 0.40,    0,    0,    0],  # Midfield
                 [   0,    0,    0,    0,    0],  # Side Atk
                 [   0,    0,    0,    0,    0]], # Cen Atk
                 #  DF,   PM,   WG,   PA,   SC
                [                           # Winger Def
                 [0.61,    0,    0,    0,    0],  # Side def
                 [0.25,    0,    0,    0,    0],  # Cen def
                 [   0, 0.30,    0,    0,    0],  # Midfield
                 [   0,    0, 0.69, 0.21,    0],  # Side Atk
                 [   0,    0,    0, 0.05,    0]], # Cen Atk
                [                           # Winger
                 [0.35,    0,    0,    0,    0],  # Side def
                 [0.20,    0,    0,    0,    0],  # Cen def
                 [   0, 0.45,    0,    0,    0],  # Midfield
                 [   0,    0, 0.86, 0.26,    0],  # Side Atk
                 [   0,    0,    0, 0.11,    0]], # Cen Atk
                [                           # Winger tm
                 [0.29,    0,    0,    0,    0],  # Side def
                 [0.25,    0,    0,    0,    0],  # Cen def
                 [   0, 0.55,    0,    0,    0],  # Midfield
                 [   0,    0, 0.74, 0.15,    0],  # Side Atk
                 [   0,    0,    0, 0.16,    0]], # Cen Atk
                [                           # Winger off
                 [0.22,    0,    0,    0,    0],  # Side def
                 [0.13,    0,    0,    0,    0],  # Cen def
                 [   0, 0.30,    0,    0,    0],  # Midfield
                 [   0,    0, 1.00, 0.29,    0],  # Side Atk
                 [   0,    0,    0, 0.13,    0]], # Cen Atk
                 #  DF,   PM,   WG,   PA,   SC
                [                           # IM Def (LR)
                 [0.27,    0,    0,    0,    0],  # Side def
                 [0.58,    0,    0,    0,    0],  # Cen def
                 [   0, 0.95,    0,    0,    0],  # Midfield
                 [   0,    0,    0, 0.14,    0],  # Side Atk
                 [   0,    0,    0, 0.18, 0.13]], # Cen Atk
                [                           # IM (L/R)
                 [0.19,    0,    0,    0,    0],  # Side def
                 [0.40,    0,    0,    0,    0],  # Cen def
                 [   0, 1.00,    0,    0,    0],  # Midfield
                 [   0,    0,    0, 0.26,    0],  # Side Atk
                 [   0,    0,    0, 0.33, 0.22]], # Cen Atk
                [                           # IM tw
                 [0.24,    0,    0,    0,    0],  # Side def
                 [0.33,    0,    0,    0,    0],  # Cen def
                 [   0, 0.90,    0,    0,    0],  # Midfield
                 [   0,    0, 0.59, 0.31,    0],  # Side Atk
                 [   0,    0,    0, 0.23,    0]], # Cen Atk
                [                           # IM off (L/R)
                 #  DF,   PM,   WG,   PA,   SC
                 [0.09,    0,    0,    0,    0],  # Side def
                 [0.16,    0,    0,    0,    0],  # Cen def
                 [   0, 0.95,    0,    0,    0],  # Midfield
                 [   0,    0,    0, 0.36,    0],  # Side Atk
                 [   0,    0,    0, 0.49, 0.31]], # Cen Atk
                [                           # Forward def
                 [   0,    0,    0,    0,    0],  # Side def
                 [   0,    0,    0,    0,    0],  # Cen def
                 [   0, 0.35,    0,    0,    0],  # Midfield
                 [   0,    0, 0.13, 0.31, 0.13],  # Side Atk
                 [   0,    0,    0, 0.53, 0.56]], # Cen Atk
                [                           # Forward
                 [   0,    0,    0,    0,    0],  # Side def
                 [   0,    0,    0,    0,    0],  # Cen def
                 [   0, 0.25,    0,    0,    0],  # Midfield
                 [   0,    0, 0.18,0.121,0.221],  # Side Atk
                 [   0,    0,    0,0.369, 1.00]], # Cen Atk
                [                           # Forward tw
                 [   0,    0,    0,    0,    0],  # Side def
                 [   0,    0,    0,    0,    0],  # Cen def
                 [   0, 0.15,    0,    0,    0],  # Midfield
                 [   0,    0, (0.64 + 0.21), (0.21 + 0.06), (0.51 + 0.19)],  # Side Atk (own side + other side)
                 [   0,    0,    0, 0.23, 0.66]], # Cen Atk
                [                           # Forward TD
                 [   0,    0,    0,    0,    0],  # Side def
                 [   0,    0,    0,    0,    0],  # Cen def
                 [   0, 0.35,    0,    0,    0],  # Midfield
                 [   0,    0, 0.13, 0.41, 0.13],  # Side Atk
                 [   0,    0,    0, 0.53, 0.56]], # Cen Atk
               ]

SECTOR_SIDE_DEF    = 0
SECTOR_CENTRAL_DEF = 1
SECTOR_MIDFIELD    = 2
SECTOR_SIDE_ATK    = 3
SECTOR_CENTRAL_ATK = 4

SKILL_CONTRIB_DEF = 0
SKILL_CONTRIB_PM  = 1
SKILL_CONTRIB_WG  = 2
SKILL_CONTRIB_PS  = 3
SKILL_CONTRIB_SC  = 4

positions = ["WB def",
             "WB    ",
             "WB tm ",
             "WB off",
             "CD    ",
             "CD tw ",
             "CD off",
             "WG def",
             "WG    ",
             "WG tm ",
             "WG off",
             "IM def",
             "IM    ",
             "IM tw ",
             "IM off",
             "FW def",
             "FW    ",
             "FW tw ",
             "TDF   "]

weights = [ #Side Def, Cen Def, Midfield, Side Atk, Cen Atk
           [     1.00,    1.00,     1.00,     1.00,    1.00], # WB def
           [     1.00,    1.00,     1.00,     1.00,    1.00], # WB
           [     1.00,    1.00,     1.00,     1.00,    1.00], # WB tm
           [     1.00,    1.00,     1.00,     1.00,    1.00], # WB off
           [     1.00,    1.00,     1.00,     1.00,    1.00], # CD
           [     1.00,    1.00,     1.00,     1.00,    1.00], # CD tw
           [     1.00,    1.00,     1.00,     1.00,    1.00], # CD off
           [     1.00,    1.00,     1.00,     1.00,    1.00], # WG def
           [     1.00,    1.00,     1.00,     1.00,    1.00], # WG
           [     1.00,    1.00,     1.00,     1.00,    1.00], # WG tm
           [     1.00,    1.00,     1.00,     1.00,    1.00], # WG off
           [     1.00,    1.00,     1.00,     1.00,    1.00], # IM def
           [     1.00,    1.00,     1.00,     1.00,    1.00], # IM
           [     1.00,    1.00,     1.00,     1.00,    1.00], # IM tw
           [     1.00,    1.00,     1.00,     1.00,    1.00], # IM off
           [     1.00,    1.00,     1.00,     1.00,    1.00], # FW def
           [     1.00,    1.00,     1.00,     1.00,    1.00], # FW
           [     1.00,    1.00,     1.00,     1.00,    1.00], # FW tw
           [     1.00,    1.00,     1.00,     1.00,    1.00], # TDF
          ]

sectors = ["Side Def",
           "Cen Def",
           "Mid",
           "Side Atk",
           "Cen Atk"]

pos_max_score = [ 0, #"Wingback defensive",
                  0, #"Wingback",
                  0, #"Wingback towards the middle",
                  0, #"Wingback ofensive",
                  0, #"Defender",
                  0, #"Defender towards the wing",
                  0, #"Defender ofensive",
                  0, #"Winger defensive",
                  0, #"Winger",
                  0, #"Winger towards the middle",
                  0, #"Winger ofensive",
                  0, #"IM defensive",
                  0, #"IM",
                  0, #"IM towards the wing",
                  0, #"IM ofensive",
                  0, #"Forward defensive",
                  0, #"Forward",
                  0, #"Forward towards the wing",
                  0  #"Forward technical defensive"
                ]

pos_max_skills = [ [], #"Wingback defensive",
                   [], #"Wingback",
                   [], #"Wingback towards the middle",
                   [], #"Wingback ofensive",
                   [], #"Defender",
                   [], #"Defender towards the wing",
                   [], #"Defender ofensive",
                   [], #"Winger defensive",
                   [], #"Winger",
                   [], #"Winger towards the middle",
                   [], #"Winger ofensive",
                   [], #"IM defensive",
                   [], #"IM",
                   [], #"IM towards the wing",
                   [], #"IM ofensive",
                   [], #"Forward defensive",
                   [], #"Forward",
                   [], #"Forward towards the wing",
                   []  #"Forward technical defensive"
                 ]

SKILL_DEF = 0
SKILL_WG  = 1
SKILL_PM  = 2
SKILL_PS  = 3
SKILL_SC  = 4

#returns tuple (skill level, training weeks left)
def training_calc(training_type, target_increment, weeks_available):
    if weeks_available == 0:
        return base_skills[training_type], 0 # base level, 0 weeks left

    weeks_necessary = training_table[training_type][target_increment]
    if target_increment > 0:
        weeks_necessary_prev = training_table[training_type][target_increment-1]
    else:
        weeks_necessary_prev = 0

    # no need to continue, training time run out in the previous increment
    if weeks_necessary_prev >= weeks_available:
        return -1, -1

    if weeks_necessary <= weeks_available:
        #full training increment
        return base_skills[training_type] + target_increment, weeks_available - weeks_necessary
    else:
        #partial training increment
        # weeks need for full training
        last_lvl_weeks_needed = weeks_necessary - weeks_necessary_prev
        # weeks available for training
        last_lvl_weeks_trained = weeks_available - weeks_necessary_prev
        # get percentage of level trained
        last_lvl_pct = last_lvl_weeks_trained / last_lvl_weeks_needed

        return 6 + target_increment + last_lvl_pct, 0

if __name__ == "__main__":
    # weeks available for training
    weeks = 80

    tr_table_len = len(training_table[TRAINING_DEFENDING])

    for def_increment in range(0, tr_table_len):
        df, def_weeks_left = training_calc(TRAINING_DEFENDING, def_increment, weeks)
        if df == -1:
            break
        for cross_increment in range(0, tr_table_len):
            wg, cross_weeks_left = training_calc(TRAINING_CROSSING, cross_increment, def_weeks_left)
            if wg == -1:
                break
            for pm_increment in range(0, tr_table_len):
                pm, pm_weeks_left = training_calc(TRAINING_PLAYMAKING, pm_increment, cross_weeks_left)
                if pm == -1:
                    break
                for ps_increment in range(0, tr_table_len):
                    ps, ps_weeks_left = training_calc(TRAINING_PASSING, ps_increment, pm_weeks_left)
                    if ps == -1:
                        break
                    for sc_increment in range(0, tr_table_len):
                        sc_weeks = training_table[TRAINING_SCORING][sc_increment]
                        if ps_weeks_left > 0:
                            if sc_weeks < ps_weeks_left and sc_increment < tr_table_len:
                                # continue untill all training is used up
                                # or we reached the end of the training array
                                continue

                        sc, sc_weeks_left = training_calc(TRAINING_SCORING, sc_increment, ps_weeks_left)
                        if sc == -1:
                            break

                        assert sc_weeks_left == 0

                        for p in range(0, len(positions)):
                            pos_contrib = contribution[p]
                            result = []

                            for sector in range (0, len(sectors)):
                                sector_contrib = pos_contrib[sector]
                                result.append((sector_contrib[SKILL_CONTRIB_DEF] * df +
                                               sector_contrib[SKILL_CONTRIB_PM]  * pm +
                                               sector_contrib[SKILL_CONTRIB_WG]  * wg +
                                               sector_contrib[SKILL_CONTRIB_PS]  * ps +
                                               sector_contrib[SKILL_CONTRIB_SC]  * sc ) * weights[p][sector])

                            tot = (result[SECTOR_SIDE_DEF]    +
                                   result[SECTOR_CENTRAL_DEF] +
                                   result[SECTOR_MIDFIELD]    +
                                   result[SECTOR_SIDE_ATK]    +
                                   result[SECTOR_CENTRAL_ATK])

                            if pos_max_score[p] < tot:
                                pos_max_skills[p] = [df, wg, pm, ps, sc]
                                pos_max_score[p] = tot

    print("Contr| Pos. |  Df    Wg    Pm    Ps    Sc |Side Def|Cen Def| Mid |Side Atk|Cen Atk")
    for p in range(0, len(positions)):
        res = []
        pos_contrib = contribution[p]
        for sector in range (0, len(sectors)):
            sector_contrib = pos_contrib[sector]
            res.append((sector_contrib[SKILL_CONTRIB_DEF] * pos_max_skills[p][SKILL_DEF] +
                        sector_contrib[SKILL_CONTRIB_PM]  * pos_max_skills[p][SKILL_PM] +
                        sector_contrib[SKILL_CONTRIB_WG]  * pos_max_skills[p][SKILL_WG] +
                        sector_contrib[SKILL_CONTRIB_PS]  * pos_max_skills[p][SKILL_PS] +
                        sector_contrib[SKILL_CONTRIB_SC]  * pos_max_skills[p][SKILL_SC]) * weights[p][sector])
        print("%2.2f|%s|%5.2f %5.2f %5.2f %5.2f %5.2f| %5.2f  | %5.2f |%5.2f| %5.2f  | %5.2f"
                %(pos_max_score[p], positions[p],
                  pos_max_skills[p][SKILL_DEF], pos_max_skills[p][SKILL_WG], pos_max_skills[p][SKILL_PM], pos_max_skills[p][SKILL_PS], pos_max_skills[p][SKILL_SC],
                  res[SECTOR_SIDE_DEF], res[SECTOR_CENTRAL_DEF], res[SECTOR_MIDFIELD], res[SECTOR_SIDE_ATK], res[SECTOR_CENTRAL_ATK]))
